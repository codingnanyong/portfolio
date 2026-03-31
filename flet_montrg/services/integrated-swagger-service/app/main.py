"""
API Dashboard Service - Main Application
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import uvicorn
import httpx

from .core.config import settings
from .core.logging_config import setup_logging, get_logger
from .core.v1_routing import resolve_service_for_v1_resource
from .models.service import ServiceOverview
from .models.swagger import IntegratedOpenAPISpec
from .services.monitor import get_service_monitor, cleanup_monitor
from .services.discovery import get_service_discovery
from .services.swagger_collector import (
    get_swagger_collector,
    cleanup_swagger_collector,
    spec_dict_for_swagger_gateway,
)

# 로깅 설정
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    
    # 시작
    logger.info("Starting API Dashboard Service")
    
    try:
        # 서비스 모니터 시작
        monitor = get_service_monitor()
        await monitor.start_monitoring()
        logger.info("Service monitoring started")
        
        # Swagger 컬렉터 초기화 및 통합 스펙 생성
        swagger_collector = get_swagger_collector()
        await swagger_collector.create_integrated_spec()
        logger.info("Swagger collector initialized and integrated spec created")
        
        logger.info(f"Integrated Swagger API available at port {settings.port}")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start services: {e}")
        raise
    
    finally:
        # 종료
        logger.info("Shutting down API Dashboard Service")
        await cleanup_monitor()
        await cleanup_swagger_collector()


# FastAPI 앱 생성 (OpenAPI 자동 생성 비활성화)
app = FastAPI(
    title="Integrated Swagger Service",
    description="통합 API 문서 서비스 - 모든 마이크로서비스의 API를 한 곳에서 확인",
    version=settings.version,
    debug=settings.debug,
    openapi_version="3.0.3",
    lifespan=lifespan,
    openapi_url=None  # 기본 OpenAPI 엔드포인트 비활성화
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 웹 UI는 web-service(Svelte)에서 제공. 본 서비스는 통합 문서·API 라우팅 전용.


# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "service": "api-dashboard-service"}


# 루트 엔드포인트
@app.get("/")
async def root():
    """루트 엔드포인트"""
    swagger_collector = get_swagger_collector()
    integrated_spec = swagger_collector.get_integrated_spec()
    service_count = len(integrated_spec.services) if integrated_spec else 0
    
    return {
        "service": "Integrated Swagger API",
        "version": settings.version,
        "status": "running",
        "integrated_api_docs": "/openapi.json",
        "integrated_services_count": service_count,
        "web_ui": "Use web-service (NodePort 30000) for Swagger UI"
    }


# 통합 OpenAPI 스펙 엔드포인트 (FastAPI 기본 스펙 오버라이드)
@app.get("/openapi.json", include_in_schema=False)
async def get_integrated_openapi_spec():
    """통합된 OpenAPI 스펙 조회 (FastAPI 기본 스펙 대신 사용)"""
    try:
        swagger_collector = get_swagger_collector()
        integrated_spec = swagger_collector.get_integrated_spec()
        
        if not integrated_spec:
            # 스펙이 없으면 새로 생성
            integrated_spec = await swagger_collector.create_integrated_spec()
        
        # 스펙이 여전히 없으면 기본 스펙 반환
        if not integrated_spec or not integrated_spec.paths:
            logger.warning("No integrated spec available, returning basic spec")
            return {
                "openapi": "3.0.3",
                "info": {
                    "title": "Felt Montrg API Documentation",
                    "version": "1.0.0",
                    "description": "Felt Montrg API Documentation (API specification collection in progress...)"
                },
                "paths": {},
                "servers": [{"url": "/", "description": "현재 호스트"}],
                "tags": [
                    {"name": "system", "description": "System management endpoints"}
                ]
            }
        
        spec_dict = integrated_spec.dict(exclude={"last_updated"})
        
        # 통합된 스펙에 서비스 목록 메타데이터 추가
        if hasattr(integrated_spec, 'services') and integrated_spec.services:
            spec_dict['x-integrated-services'] = integrated_spec.services
        
        return spec_dict
        
    except Exception as e:
        logger.error(f"Error getting integrated OpenAPI spec: {e}")
        # 오류 시 기본 스펙 반환
        return {
            "openapi": "3.0.3",
            "info": {
                "title": "Felt Montrg API Documentation",
                "version": "1.0.0",
                "description": f"Felt Montrg API Documentation (error: {str(e)})"
            },
            "paths": {},
            "servers": [{"url": "/"}]
        }


# Swagger/OpenAPI 관련 API
@app.get("/api/v1/swagger/services")
async def get_swagger_services():
    """Swagger UI를 위한 서비스 목록 조회"""
    try:
        swagger_collector = get_swagger_collector()
        service_specs = swagger_collector.get_all_service_specs()
        
        # 서비스 스펙이 없으면 새로 수집
        if not service_specs:
            service_specs = await swagger_collector.collect_all_specs()
        
        return {"services": service_specs}
        
    except Exception as e:
        logger.error(f"Error getting swagger services: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/swagger/services/{service_name}/spec")
async def get_service_openapi_spec(service_name: str):
    """특정 서비스의 OpenAPI 스펙 조회"""
    try:
        swagger_collector = get_swagger_collector()
        service_spec = swagger_collector.get_service_spec(service_name)
        
        if not service_spec:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        
        if not service_spec.is_available:
            raise HTTPException(status_code=503, detail=f"Service {service_name} OpenAPI spec is not available: {service_spec.error_message}")
        
        return spec_dict_for_swagger_gateway(service_spec.spec)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting OpenAPI spec for {service_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/swagger/refresh")
async def refresh_swagger_specs():
    """모든 서비스의 OpenAPI 스펙 새로고침"""
    try:
        swagger_collector = get_swagger_collector()
        integrated_spec = await swagger_collector.refresh_specs()
        
        return {
            "message": "OpenAPI specs refreshed successfully",
            "services_count": len(integrated_spec.services),
            "total_endpoints": len(integrated_spec.paths),
            "last_updated": integrated_spec.last_updated
        }
        
    except Exception as e:
        logger.error(f"Error refreshing swagger specs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# 서비스 관련 API
@app.get("/api/v1/services")
async def get_services():
    """모니터링 대상 서비스 목록 조회"""
    try:
        discovery = get_service_discovery()
        services = discovery.get_all_services()
        
        return {
            "services": list(services.keys()),
            "count": len(services),
            "details": services
        }
        
    except Exception as e:
        logger.error(f"Error getting services: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/services/{service_name}")
async def get_service(service_name: str):
    """특정 서비스 정보 조회"""
    try:
        discovery = get_service_discovery()
        service = discovery.get_service(service_name)
        
        if not service:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        
        return service
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting service {service_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/services/{service_name}/check")
async def check_service(service_name: str):
    """특정 서비스 즉시 헬스체크"""
    try:
        monitor = get_service_monitor()
        service = await monitor.check_service_by_name(service_name)
        
        if not service:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        
        return {
            "service": service,
            "message": f"Health check completed for {service_name}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking service {service_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/services/refresh")
async def refresh_services():
    """서비스 목록 새로고침 및 전체 헬스체크"""
    try:
        monitor = get_service_monitor()
        services = await monitor.refresh_and_check_all()
        
        return {
            "services": services,
            "count": len(services),
            "message": "Services refreshed and checked"
        }
        
    except Exception as e:
        logger.error(f"Error refreshing services: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# 모니터링 상태 API
@app.get("/api/v1/monitoring/status")
async def get_monitoring_status():
    """모니터링 상태 정보 조회"""
    try:
        monitor = get_service_monitor()
        status = monitor.get_monitoring_status()
        
        return status
        
    except Exception as e:
        logger.error(f"Error getting monitoring status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# 메트릭 API
@app.get("/api/v1/metrics/overview")
async def get_metrics_overview():
    """전체 메트릭 개요"""
    try:
        discovery = get_service_discovery()
        services = discovery.get_all_services()
        
        total_services = len(services)
        healthy_services = sum(1 for s in services.values() if s.health_status.value == "healthy")
        
        total_endpoints = sum(len(s.endpoints) for s in services.values())
        healthy_endpoints = sum(
            len([ep for ep in s.endpoints if ep.status_code and 200 <= ep.status_code < 400])
            for s in services.values()
        )
        
        response_times = []
        for service in services.values():
            for endpoint in service.endpoints:
                if endpoint.response_time:
                    response_times.append(endpoint.response_time)
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            "total_services": total_services,
            "healthy_services": healthy_services,
            "service_health_rate": (healthy_services / total_services * 100) if total_services > 0 else 0,
            "total_endpoints": total_endpoints,
            "healthy_endpoints": healthy_endpoints,
            "endpoint_health_rate": (healthy_endpoints / total_endpoints * 100) if total_endpoints > 0 else 0,
            "avg_response_time": avg_response_time,
            "response_time_count": len(response_times)
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/metrics/{service_name}")
async def get_service_metrics(service_name: str):
    """특정 서비스 메트릭 조회"""
    try:
        monitor = get_service_monitor()
        metrics_history = monitor.get_service_metrics_history(service_name)
        
        discovery = get_service_discovery()
        service = discovery.get_service(service_name)
        
        if not service:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        
        return {
            "service_name": service_name,
            "current_metrics": service.metrics,
            "metrics_history": metrics_history[-10:],  # 최근 10개
            "endpoints_status": [
                {
                    "name": ep.name,
                    "url": ep.url,
                    "status_code": ep.status_code,
                    "response_time": ep.response_time,
                    "last_checked": ep.last_checked,
                    "error_message": ep.error_message
                }
                for ep in service.endpoints
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting metrics for {service_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _forward_to_microservice(
    service_name: str,
    request: Request,
    *,
    upstream_path: Optional[str] = None,
) -> Response:
    discovery = get_service_discovery()
    service = discovery.get_service(service_name)
    if not service or not service.base_url:
        raise HTTPException(status_code=404, detail="Upstream service not found")

    path = request.url.path if upstream_path is None else upstream_path
    target_url = f"{service.base_url.rstrip('/')}{path}"
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"

    headers = dict(request.headers)
    headers.pop("host", None)
    body = await request.body()

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
        )

    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    response_headers = {
        k: v for k, v in response.headers.items() if k.lower() not in excluded
    }
    response_headers.update({
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=response_headers,
        media_type=response.headers.get("content-type"),
    )


_V1_FWD_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]


async def _forward_v1_by_resource_key(resource_key: str, request: Request) -> Response:
    """URL: {host}/api/v1/{리소스}/... — 서비스명은 URL에 없음."""
    service_name = resolve_service_for_v1_resource(resource_key)
    if not service_name:
        raise HTTPException(status_code=404, detail="Not Found")
    try:
        return await _forward_to_microservice(service_name, request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("V1 forward error (%s): %s", resource_key, e)
        raise HTTPException(status_code=500, detail=f"Upstream error: {str(e)}") from e


@app.api_route("/api/v1/{resource_key}", methods=_V1_FWD_METHODS)
async def forward_v1_exact(resource_key: str, request: Request):
    return await _forward_v1_by_resource_key(resource_key, request)


@app.api_route("/api/v1/{resource_key}/{path:path}", methods=_V1_FWD_METHODS)
async def forward_v1_subpaths(resource_key: str, path: str, request: Request):
    return await _forward_v1_by_resource_key(resource_key, request)


@app.api_route("/api/svc/{service_name}", methods=_V1_FWD_METHODS)
async def legacy_api_svc_root(service_name: str, request: Request):
    """구 클라이언트(/api/svc/{서비스명}/...) 호환 — upstream 은 /api/v1/... 만 받음."""
    return await _forward_to_microservice(service_name, request, upstream_path="/")


@app.api_route("/api/svc/{service_name}/{path:path}", methods=_V1_FWD_METHODS)
async def legacy_api_svc_paths(service_name: str, path: str, request: Request):
    upstream = "/" + path.lstrip("/")
    return await _forward_to_microservice(service_name, request, upstream_path=upstream)


# 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 핸들러"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )