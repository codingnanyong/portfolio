# 🗺️ Location Service

Sensor location management API

## 📁 Project Structure

```text
location-service/
├── app/
│   ├── main.py                 # FastAPI entry
│   ├── api/v1/
│   │   ├── api.py              # API v1 router
│   │   └── endpoints/locations.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── models/
│   │   ├── database_models.py
│   │   └── schemas.py
│   └── services/
│       └── location_service.py
├── tests/
│   ├── conftest.py
│   ├── integration/test_location_api.py
│   └── unit/test_location_service.py
├── requirements.txt
├── requirements-test.txt
├── env.example
├── test.sh
├── Dockerfile
└── README.md
```

## ⚙️ Install & Run

```bash
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# or: docker build -t location-service . && docker run -p 8000:8000 --env-file .env location-service
```

## 🔌 API Endpoints

### Location queries

#### List all locations

```http
GET /api/v1/locations/
```

**Example response:**

```json
[
  { "loc_id": "LOC001", "factory": "Factory-A", "building": "Bld-1", "floor": 1, "area": "Area-1" },
  { "loc_id": "LOC002", "factory": "Factory-A", "building": "Bld-2", "floor": 1, "area": "Area-2" }
]
```

#### Get by location ID

```http
GET /api/v1/locations/{loc_id}
```

- **Parameters**: `loc_id` (string, required), e.g. `"LOC001"`

**Example response:**

```json
{
  "loc_id": "LOC001",
  "factory": "Factory-A",
  "building": "Bld-1",
  "floor": 1,
  "area": "Area-1"
}
```

#### By factory

```http
GET /api/v1/locations/factory/{factory}
```

- **Parameters**: `factory` (string, required), e.g. `"Factory-A"`

#### By building

```http
GET /api/v1/locations/building/{building}
```

- **Parameters**: `building` (string, required), e.g. `"Bld-1"`

#### By floor

```http
GET /api/v1/locations/floor/{floor}
```

- **Parameters**: `floor` (integer, required), e.g. `1`

#### Multi-filter

```http
GET /api/v1/locations/filter?factory={factory}&building={building}&floor={floor}
```

- **Query params** (all optional): `factory`, `building`, `floor`

### Basic endpoints

- `GET /` — Service info
- `GET /health` — Health check
- `GET /ready` — Readiness (includes DB)
- `GET /docs` — Swagger UI
- `GET /redoc` — ReDoc

## 📊 Data Model

### LocationInfo

- `loc_id` (string): Location ID (PK)
- `factory` (string): Factory name
- `building` (string): Building name
- `floor` (integer): Floor
- `area` (string): Area name

## 🔧 Environment Variables

| Variable | Description | Default |
| ------------ | ----------------------------- | ---------------- |
| APP_NAME | Application name | Location Service |
| APP_VERSION | Version | 1.0.0 |
| DEBUG | Debug mode | false |
| ENVIRONMENT | development/production | development |
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 8000 |
| DATABASE_URL | Database URL | - |
| CORS_ORIGINS | CORS origins | * |
| LOG_LEVEL | Log level | INFO |

### Example .env

```bash
APP_NAME=Location Service
APP_VERSION=1.0.0
DEBUG=false
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<db>
CORS_ORIGINS=["*"]
LOG_LEVEL=INFO
```

## 🧪 Tests

```bash
./test.sh
# or
pytest
pytest --cov=app --cov-report=html
pytest tests/unit/test_location_service.py
pytest tests/integration/test_location_api.py
pytest -v
pytest -x
```

### Test layout

- **Unit** (`tests/unit/`): Business logic, e.g. `test_location_service.py`
- **Integration** (`tests/integration/`): API endpoints, e.g. `test_location_api.py`

## 📈 Monitoring

- Structured JSON logging
- Liveness: `GET /health`
- Readiness: `GET /ready` (DB check)

Kubernetes probes example:

```yaml
livenessProbe:
  httpGet: { path: /health, port: 8000 }
  initialDelaySeconds: 10
  periodSeconds: 30
readinessProbe:
  httpGet: { path: /ready, port: 8000 }
  initialDelaySeconds: 5
  periodSeconds: 10
```

## 🔗 Integration

**Realtime Service** calls this service for sensor locations. **Aggregation Service** can enrich results with location info.

## 🚀 Deployment (Kubernetes)

```bash
docker build -t location-service:latest .
kind load docker-image location-service:latest --name <cluster-name>
kubectl apply -f k8s/
kubectl get pods -n <namespace> -l app=location-service

# Access
kubectl port-forward -n <namespace> svc/location-service 30002:80
open http://localhost:30002/docs
```

## 💡 Adding a new filter

1. Update Pydantic schema (`models/schemas.py`), e.g. add `area` to `LocationFilter`.
2. Add service logic in `services/location_service.py`.
3. Add endpoint in `api/v1/endpoints/locations.py`.
4. Add tests under `tests/`.

## 🐛 Troubleshooting

**DB connection failed**: Check `DATABASE_URL`, DB server, network. Test with `psql` or `docker logs location-service`.

**Empty locations**: Verify data in DB, e.g. `SELECT * FROM <schema>.<table> LIMIT 10`; insert sample rows if needed.

## 📚 References

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)

## ✨ Features

- Location CRUD and filters
- RESTful API, Swagger/ReDoc
- Structured logging, health/ready endpoints
- Async DB, unit/integration tests
- Docker and Kubernetes–ready

---

**Last Updated**: February 2026
