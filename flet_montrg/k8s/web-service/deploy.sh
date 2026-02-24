#!/bin/bash

# web-service (API Gateway Web UI) Kubernetes 배포 스크립트

set -e

NAMESPACE="flet-montrg"
SERVICE_NAME="web-service"
IMAGE_NAME="flet-montrg/web-service:latest"
KIND_CLUSTER="flet-cluster"

echo "🚀 web-service 배포 시작..."

# 네임스페이스 확인
echo "📋 네임스페이스 확인: $NAMESPACE"
kubectl get namespace $NAMESPACE >/dev/null 2>&1 || kubectl create namespace $NAMESPACE

# 기존 리소스 삭제 (선택사항)
if [ "$1" == "--clean" ]; then
    echo "🧹 기존 리소스 정리..."
    kubectl delete -k . --ignore-not-found=true
    sleep 5
fi

# Docker 이미지 빌드 (항상 캐시 없이 빌드)
echo "🔨 Docker 이미지 빌드 (--no-cache)..."
cd ../../services/web-service
docker build --no-cache -t $IMAGE_NAME .
cd ../../k8s/web-service

# Kind에 이미지 로드
echo "📦 Kind에 이미지 로드..."
kind load docker-image $IMAGE_NAME --name $KIND_CLUSTER

# ConfigMap 배포
echo "⚙️ ConfigMap 배포..."
kubectl apply -f configmap.yaml

# 메인 리소스 배포
echo "📦 메인 리소스 배포..."
kubectl apply -k .

# 배포 상태 확인
echo "🔍 배포 상태 확인..."
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
