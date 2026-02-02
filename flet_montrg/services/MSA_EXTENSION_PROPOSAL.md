# flet_montrg MSA Extension Proposal

## 📋 Current State

### Existing Services & Ports

- ✅ **thresholds-service** (30001): Threshold CRUD
- ✅ **location-service** (30002): Location & sensor info
- ✅ **realtime-service** (30003): Real-time data (depends on thresholds, location)
- ✅ **aggregation-service** (30004): Period aggregation
- ✅ **integrated-swagger-service** (30005): Unified API docs

### Alert Domain Ports (current deployment)

- **30007**: alert-service
- **30008**: alert-subscription-service
- **30009**: alert-notification-service
- **30011**: sensor-threshold-mapping-service
- **30010**: alert-evaluation-service (internal; no external exposure)
- **30006, 30012+**: Reserved / future use

### New Requirements (ERD)

- 📊 **alerts**: Alert history
- 📧 **alert_subscriptions**: Subscriptions (factory/building/floor/area)
- 📨 **alert_notifications**: Notification delivery history
- 🔗 **sensor_threshold_map**: Sensor–threshold mapping

---

## 🏗️ MSA Extension Architecture

``` text
┌─────────────────────────────────────────────────────────────┐
│                    Alert Domain Services                    │
└─────────────────────────────────────────────────────────────┘

1. alert-service (Alert creation & management)
   ├── Responsibility: Create, query, resolve alerts
   ├── Data: alerts table
   ├── Depends on: thresholds-service, location-service, sensor-threshold-mapping-service
   └── Port: 30007

2. alert-subscription-service (Subscription management)
   ├── Responsibility: Subscription CRUD, filtering by subscriber
   ├── Data: alert_subscriptions table
   ├── Depends on: location-service (location hierarchy)
   └── Port: 30008

3. alert-notification-service (Notification delivery)
   ├── Responsibility: Send notifications, store delivery history
   ├── Data: alert_notifications table
   ├── Depends on: alert-service, alert-subscription-service
   └── Port: 30009

4. sensor-threshold-mapping-service (Sensor–threshold mapping)
   ├── Responsibility: Per-sensor threshold mapping
   ├── Data: sensor_threshold_map table
   ├── Depends on: thresholds-service, location-service
   └── Port: 30011

5. alert-evaluation-service (Threshold evaluation worker) 
   ├── Responsibility: Background threshold breach detection
   ├── Data: read-only temperature_raw
   ├── Run: Scheduler (e.g. every 1 min) or event-driven (post-ETL)
   ├── Depends on: sensor-threshold-mapping, thresholds, location, alert-service
   └── Port: 30010 (internal only)
```

---

## 🎯 Rationale: Split + alert-evaluation-service

1. **Single responsibility**: Clear ownership per service
2. **Independent scaling**: Scale notification-service for high notification load
3. **Fault isolation**: Subscription issues do not block notification delivery
4. **Team boundaries**: Services can be owned by different teams
5. **Real-time detection**: Background threshold evaluation independent of API calls ⭐

---

## 📐 Service Design (Summary)

### 1. alert-service

**Endpoints:**  
`POST/GET /api/v1/alerts`, `GET /api/v1/alerts/{id}`, `GET /api/v1/alerts/by-sensor/{sensor_id}`, `GET /api/v1/alerts/by-location/{loc_id}`, `PUT /api/v1/alerts/{id}/resolve`

**Calls:** sensor-threshold-mapping (mappings by sensor), thresholds (threshold detail), location (sensor location).

**Alert creation:** Prefer alert-evaluation-service creating alerts in background; avoid doing threshold checks only on realtime-service API calls.

---

### 2. alert-subscription-service

**Endpoints:**  
`POST/GET/PUT/DELETE /api/v1/subscriptions`, `GET /api/v1/subscriptions/match?factory=...&building=...&floor=...&area=...`

**Location matching:** Hierarchy factory → building → floor → area; null means “any”.  
**Match logic:** Subscription matches alert when (factory/building/floor/area/sensor_id/threshold_type/min_level) conditions match (e.g. `(factory IS NULL OR factory = :factory)` and similar).

---

### 3. alert-notification-service

**Endpoints:**  
`POST /api/v1/notifications/send`, `GET /api/v1/notifications`, `GET /api/v1/notifications/{id}`, `GET /api/v1/notifications/by-alert/{alert_id}`, `PUT .../retry`

**Calls:** alert-service (alert detail), alert-subscription-service (subscriptions/match for location).

**Flow:** Alert created → alert-service calls notification-service `POST /notifications/send` with `alert_id`, `subscription_ids` → send email/SMS → store in `alert_notifications`.

---

### 4. sensor-threshold-mapping-service

**Endpoints:**  
`POST/GET/PUT/DELETE /api/v1/mappings`, `GET /api/v1/mappings/sensor/{sensor_id}`, `GET /api/v1/mappings/threshold/{threshold_id}`, `GET /api/v1/mappings/active/sensor/{sensor_id}`

