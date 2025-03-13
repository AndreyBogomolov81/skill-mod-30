from typing import Type, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./recipes.db"

engine = create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
session = async_session()
Base = declarative_base()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession
    async with async_session() as session:
        yield session