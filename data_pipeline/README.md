# 🌬️ Data Pipeline - Apache Airflow

Apache Airflow–based data pipeline for IoT sensor data ingestion and processing

## 📋 Overview

This pipeline processes temperature and humidity data collected in real time from IoT sensors at manufacturing sites. It uses Apache Airflow to automate ETL (Extract, Transform, Load) and to run hourly aggregation and analysis.

## 🛠️ Tech Stack

- **Workflow**: Apache Airflow 2.10.3
- **Executor**: Celery Executor (distributed)
- **Message broker**: Redis
- **Database**: PostgreSQL
- **Monitoring**: Flower (Celery monitoring)
- **Containers**: Docker, Docker Compose
- **Language**: Python 3.x

## 📁 Project Structure

```text
data_pipeline/
├── dags/                           # Airflow DAG definitions
│   └── flet_montrg/                # Temperature monitoring DAG
│       ├── flet_montrg_master_etl.py              # Master data ETL
│       ├── flet_montrg_temperature_etl.py          # Temperature ETL (main)
│       ├── flet_montrg_temperature_backfill.py    # Temperature backfill
│       ├── flet_montrg_temperature_raw_etl.py     # Raw data ETL
│       └── flet_montrg_temperature_raw_backfill.py # Raw data backfill
│
├── plugins/                        # Custom plugins
│   └── hooks/                      # Database connection hooks
│       ├── postgres_hook.py        # PostgreSQL
│       ├── mysql_hook.py           # MySQL
│       ├── mssql_hook.py           # MS SQL Server
│       └── oracle_hook.py          # Oracle
│
├── db/                             # Database schema
│   └── flet_montrg/                # Temperature monitoring schema
│       ├── README.md               # Schema docs
│       └── hq_flet_montrg_ERD.pdf  # ERD diagram
│
├── scripts/                        # Setup scripts
│   ├── install_pymodbus.sh         # Modbus library
│   ├── install_pymodbustcp.sh       # Modbus TCP
│   └── oracledb_setting.sh         # Oracle DB setup
│
├── oracle/                         # Oracle setup
│   └── ORACLE_INSTANT_CLIENT_SETUP.md
│
├── docker-compose.yml             # Airflow services
├── Dockerfile                     # Custom Airflow image
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔄 Pipeline Flow

### Data Flow

```text
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

## 📊 Main DAGs

### 1. flet_montrg_temperature_etl.py

**Purpose**: Hourly temperature aggregation and processing (main pipeline)

**Schedule**: Every hour

**Steps**:

1. **Connection Check**: Verify DB connections
   - Source DB (pg_fdw_v1_iot): Raw data
   - Target DB (pg_fdw_v2_hq): Aggregated data
2. **Data Extraction**: Extract raw data

    ```sql
    -- Raw data for time range
    SELECT
        loc_id,
        temperature,
        humidity,
        pcv_temperature,
        capture_dt
    FROM <schema>.temperature_raw
    WHERE capture_dt >= :start_time
      AND capture_dt < :end_time
    ```

3. **Data Transformation**: Hourly aggregation

    ```sql
    -- Aggregation by location and hour
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

4. **Data Loading**: Load aggregated data
   - Upsert to avoid duplicates; update if row exists

5. **Data Validation**: Validate loaded record count and integrity

**DAG config**:

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

schedule_interval = '0 * * * *'  # Every hour on the hour
```

### 2. flet_montrg_temperature_backfill.py

**Purpose**: Backfill historical data

**Use cases**:

- Reprocess after data quality issues
- Recompute after aggregation logic changes
- Fill gaps after outages

**Features**: Configurable date range, chunked processing, progress logging

**Run**:

```python
# Airflow Variables
backfill_start_date = '2024-01-01'
backfill_end_date = '2024-01-31'

# DAG run
airflow dags backfill flet_montrg_temperature_backfill \
    --start-date 2024-01-01 \
    --end-date 2024-01-31
```

### 3. flet_montrg_temperature_raw_etl.py

**Purpose**: Raw data ingestion and preprocessing (sensor origin, validation, optional outlier filtering, load to raw table).

### 4. flet_montrg_master_etl.py

**Purpose**: Master data sync (sensor locations, metadata, threshold settings).

## 🔌 Custom Hooks

### PostgresHelper (postgres_hook.py)

Helper for PostgreSQL connections and queries.

**Methods**:

```python
class PostgresHelper:
    def __init__(self, conn_id: str):
        """Initialize with connection ID"""

    def execute_query(self, sql: str, **context) -> List[Dict]:
        """Execute SQL and return results"""

    def execute_insert(self, table: str, data: List[Dict], **context):
        """Insert data"""

    def execute_upsert(self, table: str, data: List[Dict],
                      conflict_columns: List[str], **context):
        """Upsert (Insert or Update)"""

    def check_table(self, schema: str, table: str) -> bool:
        """Check if table exists"""
```

**Example**:

