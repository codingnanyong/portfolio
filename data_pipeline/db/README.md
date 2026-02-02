# 📊 Database Schemas

Database schema definitions for the data pipeline and API services

## 📋 Overview

This directory holds database schema definitions and ERD (Entity Relationship Diagram) for the IoT sensor monitoring platform. It is based on PostgreSQL/TimescaleDB and tuned for efficient storage and querying of time-series data.

## 📁 Structure

```text
db/
├── flet_montrg/              # Temperature monitoring schema
│   ├── README.md             # Schema documentation
│   └── hq_flet_montrg_ERD.pdf # ERD diagram
└── README.md                 # This file
```

## 🗄️ Database Setup

### Technologies

- **DBMS**: PostgreSQL 14+
- **Extension**: TimescaleDB (time-series optimization)
- **Schema**: flet_montrg

### Access Layers

```text
┌─────────────────────────────────────────────┐
│         Application Layer                   │
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

## 📦 Schemas

### 1. flet_montrg (Temperature monitoring)

IoT sensor data collection and monitoring for manufacturing sites.

**Features**:

- Real-time sensor data storage
- Hourly aggregation
- Sensor location management
- Threshold-based alerting

**Details**: [flet_montrg/README.md](./flet_montrg/README.md)

## 🔧 Database Setup

### PostgreSQL

```bash
docker run -d \
  --name timescaledb \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=monitoring \
  -v pgdata:/var/lib/postgresql/data \
  timescale/timescaledb:latest-pg14
```

### Enable TimescaleDB

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';
```

### Create schema

```sql
CREATE SCHEMA IF NOT EXISTS flet_montrg;

GRANT USAGE ON SCHEMA flet_montrg TO airflow_user;
GRANT USAGE ON SCHEMA flet_montrg TO api_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA flet_montrg TO airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA flet_montrg TO api_user;
```

## 🎯 Users & Permissions

### Create users

```sql
CREATE USER airflow_user WITH PASSWORD 'airflow_password';
CREATE USER api_user WITH PASSWORD 'api_password';
CREATE USER analyst_user WITH PASSWORD 'analyst_password';
```

### Grant permissions

```sql
-- Airflow: full for ETL
GRANT CONNECT ON DATABASE monitoring TO airflow_user;
GRANT USAGE ON SCHEMA flet_montrg TO airflow_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA flet_montrg TO airflow_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA flet_montrg TO airflow_user;

-- API: read-only
GRANT CONNECT ON DATABASE monitoring TO api_user;
GRANT USAGE ON SCHEMA flet_montrg TO api_user;
GRANT SELECT ON ALL TABLES IN SCHEMA flet_montrg TO api_user;

-- Analyst: read-only
GRANT CONNECT ON DATABASE monitoring TO analyst_user;
GRANT USAGE ON SCHEMA flet_montrg TO analyst_user;
GRANT SELECT ON ALL TABLES IN SCHEMA flet_montrg TO analyst_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA flet_montrg
GRANT SELECT ON TABLES TO api_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA flet_montrg
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO airflow_user;
```

## 🔍 Monitoring & Maintenance

### Status

```sql
SELECT pg_size_pretty(pg_database_size('monitoring')) as db_size;

SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'flet_montrg'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

SELECT datname, usename, application_name, client_addr, state, query_start
FROM pg_stat_activity
WHERE datname = 'monitoring';
```

### Performance

```sql
SELECT query, calls, total_time, mean_time, max_time
FROM pg_stat_statements
ORDER BY mean_time DESC LIMIT 10;

SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'flet_montrg'
ORDER BY idx_scan ASC;

SELECT schemaname, tablename, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch,
       n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables
WHERE schemaname = 'flet_montrg';
```

## 🛠️ Maintenance

### Backup

```bash
pg_dump -h localhost -U postgres -d monitoring > monitoring_backup_$(date +%Y%m%d).sql
pg_dump -h localhost -U postgres -d monitoring -n flet_montrg > flet_montrg_backup_$(date +%Y%m%d).sql
pg_dump -h localhost -U postgres -d monitoring | gzip > monitoring_backup_$(date +%Y%m%d).sql.gz
```

### Restore

```bash
psql -h localhost -U postgres -d monitoring < monitoring_backup_20241018.sql
gunzip -c monitoring_backup_20241018.sql.gz | psql -h localhost -U postgres -d monitoring
```

### VACUUM & ANALYZE

```sql
VACUUM ANALYZE flet_montrg;
VACUUM FULL flet_montrg.temperature_raw;
ANALYZE flet_montrg.temperature;
```

### Retention

```sql
DELETE FROM flet_montrg.temperature_raw
WHERE capture_dt < NOW() - INTERVAL '90 days';

INSERT INTO flet_montrg.temperature_archive
SELECT * FROM flet_montrg.temperature
WHERE TO_DATE(ymd, 'YYYYMMDD') < CURRENT_DATE - INTERVAL '1 year';

DELETE FROM flet_montrg.temperature
WHERE TO_DATE(ymd, 'YYYYMMDD') < CURRENT_DATE - INTERVAL '1 year';
```

## 📈 Performance

### Indexes

```sql
CREATE INDEX idx_temperature_raw_capture_dt
ON flet_montrg.temperature_raw(capture_dt DESC);

CREATE INDEX idx_temperature_raw_loc_id
ON flet_montrg.temperature_raw(loc_id);

CREATE INDEX idx_temperature_ymd_hh
ON flet_montrg.temperature(ymd, hh);

CREATE INDEX idx_temperature_loc_ymd
ON flet_montrg.temperature(loc_id, ymd);
```

### TimescaleDB hypertable

```sql
SELECT create_hypertable(
    'flet_montrg.temperature_raw',
    'capture_dt',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

ALTER TABLE flet_montrg.temperature_raw SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'loc_id'
);

SELECT add_compression_policy('flet_montrg.temperature_raw', INTERVAL '7 days');
SELECT add_retention_policy('flet_montrg.temperature_raw', INTERVAL '90 days');
```

### Connection pooling

```ini
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

## 🔒 Security

### SSL

```sql
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/path/to/server.crt';
ALTER SYSTEM SET ssl_key_file = '/path/to/server.key';
ALTER USER api_user SET ssl = on;
```

### Audit logging

```sql
CREATE EXTENSION IF NOT EXISTS pgaudit;
ALTER SYSTEM SET pgaudit.log = 'write, ddl';
ALTER SYSTEM SET pgaudit.log_catalog = off;
SELECT pg_reload_conf();
```

## 📚 References

- [PostgreSQL](https://www.postgresql.org/docs/)
- [TimescaleDB](https://docs.timescale.com/)
- [flet_montrg schema](./flet_montrg/README.md)

## 🚀 Quick start

1. Install PostgreSQL + TimescaleDB
2. Create database and users
3. Run schema scripts
4. Apply permissions
5. Add indexes and optimizations

---

**Last Updated**: February 2026
