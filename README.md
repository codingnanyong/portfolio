# 🏭 IoT 센서 모니터링 데이터 플랫폼

Data Engineering Portfolio - 실시간 IoT 센서 데이터 수집, 처리 및 모니터링 플랫폼

## 📋 프로젝트 개요

제조 현장의 IoT 센서 데이터를 실시간으로 수집·처리하여 체감 온도 모니터링 및 알림 서비스를 제공하는 엔드-투-엔드 데이터 플랫폼입니다. Apache Airflow 기반 데이터 파이프라인과 Kubernetes 기반 마이크로서비스로 확장 가능한 인프라를 구성했습니다.

### ⚙️ 핵심 기능

- 🔄 **실시간 데이터 수집**: IoT 센서 온도/습도 수집
- 📊 **데이터 파이프라인**: Airflow ETL 자동화 (1시간 간격)
- 🎯 **마이크로서비스 API**: FastAPI RESTful API (9개 서비스)
- ☸️ **Kubernetes**: 서비스 배포·HPA·모니터링
- 📈 **집계·분석**: 시간/위치별 통계
- 🚨 **알림 시스템**: 임계치 기반 다채널 알림 (Email, Kakao, SMS, App)

### 🛠️ 기술 스택

| 영역 | 기술 |
| ------ | ------ |
| **Pipeline** | Apache Airflow 2.10.3, Celery, Docker Compose, PostgreSQL |
| **API** | FastAPI, SQLAlchemy 2.0, Pydantic, PostgreSQL/TimescaleDB |
| **Infra** | Docker, Kubernetes (Kind), HPA, Prometheus |

## 📁 프로젝트 구조

```text
portfolio/
├── data_pipeline/              # Airflow 파이프라인
│   ├── dags/flet_montrg/       # ETL DAG
│   ├── plugins/hooks/          # DB 훅
│   ├── db/                     # 스키마
│   └── docker-compose.yml
│
└── flet_montrg/                # 마이크로서비스
    ├── services/               # API 서비스 (각 서비스별 README 있음)
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

## 🔄 아키텍처

### 데이터 파이프라인

``` bash
IoT Sensors → PostgreSQL (Raw) → Airflow DAGs → PostgreSQL (Processed/TimescaleDB)
```

- **ETL**: Raw 추출 → 시간별 집계(MAX/AVG, 위치별) → 적재 → 검증
- **스케줄**: 1시간, 재시도 2회, 타임아웃 30분
- **상세**: [data_pipeline/README.md](./data_pipeline/README.md)

### 마이크로서비스 (Kubernetes)

| 서비스 | 포트 | 설명 |
| ------ | ------ | ------ |
| thresholds-service | 30001 | 임계치 CRUD |
| location-service | 30002 | 센서 위치 정보 |
| realtime-service | 30003 | 실시간 데이터·임계치 검사 |
| aggregation-service | 30004 | 시간별 집계 |
| integrated-swagger-service | 30005 | 통합 API 문서 |
| alert-service | 30007 | 알람 생성·관리 |
| alert-subscription-service | 30008 | 알림 구독 |
| alert-notification-service | 30009 | 알림 발송 이력 |
| sensor-threshold-mapping-service | 30011 | 센서-임계치 매핑 |

```text
+-----------------------------------------------------------+
|                Kubernetes Cluster (Kind)                 |
+-----------------------------------------------------------+
|                                                           |
|  Thresholds(30001)      Location(30002)                  |
|        \                    /                            |
|         +---> Sensor-Threshold-Mapping(30011)            |
|                         |                                |
|               Realtime(30003) ---> Aggregation(30004)    |
|                                                           |
|  Alert(30007) <--> Alert-Subscription(30008)             |
|                              |                           |
|                              v                           |
|                   Alert-Notification(30009)              |
|                                                           |
|  Integrated-Swagger(30005)                               |
|                                                           |
+-----------------------------------------------------------+
                         |
                         v
                PostgreSQL / TimescaleDB
```

각 서비스 API·실행 방법·스키마는 해당 디렉터리 README를 참고하세요.

## 📖 상세 문서

| 문서 | 경로 |
| ------ | ------ |
| 데이터 파이프라인 | [data_pipeline/README.md](./data_pipeline/README.md) |
| DB 스키마 | [data_pipeline/db/flet_montrg/README.md](./data_pipeline/db/flet_montrg/README.md) |
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

**류태현 | Data Engineer**
📎 [GitHub](https://github.com/codingnanyong/portfolio) · 📧 <codingnanyong@gmail.com>
*Last Updated: February 2026*