**Active mapping:** `enabled = true`, `effective_from`/`effective_to` within range.  
**Schema:** Use `duration_seconds` (default 60) instead of `duration_hours` — minimum time threshold must be exceeded before creating an alert (noise filtering).

---

### 5. alert-evaluation-service (worker)

**Role:** Periodically read `temperature_raw`, evaluate per-sensor thresholds, call alert-service to create alerts when exceeded (and duration_seconds satisfied).

**Run:** Scheduler (e.g. APScheduler, 1 min, max_instances=1) or event (post-ETL webhook / queue). Optional: `GET /health`, `GET /status`, `POST /evaluate/trigger`, `GET /metrics`.

**Calls:** sensor-threshold-mapping (active mappings), thresholds (detail), location (sensor location), alert-service (POST create alert).

**Core logic:** Load new rows since last run → group by sensor → for each sensor get active mappings → get threshold → compare value → if exceeded for `duration_seconds`, call alert-service (with duplicate-window check, e.g. 5 min).

**duration_seconds check:** Query `temperature_raw` for last `duration_seconds`; only create alert if every point in that window exceeds the threshold.

---

## 🔄 End-to-End Flow

```text
Airflow ETL → temperature_raw
       ↓
alert-evaluation-service (scheduler/worker)
  → read temperature_raw, get mappings, thresholds, location
  → on breach + duration → POST alert-service /alerts
       ↓
alert-service
  → create alert, GET subscriptions/match, POST notification-service /notifications/send
       ↓
alert-notification-service
  → send email/SMS, write alert_notifications
```

**alert-evaluation run options:** APScheduler interval, Airflow webhook, message queue, or Kubernetes CronJob (e.g. `*/1 * * * *`).

---

## 📦 Data Ownership

| Service                          | Own tables               | Access                          |
|----------------------------------|--------------------------|---------------------------------|
| alert-service                    | alerts                   | read/write                      |
| alert-subscription-service       | alert_subscriptions      | read/write                      |
| alert-notification-service       | alert_notifications      | read/write                      |
| sensor-threshold-mapping-service | sensor_threshold_map     | read/write                      |
| alert-evaluation-service         | (none)                   | read-only temperature_raw       |
| thresholds-service               | thresholds               | read/write                      |
| location-service                 | locations, sensors       | read/write                      |
| realtime / aggregation           | (none)                   | read-only temperature_raw       |

**Principles:** Each service writes only its own tables; cross-service data via HTTP APIs; eventual consistency acceptable.

---

## 🚀 Implementation Phases

**Phase 1:** sensor-threshold-mapping-service (CRUD, active-mapping API, migration); alert-service (create/query, integrate mapping).  
**Phase 2:** alert-subscription-service (CRUD, location match); alert-notification-service (send engine, history, retry).  
**Phase 3:** alert-evaluation-service (scheduler, scan temperature_raw, threshold logic, call alert-service).  
**Phase 4:** Simplify realtime-service (remove threshold evaluation); monitoring, tuning, error handling.

---

## 🔧 Tech Stack

Backend: Python/FastAPI. DB: PostgreSQL (per-service schema). Container: Docker. Orchestration: Kubernetes (Kind). Communication: HTTP/REST (httpx). Docs: OpenAPI/Swagger.

---

## 📊 K8s Layout

`k8s/alert/`, `k8s/alert-subscription/`, `k8s/alert-notification/`, `k8s/sensor-threshold-mapping/`, `k8s/alert-evaluation/` — each with deployment, service, configmap, secret, hpa, network-policy as needed.

---

## 🎯 Benefits

Scalability (e.g. scale notification-service), independent deploy/maintain, fault isolation, team boundaries, testability.

---

## ⚠️ Considerations

- **Distributed transactions:** Use events or Saga for alert + notification consistency.
- **Dependencies:** Keep acyclic (e.g. evaluation → alert → notification).
- **Consistency:** Eventual consistency; avoid cross-service DB writes.
- **Performance:** Async, caching, batching for HTTP calls.

---

## 📝 Next Steps

Detail API specs, finalize schema and migrations, define error/retry and monitoring/logging.

---

## 🔧 Schema: sensor_threshold_map

**Change:** Replace `duration_hours` with `duration_seconds int4 DEFAULT 60 NOT NULL`.  
**Meaning:** Minimum time (seconds) threshold must be exceeded before creating an alert.  
**Example:** `duration_seconds = 300` → 5 minutes.

```sql
-- Add column (after dropping duration_hours if present)
ALTER TABLE flet_montrg.sensor_threshold_map 
ADD COLUMN duration_seconds int4 DEFAULT 60 NOT NULL;
```

**API example:**  
`POST /api/v1/mappings` body: `sensor_id`, `threshold_id`, `duration_seconds` (e.g. 300), `enabled`, `effective_from`, `effective_to`.
