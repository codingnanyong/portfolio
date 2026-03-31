#!/bin/bash

# web-service (API Gateway Web UI) Kubernetes 배포 스크립트

set -e

# 스크립트 위치 기준 경로 (어디서 실행해도 동일하게 동작)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

NAMESPACE="flet-montrg"
SERVICE_NAME="web-service"
IMAGE_NAME="flet-montrg/web-service:latest"
KIND_CLUSTER="flet-cluster"

echo "🚀 web-service 배포 시작..."

# 네임스페이스 확인
echo "📋 네임스페이스 확인: $NAMESPACE"
kubectl get namespace $NAMESPACE >/dev/null 2>&1 || kubectl create namespace $NAMESPACE

# k8s 매니페스트 디렉터리로 이동 (kubectl -k . 사용을 위해)
cd "$SCRIPT_DIR"

# 기존 리소스 삭제 (선택사항)
if [ "$1" == "--clean" ]; then
    echo "🧹 기존 리소스 정리..."
    kubectl delete -k . --ignore-not-found=true
    sleep 5
fi

# Docker 이미지 빌드 (항상 캐시 없이 빌드)
echo "🔨 Docker 이미지 빌드 (--no-cache)..."
cd "$REPO_ROOT/services/web-service"
docker build --no-cache -t $IMAGE_NAME .
cd "$SCRIPT_DIR"

# Kind에 이미지 로드
echo "📦 Kind에 이미지 로드..."
kind load docker-image $IMAGE_NAME --name $KIND_CLUSTER

# ConfigMap 배포
echo "⚙️ ConfigMap 배포..."
kubectl apply -f configmap.yaml

# 메인 리소스 배포
echo "📦 메인 리소스 배포..."
kubectl apply -k .

# 새 이미지 적용: 같은 태그(:latest)여도 Pod를 다시 띄워 방금 로드한 이미지 사용
echo "🔄 디플로이 재시작 (새 이미지 반영)..."
kubectl rollout restart deployment/$SERVICE_NAME -n $NAMESPACE

# 배포 상태 확인
echo "🔍 배포 상태 확인..."
kubectl rollout status deployment/$SERVICE_NAME -n $NAMESPACE --timeout=120s || true

# imagePullPolicy: Never + tag :latest → 같은 태그라도 kind load 직후 노드 이미지가 바뀌므로
# 실행 중 Pod를 지우면 Deployment가 새 Pod를 띄우며 갱신된 이미지를 씀 (rollout restart만으로는
# 드물게 이전 레이어가 남는 환경이 있어 이 단계를 둠).
echo "🔄 실행 중 Pod 삭제 → 새 이미지로 재생성..."
kubectl delete pods -n $NAMESPACE -l app=$SERVICE_NAME --wait=false 2>/dev/null || true
kubectl rollout status deployment/$SERVICE_NAME -n $NAMESPACE --timeout=120s || true

# 서비스 상태 확인
echo "🌐 서비스 상태 확인..."
kubectl get service $SERVICE_NAME -n $NAMESPACE

# Pod 상태 확인
echo "📦 Pod 상태 확인..."
kubectl get pods -l app=$SERVICE_NAME -n $NAMESPACE

# HPA 상태 확인
echo "📈 HPA 상태 확인..."
kubectl get hpa ${SERVICE_NAME}-hpa -n $NAMESPACE 2>/dev/null || true

# 로그 확인 (선택사항)
if [ "$1" == "--logs" ] || [ "$2" == "--logs" ]; then
    echo "📝 최근 로그 확인..."
    kubectl logs -l app=$SERVICE_NAME -n $NAMESPACE --tail=50
fi

# 사용하지 않는 Docker 이미지 정리
echo "🧹 사용하지 않는 Docker 이미지 정리..."
docker image prune -f

# 빌드 캐시 정리 (캐시 남지 않도록)
echo "🧹 빌드 캐시 정리..."
docker builder prune -f

echo ""
echo "✅ web-service 배포 완료!"
echo "🔗 웹 UI: http://localhost:30012"
echo "   (API 연동: http://localhost:30012?apiBase=http://localhost:30005)"
echo ""
echo "📋 유용한 명령어:"
echo "  kubectl logs -f -l app=$SERVICE_NAME -n $NAMESPACE"
echo "  kubectl port-forward svc/$SERVICE_NAME 8080:80 -n $NAMESPACE"
echo ""
