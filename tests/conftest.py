import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from db.base import Base
from core.dependencies import get_db

# 🔑 Тестовая БД (изолированная SQLite в памяти)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def test_db(test_engine): # type: ignore
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False) # type: ignore
    async with async_session() as session: # type: ignore
        yield session
        await session.rollback() # type: ignore

@pytest_asyncio.fixture(scope="function")
async def client(test_db, test_engine): # type: ignore
    # 🔑 Переопределяем зависимость get_db для тестов
    def override_get_db(): # type: ignore
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    # 🔑 КЛЮЧЕВОЙ ФИКС: base_url должен быть с схемой http:// и host testserver
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, 
        base_url="http://testserver"  # ← именно testserver, не test!
    ) as c:
        yield c
    
    app.dependency_overrides.clear()