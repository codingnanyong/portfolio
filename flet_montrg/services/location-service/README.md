# 🗺️ Location Service

센서 위치 정보 관리 API 서비스

## 📁 프로젝트 구조

```text
location-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션 진입점
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py          # API v1 라우터
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── locations.py # 위치 API 엔드포인트
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # 설정 관리
│   │   ├── database.py         # 데이터베이스 연결
│   │   ├── exceptions.py       # 커스텀 예외
│   │   └── logging.py          # 로깅 설정
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database_models.py  # SQLAlchemy 모델
│   │   └── schemas.py          # Pydantic 스키마
│   └── services/
│       ├── __init__.py
│       └── location_service.py # 비즈니스 로직
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # pytest 설정
│   ├── integration/
│   │   └── test_location_api.py  # 통합 테스트
│   └── unit/
│       └── test_location_service.py # 단위 테스트
├── requirements.txt            # Python 의존성
├── requirements-test.txt       # 테스트 의존성
├── env.example                 # 환경 변수 예시
├── test.sh                     # 테스트 실행 스크립트
├── Dockerfile                  # Docker 설정
└── README.md                   # 프로젝트 문서
```

## ⚙️ 설치 및 실행

### 1. 📦 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 🔧 환경 변수 설정

```bash
cp env.example .env
# .env 파일을 편집하여 필요한 설정을 변경
```

### 3. ▶️ 애플리케이션 실행

```bash
# 개발 모드
python -m app.main

# 또는 uvicorn 직접 사용
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 🐳 Docker 실행

```bash
docker build -t location-service .
docker run -p 8000:8000 --env-file .env location-service
```

## 🔌 API 엔드포인트

### 위치 정보 조회

#### 전체 위치 조회

```http
GET /api/v1/locations/
```

**응답 예시**:

```json
[
    {
        "loc_id": "A031",
        "factory": "SinPyeong",
        "building": "F-2001",
        "floor": 1,
        "area": "조립2"
    },
    {
        "loc_id": "A011",
        "factory": "SinPyeong",
        "building": "MX-1",
        "floor": 1,
        "area": "자재 보관실"
    }
]
```

#### 특정 위치 조회

```http
GET /api/v1/locations/{loc_id}
```

**파라미터**:

-   `loc_id` (string, required): 위치 ID (예: "A031")

**응답 예시**:

```json
{
    "loc_id": "A031",
    "factory": "SinPyeong",
    "building": "F-2001",
    "floor": 1,
    "area": "조립2"
}
```

#### 공장별 위치 조회

```http
GET /api/v1/locations/factory/{factory}
```

**파라미터**:

-   `factory` (string, required): 공장명 (예: "SinPyeong")

**응답 예시**:

```json
[
    {
        "loc_id": "A031",
        "factory": "SinPyeong",
        "building": "F-2001",
        "floor": 1,
        "area": "조립2"
    },
    {
        "loc_id": "A032",
        "factory": "SinPyeong",
        "building": "F-2001",
        "floor": 2,
        "area": "조립3"
    }
]
```

#### 건물별 위치 조회

```http
GET /api/v1/locations/building/{building}
```

**파라미터**:

-   `building` (string, required): 건물명 (예: "F-2001")

#### 층별 위치 조회

```http
GET /api/v1/locations/floor/{floor}
```

**파라미터**:

-   `floor` (integer, required): 층수 (예: 1)

#### 다중 필터 조회

```http
GET /api/v1/locations/filter?factory={factory}&building={building}&floor={floor}
```

**쿼리 파라미터** (모두 선택사항):

-   `factory` (string): 공장명
-   `building` (string): 건물명
-   `floor` (integer): 층수

**응답 예시**:

```json
[
    {
        "loc_id": "A031",
        "factory": "SinPyeong",
        "building": "F-2001",
        "floor": 1,
        "area": "조립2"
    }
]
```

### 기본 엔드포인트

#### 서비스 정보

```http
GET /
```

**응답**:

```json
{
    "service": "Location Service",
    "version": "1.0.0",
    "status": "running"
}
```

#### 헬스체크

```http
GET /health
```

**응답**:

```json
{
    "status": "healthy"
}
```

#### 레디니스 체크

```http
GET /ready
```

**응답**:

```json
{
    "status": "ready",
    "database": "connected"
}
```

#### API 문서

```http
GET /docs      # Swagger UI
GET /redoc     # ReDoc
```

## 📊 데이터 모델

### LocationInfo

센서 위치 정보를 나타내는 데이터 모델

**필드**:

-   `loc_id` (string): 위치 ID (Primary Key)
-   `factory` (string): 공장명
-   `building` (string): 건물명
-   `floor` (integer): 층수
-   `area` (string): 구역명

**예시**:

```json
{
    "loc_id": "A031",
    "factory": "SinPyeong",
    "building": "F-2001",
    "floor": 1,
    "area": "조립2"
}
```

## 🔧 환경 변수

| 변수명       | 설명                          | 기본값           |
| ------------ | ----------------------------- | ---------------- |
| APP_NAME     | 애플리케이션 이름             | Location Service |
| APP_VERSION  | 애플리케이션 버전             | 1.0.0            |
| DEBUG        | 디버그 모드                   | false            |
| ENVIRONMENT  | 환경 (development/production) | development      |
| HOST         | 서버 호스트                   | 0.0.0.0          |
| PORT         | 서버 포트                     | 8000             |
| DATABASE_URL | 데이터베이스 연결 URL         | -                |
| CORS_ORIGINS | CORS 허용 오리진              | \*               |
| LOG_LEVEL    | 로그 레벨                     | INFO             |

### 환경 변수 예시 (.env)

```bash
# Application
APP_NAME=Location Service
APP_VERSION=1.0.0
DEBUG=false
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/monitoring

