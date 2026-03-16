#!/bin/bash

# integrated-swagger-service Kubernetes deployment script

set -e

NAMESPACE="flet-montrg"
SERVICE_NAME="integrated-swagger-service"
IMAGE_NAME="flet-montrg/integrated-swagger-service:latest"
KIND_CLUSTER="flet-cluster"

echo "🚀 Starting Integrated Swagger Service deployment..."

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
    cd ../../services/integrated-swagger-service
    docker build -t $IMAGE_NAME .
    cd ../../k8s/integrated-swagger
fi

# Load image into Kind
echo "📦 Loading image into Kind..."
kind load docker-image $IMAGE_NAME --name $KIND_CLUSTER

# Deploy RBAC and ConfigMap first
echo "🔐 Deploying RBAC resources..."
kubectl apply -f rbac.yaml

echo "⚙️ Deploying ConfigMap..."
kubectl apply -f configmap.yaml

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

# Check HPA status
echo "📈 Checking HPA status..."
kubectl get hpa $SERVICE_NAME-hpa -n $NAMESPACE

# Show logs (optional)
if [ "$1" == "--logs" ] || [ "$2" == "--logs" ]; then
    echo "📝 Tail recent logs..."
    kubectl logs -l app=$SERVICE_NAME -n $NAMESPACE --tail=50
fi

# Clean up unused Docker images
echo "🧹 Cleaning up unused Docker images..."
docker image prune -f

# Show access information
echo ""
echo "✅ Integrated Swagger Service deployment completed!"
echo "🔗 Public access is via web-service (NodePort 30000) — this service is not exposed directly"
echo "   Swagger UI / API (through web-service): http://localhost:30000"
echo ""
echo "📋 Useful commands:"
echo "  kubectl logs -f -l app=$SERVICE_NAME -n $NAMESPACE"
echo "  kubectl port-forward svc/$SERVICE_NAME 8000:80 -n $NAMESPACE"
echo "  kubectl port-forward svc/$SERVICE_NAME 8080:8080 -n $NAMESPACE"