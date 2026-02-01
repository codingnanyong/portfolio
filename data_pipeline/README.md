# 🌬️ Data Pipeline - Apache Airflow

IoT 센서 데이터 수집 및 처리를 위한 Apache Airflow 기반 데이터 파이프라인

## 📋 개요

이 데이터 파이프라인은 제조 현장의 IoT 센서로부터 실시간으로 수집되는 온도 및 습도 데이터를 처리합니다. Apache Airflow를 사용하여 ETL(Extract, Transform, Load) 프로세스를 자동화하고, 시간별 데이터 집계 및 분석을 수행합니다.

## 🛠️ 기술 스택

-   **워크플로우 관리**: Apache Airflow 2.10.3
-   **Executor**: Celery Executor (분산 처리)
-   **메시지 브로커**: Redis
-   **데이터베이스**: PostgreSQL
-   **모니터링**: Flower (Celery 모니터링)
-   **컨테이너**: Docker, Docker Compose
-   **언어**: Python 3.x

## 📁 프로젝트 구조

```
data_pipeline/
├── dags/                           # Airflow DAG 정의
│   └── flet_montrg/               # 온도 모니터링 DAG
│       ├── flet_montrg_master_etl.py              # 마스터 데이터 ETL
│       ├── flet_montrg_temperature_etl.py         # 온도 데이터 ETL (메인)
│       ├── flet_montrg_temperature_backfill.py    # 온도 데이터 백필
│       ├── flet_montrg_temperature_raw_etl.py     # Raw 데이터 ETL
│       └── flet_montrg_temperature_raw_backfill.py # Raw 데이터 백필
│
├── plugins/                       # 커스텀 플러그인
│   └── hooks/                     # 데이터베이스 연결 훅
│       ├── postgres_hook.py       # PostgreSQL 연결
│       ├── mysql_hook.py          # MySQL 연결
│       ├── mssql_hook.py          # MS SQL Server 연결
│       └── oracle_hook.py         # Oracle 연결
│
├── db/                            # 데이터베이스 스키마
│   └── flet_montrg/              # 온도 모니터링 스키마
│       ├── README.md             # 스키마 문서
│       └── hq_flet_montrg_ERD.pdf # ERD 다이어그램
│
├── scripts/                       # 설치 및 설정 스크립트
│   ├── install_pymodbus.sh       # Modbus 라이브러리 설치
│   ├── install_pymodbustcp.sh    # Modbus TCP 설치
│   └── oracledb_setting.sh       # Oracle DB 설정
│
├── oracle/                        # Oracle 관련 설정
│   └── ORACLE_INSTANT_CLIENT_SETUP.md
│
├── docker-compose.yml             # Airflow 서비스 구성
├── Dockerfile                     # 커스텀 Airflow 이미지
├── requirements.txt              # Python 의존성
└── README.md                     # 이 문서
```

## 🔄 데이터 파이프라인 구조

### 데이터 흐름

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ IoT Sensors │ --> │ PostgreSQL   │ --> │ Airflow DAGs  │ --> │ PostgreSQL   │
│             │     │ (Raw Data)   │     │ (ETL Process) │     │ (Processed)  │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────┘
                                                 │
                                                 │
                                          ┌──────▼──────┐
                                          │   API       │
                                          │  Services   │
                                          └─────────────┘