# CORS
CORS_ORIGINS=["*"]

# Logging
LOG_LEVEL=INFO
```

## 🧪 테스트

### 테스트 실행

```bash
# 모든 테스트 실행
./test.sh

# 또는 pytest 직접 실행
pytest

# 커버리지 포함
pytest --cov=app --cov-report=html

# 특정 테스트 파일
pytest tests/unit/test_location_service.py
pytest tests/integration/test_location_api.py

# 상세 출력
pytest -v

# 빠른 실패 (첫 실패 시 중단)
pytest -x
```

### 테스트 구조

#### 단위 테스트 (Unit Tests)

-   **위치**: `tests/unit/`
-   **목적**: 비즈니스 로직 검증
-   **예시**: `test_location_service.py`

```python
def test_get_location_by_id():
    # LocationService의 get_location_by_id 메서드 테스트
    pass

def test_get_locations_by_factory():
    # 공장별 위치 조회 로직 테스트
    pass
```

#### 통합 테스트 (Integration Tests)

-   **위치**: `tests/integration/`
-   **목적**: API 엔드포인트 검증
-   **예시**: `test_location_api.py`

```python
def test_get_all_locations_endpoint():
    # GET /api/v1/locations/ 엔드포인트 테스트
    pass

def test_get_location_by_id_endpoint():
    # GET /api/v1/locations/{loc_id} 엔드포인트 테스트
    pass
```

## 📈 모니터링

### 로깅

서비스는 구조화된 JSON 로깅을 사용합니다:

```json
{
    "timestamp": "2024-10-18T10:30:45.123Z",
    "level": "INFO",
    "service": "location-service",
    "message": "Location retrieved successfully",
    "loc_id": "A031",
    "request_id": "abc-123-def"
}
```

### 헬스체크 엔드포인트

Kubernetes 배포 시 사용되는 헬스체크:

**Liveness Probe**:

```yaml
livenessProbe:
    httpGet:
        path: /health
        port: 8000
    initialDelaySeconds: 10
    periodSeconds: 30
