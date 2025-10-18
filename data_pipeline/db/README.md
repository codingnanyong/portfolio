# 📊 Database Schemas

데이터 파이프라인 및 API 서비스를 위한 데이터베이스 스키마 정의

## 📋 개요

이 디렉토리는 IoT 센서 모니터링 플랫폼의 데이터베이스 스키마 정의와 ERD(Entity Relationship Diagram)를 포함합니다. PostgreSQL/TimescaleDB를 기반으로 하며, 시계열 데이터의 효율적인 저장과 조회를 위해 최적화되었습니다.

## 📁 구조

```
db/
├── flet_montrg/              # 온도 모니터링 스키마
│   ├── README.md             # 상세 스키마 문서
│   └── hq_flet_montrg_ERD.pdf # ERD 다이어그램
└── README.md                 # 이 문서
```

## 🗄️ 데이터베이스 구성

### 사용 기술

-   **DBMS**: PostgreSQL 14+
-   **확장**: TimescaleDB (시계열 데이터 최적화)
-   **스키마**: flet_montrg

### 접근 계층

```
┌─────────────────────────────────────────────┐
│         Application Layer                    │
├──────────────┬──────────────┬───────────────┤
│  Airflow     │  API         │  Analytics    │
│  (ETL)       │  Services    │  Tools        │
└──────────────┴──────────────┴───────────────┘
                      │
              ┌───────▼────────┐
              │   PostgreSQL   │
              │   TimescaleDB  │
              └────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
   ┌────▼────┐              ┌──────▼──────┐
   │  Raw    │              │ Aggregated  │
   │  Data   │              │    Data     │
   └─────────┘              └─────────────┘
```

## 📦 스키마 목록

### 1. flet_montrg (온도 모니터링)

제조 현장의 IoT 센서 데이터 수집 및 모니터링

**주요 기능**:

-   실시간 센서 데이터 저장
-   시간별 데이터 집계
-   센서 위치 정보 관리
-   임계치 기반 알림 시스템

**상세 문서**: [flet_montrg/README.md](./flet_montrg/README.md)

## 🔧 데이터베이스 설정

### PostgreSQL 설치

```bash
# Docker로 PostgreSQL + TimescaleDB 실행
docker run -d \
  --name timescaledb \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=monitoring \
  -v pgdata:/var/lib/postgresql/data \
  timescale/timescaledb:latest-pg14
```

### TimescaleDB 확장 활성화

```sql
-- TimescaleDB 확장 설치
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 버전 확인
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';
```

### 스키마 생성

```sql
-- 스키마 생성
CREATE SCHEMA IF NOT EXISTS flet_montrg;

-- 권한 설정
GRANT USAGE ON SCHEMA flet_montrg TO airflow_user;
GRANT USAGE ON SCHEMA flet_montrg TO api_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA flet_montrg TO airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA flet_montrg TO api_user;
```

## 🎯 사용자 및 권한 관리

### 사용자 생성

```sql
-- Airflow용 사용자 (읽기/쓰기)
CREATE USER airflow_user WITH PASSWORD 'airflow_password';

-- API 서비스용 사용자 (읽기 전용)
CREATE USER api_user WITH PASSWORD 'api_password';

-- 분석용 사용자 (읽기 전용)
CREATE USER analyst_user WITH PASSWORD 'analyst_password';
```

### 권한 부여

```sql
-- Airflow 사용자: ETL 작업을 위한 전체 권한
GRANT CONNECT ON DATABASE monitoring TO airflow_user;
GRANT USAGE ON SCHEMA flet_montrg TO airflow_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA flet_montrg TO airflow_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA flet_montrg TO airflow_user;

-- API 사용자: 읽기 전용
GRANT CONNECT ON DATABASE monitoring TO api_user;
GRANT USAGE ON SCHEMA flet_montrg TO api_user;
GRANT SELECT ON ALL TABLES IN SCHEMA flet_montrg TO api_user;

-- 분석 사용자: 읽기 전용
GRANT CONNECT ON DATABASE monitoring TO analyst_user;
GRANT USAGE ON SCHEMA flet_montrg TO analyst_user;
GRANT SELECT ON ALL TABLES IN SCHEMA flet_montrg TO analyst_user;

-- 향후 생성될 테이블에도 자동 권한 부여
ALTER DEFAULT PRIVILEGES IN SCHEMA flet_montrg
GRANT SELECT ON TABLES TO api_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA flet_montrg
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO airflow_user;
```

## 🔍 모니터링 및 유지보수

### 데이터베이스 상태 확인

```sql
-- 데이터베이스 크기
SELECT
    pg_size_pretty(pg_database_size('monitoring')) as db_size;

-- 테이블별 크기
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'flet_montrg'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 연결 상태
SELECT
    datname,
    usename,
    application_name,
    client_addr,
    state,
    query_start
FROM pg_stat_activity
WHERE datname = 'monitoring';
```

