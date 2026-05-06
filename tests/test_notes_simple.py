# tests/test_notes_simple.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app  # ← прямой импорт

@pytest.mark.asyncio
async def test_notes_route_exists():
    """Минимальный тест: проверяем, что роут вообще есть"""
    # Создаём клиент БЕЗ base_url
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Просто проверяем, что путь не 404 (даже если 401 — это уже успех)
        resp = await client.options("/api/v1/notes")  # OPTIONS обычно работает
        # 404 = роута нет, 401/405/200 = роут есть
        assert resp.status_code != 404, f"Роут не найден! Ответ: {resp.status_code}"