```

## 📊 주요 DAG 설명

### 1. flet_montrg_temperature_etl.py

**목적**: 시간별 온도 데이터 집계 및 처리 (메인 파이프라인)

**실행 주기**: 1시간마다

**처리 단계**:

1. **Connection Check**: 데이터베이스 연결 확인
    - Source DB (pg_fdw_v1_iot): Raw 데이터
    - Target DB (pg_fdw_v2_hq): 집계 데이터
2. **Data Extraction**: Raw 데이터 추출

    ```sql
    -- 시간 범위의 Raw 데이터 조회
    SELECT
        loc_id,
        temperature,
        humidity,
        pcv_temperature,
        capture_dt
    FROM flet_montrg.temperature_raw
    WHERE capture_dt >= :start_time
      AND capture_dt < :end_time
    ```

3. **Data Transformation**: 시간별 집계

    ```sql
    -- 위치별, 시간별 집계
    SELECT
        loc_id,
        TO_CHAR(capture_dt, 'YYYYMMDD') as ymd,
        TO_CHAR(capture_dt, 'HH24') as hh,
        MAX(temperature) as temperature_max,
        AVG(temperature) as temperature_avg,
        MAX(humidity) as humidity_max,
        AVG(humidity) as humidity_avg,
        MAX(pcv_temperature) as pcv_temperature_max,
        AVG(pcv_temperature) as pcv_temperature_avg
    GROUP BY loc_id, ymd, hh
    ```

4. **Data Loading**: 집계 데이터 적재

    - Upsert 방식으로 중복 방지
    - 기존 데이터가 있으면 업데이트

5. **Data Validation**: 데이터 검증
    - 적재된 레코드 수 확인
    - 데이터 무결성 검증

**DAG 설정**:

```python
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
    'execution_timeout': timedelta(minutes=30),
    'sla': timedelta(minutes=60)
}

schedule_interval = '0 * * * *'  # 매 시간 정각
```

### 2. flet_montrg_temperature_backfill.py

**목적**: 과거 데이터 재처리 (백필)

**사용 시나리오**:

-   데이터 품질 이슈 발견 시 재처리
-   집계 로직 변경 후 과거 데이터 재계산
-   시스템 장애 복구 후 누락 데이터 처리

**특징**:

-   날짜 범위 지정 가능
-   청크 단위 처리 (메모리 효율성)
-   진행 상황 로깅

**실행 방법**:

```python
# Airflow Variable 설정
backfill_start_date = '2024-01-01'
backfill_end_date = '2024-01-31'

# DAG 실행
airflow dags backfill flet_montrg_temperature_backfill \
    --start-date 2024-01-01 \
    --end-date 2024-01-31
```

### 3. flet_montrg_temperature_raw_etl.py

**목적**: Raw 데이터 수집 및 전처리

**처리 내용**:

-   IoT 센서 데이터 원본 수집
-   데이터 형식 검증
-   이상치 필터링 (선택적)
-   Raw 데이터 테이블 적재

### 4. flet_montrg_master_etl.py

**목적**: 마스터 데이터 동기화

**처리 내용**:

-   센서 위치 정보 업데이트
-   센서 메타데이터 동기화
-   임계치 설정 업데이트

## 🔌 커스텀 Hooks

### PostgresHelper (postgres_hook.py)

PostgreSQL 데이터베이스 연결 및 쿼리 실행을 위한 헬퍼 클래스

**주요 메서드**:

```python
class PostgresHelper:
    def __init__(self, conn_id: str):
        """연결 ID로 초기화"""

    def execute_query(self, sql: str, **context) -> List[Dict]:
        """SQL 쿼리 실행 및 결과 반환"""

    def execute_insert(self, table: str, data: List[Dict], **context):
        """데이터 삽입"""

    def execute_upsert(self, table: str, data: List[Dict],
                      conflict_columns: List[str], **context):
        """Upsert (Insert or Update)"""

    def check_table(self, schema: str, table: str) -> bool:
        """테이블 존재 여부 확인"""
```

**사용 예시**:

```python
from plugins.hooks.postgres_hook import PostgresHelper

# 초기화
pg_helper = PostgresHelper(conn_id='pg_fdw_v1_iot')

# 데이터 조회
result = pg_helper.execute_query(
    sql="SELECT * FROM flet_montrg.temperature_raw LIMIT 10",
    **context
)

# 데이터 삽입 (Upsert)
pg_helper.execute_upsert(
    table='flet_montrg.temperature',
    data=aggregated_data,
    conflict_columns=['loc_id', 'ymd', 'hh'],
    **context
)
```

### 지원 데이터베이스

-   **PostgreSQL**: `postgres_hook.py`
-   **MySQL**: `mysql_hook.py`
-   **MS SQL Server**: `mssql_hook.py`
-   **Oracle**: `oracle_hook.py`

## ⚙️ 설치 및 실행

### 1. 사전 요구사항

-   Docker 및 Docker Compose 설치
-   최소 4GB RAM 권장
-   PostgreSQL 데이터베이스 (Source & Target)

### 2. 환경 설정

**.env 파일 생성**:

```bash
# 데이터베이스 연결
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow

# Celery 설정
AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow

# Executor 설정
AIRFLOW__CORE__EXECUTOR=CeleryExecutor

# 보안 키 (생성 필요)
AIRFLOW__CORE__FERNET_KEY=<your-fernet-key>
AIRFLOW__WEBSERVER__SECRET_KEY=<your-secret-key>

# 기타 설정
AIRFLOW__CORE__LOAD_EXAMPLES=False
AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False
AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True
```

**보안 키 생성**:

```bash
# Airflow 컨테이너에 접속
docker exec -it <airflow-scheduler-container> bash

# Python으로 키 생성
python << EOF
from cryptography.fernet import Fernet
print(f"FERNET_KEY: {Fernet.generate_key().decode()}")

import os
print(f"SECRET_KEY: {os.urandom(16).hex()}")
EOF
```

### 3. 디렉토리 준비

```bash
# 필수 디렉토리 생성
mkdir -p ./dags ./logs ./plugins
```

### 4. Airflow 초기화 및 실행

```bash
# Airflow 데이터베이스 초기화
docker compose up airflow-init

# Airflow 서비스 시작
docker compose up -d

# 서비스 상태 확인
docker compose ps

# Flower 모니터링 시작 (선택사항)
docker compose up -d airflow-flower
```

### 5. Worker 스케일링

```bash
# Worker 수 조정 (예: 3개)
docker-compose up -d --scale airflow-worker=3 airflow-worker

# Worker 상태 확인
docker compose ps | grep worker
```

### 6. 접속 정보

-   **Airflow UI**: http://localhost:8080
    -   기본 계정: admin / admin (변경 권장)
-   **Flower UI**: http://localhost:5555

## 🔧 Airflow 연결(Connection) 설정

웹 UI에서 Admin > Connections로 이동하여 다음 연결을 설정:

### PostgreSQL 연결

**Connection ID**: `pg_fdw_v1_iot` (Raw Data Source)

-   Connection Type: Postgres
-   Host: your-postgres-host
-   Schema: flet_montrg
-   Login: your-username
-   Password: your-password
-   Port: 5432

**Connection ID**: `pg_fdw_v2_hq` (Processed Data Target)

-   Connection Type: Postgres
-   Host: your-postgres-host
-   Schema: flet_montrg
-   Login: your-username
-   Password: your-password
-   Port: 5432

## 📈 모니터링 및 디버깅

### 로그 확인

```bash
# 특정 서비스 로그
docker compose logs -f airflow-scheduler
docker compose logs -f airflow-worker

# 모든 로그
docker compose logs -f

# 로그 파일 위치
./logs/dag_id=<dag_id>/run_id=<run_id>/task_id=<task_id>/
```

### DAG 테스트

```bash
# DAG 파일 구문 검사
docker exec -it airflow-scheduler airflow dags list

# DAG 정보 확인
docker exec -it airflow-scheduler airflow dags show flet_montrg_temperature_etl

# DAG 테스트 실행
docker exec -it airflow-scheduler airflow dags test flet_montrg_temperature_etl 2024-01-01

# 특정 Task 테스트
docker exec -it airflow-scheduler airflow tasks test \
    flet_montrg_temperature_etl check_connections 2024-01-01
```

### Flower 모니터링

Flower UI (http://localhost:5555)에서 확인 가능:

-   Worker 상태 및 리소스 사용량
-   Task 실행 통계
-   Task 큐 상태
-   실패한 Task 내역

## 🚨 일반적인 문제 해결

### 1. DAG가 보이지 않을 때

```bash
# Scheduler 재시작
docker compose restart airflow-scheduler

# DAG 파일 권한 확인
ls -la ./dags/