### 성능 모니터링

```sql
-- 느린 쿼리 확인
SELECT
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- 인덱스 사용률
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'flet_montrg'
ORDER BY idx_scan ASC;

-- 테이블 스캔 통계
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins,
    n_tup_upd,
    n_tup_del
FROM pg_stat_user_tables
WHERE schemaname = 'flet_montrg';
```

## 🛠️ 유지보수 작업

### 백업

```bash
# 전체 데이터베이스 백업
pg_dump -h localhost -U postgres -d monitoring > monitoring_backup_$(date +%Y%m%d).sql

# 특정 스키마만 백업
pg_dump -h localhost -U postgres -d monitoring -n flet_montrg > flet_montrg_backup_$(date +%Y%m%d).sql

# 압축 백업
pg_dump -h localhost -U postgres -d monitoring | gzip > monitoring_backup_$(date +%Y%m%d).sql.gz
```

### 복원

```bash
# SQL 파일로 복원
psql -h localhost -U postgres -d monitoring < monitoring_backup_20241018.sql

# 압축 파일 복원
gunzip -c monitoring_backup_20241018.sql.gz | psql -h localhost -U postgres -d monitoring
```

### VACUUM 및 ANALYZE

```sql
-- 전체 스키마 VACUUM
VACUUM ANALYZE flet_montrg;

-- 특정 테이블 VACUUM (Full)
VACUUM FULL flet_montrg.temperature_raw;

-- ANALYZE만 실행
ANALYZE flet_montrg.temperature;
```

### 오래된 데이터 정리

```sql
-- Raw 데이터: 90일 이상 된 데이터 삭제
DELETE FROM flet_montrg.temperature_raw
WHERE capture_dt < NOW() - INTERVAL '90 days';

-- 집계 데이터: 1년 이상 된 데이터 아카이브
INSERT INTO flet_montrg.temperature_archive
SELECT * FROM flet_montrg.temperature
WHERE TO_DATE(ymd, 'YYYYMMDD') < CURRENT_DATE - INTERVAL '1 year';

DELETE FROM flet_montrg.temperature
WHERE TO_DATE(ymd, 'YYYYMMDD') < CURRENT_DATE - INTERVAL '1 year';
```

## 📈 성능 최적화

### 인덱스 생성 권장사항

```sql
-- 시계열 데이터 조회용
CREATE INDEX idx_temperature_raw_capture_dt
ON flet_montrg.temperature_raw(capture_dt DESC);

-- 위치별 조회용
CREATE INDEX idx_temperature_raw_loc_id
ON flet_montrg.temperature_raw(loc_id);

-- 집계 데이터 조회용 (복합 인덱스)
CREATE INDEX idx_temperature_ymd_hh
ON flet_montrg.temperature(ymd, hh);

CREATE INDEX idx_temperature_loc_ymd
ON flet_montrg.temperature(loc_id, ymd);
```

### TimescaleDB 하이퍼테이블 설정

```sql
-- 하이퍼테이블로 변환
SELECT create_hypertable(
    'flet_montrg.temperature_raw',
    'capture_dt',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

-- 자동 압축 정책 설정 (7일 이상 된 데이터)
ALTER TABLE flet_montrg.temperature_raw SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'loc_id'
);

SELECT add_compression_policy(
    'flet_montrg.temperature_raw',
    INTERVAL '7 days'
);

-- 자동 삭제 정책 (90일 이상 된 데이터)
SELECT add_retention_policy(
    'flet_montrg.temperature_raw',
    INTERVAL '90 days'
);
```

### 연결 풀링

```ini
# pgbouncer.ini
[databases]
monitoring = host=localhost port=5432 dbname=monitoring

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 100
default_pool_size = 20
reserve_pool_size = 5
```

## 🔒 보안 고려사항

### SSL 연결 활성화

```sql
-- SSL 필수 설정
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/path/to/server.crt';
ALTER SYSTEM SET ssl_key_file = '/path/to/server.key';

-- 사용자별 SSL 강제
ALTER USER api_user SET ssl = on;
```

### 감사 로깅

```sql
-- 감사 로깅 확장 설치
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- 감사 설정
ALTER SYSTEM SET pgaudit.log = 'write, ddl';
ALTER SYSTEM SET pgaudit.log_catalog = off;
SELECT pg_reload_conf();
```

## 📚 참고 자료

-   [PostgreSQL 공식 문서](https://www.postgresql.org/docs/)
-   [TimescaleDB 문서](https://docs.timescale.com/)
-   [flet_montrg 스키마 상세](./flet_montrg/README.md)

## 🚀 시작하기

1. PostgreSQL + TimescaleDB 설치
2. 데이터베이스 및 사용자 생성
3. 스키마 파일 실행
4. 권한 설정
5. 인덱스 및 최적화 적용

---

**Last Updated**: October 2025
