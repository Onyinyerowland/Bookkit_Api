from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from typing import AsyncGenerator
import os


# Base class for models
Base = declarative_base()

# Async engine
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
DATABASE_URL = os.getenv("DATABASE_URL")
SessionLocal = sessionmaker(bind=engine)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
# Async session maker
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# FastAPI dependency
async def get_db_session() ->  AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
# Synchronous engine and session for Alembic
from sqlalchemy import create_engine
sync_engine = create_engine(settings.DATABASE_URL.replace("asyncpg", "psycopg2"), echo=False, future=True)
SyncSessionLocal = sessionmaker(bind=sync_engine)
# Synchronous session maker
sync_session_maker = sessionmaker(bind=sync_engine)
def get_sync_db_session():
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()
# Alembic will use sync_engine and SyncSessionLocal for migrations
def init_db():
    import app.models  # Import all models to register them with Base
    Base.metadata.create_all(bind=sync_engine)
if __name__ == "__main__":
    init_db()
# To run this file directly for testing
    import asyncio
    async def test_connection():
        async with AsyncSessionLocal() as session:
            result = await session.execute("SELECT 1")
            print(result.scalar())
    asyncio.run(test_connection())
    print("Database initialized and connection test successful.")
