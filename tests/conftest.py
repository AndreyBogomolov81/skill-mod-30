from typing import AsyncGenerator, Any

import pytest
import uuid

from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from src.fastapp import app
from src.database import Base, get_session

# SQLite database URL for testing
SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./recipes.db"

engine = create_async_engine(SQLITE_DATABASE_URL, echo=False)
async_session = sessionmaker(engine,
    expire_on_commit=False,
    class_=AsyncSession)


async def get_session_override() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = get_session_override


@pytest.fixture(scope="module")
async def db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


@pytest.fixture
async def client(db) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as client:
        yield client