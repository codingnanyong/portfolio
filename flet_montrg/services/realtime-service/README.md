# 🚀 Realtime Service

Real-time sensor data processing and monitoring API

## 📁 Project Structure

```text
realtime-service/
├── app/
│   ├── main.py                 # FastAPI entry
│   ├── api/v1/
│   │   └── endpoints/realtime.py
│   ├── clients/
│   │   ├── location_client.py
│   │   └── thresholds_client.py
│   ├── core/
│   ├── models/
│   └── services/
│       └── realtime_service.py
├── tests/
├── requirements.txt
├── env.example
├── Dockerfile
└── README.md
```

## ⚙️ Install & Run

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# or: docker build -t realtime-service . && docker run -p 8000:8000 --env-file .env realtime-service
```

## 🔌 API Endpoints

### Real-time temperature

- `GET /api/v1/realtime/` — All temperature data (with threshold checks)

### Filters

- `GET /api/v1/realtime/factory/{factory}` — By factory
- `GET /api/v1/realtime/building/{building}` — By building
- `GET /api/v1/realtime/floor/{floor}` — By floor
- `GET /api/v1/realtime/loc_id/{loc_id}` — By location ID
- `GET /api/v1/realtime/location?factory=...&building=...&floor=...&loc_id=...` — Multi-filter

### Response shape

```json
{
  "capture_dt": "<timestamp>",
  "ymd": "<YYYYMMDD>",
  "hh": "<HH>",
  "measurements": [
    {
      "location": {
        "factory": "Factory-A",
        "building": "Bld-1",
        "floor": 1,
        "loc_id": "LOC001",
        "area": "Area-1"
      },
      "metrics": {
        "temperature": { "value": "<val>", "status": "normal" },
        "humidity": { "value": "<val>", "status": null },
        "pcv_temperature": { "value": "<val>", "status": "normal" }
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
- Per-sensor-type mapping
- Alert level determination

## 📊 Data Models

- **TemperatureCurrentData**: capture_dt, ymd, hh, measurements
- **MeasurementData**: location (LocationInfo), metrics (MetricsData)
- **LocationInfo**: factory, building, floor, loc_id, area
- **MetricsData**: temperature, humidity, pcv_temperature (MetricData)
- **MetricData**: value, status ("normal" | "warning" | "critical" | null)

## 🚨 Threshold-based Status

- **normal** — Within range
- **warning** — Above threshold
- **critical** — Severe breach
- **null** — No threshold defined

Checks use per-sensor-type thresholds; priority: critical > warning > normal; null when no threshold.

## 🔧 Environment Variables

- `DATABASE_URL` — PostgreSQL/TimescaleDB URL
- `LOCATION_SERVICE_URL` — Location service (default: [http://location-service:80])
- `THRESHOLDS_SERVICE_URL` — Thresholds service (default: [http://thresholds-service:80])
- `DEBUG`, `LOG_LEVEL`, `CORS_ORIGINS`

## 📈 Monitoring

- `/health`
- Structured JSON logging
- Error handling and logging

## 🧪 Tests

```bash
pytest
pytest --cov=app
```

## 📝 Development

**New filter:** Add parameter to `_get_temperature_data_with_filters`, add endpoint in `realtime.py`, add condition in filtering.

**New metric type:** Add field to `MetricsData` in schemas.py; handle in `_process_measurement_data`; update thresholds client mapping.

**New external service:** Add client under `clients/`, add URL in config, use in realtime service.

**New threshold level:** Add level in thresholds-service Level enum; update `_check_thresholds` mapping.

---

**Last Updated**: February 2026
