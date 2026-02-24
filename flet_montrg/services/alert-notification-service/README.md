# 📬 Alert Notification Service

API service for sending notifications and managing delivery history.

## ✨ Features

- 📋 Notification delivery history
- 📊 Status tracking: `PENDING`, `SENT`, `FAILED`, `RETRYING`
- 🔄 Retry logic
- 🔍 Notifications by alert or by subscription
- ⏳ Pending and failed notification queries

## 🔌 API Endpoints

### Notification CRUD

- `POST /api/v1/notifications/` — create notification
- `GET /api/v1/notifications/` — list notifications
- `GET /api/v1/notifications/{notification_id}` — get one
- `PUT /api/v1/notifications/{notification_id}` — update
- `DELETE /api/v1/notifications/{notification_id}` — delete

### Status updates

- `POST /api/v1/notifications/{notification_id}/mark-sent` — mark as sent
- `POST /api/v1/notifications/{notification_id}/mark-failed` — mark as failed
- `POST /api/v1/notifications/{notification_id}/mark-retrying` — mark as retrying

### Query endpoints

- `GET /api/v1/notifications/alert/{alert_id}` — notifications for an alert
- `GET /api/v1/notifications/subscription/{subscription_id}` — notifications for a subscription
- `GET /api/v1/notifications/pending` — pending notifications
- `GET /api/v1/notifications/failed` — failed notifications

## ⚙️ Environment variables

Copy `env.example` to `.env` and set values. Common variables: `DATABASE_URL`, `HOST`, `PORT` (default 8000), `LOG_LEVEL`, `CORS_ORIGINS`.

## 🚀 Run

### Local

```bash
uvicorn app.main:app --reload
```

### Docker

```bash
docker build -t alert-notification-service .
docker run -p 8000:8000 alert-notification-service
```

### K8s (Kind)

- **NodePort**: `30008` (see project [README](../../README.md) for port layout)

## 🧪 Tests

```bash
pytest
```

## 🐛 Troubleshooting

- DB connection failed: Check `DATABASE_URL`, DB server, network.
- Notifications not sending: Verify alert/subscription IDs and notify_type/notify_id; check service logs.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)

Last updated: February 2026
