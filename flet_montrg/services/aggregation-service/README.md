# 📊 Aggregation Service

API service for apparent temperature (PCV) data aggregation and statistics.

## ✨ Features

- 📈 Hourly aggregation of apparent temperature data
- 🏭 Query by location or factory
- 📋 Structured JSON responses

## 🔌 API Endpoints

### Apparent temperature aggregation

- `GET /api/v1/aggregation/pcv_temperature/` — aggregated data (max, avg) for all locations
- `GET /api/v1/aggregation/pcv_temperature/location/{location_id}` — by location
- `GET /api/v1/aggregation/pcv_temperature/factory/{factory}` — by factory

Query parameters:

- `start_date`, `end_date`: date range (`yyyy`, `yyyyMM`, or `yyyyMMdd`)

Notes:

- Time range is set to 00:00–23:59 automatically
- Metrics are fixed to `pcv_temperature_max` and `pcv_temperature_avg`
- Date granularity can be year, month, or day (`yyyy`, `yyyyMM`, `yyyyMMdd`)

### Common endpoints

- `GET /` — service info
- `GET /health` — health check
- `GET /ready` — readiness check
- `GET /docs` — API docs (Swagger UI)

## 📝 Request / Response

### Request examples

By location:

```http
GET /api/v1/aggregation/pcv_temperature/location/A031?start_date=20240922&end_date=20240922
```

By factory:

```http
GET /api/v1/aggregation/pcv_temperature/factory/SinPyeong?start_date=20240922&end_date=20240922
```

All locations:

```http
GET /api/v1/aggregation/pcv_temperature/?start_date=20240922&end_date=20240922
```

### Response example

```json
{
  "location": {
    "factory": "SinPyeong",
    "building": "F-2001",
    "floor": 1,
    "loc_id": "A031",
    "area": "Assembly 2",
    "date": [
      {
        "ymd": "20240922",
        "hour": "12",
        "metrics": {
          "pcv_temperature_max": "27.00",
          "pcv_temperature_avg": "27.00"
        }
      }
    ]
  }
}
```

## ⚙️ Environment variables

- `APP_NAME` — Application name (default: Aggregation Service)
- `APP_VERSION` — Application version (default: 1.0.0)
- `DEBUG` — Debug mode (default: true)
- `ENVIRONMENT` — Environment: `development` or `production`
- `HOST` — Server host (default: 0.0.0.0)
- `PORT` — Server port (default: 8000)
- `DATABASE_URL` — PostgreSQL connection string
- `CORS_ORIGINS` — Allowed CORS origins
- `LOG_LEVEL` — Log level (default: INFO)

## 🚀 Run

### Local development

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build image
docker build -t flet-montrg/aggregation-service:latest .

# Run container
docker run -p 8000:8000 flet-montrg/aggregation-service:latest
```

### K8s (Kind)

- **NodePort**: `30005` (see project [README](../../README.md) for port layout)

### Tests & quality

```bash
# Run tests
./test.sh

# Format and lint
./test.sh --format --lint
```

## 🗄️ Database schema

The service uses these tables:

- `flet_montrg.temperature` — raw temperature data
- `flet_montrg.locations` — location metadata
- `flet_montrg.aggregations` — aggregation results
- `flet_montrg.aggregation_jobs` — aggregation job state

## 🐛 Troubleshooting

- DB connection failed: Check `DATABASE_URL`, DB server, network. Test with `psql` or `docker logs <container>`.
- Empty aggregation results: Verify source data in `temperature` and `locations`; check date range and filters.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)

Last updated: February 2026
