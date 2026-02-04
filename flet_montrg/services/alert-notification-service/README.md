# 📧 Alert Notification Service

Notification delivery and delivery history API

## ✨ Features

- Notification delivery history
- Status: PENDING, SENT, FAILED, RETRYING
- Retry logic
- Query by alert or subscription
- Pending/failed notification lists

## 🔌 API Endpoints

### Notifications

- `POST /api/v1/notifications/` — Create notification
- `GET /api/v1/notifications/` — List
- `GET /api/v1/notifications/{notification_id}` — Get
- `PUT /api/v1/notifications/{notification_id}` — Update
- `DELETE /api/v1/notifications/{notification_id}` — Delete

### Status

- `POST /api/v1/notifications/{notification_id}/mark-sent` — Mark sent
- `POST /api/v1/notifications/{notification_id}/mark-failed` — Mark failed
- `POST /api/v1/notifications/{notification_id}/mark-retrying` — Mark retrying

### Query

- `GET /api/v1/notifications/alert/{alert_id}` — By alert
- `GET /api/v1/notifications/subscription/{subscription_id}` — By subscription
- `GET /api/v1/notifications/pending` — Pending
- `GET /api/v1/notifications/failed` — Failed

## 🔧 Environment Variables

See `.env` or copy from `env.example`.

## ⚙️ Install & Run

```bash
# Local
uvicorn app.main:app --reload

# Docker
docker build -t alert-notification-service .
docker run -p 8000:8000 alert-notification-service
```

## 🧪 Tests

```bash
pytest
```

---

**Last Updated**: February 2026
