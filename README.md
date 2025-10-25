# 🏭 IoT 센서 모니터링 데이터 플랫폼

Data Engineering Portfolio - 실시간 IoT 센서 데이터 수집, 처리 및 모니터링 플랫폼

## 📋 프로젝트 개요

제조 현장의 IoT 센서 데이터를 실시간으로 수집하고 처리하여, 체감 온도 모니터링 및 알림 서비스를 제공하는 엔드-투-엔드 데이터 플랫폼입니다. Apache Airflow를 활용한 데이터 파이프라인 구축과 Kubernetes 기반 마이크로서비스 아키텍처를 통해 확장 가능하고 안정적인 데이터 인프라를 구현했습니다.

### 핵심 기능

-   🔄 **실시간 데이터 수집**: IoT 센서로부터 온도/습도 데이터 실시간 수집
-   📊 **데이터 파이프라인**: Airflow 기반 ETL 프로세스 자동화
-   🎯 **마이크로서비스 API**: FastAPI 기반 RESTful API 서비스
-   ☸️ **컨테이너 오케스트레이션**: Kubernetes를 활용한 서비스 배포 및 관리
-   📈 **데이터 집계 및 분석**: 시간/위치별 데이터 집계 및 통계
-   🚨 **실시간 알림**: 임계치 기반 알림 시스템

## 🛠️ 기술 스택

### Data Pipeline

-   **워크플로우 관리**: Apache Airflow 2.10.3
-   **컨테이너화**: Docker, Docker Compose
-   **스케줄링**: Celery Executor
-   **데이터베이스**: PostgreSQL (Source & Target)
-   **언어**: Python 3.x

### API Services

-   **프레임워크**: FastAPI
-   **데이터베이스**: PostgreSQL, TimescaleDB
-   **컨테이너 오케스트레이션**: Kubernetes (Kind)
-   **HTTP 클라이언트**: httpx
-   **데이터 검증**: Pydantic
-   **ORM**: SQLAlchemy 2.0

### 인프라

-   **컨테이너**: Docker
-   **오케스트레이션**: Kubernetes
-   **로드 밸런싱**: Kubernetes Service
-   **Auto Scaling**: HPA (Horizontal Pod Autoscaler)
-   **모니터링**: Prometheus, Kubernetes Dashboard

## 📁 프로젝트 구조

```
portfolio/
├── data_pipeline/              # 데이터 수집 및 처리 파이프라인
│   ├── dags/                   # Airflow DAG 정의
│   │   └── flet_montrg/        # 온도 센서 모니터링 DAG
│   ├── plugins/                # 커스텀 훅 및 플러그인
│   │   └── hooks/              # 데이터베이스 연결 훅
│   ├── db/                     # 데이터베이스 스키마
│   ├── scripts/                # 설정 및 설치 스크립트
│   ├── docker-compose.yml      # Airflow 서비스 구성
│   └── requirements.txt        # Python 의존성
│
└── flet_montrg/               # 마이크로서비스 API
    ├── services/              # 서비스 소스 코드
    │   ├── thresholds-service/    # 임계치 관리 API
    │   ├── location-service/      # 센서 위치 정보 API
    │   ├── realtime-service/      # 실시간 현황 API
    │   └── aggregation-service/   # 데이터 집계 API
    └── k8s/                   # Kubernetes 배포 설정
        ├── thresholds/
        ├── location/
        ├── realtime/
        └── aggregation/
```

## 🔄 데이터 파이프라인 아키텍처

### 1. 데이터 수집 레이어 (Data Ingestion)

```
IoT Sensors → PostgreSQL (Raw) → Airflow DAGs → PostgreSQL (Processed)
```

#### Airflow DAG 구성

**온도 데이터 파이프라인 (`flet_montrg_temperature_etl.py`)**

-   Raw 데이터 추출 (Extract)
-   시간별 데이터 집계 (Transform)
    -   최대값 (MAX)
    -   평균값 (AVG)
    -   위치별 그룹핑
-   처리된 데이터 적재 (Load)

**주요 특징**

-   ⏰ 스케줄: 1시간 간격 실행
-   🔄 재시도 로직: 2회 재시도, 2분 대기
-   ⏱️ 실행 타임아웃: 30분
-   📊 SLA: 60분 이내 완료

#### 백필 (Backfill) 지원

-   `flet_montrg_temperature_backfill.py`: 과거 데이터 재처리
-   `flet_montrg_temperature_raw_backfill.py`: Raw 데이터 백필

### 2. 데이터 처리 프로세스

