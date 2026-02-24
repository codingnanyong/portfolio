# 🔗 Sensor Threshold Mapping Service

API for managing sensor–threshold mappings (which threshold applies to which sensor, with validity and enable/disable).

## ✨ Features

- 📝 Create and query mappings per sensor or threshold
- 🔍 Filter by sensor_id or threshold_id
- 🔘 Enable / disable mappings
- 📅 Validity window: `effective_from`, `effective_to`
- ⏱️ `duration_seconds` for alert evaluation (e.g. 60)

## 🔌 API Endpoints

### Mapping management

- `POST /api/v1/mappings` — create mapping
- `GET /api/v1/mappings` — list (with filters)
- `GET /api/v1/mappings/{map_id}` — get one
- `GET /api/v1/mappings/sensor/{sensor_id}` — list by sensor
- `GET /api/v1/mappings/threshold/{threshold_id}` — list by threshold
- `PUT /api/v1/mappings/{map_id}` — update
- `DELETE /api/v1/mappings/{map_id}` — delete
- `POST /api/v1/mappings/{map_id}/enable` — enable
- `POST /api/v1/mappings/{map_id}/disable` — disable

### Common endpoints

- `GET /` — service info
- `GET /health` — health check
- `GET /ready` — readiness check
- `GET /docs` — Swagger UI

## 📊 Data model

### Mapping fields

- `map_id` — ID (auto)
- `sensor_id` — sensor ID
- `threshold_id` — threshold ID
- `duration_seconds` — duration in seconds (default: 60)
- `enabled` — active or not (default: true)
- `effective_from` — valid from
- `effective_to` — valid to
- `upd_dt` — last updated

## ⚙️ Environment variables

- `APP_NAME` — Application name (default: Sensor Threshold Mapping Service)
- `APP_VERSION` — Application version (default: 1.0.0)
- `DATABASE_URL` — Database connection URL
- `THRESHOLDS_SERVICE_URL` — Thresholds service URL
- `LOCATION_SERVICE_URL` — Location service URL

## 🚀 Run

### Local

```bash
pip install -r requirements.txt
cp env.example .env
# Edit .env as needed

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker build -t sensor-threshold-mapping-service .
docker run -p 8000:8000 --env-file .env sensor-threshold-mapping-service
```

### K8s (Kind)

- **NodePort**: `30009` (see project [README](../../README.md) for port layout)

```bash
# From repo root
kubectl apply -f k8s/sensor-threshold-mapping/
# Or from this service dir:
kubectl apply -f ../../k8s/sensor-threshold-mapping/
```

## 🧪 Tests

```bash
./tests/test.sh
# or
pytest tests/ -v
```

## 🐛 Troubleshooting

- DB connection failed: Check `DATABASE_URL`, DB server, network.
- Empty or missing mappings: Verify data in `sensor_threshold_map`; check effective_from/effective_to and enabled flag.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)

Last updated: February 2026

