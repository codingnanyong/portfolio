# 📡 Realtime Service

Real-time sensor data and monitoring API (temperature, humidity, PCV temperature with threshold-based status).

## ✨ Features

- 📊 Real-time temperature and metrics per location
- 🔍 Filter by factory, building, floor, or loc_id; multi-filter support
- 🚦 Threshold-based status (normal / warning / critical) via Thresholds service
- 🔗 Integrates Location and Thresholds services for enrichment
- 💓 Health check and structured logging

## 📁 Project structure

```text
realtime-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry
│   ├── api/
│   │   └── v1/
│   │       ├── api.py          # API v1 router
│   │       └── endpoints/
│   │           └── realtime.py # Realtime API endpoints
│   ├── clients/
│   │   ├── location_client.py  # Location service client
│   │   └── thresholds_client.py # Thresholds service client
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── models/
│   │   ├── database_models.py  # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   └── services/
│       └── temperature_service.py # Realtime data and threshold logic
├── tests/
│   └── conftest.py
├── requirements.txt
├── env.example
├── Dockerfile
└── README.md
```

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
docker build -t realtime-service .
docker run -p 8000:8000 --env-file .env realtime-service
```

### K8s (Kind)

- **NodePort**: `30003` (see project [README](../../README.md) for port layout)

## 🔌 API endpoints

### Realtime temperature data

- `GET /api/v1/realtime/` — all temperature data (with threshold checks)

### By single filter

- `GET /api/v1/realtime/factory/{factory}` — by factory
- `GET /api/v1/realtime/building/{building}` — by building
- `GET /api/v1/realtime/floor/{floor}` — by floor
- `GET /api/v1/realtime/loc_id/{loc_id}` — by location ID

### Multi-filter

- `GET /api/v1/realtime/location?factory=...&building=...&floor=...&loc_id=...` — combined location filters

### Response shape

```json
{
  "capture_dt": "2025-09-12T05:59:38.837000Z",
  "ymd": "20250912",
  "hh": "14",
  "measurements": [
    {
      "location": {
        "factory": "SinPyeong",
        "building": "MX-1",
        "floor": 1,
        "loc_id": "A011",
        "area": "Storage"
      },
      "metrics": {
        "temperature": { "value": "22.1", "status": "normal" },
        "humidity": { "value": "77.7", "status": null },
        "pcv_temperature": { "value": "23.8", "status": "normal" }
      }
    }
  ]
}
```

## 🔗 Integration

- **Location Service**: sensor location and grouping
- **Thresholds Service**: threshold lookup, per-sensor-type mapping, status level (normal / warning / critical)

## 📊 Data model

- **TemperatureCurrentData**: `capture_dt`, `ymd`, `hh`, `measurements`
- **MeasurementData**: `location` (LocationInfo), `metrics` (MetricsData)
- **LocationInfo**: `factory`, `building`, `floor`, `loc_id`, `area`
- **MetricsData**: `temperature`, `humidity`, `pcv_temperature` (each MetricData)
- **MetricData**: `value` (Decimal), `status` ("normal" | "warning" | "critical" | null)

## 🚦 Threshold-based status

- **normal** — within range
- **warning** — above warning threshold
- **critical** — above critical threshold
- **null** — no threshold defined for that metric

Thresholds are resolved via Thresholds service; priority is critical > warning > normal.

## ⚙️ Environment variables

- `DATABASE_URL` — PostgreSQL/TimescaleDB URL
- `LOCATION_SERVICE_URL` — Location service URL (default: <http://location-service:80>)
- `THRESHOLDS_SERVICE_URL` — Thresholds service URL (default: <http://thresholds-service:80>)
- `DEBUG` — debug mode (default: false)
- `LOG_LEVEL` — log level (default: INFO)
- `CORS_ORIGINS` — CORS origins (default: ["*"])

## 📈 Monitoring

- Health: `GET /health`
- Structured JSON logging and error handling

## 🧪 Tests

```bash
pytest
pytest --cov=app
```

## 📝 Development guide

### Add a new filter

1. Add filter parameters in `temperature_service.py` → `_get_temperature_data_with_filters`.
2. Add endpoint in `realtime.py`.
3. Update filtering logic.

### Add a new metric type

1. Add field to `MetricsData` in `schemas.py`.
2. Handle it in `temperature_service.py` → `_process_measurement_data`.
3. Update mapping in `thresholds_client.py`.

### Add external service client

1. Add client under `clients/`.
2. Add URL in `config.py`.
3. Use client in `temperature_service.py`.

### Add threshold level

1. Add level to `Level` enum in thresholds-service.
2. Update level mapping in `temperature_service.py` → `_check_thresholds`.

## 🐛 Troubleshooting

- DB connection failed: Check `DATABASE_URL`, DB server, network.
- Location/Thresholds client errors: Verify `LOCATION_SERVICE_URL`, `THRESHOLDS_SERVICE_URL`; ensure those services are up.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)

Last updated: February 2026
