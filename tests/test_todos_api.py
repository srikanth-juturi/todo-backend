from fastapi.testclient import TestClient


def test_create_todo_returns_201(client: TestClient) -> None:
    response = client.post("/api/v1/todos", json={"title": "Buy milk"})

    assert response.status_code == 201
    payload = response.json()
    assert payload["id"] > 0
    assert payload["title"] == "Buy milk"
    assert payload["category"] == "general"
    assert payload["is_completed"] is False
    assert payload["created_at"]
    assert payload["updated_at"]


def test_create_todo_accepts_category(client: TestClient) -> None:
    response = client.post("/api/v1/todos", json={"title": "Buy milk", "category": "home"})

    assert response.status_code == 201
    payload = response.json()
    assert payload["category"] == "home"


def test_create_todo_rejects_whitespace_title(client: TestClient) -> None:
    response = client.post("/api/v1/todos", json={"title": "   "})

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "REQUEST_VALIDATION_ERROR"
    assert payload["error"]["trace_id"]


def test_list_todos_returns_newest_first(client: TestClient) -> None:
    client.post("/api/v1/todos", json={"title": "First"})
    client.post("/api/v1/todos", json={"title": "Second"})

    response = client.get("/api/v1/todos")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert payload[0]["title"] == "Second"
    assert payload[1]["title"] == "First"


def test_patch_todo_partial_update(client: TestClient) -> None:
    created = client.post("/api/v1/todos", json={"title": "Write tests"}).json()

    response = client.patch(
        f"/api/v1/todos/{created['id']}",
        json={"is_completed": True},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "Write tests"
    assert payload["category"] == "general"
    assert payload["is_completed"] is True


def test_patch_todo_updates_category(client: TestClient) -> None:
    created = client.post("/api/v1/todos", json={"title": "Write tests"}).json()

    response = client.patch(
        f"/api/v1/todos/{created['id']}",
        json={"category": "work"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "Write tests"
    assert payload["category"] == "work"


def test_delete_todo_then_patch_returns_404(client: TestClient) -> None:
    created = client.post("/api/v1/todos", json={"title": "To delete"}).json()

    delete_response = client.delete(f"/api/v1/todos/{created['id']}")
    patch_response = client.patch(f"/api/v1/todos/{created['id']}", json={"title": "new"})

    assert delete_response.status_code == 204
    assert patch_response.status_code == 404
    payload = patch_response.json()
    assert payload["error"]["code"] == "TODO_NOT_FOUND"
    assert payload["error"]["details"]["todo_id"] == created["id"]
