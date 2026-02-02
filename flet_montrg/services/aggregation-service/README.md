# Aggregation Service

Perceived-temperature aggregation and statistics API

## Features

- Hourly perceived-temperature aggregation
- Query by location and factory
- Structured JSON responses

## API Endpoints

### Perceived-temperature aggregation

- `GET /api/v1/aggregation/pcv_temperature/` — All pcv_temperature (max, avg) aggregation
- `GET /api/v1/aggregation/pcv_temperature/location/{location_id}` — By location
- `GET /api/v1/aggregation/pcv_temperature/factory/{factory}` — By factory

**Parameters:**

- `start_date`, `end_date`: Date range (supports yyyy, yyyyMM, yyyyMMdd)

**Notes:**

- Time range is 00:00–23:59 for the given dates
- Metrics are pcv_temperature_max, pcv_temperature_avg
- Dates can be yyyy, yyyyMM, or yyyyMMdd

### Basic endpoints

- `GET /` — Service info
- `GET /health` — Health check
- `GET /ready` — Readiness check
- `GET /docs` — Swagger UI

## Request/Response

### Example requests

**By location:**

```http
GET /api/v1/aggregation/pcv_temperature/location/A031?start_date=20240922&end_date=20240922
```

**By factory:**

```http
GET /api/v1/aggregation/pcv_temperature/factory/SinPyeong?start_date=20240922&end_date=20240922
```

**All:**

```http
GET /api/v1/aggregation/pcv_temperature/?start_date=20240922&end_date=20240922
```

### Example response

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

## Environment Variables

- `APP_NAME`: Application name (default: Aggregation Service)
- `APP_VERSION`: Version (default: 1.0.0)
- `DEBUG`: Debug mode (default: true)
- `ENVIRONMENT`: development/production
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DATABASE_URL`: PostgreSQL connection string
- `CORS_ORIGINS`: CORS origins
- `LOG_LEVEL`: Log level (default: INFO)

## Run

### Local

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker build -t flet-montrg/aggregation-service:latest .
docker run -p 8000:8000 flet-montrg/aggregation-service:latest
```

### Tests

```bash
./test.sh
./test.sh --format --lint
```

## Database

Uses:

- `flet_montrg.temperature` — Temperature data
- `flet_montrg.locations` — Location info
- `flet_montrg.aggregations` — Aggregation results
- `flet_montrg.aggregation_jobs` — Aggregation job metadata
