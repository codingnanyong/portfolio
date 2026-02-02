# 🚀 Thresholds Service

Perceived-temperature threshold management API

## 📁 Project Structure

```text
thresholds-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py          # API v1 router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── thresholds.py  # Threshold API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database connection
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── logging.py          # Logging config
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database_models.py  # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       └── threshold_service.py  # Business logic
├── tests/
│   ├── __init__.py
│   └── conftest.py             # pytest config
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variable example
├── Dockerfile                  # Docker config
└── README.md                   # This file
```

## ⚙️ Install & Run

### 1. 📦 Dependencies

```bash
pip install -r requirements.txt
```

### 2. 🔧 Environment

```bash
cp env.example .env
# Edit .env as needed
```

### 3. ▶️ Run

```bash
# Development
python -m app.main

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 🐳 Docker

```bash
docker build -t thresholds-service .
docker run -p 8000:8000 thresholds-service
```

## 📘 API Docs

- Swagger UI: [http://localhost:8000/docs]
- ReDoc: [http://localhost:8000/redoc]

## 🧪 Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_thresholds.py
```

## ✨ Features

- Threshold CRUD
- Query by type
- Validation, logging, exception handling
- Health-check endpoint

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| APP_NAME | Application name | Thresholds Service |
| APP_VERSION | Application version | 1.0.0 |
| DEBUG | Debug mode | false |
| ENVIRONMENT | development/production | development |
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 8000 |
| DATABASE_URL | Database connection URL | - |
| CORS_ORIGINS | CORS origins | * |
| LOG_LEVEL | Log level | INFO |
