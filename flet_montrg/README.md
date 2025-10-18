# 📊 flet-montrg 마이크로서비스

IoT 센서를 통한 체감 온도 데이터 모니터링 및 알림 시스템을 위한 마이크로서비스 API

## 📋 개요

flet-montrg는 제조 현장의 IoT 센서 데이터를 실시간으로 모니터링하고 분석하는 마이크로서비스 기반 API 플랫폼입니다. FastAPI를 사용하여 구축되었으며, Kubernetes를 통해 배포 및 관리됩니다.

### 핵심 기능

-   🌡️ **실시간 온도 모니터링**: 센서 데이터 실시간 조회 및 임계치 검사
-   📍 **위치 기반 관리**: 공장/건물/층/구역별 센서 위치 정보
-   📊 **데이터 집계**: 시간별 최대/평균 온도 통계
-   ⚙️ **임계치 관리**: 센서 타입별 임계치 설정 및 CRUD
-   🚨 **알림 시스템**: 임계치 초과 시 실시간 알림 (구현 예정)

## 📁 프로젝트 구조

```text
flet_montrg/
├── services/                     # 마이크로서비스 소스 코드
│   ├── thresholds-service/       # 임계치 CRUD API
│   │   ├── app/                  # 애플리케이션 코드
│   │   ├── tests/                # 테스트
│   │   ├── Dockerfile            # Docker 이미지
│   │   ├── requirements.txt      # 의존성
│   │   └── README.md            # 서비스 문서
│   │
│   ├── location-service/         # 센서 위치 정보 API
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── realtime-service/         # 실시간 현황 API
│   │   ├── app/
│   │   │   ├── clients/         # 외부 서비스 클라이언트
│   │   │   ├── services/        # 비즈니스 로직
│   │   │   └── ...
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   └── aggregation-service/      # 기간 조회 API
│       ├── app/
│       ├── tests/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── README.md
│
└── k8s/                          # Kubernetes 배포 파일
    ├── thresholds/               # thresholds-service 배포
    │   ├── deployment.yaml       # Pod 배포 설정
    │   ├── service.yaml          # Service 설정
    │   ├── configmap.yaml        # 환경 설정
    │   ├── secret.yaml           # 비밀 정보
    │   ├── hpa.yaml              # 자동 스케일링
    │   ├── network-policy.yaml   # 네트워크 정책
    │   ├── kustomization.yaml    # Kustomize 설정
    │   └── deploy.sh             # 배포 스크립트
    │
    ├── location/                 # location-service 배포
    ├── realtime/                 # realtime-service 배포
    └── aggregation/              # aggregation-service 배포
```

## 🔌 서비스 포트 및 엔드포인트

| 서비스                    | 포트  | 주요 엔드포인트                        | 설명               | 상태         |
| ------------------------- | ----- | -------------------------------------- | ------------------ | ------------ |
| **thresholds-service**    | 30001 | `/api/v1/thresholds/`                  | 임계치 CRUD        | ✅ 구현 완료 |
| **location-service**      | 30002 | `/api/v1/locations/`                   | 위치 정보 조회     | ✅ 구현 완료 |
| **realtime-service**      | 30003 | `/api/v1/realtime/`                    | 실시간 센서 데이터 | ✅ 구현 완료 |
| **aggregation-service**   | 30004 | `/api/v1/aggregation/pcv_temperature/` | 데이터 집계        | ✅ 구현 완료 |
| **alert-service**         | 30005 | `/api/v1/alerts/`                      | 알림 발송          | 🚧 구현 예정 |
| **alert-history-service** | 30006 | `/api/v1/alert-history/`               | 알림 이력 조회     | 🚧 구현 예정 |

### API 문서

각 서비스는 Swagger UI를 통한 대화형 API 문서를 제공합니다:

-   Thresholds Service: http://localhost:30001/docs
-   Location Service: http://localhost:30002/docs
-   Realtime Service: http://localhost:30003/docs
-   Aggregation Service: http://localhost:30004/docs

## 🏗️ 마이크로서비스 아키텍처

```
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster (Kind)               │
│              Namespace: flet-montrg                  │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────────┐    ┌──────────────────┐      │
│  │  Thresholds      │    │   Location       │      │
│  │  Service         │    │   Service        │      │
│  │  (Port: 30001)   │    │   (Port: 30002)  │      │
│  └────────┬─────────┘    └────────┬─────────┘      │
│           │                       │                  │
│           │   HTTP API Calls      │                 │
│           └───────────┬───────────┘                 │
│                       ▼                              │
│           ┌──────────────────────┐                  │
│           │   Realtime Service   │                  │
│           │   (Port: 30003)      │                  │
│           │                      │                  │
│           │ - Location Client    │                  │
│           │ - Thresholds Client  │                  │
│           └──────────────────────┘                  │
│                                                       │
│           ┌──────────────────────┐                  │
│           │ Aggregation Service  │                  │
│           │   (Port: 30004)      │                  │
│           └──────────────────────┘                  │
│                                                       │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
                ┌───────────────┐
                │  PostgreSQL   │
                │  TimescaleDB  │
                └───────────────┘
```

