# 🚨 Alert Service

API service for creating and managing alerts (threshold breach and resolution).

## ✨ Features

- 📝 Create and query alerts
- 📍 Query by sensor or location
- ✅ Resolve alerts (status management)
- 📊 Record threshold-exceeded alerts

## 🔌 API Endpoints

### Alert management

- `POST /api/v1/alerts` — create alert
- `GET /api/v1/alerts` — list alerts
- `GET /api/v1/alerts/{alert_id}` — get one
- `GET /api/v1/alerts/by-sensor/{sensor_id}` — alerts by sensor
- `GET /api/v1/alerts/by-location/{loc_id}` — alerts by location
- `PUT /api/v1/alerts/{alert_id}` — update alert
- `PUT /api/v1/alerts/{alert_id}/resolve` — mark as resolved

### Common endpoints

- `GET /` — service info
- `GET /health` — health check
- `GET /ready` — readiness check
- `GET /docs` — API docs (Swagger UI)

## ⚙️ Environment variables

- `APP_NAME` — Application name (default: Alert Service)
- `APP_VERSION` — Application version (default: 1.0.0)
- `DATABASE_URL` — Database connection URL
- `THRESHOLDS_SERVICE_URL` — Thresholds service URL
- `LOCATION_SERVICE_URL` — Location service URL
- `SENSOR_THRESHOLD_MAPPING_SERVICE_URL` — Sensor Threshold Mapping service URL

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
docker build -t flet-montrg/alert-service:latest .
docker run -p 8000:8000 --env-file .env flet-montrg/alert-service:latest
```

### K8s (Kind)

- **NodePort**: `30006` (see project [README](../../README.md) for port layout)

## 🐛 Troubleshooting

- DB connection failed: Check `DATABASE_URL`, DB server, network.
- Dependent services unreachable: Verify `THRESHOLDS_SERVICE_URL`, `LOCATION_SERVICE_URL`, `SENSOR_THRESHOLD_MAPPING_SERVICE_URL`.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)

Last updated: February 2026
