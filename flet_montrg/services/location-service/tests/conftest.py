"""
Pytest configuration and fixtures
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.main import app
from app.core.database import Base, get_db
from app.models.database_models import Location, Sensor

# 테스트용 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def override_get_db():
    """테스트용 데이터베이스 세션"""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# 의존성 오버라이드
app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """각 테스트 전에 실행되는 설정"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

pytestmark = pytest.mark.asyncio
