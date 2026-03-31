# 📊 Thresholds Service

API for managing apparent temperature (and related) thresholds — CRUD, levels (e.g. green / yellow / orange), and type-based lookup.

## ✨ Features

- 📝 Threshold CRUD
- 🔍 Query by type (e.g. pcv_temperature)
- ✅ Validation and error handling
- 💓 Health check and structured logging
- 🐳 Docker and Kubernetes–ready

## 📁 Project structure

```text
thresholds-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry
│   ├── api/
│   │   └── v1/
│   │       ├── api.py          # API v1 router
│   │       └── endpoints/
│   │           └── thresholds.py # Threshold endpoints
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── models/
│   │   ├── database_models.py  # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   └── services/
│       └── threshold_service.py # Business logic
├── tests/
│   └── conftest.py
├── requirements.txt
├── env.example
├── Dockerfile
└── README.md
```

## 🚀 Run

### Local

```bash
pip install -r requirements.txt
cp env.example .env
# Edit .env as needed

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker build -t thresholds-service .
docker run -p 8000:8000 --env-file .env thresholds-service
```

### K8s (Kind)

- **NodePort**: `30001` (see project [README](../../README.md) for port layout)

## 🔌 API docs

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- `GET /` — service info | `GET /health` — health | `GET /ready` — readiness

## 🧪 Tests

```bash
pytest
pytest --cov=app
pytest tests/
```

## ⚙️ Environment variables

- `APP_NAME` — Application name (default: Thresholds Service)
- `APP_VERSION` — Version (default: 1.0.0)
- `DEBUG` — Debug mode (default: false)
- `ENVIRONMENT` — development / production (default: development)
- `HOST` — Server host (default: 0.0.0.0)
- `PORT` — Server port (default: 8000)
- `DATABASE_URL` — Database URL
- `CORS_ORIGINS` — CORS origins (default: \*)
- `LOG_LEVEL` — Log level (default: INFO)

## 🐛 Troubleshooting

- DB connection failed: Check `DATABASE_URL`, DB server, network.
- Empty thresholds: Verify data in thresholds table; insert default levels if needed.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)

Last updated: February 2026
