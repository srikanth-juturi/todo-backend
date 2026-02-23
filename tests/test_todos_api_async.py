import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient) -> None:
    response = await async_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_and_list_todos_contract(async_client: AsyncClient) -> None:
    create_response = await async_client.post("/api/v1/todos", json={"title": "  Async task  "})

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Async task"
    assert created["category"] == "general"
    assert created["is_completed"] is False

    list_response = await async_client.get("/api/v1/todos")

    assert list_response.status_code == 200
    payload = list_response.json()
    assert len(payload) == 1
    assert payload[0]["id"] == created["id"]
    assert payload[0]["category"] == "general"


@pytest.mark.asyncio
async def test_update_missing_todo_returns_error_contract(async_client: AsyncClient) -> None:
    response = await async_client.patch("/api/v1/todos/9999", json={"title": "missing"})

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "TODO_NOT_FOUND"
    assert payload["error"]["message"] == "Todo not found"
    assert payload["error"]["details"] == {"todo_id": 9999}
    assert payload["error"]["trace_id"]


@pytest.mark.asyncio
async def test_patch_requires_payload_fields(async_client: AsyncClient) -> None:
    created = (await async_client.post("/api/v1/todos", json={"title": "Patch me"})).json()

    response = await async_client.patch(f"/api/v1/todos/{created['id']}", json={})

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "REQUEST_VALIDATION_ERROR"
    assert payload["error"]["trace_id"]
