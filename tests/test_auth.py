# tests/test_auth.py
import pytest
from httpx import AsyncClient

TEST_USER = {"email": "test@example.com", "password": "secure123"}

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # 1. Регистрация
    resp = await client.post("/api/v1/auth/register", json=TEST_USER)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == TEST_USER["email"]
    assert "hashed_password" not in data  # 🔒 пароль не возвращается
    
    # 2. Логин
    resp = await client.post("/api/v1/auth/token", data={
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_protected_route_requires_auth(client: AsyncClient):
    # Попытка доступа без токена
    resp = await client.get("/api/v1/notes/")
    assert resp.status_code == 401