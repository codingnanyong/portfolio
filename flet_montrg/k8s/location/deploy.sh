#!/bin/bash

# location-service Kubernetes deployment script

set -e

NAMESPACE="flet-montrg"
SERVICE_NAME="location-service"
IMAGE_NAME="flet-montrg/location-service:latest"
KIND_CLUSTER="flet-cluster"

echo "🚀 Starting location-service deployment..."

# Check namespace
echo "📋 Checking namespace: $NAMESPACE"
kubectl get namespace $NAMESPACE || kubectl create namespace $NAMESPACE

# Delete existing resources (optional)
if [ "$1" == "--clean" ]; then
    echo "🧹 Cleaning up existing resources..."
    kubectl delete -k . --ignore-not-found=true
    sleep 5
fi

# Build Docker image (optional - skip if already built)
if [ "$1" != "--no-build" ] && [ "$2" != "--no-build" ]; then
    echo "🔨 Building Docker image..."
    cd ../../services/location-service
    docker build -t $IMAGE_NAME .
    cd ../../k8s/location
fi

# Load image into Kind
echo "📦 Loading image into Kind..."
kind load docker-image $IMAGE_NAME --name $KIND_CLUSTER

# Deploy ConfigMap and Secret
echo "⚙️ Deploying ConfigMap and Secret..."
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml

# Deploy main resources
echo "📦 Deploying main resources..."
kubectl apply -k .

# Check rollout status
echo "🔍 Checking rollout status..."
kubectl rollout status deployment/$SERVICE_NAME -n $NAMESPACE --timeout=300s || true

# Check service status
echo "🌐 Checking service status..."
kubectl get service $SERVICE_NAME -n $NAMESPACE

# Check pod status
echo "📦 Checking pod status..."
kubectl get pods -l app=$SERVICE_NAME -n $NAMESPACE

# Show logs (optional)
if [ "$1" == "--logs" ]; then
    echo "📝 Tail logs..."
    kubectl logs -l app=$SERVICE_NAME -n $NAMESPACE --tail=50
fi

# Clean up unused Docker images
echo "🧹 Cleaning up unused Docker images..."
docker image prune -f

echo "✅ location-service deployment completed!"
echo "🌐 Service URL: http://localhost:30003"
echo "📊 API Docs: http://localhost:30003/docs"
