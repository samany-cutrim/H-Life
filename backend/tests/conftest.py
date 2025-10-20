import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import get_session
from app.core.deps import get_current_user
from app.main import app
from app.models import Base, User


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture()
async def session_factory(test_engine):
    return async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture()
async def seed_user(session_factory) -> User:
    async with session_factory() as session:
        user = User(email="user@example.com", hashed_password="hashed")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest.fixture(autouse=True)
async def override_dependencies(session_factory, seed_user, monkeypatch):
    async def _get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    async def _get_user() -> User:
        return seed_user

    app.dependency_overrides[get_session] = _get_session
    app.dependency_overrides[get_current_user] = _get_user

    from app.services import storage as storage_module

    def fake_init(self) -> None:
        self.bucket = "test"
        self.client = None

    def fake_presign(self, *, key: str, expires_in: int = 600) -> dict[str, Any]:
        return {"url": f"https://example.com/upload/{key}", "fields": {"key": key}}

    def fake_url(self, key: str) -> str:
        return f"https://cdn.example.com/{key}"

    monkeypatch.setattr(storage_module.StorageService, "__init__", fake_init)
    monkeypatch.setattr(storage_module.StorageService, "generate_presigned_upload", fake_presign)
    monkeypatch.setattr(storage_module.StorageService, "build_object_url", fake_url)

    yield

    app.dependency_overrides.clear()


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
