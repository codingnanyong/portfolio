# Alert & Notification API Examples

Quick reference for Alert (port 30007) and Notification (port 30009) APIs.

---

## Alert API — POST /api/v1/alerts/

**Threshold levels (pcv_temperature):**

| Level  | threshold_id | Range         |
|--------|--------------|---------------|
| green  | 1            | 0.00–30.90°C  |
| yellow | 2            | 31.00–32.90°C |
| orange | 3            | ≥33.00°C      |

Sensors: `TEMPIOT-A011` ~ `TEMPIOT-A038` (loc_id `A011`–`A038`). Each sensor has Yellow and Orange threshold mappings (see sensor-threshold-mapping-service). Optional: `threshold_map_id`.

### cURL — create alert

```bash
curl -X POST "http://localhost:30007/api/v1/alerts/" \
  -H "Content-Type: application/json" \
  -d '{
    "loc_id": "A011",
    "sensor_id": "TEMPIOT-A011",
    "alert_type": "pcv_temperature",
    "alert_level": "yellow",
    "threshold_id": 2,
    "threshold_type": "pcv_temperature",
    "threshold_level": "yellow",
    "measured_value": 32.0,
    "threshold_min": 31.00,
    "threshold_max": 32.90,
    "message": "Temperature in warning range"
  }'
```

### Python — create alert

```python
import requests

r = requests.post("http://localhost:30007/api/v1/alerts/", json={
    "loc_id": "A011",
    "sensor_id": "TEMPIOT-A011",
    "alert_type": "pcv_temperature",
    "alert_level": "orange",
    "threshold_id": 3,
    "threshold_type": "pcv_temperature",
    "threshold_level": "orange",
    "measured_value": 35.0,
    "threshold_min": 33.00,
    "threshold_max": None,
    "message": "Temperature exceeded danger range"
})
print(r.json())
```

---

## Notification API — POST /api/v1/notifications/

**Body:** `alert_id`, `subscription_id`, `notify_type` (`email` | `kakao` | `sms` | `app`), `notify_id` (e.g. email address, phone, account name).

**Response:** `notification_id`, `status` (default `PENDING`), `try_count`, `created_time`, etc.

### cURL — create notification

```bash
curl -X POST "http://localhost:30009/api/v1/notifications/" \
  -H "Content-Type: application/json" \
  -d '{"alert_id": 1, "subscription_id": 1, "notify_type": "email", "notify_id": "user@example.com"}'
```

### Python — alert then notification

```python
import requests

# Create alert
alert = requests.post("http://localhost:30007/api/v1/alerts/", json={
    "loc_id": "A011", "sensor_id": "TEMPIOT-A011", "alert_type": "pcv_temperature",
    "alert_level": "orange", "threshold_id": 3, "threshold_type": "pcv_temperature",
    "threshold_level": "orange", "measured_value": 35.5, "threshold_min": 33.00,
    "threshold_max": None, "message": "Temperature danger"
}).json()

# Create notification for that alert
notif = requests.post("http://localhost:30009/api/v1/notifications/", json={
    "alert_id": alert["alert_id"], "subscription_id": 1,
    "notify_type": "email", "notify_id": "admin@company.com"
}).json()
print("Notification id:", notif["notification_id"])
```

---

**Swagger:** [http://localhost:30005]/ — use alert-service and alert-notification-service sections.