### 서비스 간 통신

-   **Realtime Service** → Location Service: 센서 위치 정보 조회
-   **Realtime Service** → Thresholds Service: 임계치 정보 조회
-   모든 서비스 → PostgreSQL: 데이터 읽기/쓰기

## 🛠️ 기술 스택

### Backend

-   **프레임워크**: FastAPI (비동기 웹 프레임워크)
-   **언어**: Python 3.11+
-   **ORM**: SQLAlchemy 2.0 (Async)
-   **데이터 검증**: Pydantic v2
-   **HTTP 클라이언트**: httpx (비동기)

### 데이터베이스

-   **DBMS**: PostgreSQL 14+
-   **확장**: TimescaleDB (시계열 데이터 최적화)
-   **연결 풀**: asyncpg

### 컨테이너 & 오케스트레이션

-   **컨테이너**: Docker
-   **오케스트레이션**: Kubernetes (Kind)
-   **패키지 관리**: Kustomize
-   **Auto Scaling**: HPA (Horizontal Pod Autoscaler)

### 모니터링 & 로깅

-   **헬스체크**: Kubernetes Liveness/Readiness Probes
-   **로깅**: 구조화된 JSON 로깅
-   **메트릭**: Prometheus (통합 예정)
-   **대시보드**: Kubernetes Dashboard

## 🚀 빠른 시작

### 1. 사전 요구사항

```bash
# Docker 설치 확인
docker --version

# Kubernetes (Kind) 설치
brew install kind  # macOS
# 또는
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# kubectl 설치
brew install kubectl  # macOS
```

### 2. Kubernetes 클러스터 생성

```bash
# Kind 클러스터 생성
kind create cluster --name flet-cluster

# 클러스터 확인
kubectl cluster-info --context kind-flet-cluster

# 네임스페이스 생성
kubectl create namespace flet-montrg
```

### 3. Docker 이미지 빌드

```bash
# 각 서비스 이미지 빌드
cd services/thresholds-service
docker build -t flet-montrg/thresholds-service:latest .

cd ../location-service
docker build -t flet-montrg/location-service:latest .

cd ../realtime-service
docker build -t flet-montrg/realtime-service:latest .

cd ../aggregation-service
docker build -t flet-montrg/aggregation-service:latest .
```

### 4. Kind로 이미지 로드

```bash
# Kind 클러스터로 이미지 로드
kind load docker-image flet-montrg/thresholds-service:latest --name flet-cluster
kind load docker-image flet-montrg/location-service:latest --name flet-cluster
kind load docker-image flet-montrg/realtime-service:latest --name flet-cluster
kind load docker-image flet-montrg/aggregation-service:latest --name flet-cluster
```

### 5. 서비스 배포

```bash
# 전체 서비스 배포
kubectl apply -f k8s/thresholds/
kubectl apply -f k8s/location/
kubectl apply -f k8s/realtime/
kubectl apply -f k8s/aggregation/

# 또는 배포 스크립트 사용
cd k8s/thresholds && bash deploy.sh
cd ../location && bash deploy.sh
cd ../realtime && bash deploy.sh
cd ../aggregation && bash deploy.sh
```

### 6. 배포 확인

```bash
# Pod 상태 확인
kubectl get pods -n flet-montrg

# Service 확인
kubectl get svc -n flet-montrg

# 로그 확인
kubectl logs -f -n flet-montrg <pod-name>

# 상세 정보
kubectl describe pod -n flet-montrg <pod-name>
```

### 7. 서비스 접속

```bash
# 포트 포워딩
kubectl port-forward -n flet-montrg service/thresholds-service 30001:80
kubectl port-forward -n flet-montrg service/location-service 30002:80
kubectl port-forward -n flet-montrg service/realtime-service 30003:80
kubectl port-forward -n flet-montrg service/aggregation-service 30004:80

# API 테스트
curl http://localhost:30001/health
curl http://localhost:30002/api/v1/locations/
curl http://localhost:30003/api/v1/realtime/
curl http://localhost:30004/api/v1/aggregation/pcv_temperature/?start_date=20240922&end_date=20240922
```

## 🧭 개발 환경 실행

각 서비스를 로컬에서 개발 모드로 실행:

### Thresholds Service

```bash
cd services/thresholds-service

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp env.example .env
# .env 파일 편집

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API 문서
open http://localhost:8000/docs
```

### Location Service

```bash
cd services/location-service
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Realtime Service

```bash
cd services/realtime-service
pip install -r requirements.txt
cp env.example .env

# 외부 서비스 URL 설정
export LOCATION_SERVICE_URL=http://localhost:8001
export THRESHOLDS_SERVICE_URL=http://localhost:8000

uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### Aggregation Service

```bash
cd services/aggregation-service
pip install -r requirements.txt
cp env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
```

## 🧪 테스트

### 전체 테스트 실행

```bash
# 각 서비스 디렉토리에서
pytest

# 커버리지 포함
pytest --cov=app --cov-report=html

# 특정 테스트만
pytest tests/test_main.py -v

# 통합 테스트
pytest tests/integration/

# 단위 테스트
pytest tests/unit/
```