```

**Readiness Probe**:

```yaml
readinessProbe:
    httpGet:
        path: /ready
        port: 8000
    initialDelaySeconds: 5
    periodSeconds: 10
```

## 🔗 다른 서비스와의 연동

### Realtime Service

Realtime Service는 Location Service를 호출하여 센서 위치 정보를 가져옵니다:

```python
# realtime-service의 location_client.py
async def get_locations():
    response = await httpx.get(
        f"{LOCATION_SERVICE_URL}/api/v1/locations/"
    )
    return response.json()
```

### Aggregation Service

Aggregation Service는 집계 데이터에 위치 정보를 포함시킵니다:

```python
# aggregation-service의 코드 예시
location_info = await location_client.get_location(loc_id)
result = {
    "location": location_info,
    "metrics": aggregated_metrics
}
```

## 🚀 배포

### Kubernetes 배포

```bash
# 이미지 빌드
docker build -t flet-montrg/location-service:latest .

# Kind로 이미지 로드
kind load docker-image flet-montrg/location-service:latest --name flet-cluster

# Kubernetes 배포
kubectl apply -f ../../k8s/location/

# 배포 확인
kubectl get pods -n flet-montrg -l app=location-service
```

### 서비스 접속

```bash
# 포트 포워딩
kubectl port-forward -n flet-montrg service/location-service 30002:80

# API 문서 접속
open http://localhost:30002/docs
```

## 💡 개발 가이드

### 새로운 필터 추가

1. **Pydantic 스키마 업데이트** (`models/schemas.py`):

```python
class LocationFilter(BaseModel):
    factory: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[int] = None
    area: Optional[str] = None  # 새로운 필터
```

2. **서비스 로직 추가** (`services/location_service.py`):

```python
async def get_locations_by_filter(self, filters: LocationFilter):
    query = select(Location)
    if filters.area:
        query = query.where(Location.area == filters.area)
    # ...
```

3. **엔드포인트 추가** (`api/v1/endpoints/locations.py`):

```python
@router.get("/area/{area}")
async def get_locations_by_area(area: str):
    return await location_service.get_locations_by_area(area)
```

4. **테스트 추가** (`tests/`):

```python
def test_get_locations_by_area():
    # 테스트 코드
    pass
```

## 🐛 트러블슈팅

### 데이터베이스 연결 실패

**증상**: `ConnectionError: could not connect to server`

**해결**:

1. DATABASE_URL 환경 변수 확인
2. 데이터베이스 서버 상태 확인
3. 네트워크 연결 확인

```bash
# 데이터베이스 연결 테스트
psql -h localhost -U user -d monitoring

# Docker 컨테이너 로그 확인
docker logs location-service
```

### 위치 정보 없음

**증상**: `GET /api/v1/locations/` 응답이 빈 배열 `[]`

**해결**:

1. 데이터베이스에 위치 데이터 확인

```sql
SELECT * FROM flet_montrg.location LIMIT 10;
```

2. 데이터 삽입

```sql
INSERT INTO flet_montrg.location (loc_id, factory, building, floor, area)
VALUES ('A031', 'SinPyeong', 'F-2001', 1, '조립2');
```

## 📚 참고 자료

-   [FastAPI Documentation](https://fastapi.tiangolo.com/)
-   [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
-   [Pydantic Documentation](https://docs.pydantic.dev/)
-   [Pytest Documentation](https://docs.pytest.org/)

## ✨ 주요 기능

-   ✅ 위치 정보 CRUD 작업
-   ✅ 다양한 필터 조건 지원
-   ✅ RESTful API 설계
-   ✅ 자동 API 문서 생성 (Swagger/ReDoc)
-   ✅ 구조화된 로깅
-   ✅ 헬스체크 엔드포인트
-   ✅ 비동기 데이터베이스 처리
-   ✅ 단위/통합 테스트
-   ✅ Docker 지원
-   ✅ Kubernetes 배포 준비

---

**Last Updated**: October 2025
