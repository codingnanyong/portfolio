# 🔗 Sensor Threshold Mapping Service

Sensor–threshold mapping management API

## ✨ Features

- Create and query sensor–threshold mappings
- Filter by sensor or threshold
- Enable/disable mappings
- Validity window (effective_from, effective_to)

## 🔌 API Endpoints

### Mappings

- `POST /api/v1/mappings` — Create mapping
- `GET /api/v1/mappings` — List (with filters)
- `GET /api/v1/mappings/{map_id}` — Get mapping
- `GET /api/v1/mappings/sensor/{sensor_id}` — By sensor
- `GET /api/v1/mappings/threshold/{threshold_id}` — By threshold
- `PUT /api/v1/mappings/{map_id}` — Update
- `DELETE /api/v1/mappings/{map_id}` — Delete
- `POST /api/v1/mappings/{map_id}/enable` — Enable
- `POST /api/v1/mappings/{map_id}/disable` — Disable

### Basic

- `GET /` — Service info
- `GET /health` — Health check
- `GET /ready` — Readiness check
- `GET /docs` — Swagger UI

## 📊 Data Model

### Mapping fields

- `map_id`: Mapping ID (auto)
- `sensor_id`, `threshold_id`
- `duration_seconds`: Duration in seconds (default: 60)
- `enabled`: Default true
- `effective_from`, `effective_to`, `upd_dt`

## 🔧 Environment Variables

- `APP_NAME`: Application name (default: Sensor Threshold Mapping Service)
- `APP_VERSION`: Version (default: 1.0.0)
- `DATABASE_URL`: Database URL
- `THRESHOLDS_SERVICE_URL`: Thresholds service URL
- `LOCATION_SERVICE_URL`: Location service URL

## ⚙️ Install & Run

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Tests

```bash
./tests/test.sh
# or
pytest tests/ -v
```

## 🚀 Deployment (Kubernetes)

```bash
cd k8s/sensor-threshold-mapping
./deploy.sh
```

## 🔌 Ports

- HTTP: 30011
- Metrics: 30240

---

**Last Updated**: February 2026
