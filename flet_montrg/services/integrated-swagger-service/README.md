# 📊 API Dashboard Service (Integrated Swagger)

Centralized API monitoring dashboard. Monitors and visualizes the status of all microservices running in the Kubernetes cluster.

## 📋 Features

- **Real-time service status**: Health and status of each API service
- **Service discovery**: Auto-discovery of services from Kubernetes
- **Endpoint monitoring**: Status of each service’s API endpoints
- **Performance metrics**: Response time, error rate, request count
- **Web dashboard**: Flet-based interactive UI
- **Auto-refresh**: Live updates

## 🚀 Monitored Services

- aggregation-service
- alert-service
- alert-history-service
- location-service
- realtime-service
- thresholds-service

## 📁 Structure

```text
api-dashboard-service/
├── app/
│   ├── main.py                 # FastAPI entry
│   ├── api/routes/
│   │   ├── dashboard.py        # Dashboard API
│   │   ├── services.py         # Service status API
│   │   └── metrics.py          # Metrics API
│   ├── core/
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   └── kubernetes.py       # K8s client
│   ├── models/
│   ├── services/
│   │   ├── dashboard.py        # Flet dashboard
│   │   ├── monitor.py
│   │   └── discovery.py
├── tests/
├── Dockerfile
├── requirements.txt
├── env.example
└── README.md
```

## ⚙️ Install & Run

### 🖥️ Local

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 🐳 Docker

```bash
docker build -t api-dashboard-service .
docker run -p 8000:8000 -p 8080:8080 api-dashboard-service
```

### ☸️ Kubernetes

```bash
kubectl apply -f ../k8s/api-dashboard/
```

## 🌐 Access

- **API docs**: [http://localhost:8000/docs]
- **Dashboard UI**: [http://localhost:8080]
- **Health**: [http://localhost:8000/health]
- **Metrics**: [http://localhost:8000/metrics]

## 🔌 API Endpoints

### 📊 Dashboard

- `GET /api/v1/dashboard/services` — All service status
- `GET /api/v1/dashboard/overview` — Overview

### 🔍 Service monitoring

- `GET /api/v1/services` — Monitored services list
- `GET /api/v1/services/{service_name}/status` — Service status
- `GET /api/v1/services/{service_name}/health` — Health check

### 📈 Metrics

- `GET /api/v1/metrics/overview` — Overall metrics
- `GET /api/v1/metrics/{service_name}` — Per-service metrics

## 🔧 Environment Variables

See `env.example`.

## 🧪 Tests

```bash
pytest
```

## 📡 Monitoring

1. Service status (online/offline)
2. API endpoint status per service
3. Performance: response time, throughput, error rate
4. Resource usage (CPU, memory where available)
5. Alerts on failure (planned)

## 🚀 Roadmap

- [ ] Real-time alerts
- [ ] History storage
- [ ] Custom dashboard layout
- [ ] Per-service SLA monitoring
- [ ] Integrated log viewer

---

**Last Updated**: February 2026
