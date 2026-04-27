import pytest
from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_todos():
    import app as app_module
    app_module.todos.clear()
    app_module.next_id = 1


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_list_todos_empty(client):
    resp = client.get("/todos")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_todo(client):
    resp = client.post("/todos", json={"title": "Buy milk"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["id"] == 1
    assert data["title"] == "Buy milk"
    assert data["done"] is False


def test_create_todo_missing_title(client):
    resp = client.post("/todos", json={})
    assert resp.status_code == 400


def test_get_todo(client):
    client.post("/todos", json={"title": "Task A"})
    resp = client.get("/todos/1")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Task A"


def test_get_todo_not_found(client):
    resp = client.get("/todos/999")
    assert resp.status_code == 404


def test_update_todo(client):
    client.post("/todos", json={"title": "Old title"})
    resp = client.put("/todos/1", json={"title": "New title", "done": True})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["title"] == "New title"
    assert data["done"] is True


def test_update_todo_no_body(client):
    client.post("/todos", json={"title": "Task"})
    resp = client.put("/todos/1", data="", content_type="application/json")
    assert resp.status_code == 400


def test_update_todo_not_found(client):
    resp = client.put("/todos/999", json={"title": "X"})
    assert resp.status_code == 404


def test_delete_todo(client):
    client.post("/todos", json={"title": "To delete"})
    resp = client.delete("/todos/1")
    assert resp.status_code == 204
    assert client.get("/todos/1").status_code == 404
