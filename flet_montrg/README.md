# 📊 flet-montrg MicroServices

MicroService APIs for perceived-temperature monitoring and alerting via IoT sensors

## 📋 Overview

flet-montrg is a microservice-based API platform for real-time monitoring and analysis of IoT sensor data from manufacturing sites. It is built with FastAPI and deployed and managed via Kubernetes.

### Core Features

- 🌡️ **Real-time temperature monitoring**: Live sensor data and threshold checks
- 📍 **Location-based management**: Sensor locations by factory/building/floor/area
- 📊 **Data aggregation**: Hourly max/avg temperature statistics
- ⚙️ **Threshold management**: Per-sensor-type threshold CRUD
- 🚨 **Alerting**: Real-time alerts on threshold breach (in progress)

## 📁 Project Structure

```text
flet_montrg/
├── services/                     # Microservice source
│   ├── thresholds-service/       # Threshold CRUD API
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── location-service/         # Sensor location API
│   ├── realtime-service/         # Real-time status API
│   │   ├── app/
│   │   │   ├── clients/
│   │   │   ├── services/
│   │   │   └── ...
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   ├── aggregation-service/      # Period query API
│   ├── alert-service/
│   ├── alert-subscription-service/
│   ├── alert-notification-service/
│   ├── sensor-threshold-mapping-service/
│   └── integrated-swagger-service/
│
└── k8s/                          # Kubernetes manifests
    ├── thresholds/
    ├── location/
    ├── realtime/
    ├── aggregation/
    ├── alert/
    ├── alert-subscription/
    ├── alert-notification/
    ├── sensor-threshold-mapping/
    └── integrated-swagger/
```

## 🔌 Services & Ports

| Service | Port | Main endpoints | Description | Status |
| ------- | ----- | -------------- | ----------- | ------ |
| **thresholds-service** | 30001 | `/api/v1/thresholds/` | Threshold CRUD | ✅ Done |
| **location-service** | 30002 | `/api/v1/locations/` | Location info | ✅ Done |
| **realtime-service** | 30003 | `/api/v1/realtime/` | Real-time sensor data | ✅ Done |
| **aggregation-service** | 30004 | `/api/v1/aggregation/pcv_temperature/` | Aggregation | ✅ Done |
| **integrated-swagger-service** | 30005 | `/` | Unified API docs | ✅ Done |
| **alert-service** | 30007 | `/api/v1/alerts/` | Alert creation & management | ✅ Done |
| **alert-subscription-service** | 30008 | `/api/v1/subscriptions/` | Alert subscriptions | ✅ Done |
| **alert-notification-service** | 30009 | `/api/v1/notifications/` | Notification history | ✅ Done |
| **sensor-threshold-mapping-service** | 30011 | `/api/v1/mappings/` | Sensor–threshold mapping | ✅ Done |

### API docs

Each service exposes interactive docs via Swagger UI:

- Thresholds: <http://localhost:30001/docs>
- Location: <http://localhost:30002/docs>
- Realtime: <http://localhost:30003/docs>
- Aggregation: <http://localhost:30004/docs>
- **Integrated Swagger** (all services): <http://localhost:30005/>
- Alert: <http://localhost:30007/docs>
- Alert Subscription: <http://localhost:30008/docs>
- Alert Notification: <http://localhost:30009/docs>
- Sensor-Threshold Mapping: <http://localhost:30011/docs>

## 🏗️ Architecture

```text
┌───────────────────────────────────────────────────────────┐
│                Kubernetes Cluster (Kind)                  │
│                Namespace: flet-montrg                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  Thresholds(30001)      Location(30002)                   │
│        \                    /                             │
│         +---> Sensor-Threshold-Mapping(30011)             │
│                         |                                 │
│               Realtime(30003) ---> Aggregation(30004)     │
│                                                           │
│  Alert(30007) <--> Alert-Subscription(30008)              │
│                              |                            │
│                              v                            │
│                   Alert-Notification(30009)               │
│                                                           │
│  Integrated-Swagger(30005)                                │
│                                                           │
└───────────────────────┬───────────────────────────────────┘
                        │
                        v
            PostgreSQL / TimescaleDB
```

### Inter-service communication

- **Realtime Service** → Location Service, Thresholds Service
- **Sensor-Threshold-Mapping** → Thresholds Service, Location Service
- **Alert Service** → Thresholds, Location, Sensor-Threshold-Mapping; notifies Alert-Notification
- **Alert-Notification** → Alert Service, Alert-Subscription (match subscribers)
- All services → PostgreSQL: read/write

## 🛠️ Tech Stack

### Backend

- **Framework**: FastAPI (async)
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy 2.0 (Async)
- **Validation**: Pydantic v2
- **HTTP client**: httpx (async)

### Database

- **DBMS**: PostgreSQL 14+
- **Extension**: TimescaleDB (time-series)
- **Driver**: asyncpg

### Containers & orchestration