# Scheduler 로그 확인
docker compose logs airflow-scheduler | grep -i error
```

### 2. Task 실패 시

**확인 사항**:

1. 데이터베이스 연결 상태
2. 데이터 형식 검증
3. 리소스 부족 (메모리/CPU)
4. 타임아웃 설정

**해결 방법**:

```bash
# Task 로그 확인 (Web UI)
# Airflow UI > DAGs > [DAG 이름] > Graph > [Task 클릭] > Log

# Task 재실행
# Airflow UI에서 Clear 버튼 클릭
```

### 3. Worker 연결 끊김

```bash
# Worker 상태 확인
docker compose ps airflow-worker

# Worker 재시작
docker compose restart airflow-worker

# Redis 연결 확인
docker exec -it redis redis-cli ping
```

### 4. 메모리 부족

```bash
# Worker 수 줄이기
docker-compose up -d --scale airflow-worker=1 airflow-worker

# docker-compose.yml에서 리소스 제한 조정
```

## 📊 성능 최적화

### 1. Executor 최적화

**Celery Worker 설정**:

```yaml
# docker-compose.yml
airflow-worker:
    environment:
        - AIRFLOW__CELERY__WORKER_CONCURRENCY=4
        - AIRFLOW__CELERY__WORKER_PREFETCH_MULTIPLIER=2
```

### 2. 데이터베이스 최적화

**Connection Pool 설정**:

```ini
[core]
sql_alchemy_pool_size = 10
sql_alchemy_max_overflow = 20
sql_alchemy_pool_recycle = 3600
```

### 3. DAG 최적화

**권장 사항**:

-   Task 간 데이터 전달은 XCom 대신 데이터베이스 사용
-   큰 데이터셋은 청크 단위로 처리
-   병렬 처리 가능한 Task는 독립적으로 실행

## 🔐 보안 고려사항

### 1. 인증 설정

**.env 파일**:

```bash
# 기본 인증 활성화
AIRFLOW__WEBSERVER__AUTHENTICATE=True
AIRFLOW__WEBSERVER__AUTH_BACKEND=airflow.contrib.auth.backends.password_auth

# RBAC 활성화
AIRFLOW__WEBSERVER__RBAC=True
```

### 2. 연결 정보 암호화

-   Fernet Key 사용
-   Connections는 Airflow 메타데이터 DB에 암호화 저장
-   민감 정보는 환경 변수로 관리

### 3. 네트워크 보안

```yaml
# docker-compose.yml
networks:
    airflow:
        driver: bridge
        internal: true # 외부 접근 차단
```

## 📚 추가 리소스

### 문서

-   [Database Schema](./db/flet_montrg/README.md)
-   [Oracle Setup Guide](./oracle/ORACLE_INSTANT_CLIENT_SETUP.md)

### 참고 자료

-   [Apache Airflow 공식 문서](https://airflow.apache.org/docs/)
-   [Celery 공식 문서](https://docs.celeryproject.org/)
-   [Docker Compose 문서](https://docs.docker.com/compose/)

## 🎯 DAG 개발 가이드

### 새로운 DAG 추가

1. **DAG 파일 생성**: `./dags/` 디렉토리에 Python 파일 생성
2. **DAG 정의**:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'my_new_dag',
    default_args=default_args,
    schedule_interval='0 * * * *',
    catchup=False,
    tags=['example', 'etl']
) as dag:

    def my_task(**context):
        # Task 로직
        pass

    task = PythonOperator(
        task_id='my_task',
        python_callable=my_task
    )
```

3. **DAG 검증**: `airflow dags test my_new_dag 2024-01-01`
4. **활성화**: Web UI에서 DAG 토글 ON

### 베스트 프랙티스

1. **Idempotency**: Task는 여러 번 실행해도 같은 결과
2. **Atomicity**: Task는 완전 성공 또는 완전 실패
3. **Logging**: 충분한 로그 메시지 추가
4. **Error Handling**: 예외 처리 및 재시도 로직
5. **Testing**: 운영 배포 전 충분한 테스트

## 📞 문의 및 지원

이슈가 있거나 개선 제안이 있다면 프로젝트 리포지토리의 Issues 섹션을 활용해주세요.

---

**Last Updated**: October 2025
