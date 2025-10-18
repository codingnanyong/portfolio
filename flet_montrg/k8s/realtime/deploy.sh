#!/bin/bash

# realtime-service Kubernetes 배포 스크립트

set -e

NAMESPACE="flet-montrg"
SERVICE_NAME="realtime-service"

echo "🚀 realtime-service 배포 시작..."

# 네임스페이스 확인
echo "📋 네임스페이스 확인: $NAMESPACE"
kubectl get namespace $NAMESPACE || kubectl create namespace $NAMESPACE

# 기존 리소스 삭제 (선택사항)
if [ "$1" == "--clean" ]; then
    echo "🧹 기존 리소스 정리..."
    kubectl delete -k . --ignore-not-found=true
    sleep 5
fi

# Kind에 이미지 로드
echo "📦 Kind에 이미지 로드..."
kind load docker-image flet-montrg/realtime-service:latest --name flet-cluster

# ConfigMap과 Secret 배포
echo "⚙️ ConfigMap 및 Secret 배포..."
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml

# 메인 리소스 배포
echo "📦 메인 리소스 배포..."
kubectl apply -k .

# 배포 상태 확인
echo "🔍 배포 상태 확인..."
kubectl rollout status deployment/$SERVICE_NAME -n $NAMESPACE

# 서비스 상태 확인
echo "🌐 서비스 상태 확인..."
kubectl get service $SERVICE_NAME -n $NAMESPACE

# Pod 상태 확인
echo "📦 Pod 상태 확인..."
kubectl get pods -l app=$SERVICE_NAME -n $NAMESPACE

# 로그 확인 (선택사항)
if [ "$1" == "--logs" ]; then
    echo "📝 로그 확인..."
    kubectl logs -l app=$SERVICE_NAME -n $NAMESPACE --tail=50
fi

echo "✅ realtime-service 배포 완료!"
echo "🌐 서비스 접속: http://localhost:30003"
echo "📊 API 문서: http://localhost:30003/docs"