```python
# ETL 프로세스 단계
1. Connection Check    → 데이터베이스 연결 확인
2. Data Extraction     → Raw 데이터 추출
3. Data Transformation → 집계 및 변환
4. Data Loading        → 타겟 DB 적재
5. Validation         → 데이터 검증
```

### 3. 커스텀 Hooks

**지원 데이터베이스**

-   PostgreSQL Hook (`postgres_hook.py`)
-   MySQL Hook (`mysql_hook.py`)
-   MS SQL Hook (`mssql_hook.py`)
-   Oracle Hook (`oracle_hook.py`)

## 🎯 마이크로서비스 아키텍처

### 서비스 목록

| 서비스                    | 포트  | 설명                        | 상태         |
| ------------------------- | ----- | --------------------------- | ------------ |
| **thresholds-service**    | 30001 | 센서 임계치 관리 CRUD API   | ✅ 구현 완료 |
| **location-service**      | 30002 | 센서 위치 정보 관리 API     | ✅ 구현 완료 |
| **realtime-service**      | 30003 | 실시간 센서 데이터 조회 API | ✅ 구현 완료 |
| **aggregation-service**   | 30004 | 시간별 데이터 집계 API      | ✅ 구현 완료 |
| **alert-service**         | 30005 | 임계치 기반 알림 발송       | 🚧 구현 예정 |
| **alert-history-service** | 30006 | 알림 이력 조회 API          | 🚧 구현 예정 |

### 서비스 구성

```
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster (Kind)              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐    ┌──────────────────┐       │
│  │  Thresholds      │    │   Location       │       │
│  │  Service         │◄───┤   Service        │       │
│  │  (Port: 30001)   │    │   (Port: 30002)  │       │
│  └────────┬─────────┘    └────────┬─────────┘       │
│           │                       │                 │
│           └───────────┬───────────┘                 │
│                       ▼                             │
│           ┌──────────────────────┐                  │
│           │   Realtime Service   │                  │
│           │   (Port: 30003)      │                  │
│           └──────────────────────┘                  │
│                                                     │
│           ┌──────────────────────┐                  │
│           │ Aggregation Service  │                  │
│           │   (Port: 30004)      │                  │
│           └──────────────────────┘                  │
│                                                     │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
                ┌───────────────┐
                │  PostgreSQL   │
                │  TimescaleDB  │
                └───────────────┘
```

### 1. Thresholds Service (Port: 30001)

**기능**: 센서 임계치 관리 CRUD API

```python
# 주요 엔드포인트
GET    /api/v1/thresholds/          # 모든 임계치 조회
GET    /api/v1/thresholds/{id}      # 특정 임계치 조회
POST   /api/v1/thresholds/          # 임계치 생성
PUT    /api/v1/thresholds/{id}      # 임계치 수정
DELETE /api/v1/thresholds/{id}      # 임계치 삭제
```

**기술 스택**

-   FastAPI
-   SQLAlchemy ORM
-   Pydantic 데이터 검증
-   구조화된 로깅

### 2. Location Service (Port: 30002)

**기능**: 센서 위치 정보 관리 API

```python
# 위치 정보 구조
{
  "factory": "SinPyeong",
  "building": "F-2001",
  "floor": 1,
  "loc_id": "A031",
  "area": "조립2"
}
```

**주요 기능**

-   공장/건물/층/구역별 위치 정보
-   센서 위치 매핑
-   다이나믹 필터링

### 3. Realtime Service (Port: 30003)

**기능**: 실시간 센서 데이터 조회 및 임계치 검사

```python
# 주요 엔드포인트
GET /api/v1/realtime/                    # 전체 데이터
GET /api/v1/realtime/factory/{factory}   # 공장별 조회
GET /api/v1/realtime/building/{building} # 건물별 조회
GET /api/v1/realtime/floor/{floor}       # 층별 조회
GET /api/v1/realtime/loc_id/{loc_id}     # 위치별 조회
```

**응답 구조**

```json
{
    "capture_dt": "2025-09-12T05:59:38.837000Z",
    "ymd": "20250912",
    "hh": "14",
    "measurements": [
        {
            "location": {
                "factory": "SinPyeong",
                "building": "MX-1",
                "floor": 1,
                "loc_id": "A011"
            },
            "metrics": {
                "temperature": { "value": "22.1", "status": "normal" },
                "humidity": { "value": "77.7", "status": null },
                "pcv_temperature": { "value": "23.8", "status": "normal" }
            }
        }
    ]
}
```

**임계치 상태 시스템**

-   `normal`: 정상 범위
-   `warning`: 경고 상태
-   `critical`: 위험 상태
-   `null`: 임계치 미설정

