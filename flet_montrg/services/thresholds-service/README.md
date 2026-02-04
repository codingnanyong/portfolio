# 🚀 Thresholds Service

Perceived-temperature threshold management API

## 📁 Project Structure

```text
thresholds-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry
│   ├── api/
│   │   └── v1/
│   │       ├── api.py          # API v1 router
│   │       └── endpoints/
│   │           └── thresholds.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── models/
│   │   ├── database_models.py
│   │   └── schemas.py
│   └── services/
│       └── threshold_service.py
├── tests/
│   └── conftest.py
├── requirements.txt
├── env.example
├── Dockerfile
└── README.md
```

## ⚙️ Install & Run

### 1. Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment

```bash
cp env.example .env
# Edit .env as needed
```

### 3. Run

```bash
python -m app.main
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Docker

```bash
docker build -t thresholds-service .
docker run -p 8000:8000 thresholds-service
```

## 📘 API Docs

- Swagger UI: [http://localhost:8000/docs]
- ReDoc: [http://localhost:8000/redoc]

## 🧪 Tests

```bash
pytest
pytest --cov=app
pytest tests/test_thresholds.py
```

## ✨ Features

- Threshold CRUD
- Query by type
- Validation, logging, exception handling
- Health-check endpoint

## 🔧 Environment Variables

| Variable | Description | Default |
| ------------ | ----------------------------- | ------------------ |
| APP_NAME | Application name | Thresholds Service |
| APP_VERSION | Version | 1.0.0 |
| DEBUG | Debug mode | false |
| ENVIRONMENT | development/production | development |
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 8000 |
| DATABASE_URL | DB connection URL | - |
| CORS_ORIGINS | CORS origins | * |
| LOG_LEVEL | Log level | INFO |

---

**Last Updated**: February 2026
