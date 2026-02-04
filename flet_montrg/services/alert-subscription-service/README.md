# 📋 Alert Subscription Service

Alert subscription management API

## ✨ Features

- Create and query subscriptions
- Per-subscriber subscription management
- Filter by location hierarchy (plant, factory, building, floor, area)
- Filter by sensor and threshold type
- Enable/disable subscriptions

## 🔌 API Endpoints

### Subscriptions

- `POST /api/v1/subscriptions` — Create subscription
- `GET /api/v1/subscriptions` — List (with filters)
- `GET /api/v1/subscriptions/{subscription_id}` — Get subscription
- `GET /api/v1/subscriptions/subscriber/{subscriber}` — By subscriber
- `PUT /api/v1/subscriptions/{subscription_id}` — Update
- `DELETE /api/v1/subscriptions/{subscription_id}` — Delete
- `POST /api/v1/subscriptions/{subscription_id}/enable` — Enable
- `POST /api/v1/subscriptions/{subscription_id}/disable` — Disable

### Basic

- `GET /` — Service info
- `GET /health` — Health check
- `GET /ready` — Readiness check
- `GET /docs` — Swagger UI

## 📊 Data Model

### Subscription fields

- `subscription_id`: Subscription ID (auto)
- `plant`, `factory`, `building`, `floor`, `area`
- `sensor_id`, `threshold_type`, `min_level`
- `subscriber`, `notify_type` (email, kakao, sms, app), `notify_id`
- `enabled`, `upd_dt`

## 🔧 Environment Variables

- `APP_NAME`: Application name (default: Alert Subscription Service)
- `APP_VERSION`: Version (default: 1.0.0)
- `DATABASE_URL`: Database URL
- `LOCATION_SERVICE_URL`: Location service URL

## ⚙️ Install & Run

### Local

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

```bash
docker build -t alert-subscription-service:latest .
docker run -p 8000:8000 --env-file .env alert-subscription-service:latest
```

---

**Last Updated**: February 2026