```python
from plugins.hooks.postgres_hook import PostgresHelper

pg_helper = PostgresHelper(conn_id='pg_fdw_v1_iot')

result = pg_helper.execute_query(
    sql="SELECT * FROM <schema>.temperature_raw LIMIT 10",
    **context
)

pg_helper.execute_upsert(
    table='<schema>.temperature',
    data=aggregated_data,
    conflict_columns=['loc_id', 'ymd', 'hh'],
    **context
)
```

### Supported databases

- **PostgreSQL**: `postgres_hook.py`
- **MySQL**: `mysql_hook.py`
- **MS SQL Server**: `mssql_hook.py`
- **Oracle**: `oracle_hook.py`

## ⚙️ Install & Run

### 1. Prerequisites

- Docker and Docker Compose
- At least 4GB RAM recommended
- PostgreSQL (source and target)

### 2. Environment

**.env**:

```bash
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__CORE__FERNET_KEY=<your-fernet-key>
AIRFLOW__WEBSERVER__SECRET_KEY=<your-secret-key>
AIRFLOW__CORE__LOAD_EXAMPLES=False
AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False
AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True
```

**Generate keys**:

```bash
docker exec -it <airflow-scheduler-container> bash

python << EOF
from cryptography.fernet import Fernet
print(f"FERNET_KEY: {Fernet.generate_key().decode()}")

import os
print(f"SECRET_KEY: {os.urandom(16).hex()}")
EOF
```

### 3. Directories

```bash
mkdir -p ./dags ./logs ./plugins
```

### 4. Init & start

```bash
docker compose up airflow-init
docker compose up -d
docker compose ps
docker compose up -d airflow-flower  # optional
```

### 5. Worker scaling

```bash
docker-compose up -d --scale airflow-worker=3 airflow-worker
docker compose ps | grep worker
```

### 6. Access

- **Airflow UI**: [http://localhost:8080] (default admin/admin; change in production)
- **Flower**: [http://localhost:5555]

## 🔧 Airflow Connections

In the UI: Admin > Connections.

### PostgreSQL

**Connection ID**: `pg_fdw_v1_iot` (Raw source)

- Connection Type: Postgres
- Host: your-postgres-host
- Schema: flet_montrg
- Login / Password / Port: 5432

**Connection ID**: `pg_fdw_v2_hq` (Processed target)

- Same type; use your target host and credentials.

## 📈 Monitoring & Debugging

### Logs

```bash
docker compose logs -f airflow-scheduler
docker compose logs -f airflow-worker
docker compose logs -f
# Log files: ./logs/dag_id=<dag_id>/run_id=<run_id>/task_id=<task_id>/
```

### DAG test

```bash
docker exec -it airflow-scheduler airflow dags list
docker exec -it airflow-scheduler airflow dags show flet_montrg_temperature_etl
docker exec -it airflow-scheduler airflow dags test flet_montrg_temperature_etl 2024-01-01
docker exec -it airflow-scheduler airflow tasks test \
    flet_montrg_temperature_etl check_connections 2024-01-01
```

### Flower

At [http://localhost:5555] : worker status, resource usage, task stats, queue, failed tasks.

## 🚨 Troubleshooting

### DAG not visible

```bash
docker compose restart airflow-scheduler
ls -la ./dags/
docker compose logs airflow-scheduler | grep -i error
```

### Task failure

Check: DB connectivity, data format, memory/CPU, timeout. Use Web UI > DAG > Graph > Task > Log; use Clear to retry.

### Worker disconnect

```bash
docker compose ps airflow-worker
docker compose restart airflow-worker
docker exec -it redis redis-cli ping
```

### Out of memory

Reduce workers: `docker-compose up -d --scale airflow-worker=1 airflow-worker` or adjust resource limits in docker-compose.yml.

## 📊 Performance

### Celery worker

```yaml
airflow-worker:
    environment:
        - AIRFLOW__CELERY__WORKER_CONCURRENCY=4
        - AIRFLOW__CELERY__WORKER_PREFETCH_MULTIPLIER=2
```

### DB pool

```ini
[core]
sql_alchemy_pool_size = 10
sql_alchemy_max_overflow = 20
sql_alchemy_pool_recycle = 3600
```

### DAG tips

- Prefer DB over XCom for passing data between tasks
- Process large datasets in chunks
- Run parallelizable tasks independently

## 🔐 Security

- Use auth and RBAC in .env; encrypt connections with Fernet; keep secrets in env vars.
- For internal-only network: `internal: true` in docker-compose networks.

## 📚 References

- [Database Schema](./db/flet_montrg/README.md)
- [Oracle Setup](./oracle/ORACLE_INSTANT_CLIENT_SETUP.md)
- [Apache Airflow](https://airflow.apache.org/docs/)
- [Celery](https://docs.celeryproject.org/)
- [Docker Compose](https://docs.docker.com/compose/)

## 🎯 Adding a new DAG

1. Add a Python file under `./dags/`.
2. Define DAG with `default_args`, `schedule_interval`, `catchup=False`, and tasks.
3. Validate: `airflow dags test my_new_dag 2024-01-01`
4. Enable in the Web UI.

**Practices**: Idempotent tasks, atomic success/failure, logging, error handling, testing before production.

## 📞 Support

Use the repository Issues for bugs or suggestions.

---

**Last Updated**: February 2026
