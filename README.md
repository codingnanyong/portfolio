# 🏭 IoT Sensor Monitoring Data Platform

Data Engineering Portfolio — Real-time IoT sensor data collection, processing, and monitoring platform

## 📋 Project Overview

An end-to-end data platform that collects and processes IoT sensor data from manufacturing sites in real time to provide perceived-temperature monitoring and alerting. It uses Apache Airflow–based data pipelines and Kubernetes-based microservices for scalable infrastructure.

### ⚙️ Core Features

- 🔄 **Real-time data ingestion**: IoT sensor temperature/humidity collection
- 📊 **Data pipeline**: Airflow ETL automation (hourly)
- 🎯 **Microservice APIs**: FastAPI RESTful APIs (9 services)
- ☸️ **Kubernetes**: Service deployment, HPA, and monitoring
- 📈 **Aggregation & analytics**: Time- and location-based statistics
- 🚨 **Alerting**: Threshold-based multi-channel notifications (Email, Kakao, SMS, App)

### 🛠️ Tech Stack

| Area | Technologies |
| ------ | ------ |
| **Pipeline** | Apache Airflow 2.10.3, Celery, Docker Compose, PostgreSQL |
| **API** | FastAPI, SQLAlchemy 2.0, Pydantic, PostgreSQL/TimescaleDB |
| **Infra** | Docker, Kubernetes (Kind), HPA, Prometheus |

## 📁 Project Structure

```text
portfolio/
├── data_pipeline/              # Airflow pipeline
│   ├── dags/flet_montrg/       # ETL DAG
│   ├── plugins/hooks/          # DB hooks
│   ├── db/                     # Schema
│   └── docker-compose.yml
│
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
    │   └── integrated-swagger-service/
    └── k8s/                    # Kubernetes manifests
```

## 🔄 Architecture

### Data Pipeline

``` bash
IoT Sensors → PostgreSQL (Raw) → Airflow DAGs → PostgreSQL (Processed/TimescaleDB)
```

- **ETL**: Raw extract → hourly aggregation (MAX/AVG, by location) → load → validation
- **Schedule**: Hourly, 2 retries, 30 min timeout
- **Details**: [data_pipeline/README.md](./data_pipeline/README.md)

### Microservices (Kubernetes)

| Service | Port | Description |
| ------ | ------ | ------ |
| thresholds-service | 30001 | Threshold CRUD |
| location-service | 30002 | Sensor location info |
| realtime-service | 30003 | Real-time data & threshold checks |
| aggregation-service | 30004 | Hourly aggregation |
| integrated-swagger-service | 30005 | Unified API docs |
| alert-service | 30007 | Alert creation & management |
| alert-subscription-service | 30008 | Alert subscriptions |
| alert-notification-service | 30009 | Notification history |
| sensor-threshold-mapping-service | 30011 | Sensor–threshold mapping |

```text
+-----------------------------------------------------------+
|                Kubernetes Cluster (Kind)                  |
+-----------------------------------------------------------+
|                                                           |
|  Thresholds(30001)      Location(30002)                   |
|        \                    /                             |
|         +---> Sensor-Threshold-Mapping(30011)             |
|                         |                                 |
|               Realtime(30003) ---> Aggregation(30004)     |
|                                                           |
|  Alert(30007) <--> Alert-Subscription(30008)              |
|                              |                            |
|                              v                            |
|                   Alert-Notification(30009)               |
|                                                           |
|  Integrated-Swagger(30005)                                |
|                                                           |
+-----------------------------------------------------------+
                         |
                         v
                PostgreSQL / TimescaleDB
```

See each service directory’s README for API, run instructions, and schema.

## 📖 Documentation

| Document | Path |
| ------ | ------ |
| Data Pipeline | [data_pipeline/README.md](./data_pipeline/README.md) |
| DB Schema | [data_pipeline/db/flet_montrg/README.md](./data_pipeline/db/flet_montrg/README.md) |
| Thresholds Service | [flet_montrg/services/thresholds-service/README.md](./flet_montrg/services/thresholds-service/README.md) |
| Location Service | [flet_montrg/services/location-service/](./flet_montrg/services/location-service/) |
| Realtime Service | [flet_montrg/services/realtime-service/README.md](./flet_montrg/services/realtime-service/README.md) |
| Aggregation Service | [flet_montrg/services/aggregation-service/README.md](./flet_montrg/services/aggregation-service/README.md) |
| Alert Service | [flet_montrg/services/alert-service/README.md](./flet_montrg/services/alert-service/README.md) |
| Alert Subscription | [flet_montrg/services/alert-subscription-service/README.md](./flet_montrg/services/alert-subscription-service/README.md) |
| Alert Notification | [flet_montrg/services/alert-notification-service/README.md](./flet_montrg/services/alert-notification-service/README.md) |
| Sensor-Threshold Mapping | [flet_montrg/services/sensor-threshold-mapping-service/README.md](./flet_montrg/services/sensor-threshold-mapping-service/README.md) |
| Integrated Swagger | [flet_montrg/services/integrated-swagger-service/README.md](./flet_montrg/services/integrated-swagger-service/README.md) |

---

**Taehyeon Ryu | Data Engineer**  
📎 [GitHub](https://github.com/codingnanyong/portfolio) · 📧 <codingnanyong@gmail.com>  
*Last Updated: February 2026*
