"""URL 첫 세그먼트(/api/v1/{key}/...) → Kubernetes 서비스명 (호스트에 서비스명 노출 없음)."""

from typing import Dict, Optional

# integrated-swagger 자체 API (이 세그먼트는 백엔드로 넘기지 않음)
V1_BUILTIN_SEGMENTS = frozenset({"swagger", "services", "monitoring", "metrics"})

# OpenAPI 경로의 리소스 접두와 web-service config.js SERVICE_MAPPING 과 동일하게 유지
RESOURCE_TO_SERVICE: Dict[str, str] = {
    "aggregation": "aggregation-service",
    "location": "location-service",
    "realtime": "realtime-service",
    "thresholds": "thresholds-service",
    "alerts": "alert-service",
    "subscriptions": "alert-subscription-service",
    "notifications": "alert-notification-service",
    "mappings": "sensor-threshold-mapping-service",
}


def resolve_service_for_v1_resource(resource_key: str) -> Optional[str]:
    if resource_key in V1_BUILTIN_SEGMENTS:
        return None
    return RESOURCE_TO_SERVICE.get(resource_key)
