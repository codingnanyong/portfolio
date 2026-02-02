# 🚀 Realtime Service

Real-time sensor data processing and monitoring API

## 📁 Project Structure

```text
realtime-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py          # API v1 router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── realtime.py  # Real-time data API endpoints
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── location_client.py  # Location service client
│   │   └── thresholds_client.py # Thresholds service client
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database connection
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── logging.py          # Logging config
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database_models.py  # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       └── realtime_service.py  # Real-time data processing logic
├── tests/
│   ├── __init__.py
│   └── conftest.py             # pytest config
├── requirements.txt           # Python dependencies
├── env.example                # Environment variable example
├── Dockerfile                 # Docker config
└── README.md                  # This file
```

## ⚙️ Install & Run

### 1. 📦 Dependencies

```bash
pip install -r requirements.txt
```

### 2. 🔧 Environment

```bash
cp env.example .env
# Edit .env as needed
```

### 3. ▶️ Run

```bash
# Development
python -m app.main

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 🐳 Docker

```bash
docker build -t realtime-service .
docker run -p 8000:8000 --env-file .env realtime-service
```

## 🔌 API Endpoints

### Real-time temperature

- `GET /api/v1/realtime/` — All temperature data (with threshold checks)

### Filters

- `GET /api/v1/realtime/factory/{factory}` — By factory
- `GET /api/v1/realtime/building/{building}` — By building
- `GET /api/v1/realtime/floor/{floor}` — By floor
- `GET /api/v1/realtime/loc_id/{loc_id}` — By location ID

### Multi-filter

- `GET /api/v1/realtime/location?factory=...&building=...&floor=...&loc_id=...` — By location (multi-filter)

### Response structure

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
        "temperature": {
          "value": "22.1",
          "status": "normal"
        },
        "humidity": {
          "value": "77.7",
          "status": null
        },
        "pcv_temperature": {
          "value": "23.8",
          "status": "normal"
        }
      }
    }
  ]
}
```

## 🔗 External Services

### Location Service

- Sensor location lookup
- Grouping by location

### Thresholds Service

- Threshold lookup
- Per-sensor-type threshold mapping
- Alert level determination

## 📊 Data Models

### TemperatureCurrentData

- `capture_dt`: Measurement time
- `ymd`: Date (YYYYMMDD)
- `hh`: Hour (HH)
- `measurements`: List of measurements

### MeasurementData

- `location`: Location info (LocationInfo)
- `metrics`: Metrics (MetricsData)

### LocationInfo

- `factory`: Factory name
- `building`: Building name
- `floor`: Floor
- `loc_id`: Location ID
- `area`: Area name

### MetricsData

- `temperature`: Temperature (MetricData)
- `humidity`: Humidity (MetricData)
- `pcv_temperature`: PCV temperature (MetricData)

### MetricData

- `value`: Value (Decimal)
- `status`: Status ("normal", "warning", "critical", null)

## 🚨 Threshold-based Status

### Status levels

- `normal` — Within range
- `warning` — Above threshold
- `critical` — Severe breach
- `null` — No threshold defined

### Threshold checks

- Per-sensor-type mapping (temperature, humidity, pcv_temperature)
- Real-time range checks
- Priority: critical > warning > normal
- Returns null when no threshold is set

## 🔧 Configuration

### Environment variables

- `DATABASE_URL` — PostgreSQL/TimescaleDB URL
- `LOCATION_SERVICE_URL` — Location service URL (default: http://location-service:80)
- `THRESHOLDS_SERVICE_URL` — Thresholds service URL (default: http://thresholds-service:80)
- `DEBUG` — Debug mode (default: false)
- `LOG_LEVEL` — Log level (default: INFO)
- `CORS_ORIGINS` — CORS origins (default: ["*"])

## 📈 Monitoring

- Health check endpoint (`/health`)
- Structured JSON logging
- Error handling and logging

## 🧪 Tests

```bash
# Run tests
pytest

# With coverage
pytest --cov=app
```

## 📝 Development Guide

### Adding a filter

1. Add filter parameter to `_get_temperature_data_with_filters` in `temperature_service.py`
2. Add new endpoint in `realtime.py`
3. Add condition in filtering logic

### Adding a metric type

1. Add field to `MetricsData` in `schemas.py`
2. Add handling in `_process_measurement_data` in `temperature_service.py`
3. Update mapping in `thresholds_client.py`

### External service integration

1. Add new client under `clients/`
2. Add service URL in `config.py`
3. Use client in `temperature_service.py`

### Adding a threshold level

1. Add level to `Level` enum in `thresholds-service`
2. Update level mapping in `_check_thresholds` in `temperature_service.py`
