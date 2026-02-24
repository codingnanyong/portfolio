# 🏭 IoT Sensor Monitoring Data Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-supported-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Kind-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Svelte](https://img.shields.io/badge/Svelte-4+-FF3E00?logo=svelte&logoColor=white)](https://svelte.dev/)
[![Vite](https://img.shields.io/badge/Vite-5+-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)

**Data Engineering Portfolio** — Real-time IoT sensor data collection, processing, and monitoring platform.

## 📋 Project Overview

An end-to-end data platform that collects and processes IoT sensor data from manufacturing sites in real time for perceived-temperature monitoring and alerting. Kubernetes-based microservices with optional Airflow pipelines (see main repo for pipeline code).

### ⚙️ Core Features

- 🔄 Real-time data ingestion: IoT sensor temperature/humidity
- 🎯 Microservice APIs: FastAPI (9 services + web dashboard)
- ☸️ Kubernetes: Service deployment, HPA, monitoring
- 📈 Aggregation & analytics: Time- and location-based stats
- 🚨 Alerting: Threshold-based notifications (Email, Kakao, SMS, App)

### 🛠️ Tech Stack

- **API**: FastAPI, SQLAlchemy 2.0, Pydantic, PostgreSQL/TimescaleDB
- **Infra**: Docker, Kubernetes (Kind), HPA, Prometheus
- **Frontend**: Svelte 4, Vite 5 (dashboard); integrated Swagger UI

## 📁 Project Structure

```text
portfolio/
└── flet_montrg/                # Microservices
    ├── services/               # API services (README per service)
    │   ├── thresholds-service/
    │   ├── location-service/
    │   ├── realtime-service/
    │   ├── aggregation-service/
    │   ├── alert-service/
    │   ├── alert-subscription-service/
    │   ├── alert-notification-service/
    │   ├── sensor-threshold-mapping-service/
    │   ├── integrated-swagger-service/
    │   └── web-service/         # Dashboard (Svelte + Vite)
    └── k8s/                     # Kubernetes manifests
        ├── thresholds/
        ├── location/
        ├── realtime/
        ├── aggregation/
        ├── integrated-swagger/
        ├── alert/
        ├── alert-subscription/
        ├── alert-notification/
        └── sensor-threshold-mapping/
```

Note: Data pipeline (Airflow ETL) lives in the main [flet-montrg](https://github.com/codingnanyong/flet-montrg) repo if needed.

## 🔄 Architecture

### Microservices (Kubernetes)

| Service                            | Port   | Description                    |
| ---------------------------------- | ------ | ------------------------------ |
| thresholds-service                 | 30001  | Threshold CRUD                 |
| location-service                   | 30002  | Sensor location info           |
| realtime-service                   | 30003  | Real-time data & threshold     |
| aggregation-service                | 30004  | Hourly aggregation             |
| integrated-swagger-service         | 30005  | Unified API docs               |
| alert-service                      | 30007  | Alert creation & management    |
| alert-subscription-service         | 30008  | Alert subscriptions            |
| alert-notification-service         | 30009  | Notification history           |
| sensor-threshold-mapping-service   | 30011  | Sensor–threshold mapping       |

Web dashboard (Svelte/Vite) is served separately; points to integrated-swagger for API.

```text
┌───────────────────────────────────────────────────────────┐
│                Kubernetes Cluster (Kind)                  │
├───────────────────────────────────────────────────────────┤
│  Thresholds(30001)      Location(30002)                   │
│        \                    /                             │
│         +---> Sensor-Threshold-Mapping(30011)             │
│                         |                                 │
│               Realtime(30003) ---> Aggregation(30004)     │
│                                                           │
│  Alert(30007) <--> Alert-Subscription(30008)              │
│                              |                            │
│                              v                            │
│                   Alert-Notification(30009)               │
│                                                           │
│  Integrated-Swagger(30005)                                │
└───────────────────────┬───────────────────────────────────┘
                        v
            PostgreSQL / TimescaleDB
```

See each service directory’s README for API, run instructions, and schema.

## 📖 Documentation

- [Services overview](./flet_montrg/services/README.md)
- [Thresholds Service](./flet_montrg/services/thresholds-service/README.md)
- [Location Service](./flet_montrg/services/location-service/README.md)
- [Realtime Service](./flet_montrg/services/realtime-service/README.md)
- [Aggregation Service](./flet_montrg/services/aggregation-service/README.md)
- [Alert Service](./flet_montrg/services/alert-service/README.md)
- [Alert Subscription](./flet_montrg/services/alert-subscription-service/README.md)
- [Alert Notification](./flet_montrg/services/alert-notification-service/README.md)
- [Sensor-Threshold Mapping](./flet_montrg/services/sensor-threshold-mapping-service/README.md)
- [Integrated Swagger](./flet_montrg/services/integrated-swagger-service/README.md)

---

**Taehyeon Ryu | Data Engineer**  
📎 [GitHub](https://github.com/codingnanyong) · 📧 <codingnanyong@gmail.com>  
*Last updated: February 2026*