- **Containers**: Docker
- **Orchestration**: Kubernetes (Kind)
- **Packaging**: Kustomize
- **Scaling**: HPA (Horizontal Pod Autoscaler)

### Monitoring & logging

- **Health**: Kubernetes Liveness/Readiness Probes
- **Logging**: Structured JSON
- **Metrics**: Prometheus (planned)
- **Dashboard**: Kubernetes Dashboard

## 🚀 Quick start

### 1. Prerequisites

```bash
docker --version

# Kind (macOS example)
brew install kind

# kubectl
brew install kubectl
```

### 2. Create cluster

```bash
kind create cluster --name flet-cluster
kubectl cluster-info --context kind-flet-cluster
kubectl create namespace flet-montrg
```

### 3. Build images

```bash
cd services/thresholds-service && docker build -t flet-montrg/thresholds-service:latest .
cd ../location-service && docker build -t flet-montrg/location-service:latest .
cd ../realtime-service && docker build -t flet-montrg/realtime-service:latest .
cd ../aggregation-service && docker build -t flet-montrg/aggregation-service:latest .
# ... other services
```

### 4. Load images into Kind

```bash
kind load docker-image flet-montrg/thresholds-service:latest --name flet-cluster
kind load docker-image flet-montrg/location-service:latest --name flet-cluster
kind load docker-image flet-montrg/realtime-service:latest --name flet-cluster
kind load docker-image flet-montrg/aggregation-service:latest --name flet-cluster
```

### 5. Deploy

```bash
kubectl apply -f k8s/thresholds/
kubectl apply -f k8s/location/
kubectl apply -f k8s/realtime/
kubectl apply -f k8s/aggregation/
# Or: cd k8s/<service> && ./deploy.sh
```

### 6. Verify

```bash
kubectl get pods -n flet-montrg
kubectl get svc -n flet-montrg
kubectl logs -f -n flet-montrg <pod-name>
```

### 7. Access

```bash
kubectl port-forward -n flet-montrg service/thresholds-service 30001:80
kubectl port-forward -n flet-montrg service/location-service 30002:80
kubectl port-forward -n flet-montrg service/realtime-service 30003:80
kubectl port-forward -n flet-montrg service/aggregation-service 30004:80

curl http://localhost:30001/health
curl http://localhost:30002/api/v1/locations/
curl http://localhost:30003/api/v1/realtime/
curl http://localhost:30004/api/v1/aggregation/pcv_temperature/?start_date=20240922&end_date=20240922
```

## 🧭 Local development

Run each service in dev mode (example):

```bash
cd services/thresholds-service
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Docs: http://localhost:8000/docs
```

For realtime-service, set `LOCATION_SERVICE_URL` and `THRESHOLDS_SERVICE_URL` in `.env`.

## 🧪 Tests

```bash
cd services/<service>
pytest
pytest --cov=app --cov-report=html
pytest tests/unit/
pytest tests/integration/
```

## 📊 Monitoring

- Kubernetes Dashboard: deploy and use token as per official docs
- `kubectl top pods -n flet-montrg`
- `kubectl get hpa -n flet-montrg`
- `kubectl logs -f -n flet-montrg <pod-name>`

## 🔧 Config (ConfigMap & Secret)

Each service uses ConfigMap for app config and Secret for `DATABASE_URL` and other secrets. See `k8s/<service>/configmap.yaml` and `secret.yaml`. Create secrets with `kubectl create secret generic ...` or from `.env`.

## 🔄 HPA

Services use CPU/memory-based HPA (see `k8s/*/hpa.yaml`).

## 🔒 Security

NetworkPolicy examples in `k8s/*/network-policy.yaml` restrict pod ingress/egress.

## 📚 Service docs

- [Thresholds Service](./services/thresholds-service/README.md)
- [Location Service](./services/location-service/README.md)
- [Realtime Service](./services/realtime-service/README.md)
- [Aggregation Service](./services/aggregation-service/README.md)
- [Alert Service](./services/alert-service/README.md)
- [Alert Subscription](./services/alert-subscription-service/README.md)
- [Alert Notification](./services/alert-notification-service/README.md)
- [Sensor-Threshold Mapping](./services/sensor-threshold-mapping-service/README.md)
- [Integrated Swagger](./services/integrated-swagger-service/README.md)

## 🐛 Troubleshooting

**Pod not starting**: `kubectl describe pod -n flet-montrg <pod>`, check events and logs.

**Image pull**: Load image into Kind: `kind load docker-image flet-montrg/<service>:latest --name flet-cluster`; consider `imagePullPolicy: IfNotPresent`.

**Service-to-service**: Check DNS, e.g. `nslookup location-service.flet-montrg.svc.cluster.local` from a debug pod; verify NetworkPolicies.

## 🌟 Roadmap

- [ ] Centralized logging (ELK)
- [ ] Distributed tracing (Jaeger)
- [ ] Prometheus & Grafana
- [ ] CI/CD (e.g. GitHub Actions)
- [ ] Ingress & TLS
- [ ] Rate limiting & API Gateway

---

**Last Updated**: February 2026
