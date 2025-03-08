from typing import AsyncGenerator, Any, Generator

import pytest_asyncio
from fakeredis.aioredis import FakeRedis
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.domain.models import Base, User

from app.infrastructure.db_connection import get_async_session
from app.infrastructure.redis_cache import redis_client
from app.main import app

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = async_sessionmaker(
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest_asyncio.fixture(autouse=True)
async def init_db() -> AsyncGenerator[None, Any]:
    """Инициализирует и очищает базу данных для каждого теста."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_async_session() -> Generator[AsyncSession, Any, None]:
    """Переопределяет зависимость получения сессии базы данных для тестов."""
    async with TestingSessionLocal() as session:
        yield session


async def override_get_aioredis() -> Generator[FakeRedis, Any, None]:
    """Переопределяет зависимость получения клиента Redis для тестов с использованием FakeRedis."""
    redis = FakeRedis()
    yield redis
    await redis.flushall()


app.dependency_overrides[get_async_session] = override_get_async_session
app.dependency_overrides[redis_client] = override_get_aioredis


@pytest_asyncio.fixture
async def get_test_session() -> Generator[AsyncSession, Any, None]:
    """Возвращает сессию базы данных для тестов."""
    async for session in override_get_async_session():
        yield session


@pytest_asyncio.fixture
async def get_test_redis() -> Generator[FakeRedis, Any, None]:
    """Возвращает клиент Redis для тестов с FakeRedis."""
    async for aioredis in override_get_aioredis():
        yield aioredis


@pytest_asyncio.fixture
async def async_client() -> Generator[AsyncClient, Any, None]:
    """Создает клиент HTTP для тестирования API с использованием ASGI."""
    async with AsyncClient(
        base_url="http://test",
        transport=ASGITransport(app=app),
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def test_user(async_client: AsyncClient, get_test_session) -> User:
    """Создает тестового пользователя и назначает его суперпользователем."""
    client_data = {
        "email": "test_user@gmail.com",
        "password": "123",
        "is_superuser": False,
        "is_active": True,
    }
    response = await async_client.post("/auth/register", json=client_data)
    print(response.json())
    assert response.status_code == 201
    async with get_test_session as session:
        result: Result = await session.execute(
            select(User).filter_by(id=response.json()["id"])
        )
        user: User = result.scalars().first()
        user.is_superuser = True
        await session.commit()
    return user


@pytest_asyncio.fixture
async def login_user(async_client: AsyncClient, test_user):
    """Логинит тестового пользователя и возвращает клиент с обновленными заголовками для авторизации."""
    client_data = {
        "username": test_user.email,
        "password": "123",
        "grant_type": "password",
    }
    response = await async_client.post("/auth/login", data=client_data)

    assert response.status_code == 200
    token = response.json()["access_token"]
    async_client.headers.update({"Authorization": f"Bearer {token}"})

    return async_client, test_user