**외부 서비스 연동**

-   Location Service: 센서 위치 정보
-   Thresholds Service: 임계치 정보

### 4. Aggregation Service (Port: 30004)

**기능**: 시간별 데이터 집계 및 통계

```python
# 주요 엔드포인트
GET /api/v1/aggregation/pcv_temperature/
GET /api/v1/aggregation/pcv_temperature/location/{location_id}
GET /api/v1/aggregation/pcv_temperature/factory/{factory}

# 파라미터
start_date: yyyy, yyyyMM, yyyyMMdd
end_date: yyyy, yyyyMM, yyyyMMdd
```

**집계 메트릭**

-   `pcv_temperature_max`: 최대 체감 온도
-   `pcv_temperature_avg`: 평균 체감 온도

**응답 예시**

```json
{
    "location": {
        "factory": "SinPyeong",
        "building": "F-2001",
        "floor": 1,
        "loc_id": "A031",
        "area": "조립2",
        "date": [
            {
                "ymd": "20240922",
                "hour": "12",
                "metrics": {
                    "pcv_temperature_max": "27.00",
                    "pcv_temperature_avg": "27.00"
                }
            }
        ]
    }
}
```

## 🚀 실행 방법

### 1. 데이터 파이프라인 실행

#### Airflow 설정

```bash
# 프로젝트 디렉토리로 이동
cd data_pipeline

# 필수 디렉토리 생성
mkdir -p ./dags ./logs ./plugins

# Airflow 초기화
docker compose up airflow-init

# Airflow 서비스 시작
docker compose up -d

# Worker 스케일 업 (선택사항)
docker-compose up -d --scale airflow-worker=3 airflow-worker
```

#### 접속 정보

-   **Airflow UI**: http://localhost:8080
-   **Flower UI** (선택): http://localhost:5555

#### 환경 변수 설정

`.env` 파일 생성:

```bash
# 데이터베이스 연결
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow

# Celery 설정
AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow

# 보안 키
AIRFLOW__CORE__FERNET_KEY=<generated-key>
AIRFLOW__WEBSERVER__SECRET_KEY=<generated-key>

# Executor
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
```

### 2. 마이크로서비스 배포

#### Kubernetes 클러스터 설정

```bash
# Kind 클러스터 생성
kind create cluster --name flet-cluster

# 네임스페이스 생성
kubectl create namespace flet-montrg

# Docker 이미지 빌드
cd flet_montrg/services/thresholds-service
docker build -t flet-montrg/thresholds-service:latest .

cd ../location-service
docker build -t flet-montrg/location-service:latest .

cd ../realtime-service
docker build -t flet-montrg/realtime-service:latest .

cd ../aggregation-service
docker build -t flet-montrg/aggregation-service:latest .

# Kind로 이미지 로드
kind load docker-image flet-montrg/thresholds-service:latest --name flet-cluster
kind load docker-image flet-montrg/location-service:latest --name flet-cluster
kind load docker-image flet-montrg/realtime-service:latest --name flet-cluster
kind load docker-image flet-montrg/aggregation-service:latest --name flet-cluster
```

#### 서비스 배포

```bash
cd flet_montrg/k8s

# 각 서비스 배포
kubectl apply -f thresholds/
kubectl apply -f location/
kubectl apply -f realtime/
kubectl apply -f aggregation/

# 배포 상태 확인
kubectl get pods -n flet-montrg
kubectl get services -n flet-montrg

# 또는 배포 스크립트 사용
cd thresholds && bash deploy.sh
cd ../location && bash deploy.sh
cd ../realtime && bash deploy.sh
cd ../aggregation && bash deploy.sh
```

#### 서비스 접속

```bash
# 포트 포워딩 (로컬 테스트용)
kubectl port-forward -n flet-montrg service/thresholds-service 30001:80
kubectl port-forward -n flet-montrg service/location-service 30002:80
kubectl port-forward -n flet-montrg service/realtime-service 30003:80
kubectl port-forward -n flet-montrg service/aggregation-service 30004:80
```

**API 문서 접속**

-   Thresholds Service: http://localhost:30001/docs
-   Location Service: http://localhost:30002/docs
-   Realtime Service: http://localhost:30003/docs
-   Aggregation Service: http://localhost:30004/docs

### 3. 개발 환경 실행

#### 각 서비스 로컬 실행

