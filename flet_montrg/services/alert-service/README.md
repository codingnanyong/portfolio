# 🚨 Alert Service

Alert creation and management API

## ✨ Features

- Create and query alerts
- Query by sensor or location
- Alert state (e.g. resolved)
- Threshold-breach alert records

## 🔌 API Endpoints

### Alerts

- `POST /api/v1/alerts` — Create alert
- `GET /api/v1/alerts` — List alerts
- `GET /api/v1/alerts/{alert_id}` — Get alert
- `GET /api/v1/alerts/by-sensor/{sensor_id}` — By sensor
- `GET /api/v1/alerts/by-location/{loc_id}` — By location
- `PUT /api/v1/alerts/{alert_id}` — Update alert
- `PUT /api/v1/alerts/{alert_id}/resolve` — Mark resolved

### Basic

- `GET /` — Service info
- `GET /health` — Health check
- `GET /ready` — Readiness check
- `GET /docs` — Swagger UI

## 🔧 Environment Variables

- `APP_NAME`: Application name (default: Alert Service)
- `APP_VERSION`: Version (default: 1.0.0)
- `DATABASE_URL`: Database URL
- `THRESHOLDS_SERVICE_URL`: Thresholds service URL
- `LOCATION_SERVICE_URL`: Location service URL
- `SENSOR_THRESHOLD_MAPPING_SERVICE_URL`: Sensor Threshold Mapping service URL

## ⚙️ Install & Run

### Local

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

```bash
docker build -t alert-service:latest .
docker run -p 8000:8000 --env-file .env alert-service:latest
```

---

**Last Updated**: February 2026