### 테스트 자동화

```bash
# location-service 테스트 스크립트
cd services/location-service
./test.sh

# aggregation-service 테스트
cd services/aggregation-service
pytest --cov=app
```

## 📊 모니터링

### Kubernetes Dashboard

```bash
# Dashboard 설치
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# 서비스 계정 생성
kubectl create serviceaccount dashboard-admin -n kubernetes-dashboard
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kubernetes-dashboard:dashboard-admin

# 토큰 생성
kubectl create token dashboard-admin -n kubernetes-dashboard

# 대시보드 접속
kubectl proxy
# http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

### 리소스 사용량

```bash
# Pod 리소스 사용량
kubectl top pods -n flet-montrg

# Node 리소스 사용량
kubectl top nodes

# HPA 상태
kubectl get hpa -n flet-montrg
```

### 로그 수집

```bash
# 실시간 로그
kubectl logs -f -n flet-montrg <pod-name>

# 이전 컨테이너 로그
kubectl logs -n flet-montrg <pod-name> --previous

# 여러 Pod 로그
kubectl logs -n flet-montrg -l app=realtime-service
```

## 🔧 환경 설정

### ConfigMap & Secret

각 서비스는 ConfigMap과 Secret을 통해 설정을 관리합니다:

**ConfigMap** (k8s/\*/configmap.yaml):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
    name: thresholds-service-config
    namespace: flet-montrg
data:
    APP_NAME: "Thresholds Service"
    ENVIRONMENT: "production"
    LOG_LEVEL: "INFO"
```

**Secret** (k8s/\*/secret.yaml):

```yaml
apiVersion: v1
kind: Secret
metadata:
    name: thresholds-service-secret
    namespace: flet-montrg
type: Opaque
data:
    DATABASE_URL: <base64-encoded-url>
```

### Secret 생성

```bash
# Base64 인코딩
echo -n "postgresql://user:pass@host:5432/db" | base64

# Secret 생성
kubectl create secret generic thresholds-service-secret \
  --from-literal=DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -n flet-montrg
```

## 🔄 HPA (Auto Scaling)

각 서비스는 CPU/메모리 기반 자동 스케일링을 지원합니다:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
    name: thresholds-service-hpa
    namespace: flet-montrg
spec:
    scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: thresholds-service
    minReplicas: 2
    maxReplicas: 10
    metrics:
        - type: Resource
          resource:
              name: cpu
              target:
                  type: Utilization
                  averageUtilization: 70
        - type: Resource
          resource:
              name: memory
              target:
                  type: Utilization
                  averageUtilization: 80
```

## 🔒 보안

### Network Policy

서비스 간 통신을 제한하는 네트워크 정책:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
    name: realtime-service-netpol
    namespace: flet-montrg
spec:
    podSelector:
        matchLabels:
            app: realtime-service
    policyTypes:
        - Ingress
        - Egress
    ingress:
        - from:
              - podSelector: {}
          ports:
              - protocol: TCP
                port: 8000
    egress:
        - to:
              - podSelector:
                    matchLabels:
                        app: location-service
              - podSelector:
                    matchLabels:
                        app: thresholds-service
          ports:
              - protocol: TCP
                port: 80
```

## 📚 서비스별 상세 문서

각 서비스의 상세 문서는 아래 링크를 참조하세요:

-   [Thresholds Service 문서](./services/thresholds-service/README.md)
-   [Location Service 문서](./services/location-service/README.md)
-   [Realtime Service 문서](./services/realtime-service/README.md)
-   [Aggregation Service 문서](./services/aggregation-service/README.md)

## 🐛 트러블슈팅

### Pod가 시작되지 않을 때

```bash
# Pod 상태 확인
kubectl describe pod -n flet-montrg <pod-name>

# 이벤트 확인
kubectl get events -n flet-montrg --sort-by='.lastTimestamp'

# 로그 확인
kubectl logs -n flet-montrg <pod-name>
```

### 이미지 Pull 실패

```bash
# Kind로 이미지 다시 로드
kind load docker-image flet-montrg/<service-name>:latest --name flet-cluster

# imagePullPolicy 확인 (Always → IfNotPresent)
kubectl edit deployment -n flet-montrg <deployment-name>
```

### 서비스 간 통신 실패

```bash
# Service DNS 확인
kubectl run -it --rm debug --image=alpine --restart=Never -- sh
/ # nslookup location-service.flet-montrg.svc.cluster.local

# 네트워크 정책 확인
kubectl get networkpolicies -n flet-montrg
```

## 🌟 향후 계획

-   [ ] Alert Service 구현
-   [ ] Alert History Service 구현
-   [ ] 중앙 집중식 로깅 (ELK Stack)
-   [ ] 분산 추적 (Jaeger)
-   [ ] Prometheus & Grafana 연동
-   [ ] CI/CD 파이프라인 (GitHub Actions)
-   [ ] Ingress Controller 설정
-   [ ] TLS/HTTPS 지원
-   [ ] Rate Limiting
-   [ ] API Gateway (Kong/Ambassador)

---

**Last Updated**: October 2025
