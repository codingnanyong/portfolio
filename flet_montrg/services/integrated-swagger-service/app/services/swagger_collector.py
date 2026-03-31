"""
OpenAPI 스펙 수집 및 통합 서비스
"""

import asyncio
import copy
import httpx
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

from ..core.config import settings
from ..models.swagger import OpenAPISpec, IntegratedOpenAPISpec
from .discovery import get_service_discovery

logger = logging.getLogger(__name__)

# OpenAPI path item / operation 의 servers 는 전역 servers 보다 우선 — 게이트웨이 URL을 망가뜨림
_HTTP_METHODS_PATH = frozenset(
    {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
)


def _strip_servers_from_path_items(paths: Optional[Dict[str, Any]]) -> None:
    if not paths:
        return
    for _pk, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        path_item.pop("servers", None)
        for key, op in path_item.items():
            if key in _HTTP_METHODS_PATH and isinstance(op, dict):
                op.pop("servers", None)


def spec_dict_for_swagger_gateway(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Try-it 이 항상 현재 호스트의 /api/v1/... 를 쓰도록 servers·경로별 servers 제거."""
    out = copy.deepcopy(spec)
    out["servers"] = [{"url": "/", "description": "현재 호스트"}]
    _strip_servers_from_path_items(out.get("paths"))
    return out


class SwaggerCollector:
    """OpenAPI 스펙 수집 및 통합"""
    
    def __init__(self):
        self.service_discovery = get_service_discovery()
        self.collected_specs: Dict[str, OpenAPISpec] = {}
        self.integrated_spec: Optional[IntegratedOpenAPISpec] = None
        
        # HTTP 클라이언트 설정
        self.http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(10),
            follow_redirects=True
        )
    
    async def collect_all_specs(self) -> Dict[str, OpenAPISpec]:
        """모든 서비스의 OpenAPI 스펙 수집"""
        logger.info("Collecting OpenAPI specs from all services")
        
        # 서비스 목록 가져오기
        services = self.service_discovery.get_all_services()
        if not services:
            # 서비스가 없으면 디스커버리 실행
            services = await self.service_discovery.discover_services()
        
        # 각 서비스의 OpenAPI 스펙 수집
        tasks = []
        for service_name, service in services.items():
            task = asyncio.create_task(self._collect_service_spec(service_name, service.base_url))
            tasks.append((service_name, task))
        
        # 결과 수집
        for service_name, task in tasks:
            try:
                spec = await task
                if spec:
                    self.collected_specs[service_name] = spec
                    logger.info(f"Collected OpenAPI spec for {service_name}")
                else:
                    logger.warning(f"Failed to collect OpenAPI spec for {service_name}")
            except Exception as e:
                logger.error(f"Error collecting spec for {service_name}: {e}")
        
        logger.info(f"Collected OpenAPI specs from {len(self.collected_specs)} services")
        return self.collected_specs.copy()
    
    async def _collect_service_spec(self, service_name: str, base_url: Optional[str]) -> Optional[OpenAPISpec]:
        """단일 서비스의 OpenAPI 스펙 수집"""
        if not base_url:
            logger.warning(f"No base URL for service {service_name}")
            return OpenAPISpec(
                service_name=service_name,
                title=service_name,
                version="unknown",
                base_url="",
                is_available=False,
                error_message="No base URL available"
            )
        
        try:
            # OpenAPI JSON 엔드포인트 시도 (/openapi.json, /docs/openapi.json 등)
            openapi_urls = [
                urljoin(base_url, "/openapi.json"),
                urljoin(base_url, "/docs/openapi.json"),
                urljoin(base_url, "/api/openapi.json"),
                urljoin(base_url, "/api/v1/openapi.json")
            ]
            
            spec_data = None
            used_url = None
            
            for url in openapi_urls:
                try:
                    response = await self.http_client.get(url)
                    if response.status_code == 200:
                        spec_data = response.json()
                        used_url = url
                        break
                except Exception as e:
                    logger.debug(f"Failed to fetch {url}: {e}")
                    continue
            
            if not spec_data:
                logger.warning(f"No OpenAPI spec found for {service_name}")
                return OpenAPISpec(
                    service_name=service_name,
                    title=service_name,
                    version="unknown",
                    base_url=base_url,
                    is_available=False,
                    error_message="OpenAPI spec not found"
                )
            
            # OpenAPI 스펙 파싱
            info = spec_data.get("info", {})
            paths = spec_data.get("paths", {})
            components = spec_data.get("components", {})
            tags = spec_data.get("tags", [])
            servers = spec_data.get("servers", [])
            
            # OpenAPI 버전을 3.0.3으로 고정 (Swagger UI 호환성)
            spec_data["openapi"] = "3.0.3"
            
            # 서버 URL이 상대경로인 경우 절대경로로 변환
            if servers:
                for server in servers:
                    if server.get("url", "").startswith("/"):
                        server["url"] = urljoin(base_url, server["url"])
            else:
                servers = [{"url": base_url, "description": f"{service_name} server"}]
            
            return OpenAPISpec(
                service_name=service_name,
                title=info.get("title", service_name),
                version=info.get("version", "1.0.0"),
                description=info.get("description", f"{service_name} API"),
                base_url=base_url,
                spec=spec_data,
                paths=paths,
                components=components,
                tags=tags,
                servers=servers,
                is_available=True
            )
            
        except Exception as e:
            logger.error(f"Error collecting spec for {service_name}: {e}")
            return OpenAPISpec(
                service_name=service_name,
                title=service_name,
                version="unknown",
                base_url=base_url,
                is_available=False,
                error_message=str(e)
            )
    
    async def create_integrated_spec(self) -> IntegratedOpenAPISpec:
        """통합된 OpenAPI 스펙 생성"""
        logger.info("Creating integrated OpenAPI specification")
        
        # 최신 스펙 수집
        await self.collect_all_specs()
        
        # 통합 스펙 초기화
        integrated_spec = IntegratedOpenAPISpec()
        
        # 기본 정보 설정
        integrated_spec.info = {
            "title": "🌡️ Felt Montrg API Documentation",
            "version": "1.0.0",
            "description": f"Total {len(self.collected_specs)} microservices integrated API documentation",
            "contact": {
                "name": "🌡️ Felt Montrg API Documentation Service",
                "url": f"http://localhost:{settings.port}/swagger"
            }
        }
        
        # OpenAPI 버전을 3.0.3으로 설정
        integrated_spec.openapi = "3.0.3"
        
        # 1단계: 스키마와 태그 수집
        all_tags = []
        all_schemas = {}
        all_security_schemes = {}
        
        # 먼저 모든 스키마 수집
        for service_name, spec in self.collected_specs.items():
            if not spec.is_available:
                continue
                
            # 스키마 컴포넌트 수집
            if "schemas" in spec.components:
                for schema_name, schema_def in spec.components["schemas"].items():
                    if schema_name in all_schemas:
                        # 중복시 서비스명으로 prefix
                        prefixed_name = f"{service_name}_{schema_name}"
                        all_schemas[prefixed_name] = schema_def
                    else:
                        # 중복이 아니면 원래 이름 사용
                        all_schemas[schema_name] = schema_def
            
            # 보안 스키마 수집
            if "securitySchemes" in spec.components:
                for security_name, security_def in spec.components["securitySchemes"].items():
                    if security_name in all_security_schemes:
                        prefixed_name = f"{service_name}_{security_name}"
                        all_security_schemes[prefixed_name] = security_def
                    else:
                        all_security_schemes[security_name] = security_def
        
        # 2단계: 서비스별 통합 처리
        for service_name, spec in self.collected_specs.items():
            if not spec.is_available:
                continue
            
            # 서비스 목록에 추가
            integrated_spec.services.append(service_name)
            
            # 서버 정보 추가
            for server in spec.servers:
                if server not in integrated_spec.servers:
                    integrated_spec.servers.append({
                        **server,
                        "description": f"{server.get('description', '')} ({service_name})"
                    })
            
            # 깔끔한 태그 생성
            service_display_name = service_name.replace("-service", "").replace("-", " ").title()
            service_tag = {
                "name": service_display_name,
                "description": f"{spec.title} - {spec.description or f'{service_display_name} API 엔드포인트'}"
            }
            all_tags.append(service_tag)
            
            # 경로 추가 (스키마 참조 처리 포함)
            for path, path_info in spec.paths.items():
                # 기본 경로 사용 (prefix 최소화)
                clean_path = path
                
                # 각 HTTP 메서드별로 처리
                for method, operation in path_info.items():
                    if isinstance(operation, dict):
                        # operationId에 서비스명 prefix 추가 (내부 구분용)
                        if "operationId" in operation:
                            operation["operationId"] = f"{service_name}_{operation['operationId']}"
                        
                        # 태그를 깔끔하게 정리 (중복 제거)
                        service_display_name = service_name.replace("-service", "").replace("-", " ").title()
                        operation["tags"] = [service_display_name]
                        
                        # 설명에 서비스 정보 추가
                        if "summary" in operation:
                            operation["summary"] = f"[{service_display_name}] {operation['summary']}"
                        
                        # 내부 스키마/참조용 (브라우저 URL에는 서비스명 미노출)
                        operation["x-service-name"] = service_name
                        
                
                integrated_spec.paths[clean_path] = path_info
            
        
        # 통합 스펙에 추가
        integrated_spec.tags = all_tags
        integrated_spec.components = {
            "schemas": all_schemas,
            "securitySchemes": all_security_schemes
        }
        
        # 동일 출처: 호스트 기준 /api/v1/... 만 사용 (서비스명·중간 경로 없음)
        integrated_spec.servers = [{"url": "/", "description": "현재 호스트"}]
        _strip_servers_from_path_items(integrated_spec.paths)

        # 3단계: 모든 경로의 스키마 참조 정리
        for path, path_info in integrated_spec.paths.items():
            for method, operation in path_info.items():
                if isinstance(operation, dict):
                    service_name = operation.get("x-service-name")
                    if service_name:
                        self._fix_all_schema_refs(operation, service_name, all_schemas)
        
        self.integrated_spec = integrated_spec
        logger.info(f"Integrated OpenAPI spec created with {len(integrated_spec.paths)} endpoints from {len(integrated_spec.services)} services")
        logger.info(f"Total schemas: {len(all_schemas)}")
        
        return integrated_spec
    
    def _fix_all_schema_refs(self, operation, service_name: str, all_schemas: dict):
        """Operation 내 모든 스키마 참조 수정"""
        # 응답 스키마 참조 처리
        if "responses" in operation:
            for response_code, response_info in operation["responses"].items():
                if isinstance(response_info, dict) and "content" in response_info:
                    for content_type, content_info in response_info["content"].items():
                        if isinstance(content_info, dict) and "schema" in content_info:
                            self._update_schema_refs(content_info["schema"], service_name, all_schemas)
        
        # 요청 본문 스키마 참조 처리
        if "requestBody" in operation:
            request_body = operation["requestBody"]
            if isinstance(request_body, dict) and "content" in request_body:
                for content_type, content_info in request_body["content"].items():
                    if isinstance(content_info, dict) and "schema" in content_info:
                        self._update_schema_refs(content_info["schema"], service_name, all_schemas)
        
        # 파라미터 스키마 참조 처리
        if "parameters" in operation:
            for param in operation["parameters"]:
                if isinstance(param, dict) and "schema" in param:
                    self._update_schema_refs(param["schema"], service_name, all_schemas)
    
    def _update_schema_refs(self, schema_obj, service_name: str, all_schemas: dict):
        """스키마 참조를 업데이트하여 올바른 스키마명을 참조하도록 함"""
        if not isinstance(schema_obj, dict):
            return
            
        # $ref 처리
        if "$ref" in schema_obj:
            ref_path = schema_obj["$ref"]
            if ref_path.startswith("#/components/schemas/"):
                schema_name = ref_path.replace("#/components/schemas/", "")
                
                # 원래 스키마명이 존재하는지 확인
                if schema_name in all_schemas:
                    # 원래 스키마명 그대로 사용
                    pass
                else:
                    # 서비스명 prefix가 있는 스키마명 확인
                    prefixed_name = f"{service_name}_{schema_name}"
                    if prefixed_name in all_schemas:
                        schema_obj["$ref"] = f"#/components/schemas/{prefixed_name}"
        
        # 중첩된 스키마들 재귀적으로 처리
        for key, value in schema_obj.items():
            if key == "$ref":
                continue
            elif isinstance(value, dict):
                self._update_schema_refs(value, service_name, all_schemas)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._update_schema_refs(item, service_name, all_schemas)
    
    def get_service_spec(self, service_name: str) -> Optional[OpenAPISpec]:
        """특정 서비스의 OpenAPI 스펙 조회"""
        return self.collected_specs.get(service_name)
    
    def get_all_service_specs(self) -> Dict[str, OpenAPISpec]:
        """모든 서비스의 OpenAPI 스펙 조회"""
        return self.collected_specs.copy()
    
    def get_integrated_spec(self) -> Optional[IntegratedOpenAPISpec]:
        """통합된 OpenAPI 스펙 조회"""
        return self.integrated_spec
    
    async def refresh_specs(self) -> IntegratedOpenAPISpec:
        """모든 스펙 새로고침"""
        logger.info("Refreshing all OpenAPI specs")
        await self.collect_all_specs()
        return await self.create_integrated_spec()
    
    async def cleanup(self):
        """리소스 정리"""
        await self.http_client.aclose()


# 전역 Swagger Collector 인스턴스
_swagger_collector: Optional[SwaggerCollector] = None


def get_swagger_collector() -> SwaggerCollector:
    """Swagger Collector 인스턴스 반환"""
    global _swagger_collector
    
    if _swagger_collector is None:
        _swagger_collector = SwaggerCollector()
    
    return _swagger_collector


async def cleanup_swagger_collector():
    """Swagger Collector 정리"""
    global _swagger_collector
    
    if _swagger_collector:
        await _swagger_collector.cleanup()
        _swagger_collector = None