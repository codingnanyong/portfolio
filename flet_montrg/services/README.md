# 📊 flet-montrg Project

Perceived-temperature monitoring and alerting via IoT sensors

## 📁 Project Structure

```text
flet_montrg/
├── services/                              # Microservice source
│   ├── thresholds-service/               # Threshold CRUD API
│   ├── location-service/                 # Sensor location API
│   ├── realtime-service/                 # Real-time status API
│   ├── aggregation-service/              # Period query API
│   ├── alert-service/                    # Alert creation & management
│   ├── alert-subscription-service/       # Alert subscription management
│   ├── alert-notification-service/       # Notification delivery management
│   ├── sensor-threshold-mapping-service/  # Sensor–threshold mapping
│   └── integrated-swagger-service/       # Unified API docs & proxy
├── k8s/                                   # K8s manifests
│   ├── thresholds/
│   ├── location/
│   ├── realtime/
│   ├── aggregation/
│   ├── alert/
│   ├── alert-subscription/
│   ├── alert-notification/
│   ├── sensor-threshold-mapping/
│   └── integrated-swagger/
├── config/                                # Shared config
└── README.md                              # This file
```

## 🔌 Service Ports

### Data services

- **30001**: thresholds-service (Threshold CRUD API)
- **30002**: location-service (Sensor location API)
- **30003**: realtime-service (Real-time status API)
- **30004**: aggregation-service (Period query API)

### Alert services

- **30007**: alert-service (Alert creation & management)
- **30008**: alert-subscription-service (Alert subscription management)
- **30009**: alert-notification-service (Notification delivery management)

### Mapping service

- **30011**: sensor-threshold-mapping-service (Sensor–threshold mapping)

### Unified service

- **30005**: integrated-swagger-service (Unified API docs & proxy)

## 🎯 Main Features

### Data management

- **Thresholds**: Per-sensor threshold configuration and query
- **Locations**: Sensor location hierarchy (factory > building > floor > area)
- **Real-time**: Current sensor data
- **Aggregation**: Time-based aggregation and analysis

### Alert system

- **Alerts**: Auto-create alerts on threshold breach
- **Subscriptions**: Per-location/sensor/threshold-type subscription
- **Notifications**: Per-subscriber notification creation and delivery
- **Hierarchy**: Subscription matching by factory > building > floor > area

### Mapping

- **Sensor–threshold mapping**: Per-sensor threshold assignment
- **Validity**: effective_from / effective_to
- **Enable/disable**: Per-mapping activation

### Unified API

- **Docs**: All services in one Swagger UI
- **Proxy**: Single endpoint to reach all services
- **Discovery**: Kubernetes-based service discovery

## 🛠️ Tech Stack

- 🐍 **Backend**: Python / FastAPI
- 🐳 **Container**: Docker
- ☸️ **Orchestration**: Kubernetes (Kind)
- 📊 **Monitoring**: Kubernetes Dashboard, Prometheus
- 🗄️ **Database**: PostgreSQL

## 🧭 Development

- **K8s cluster**: Kind (flet-cluster)
- **Dashboard**: https://&lt;K8S_INGRESS&gt;:8083/
- **Namespace**: flet-montrg

## 🚀 Deployment

### Per-service deployment

Use each service’s `deploy.sh` under `k8s/<service>`:

```bash
# Data services
cd k8s/thresholds && ./deploy.sh
cd k8s/location && ./deploy.sh
cd k8s/realtime && ./deploy.sh
cd k8s/aggregation && ./deploy.sh

# Alert services
cd k8s/alert && ./deploy.sh
cd k8s/alert-subscription && ./deploy.sh
cd k8s/alert-notification && ./deploy.sh

# Mapping
cd k8s/sensor-threshold-mapping && ./deploy.sh

# Unified docs
cd k8s/integrated-swagger && ./deploy.sh
```

### Unified API docs

All service APIs are available via integrated Swagger:

- **Swagger UI**: http://&lt;K8S_INGRESS&gt;:30005/
- **Proxy API**: http://&lt;K8S_INGRESS&gt;:30005/api/{resource}/

Examples:

- `/api/thresholds/` → thresholds-service
- `/api/location/` → location-service
- `/api/alerts/` → alert-service
- `/api/subscriptions/` → alert-subscription-service
- `/api/notifications/` → alert-notification-service
- `/api/mappings/` → sensor-threshold-mapping-service
