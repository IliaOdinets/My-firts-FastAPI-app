# tests/test_notes.py
import pytest
from httpx import AsyncClient

# 🔑 Слеш в конце обязателен, чтобы httpx не получал 307 редиректы
BASE_URL = "/api/v1/notes/"


@pytest.mark.asyncio
async def test_crud_requires_auth(client: AsyncClient):
    """Проверяет, что CRUD недоступен без токена"""
    resp = await client.post(BASE_URL, json={"title": "Тест", "content": "Контент"})
    assert resp.status_code == 401

    resp = await client.get(BASE_URL)
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_crud_note_with_auth(client: AsyncClient):
    """Полный цикл CRUD с авторизацией"""
    # 1️⃣ Регистрация и получение токена
    await client.post("/api/v1/auth/register", json={
        "email": "notes-test@example.com",
        "password": "secure123"
    })

    login_resp = await client.post("/api/v1/auth/token", data={
        "username": "notes-test@example.com",
        "password": "secure123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2️⃣ CREATE
    create_resp = await client.post(BASE_URL, json={
        "title": "моя тестовая заметка",
        "content": "Проверка полного цикла CRUD"
    }, headers=headers)

    assert create_resp.status_code == 201
    note = create_resp.json()
    note_id = note["id"]
    
    # 🔍 ОТЛАДКА: проверяем, что ID сгенерировался и имеет тип str
    print(f"\n🔍 Создан ID: {note_id} (тип: {type(note_id)})")
    assert isinstance(note_id, str) and len(note_id) > 0
    
    # Валидатор .title() в схеме делает "Моя Тестовая Заметка"
    assert note["title"] == "Моя Тестовая Заметка"

    # 3️⃣ READ
    get_url = f"{BASE_URL}{note_id}"
    print(f"🔍 GET запрос по пути: {get_url}")
    
    get_resp = await client.get(get_url, headers=headers)
    print(f"🔍 GET ответ: {get_resp.status_code} | {get_resp.json()}")
    
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == note_id

    # 4️⃣ UPDATE
    update_resp = await client.put(f"{BASE_URL}{note_id}", json={
        "title": "Обновлённый Заголовок",
        "content": "Обновлённый текст"
    }, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Обновлённый Заголовок"

    # 5️⃣ DELETE
    delete_resp = await client.delete(f"{BASE_URL}{note_id}", headers=headers)
    assert delete_resp.status_code == 204

    # 6️⃣ VERIFY DELETION
    verify_resp = await client.get(f"{BASE_URL}{note_id}", headers=headers)
    assert verify_resp.status_code == 404