# 📚 Integrated Swagger Service

Unified API documentation and proxy for all microservices. Exposes a single Swagger UI and forwards API calls to the right backend services (with optional service discovery and monitoring).

**Note:** The separate Web dashboard UI has been removed. `app/static` remains from earlier use (e.g. Swagger UI assets only).

## ✨ Features

- 📖 Single Swagger UI for all microservice APIs
- 🔀 API proxy: one base URL for every backend
- 🔍 Service discovery from Kubernetes
- 💓 Health checks and status per service
- 📊 Metrics and monitoring endpoints (when enabled)
- 🔄 Live docs from each service’s OpenAPI spec

## 🎯 Proxied / monitored services

- aggregation-service
- alert-service
- alert-subscription-service
- alert-notification-service
- location-service
- realtime-service
- thresholds-service
- sensor-threshold-mapping-service

## 📁 Directory structure

```text
integrated-swagger-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry
│   ├── api/
│   │   ├── routes/
│   │   │   ├── swagger.py   # Swagger / OpenAPI aggregation
│   │   │   ├── proxy.py     # API proxy to backends
│   │   │   └── ui.py        # UI routes (if any)
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   └── kubernetes.py    # K8s client for discovery
│   ├── models/
│   │   ├── service.py
│   │   └── swagger.py
│   ├── services/
│   │   ├── swagger_collector.py
│   │   ├── discovery.py
│   │   ├── monitor.py
│   │   └── dashboard.py
│   └── static/              # Legacy; Swagger UI assets (Web UI removed)
├── Dockerfile
├── requirements.txt
├── env.example
└── README.md
```

## 🚀 Run

### Local

```bash
pip install -r requirements.txt
cp env.example .env
# Edit .env as needed

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

```bash
docker build -t flet-montrg/integrated-swagger-service:latest .
docker run -p 8000:8000 flet-montrg/integrated-swagger-service:latest
```

### K8s (Kind)

```bash
kubectl apply -f ../../k8s/integrated-swagger/
```

- **NodePort**: `30001` (see project [README](../../README.md) for port layout)

## 🌐 URLs

- **Swagger UI**: <http://localhost:8000/docs> (or `/` depending on app)
- **OpenAPI JSON**: <http://localhost:8000/openapi.json>
- **Health**: <http://localhost:8000/health>
- **Metrics**: <http://localhost:8000/metrics> (if implemented)

## 🔌 API endpoints

### Dashboard / overview

- `GET /api/v1/dashboard/services` — list service status
- `GET /api/v1/dashboard/overview` — dashboard overview

### Service monitoring

- `GET /api/v1/services` — list of monitored services
- `GET /api/v1/services/{service_name}/status` — status for one service
- `GET /api/v1/services/{service_name}/health` — health for one service

### Metrics

- `GET /api/v1/metrics/overview` — metrics overview
- `GET /api/v1/metrics/{service_name}` — metrics for one service

## ⚙️ Environment variables

See `env.example`. Typical: `DATABASE_URL` (if used), `HOST`, `PORT` (default 8000), K8s namespace for discovery, logging level.

## 📈 Monitoring (when enabled)

1. Service status: online/offline per service
2. API endpoint checks for each service
3. Performance: response time, throughput, error rate
4. Resource usage: CPU/memory where available
5. Alerts on failure (planned)

## 📋 Possible improvements

- [ ] Real-time alerting
- [ ] Persisted history for metrics
- [ ] Custom dashboard layout
- [ ] Per-service SLA monitoring
- [ ] Unified log viewer

## 🐛 Troubleshooting

- Backend services not discovered: Check K8s namespace and service names; verify in-cluster DNS or configured URLs.
- Proxy returns 502/503: Ensure target microservices are running and reachable from this pod.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAPI/Swagger](https://swagger.io/specification/)
- [Pytest](https://docs.pytest.org/)

Last updated: February 2026
