# 📋 Alert Subscription Service

API service for managing alert subscriptions (who gets notified and where).

## ✨ Features

- 📝 Create and query subscriptions
- 👤 Manage subscriptions per subscriber
- 🏭 Filter by location hierarchy (plant, factory, building, floor, area)
- 🔧 Filter by sensor or threshold type
- 🔘 Enable / disable subscriptions

## 🔌 API Endpoints

### Subscription management

- `POST /api/v1/subscriptions` — create subscription
- `GET /api/v1/subscriptions` — list (with filters)
- `GET /api/v1/subscriptions/{subscription_id}` — get one
- `GET /api/v1/subscriptions/subscriber/{subscriber}` — list by subscriber
- `PUT /api/v1/subscriptions/{subscription_id}` — update
- `DELETE /api/v1/subscriptions/{subscription_id}` — delete
- `POST /api/v1/subscriptions/{subscription_id}/enable` — enable
- `POST /api/v1/subscriptions/{subscription_id}/disable` — disable

### Common endpoints

- `GET /` — service info
- `GET /health` — health check
- `GET /ready` — readiness check
- `GET /docs` — API docs (Swagger UI)

## 📐 Data model

### Subscription fields

- `subscription_id` — ID (auto)
- `plant` — plant
- `factory` — factory name
- `building` — building
- `floor` — floor
- `area` — area
- `sensor_id` — sensor ID
- `threshold_type` — threshold type
- `min_level` — minimum alert level
- `subscriber` — subscriber name
- `notify_type` — notification type: `email`, `kakao`, `sms`, `app`
- `notify_id` — contact (e.g. email address or app account)
- `enabled` — whether subscription is active
- `upd_dt` — last updated

## ⚙️ Environment variables

- `APP_NAME` — Application name (default: Alert Subscription Service)
- `APP_VERSION` — Application version (default: 1.0.0)
- `DATABASE_URL` — Database connection URL
- `LOCATION_SERVICE_URL` — Location service URL

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
docker build -t flet-montrg/alert-subscription-service:latest .
docker run -p 8000:8000 --env-file .env flet-montrg/alert-subscription-service:latest
```

### K8s (Kind)

- **NodePort**: `30007` (see project [README](../../README.md) for port layout)

## 🐛 Troubleshooting

- DB connection failed: Check `DATABASE_URL`, DB server, network.
- Location service unreachable: Verify `LOCATION_SERVICE_URL` for hierarchy-based filters.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)

Last updated: February 2026