```bash
cd flet_montrg/services/thresholds-service

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp env.example .env
# .env 파일 편집

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 데이터베이스 스키마

### 주요 테이블

#### 1. flet_montrg.temperature_raw

```sql
-- Raw 센서 데이터 (수집 원본)
CREATE TABLE flet_montrg.temperature_raw (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50),
    capture_dt TIMESTAMP,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    pcv_temperature DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 2. flet_montrg.temperature

```sql
-- 집계된 온도 데이터 (시간별)
CREATE TABLE flet_montrg.temperature (
    id SERIAL PRIMARY KEY,
    loc_id VARCHAR(50),
    ymd VARCHAR(8),
    hh VARCHAR(2),
    temperature_max DECIMAL(5,2),
    temperature_avg DECIMAL(5,2),
    humidity_max DECIMAL(5,2),
    humidity_avg DECIMAL(5,2),
    pcv_temperature_max DECIMAL(5,2),
    pcv_temperature_avg DECIMAL(5,2),
    processed_at TIMESTAMP DEFAULT NOW()
);
```

#### 3. flet_montrg.location

```sql
-- 센서 위치 정보
CREATE TABLE flet_montrg.location (
    loc_id VARCHAR(50) PRIMARY KEY,
    factory VARCHAR(100),
    building VARCHAR(100),
    floor INTEGER,
    area VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 4. flet_montrg.thresholds

```sql
-- 임계치 설정
CREATE TABLE flet_montrg.thresholds (
    id SERIAL PRIMARY KEY,
    sensor_type VARCHAR(50),
    metric_name VARCHAR(50),
    min_value DECIMAL(10,2),
    max_value DECIMAL(10,2),
    level VARCHAR(20),  -- 'warning' or 'critical'
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🎯 주요 기능 및 특징

### 1. 확장 가능한 아키텍처

-   **마이크로서비스 패턴**: 독립적인 서비스 배포 및 확장
-   **수평적 확장**: HPA를 통한 자동 스케일링
-   **느슨한 결합**: 서비스 간 HTTP API 통신

### 2. 안정적인 데이터 파이프라인

-   **재시도 메커니즘**: 실패 시 자동 재시도
-   **데이터 검증**: 각 단계별 데이터 무결성 확인
-   **백필 지원**: 과거 데이터 재처리 기능
-   **모니터링**: Airflow UI를 통한 실시간 모니터링

### 3. 실시간 처리

-   **스트리밍 데이터**: 1시간 간격 실시간 데이터 수집
-   **즉시 알림**: 임계치 초과 시 실시간 상태 변경
-   **다중 필터링**: 다양한 조건으로 데이터 조회

### 4. 운영 효율성

-   **컨테이너화**: Docker를 통한 일관된 환경
-   **선언적 배포**: Kubernetes manifest로 인프라 코드화
-   **자동화**: CI/CD 파이프라인 구축 가능
-   **헬스체크**: 각 서비스 헬스체크 엔드포인트

## 📈 성능 최적화

### 1. 데이터베이스 최적화

-   TimescaleDB 활용: 시계열 데이터 효율적 저장
-   인덱싱: loc_id, ymd, hh 컬럼 인덱스
-   파티셔닝: 날짜 기반 파티셔닝

### 2. API 성능

-   비동기 처리: FastAPI의 async/await
-   연결 풀링: SQLAlchemy connection pool
-   캐싱: 위치 정보 및 임계치 캐싱

### 3. 인프라 최적화

-   HPA: CPU/메모리 기반 자동 스케일링
-   리소스 제한: CPU/메모리 request/limit 설정
-   네트워크 정책: 불필요한 트래픽 차단

## 🧪 테스트

### Airflow DAG 테스트

```bash
cd data_pipeline

# DAG 구문 검사
docker exec -it <airflow-scheduler> airflow dags list

# 특정 DAG 테스트
docker exec -it <airflow-scheduler> airflow dags test flet_montrg_temperature_etl 2024-01-01
```

### API 서비스 테스트

```bash
cd flet_montrg/services/aggregation-service

# 단위 테스트
pytest

# 커버리지 포함
pytest --cov=app --cov-report=html

# 특정 테스트
pytest tests/test_services.py
```

## 📝 모니터링 및 로깅

### Airflow 모니터링

-   **WebUI**: DAG 실행 상태, 로그 확인
-   **Flower**: Celery Worker 모니터링
-   **로그**: `./logs` 디렉토리에 저장

### Kubernetes 모니터링

```bash
# Pod 상태 확인
kubectl get pods -n flet-montrg

# 로그 확인
kubectl logs -f <pod-name> -n flet-montrg

# 리소스 사용량
kubectl top pods -n flet-montrg

# Dashboard 접속
kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443
```

### 애플리케이션 로그

-   구조화된 JSON 로깅
-   로그 레벨: DEBUG, INFO, WARNING, ERROR, CRITICAL
-   각 요청별 로그 추적

## 🔒 보안 고려사항

### 1. 인증 및 권한

-   Airflow: 기본 인증 (추후 LDAP/OAuth 통합 가능)
-   API: JWT 토큰 기반 인증 (구현 준비)

### 2. 네트워크 보안

-   Kubernetes Network Policy
-   서비스 간 TLS 통신 (구현 가능)
-   Secret 관리: Kubernetes Secret

### 3. 데이터 보안

-   데이터베이스 연결 암호화
-   민감 정보 환경 변수 관리
-   Fernet 키를 통한 Airflow 암호화

## 🚧 향후 개선 사항

### 기능 개선

-   [ ] **Alert Service** 구현 (Port: 30005)
    -   임계치 초과 시 실시간 알림 발송
    -   Slack, Email, SMS 등 다중 채널 지원
    -   알림 규칙 및 에스컬레이션 정책
-   [ ] **Alert History Service** 구현 (Port: 30006)
    -   알림 발송 이력 조회 API
    -   알림 통계 및 리포팅
    -   알림 승인/무시 처리
-   [ ] 대시보드 UI 개발 (React/Vue)
    -   실시간 센서 데이터 시각화
    -   알림 현황 모니터링
-   [ ] 데이터 시각화 기능
-   [ ] 예측 분석 모델 통합 (이상 탐지, 온도 예측)

### 인프라 개선

-   [ ] CI/CD 파이프라인 구축 (GitHub Actions/ArgoCD)
-   [ ] 프로덕션 Kubernetes 클러스터 (EKS/GKE)
-   [ ] 분산 추적 (Jaeger/Zipkin)
-   [ ] 중앙 집중식 로깅 (ELK Stack)

### 성능 개선

-   [ ] Redis 캐싱 레이어
-   [ ] GraphQL API 지원
-   [ ] 메시지 큐 도입 (Kafka/RabbitMQ)
-   [ ] 데이터 압축 및 아카이빙

## 📖 참고 문서

### 상세 문서

-   [Data Pipeline 상세 가이드](./data_pipeline/README.md)
-   [Database Schema 문서](./data_pipeline/db/flet_montrg/README.md)
-   [Thresholds Service 문서](./flet_montrg/services/thresholds-service/README.md)
-   [Location Service 문서](./flet_montrg/services/location-service/)
-   [Realtime Service 문서](./flet_montrg/services/realtime-service/README.md)
-   [Aggregation Service 문서](./flet_montrg/services/aggregation-service/README.md)

### 기술 문서

-   [Apache Airflow Documentation](https://airflow.apache.org/docs/)
-   [FastAPI Documentation](https://fastapi.tiangolo.com/)
-   [Kubernetes Documentation](https://kubernetes.io/docs/)
-   [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 💡 주요 학습 내용

이 프로젝트를 통해 다음과 같은 Data Engineering 핵심 역량을 습득했습니다:

1. **데이터 파이프라인 설계 및 구현**

    - Apache Airflow를 활용한 ETL 프로세스 자동화
    - 데이터 품질 관리 및 검증 로직
    - 백필 및 재처리 메커니즘

2. **마이크로서비스 아키텍처**

    - RESTful API 설계 및 구현
    - 서비스 간 통신 및 의존성 관리
    - 독립적인 배포 및 확장 전략

3. **컨테이너 및 오케스트레이션**

    - Docker를 활용한 애플리케이션 컨테이너화
    - Kubernetes를 통한 서비스 배포 및 관리
    - HPA를 활용한 자동 스케일링

4. **데이터베이스 설계**

    - 시계열 데이터를 위한 스키마 설계
    - 집계 테이블 및 최적화 기법
    - 인덱싱 및 쿼리 최적화

5. **운영 및 모니터링**
    - 로깅 및 모니터링 전략
    - 에러 핸들링 및 재시도 로직
    - 헬스체크 및 서비스 디스커버리

## 👤 작성자

**류태현 | Data Engineer**

실시간 데이터 파이프라인과 마이크로서비스 아키텍처를 직접 설계하고 구축한 경험을 바탕으로,  
데이터 신뢰성과 운영 효율성을 동시에 달성할 수 있는 시스템을 지향합니다.  

📎 GitHub Repository: [https://github.com/codingnanyong/portfolio](https://github.com/codingnanyong/portfolio)
📧 Email: ryu.coding1@gmail.com 

---

**Last Updated**: October 2025
