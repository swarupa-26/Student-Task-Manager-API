import pytest
from fastapi.testclient import TestClient
from main import app
from src.db.config import SessionLocal, engine
from sqlalchemy import text
from src.db.base import Base

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # create tables
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def clear_data():
    # truncate tasks table between tests
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM tasks"))
        db.commit()
    finally:
        db.close()


def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_get_task():
    r = client.post("/tasks", json={"title": "Study math", "description": "Algebra assignment"})
    assert r.status_code == 201
    task = r.json()

    get_response = client.get(f"/tasks/{task['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == task["id"]


def test_list_tasks_is_empty():
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []


def test_update_task():
    r = client.post("/tasks", json={"title": "Study math"})
    task = r.json()

    update_response = client.patch(f"/tasks/{task['id']}", json={"status": "completed"})
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "completed"


def test_delete_task():
    r = client.post("/tasks", json={"title": "Study math"})
    task = r.json()

    delete_response = client.delete(f"/tasks/{task['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task['id']}")
    assert get_response.status_code == 404


def test_create_task_validation_error():
    r = client.post("/tasks", json={"title": ""})
    assert r.status_code == 422
    body = r.json()
    assert body["error"] == "validation_error"
    assert "title" in body["fields"]
    assert isinstance(body["message"], str)


def test_patch_task_invalid_status_returns_validation_error():
    r = client.post("/tasks", json={"title": "Study math"})
    task = r.json()

    update_response = client.patch(f"/tasks/{task['id']}", json={"status": "invalid_state"})
    assert update_response.status_code == 422
    body = update_response.json()
    assert body["error"] == "validation_error"
    assert "status" in body["fields"]


def test_patch_task_clear_description():
    r = client.post("/tasks", json={"title": "Study math", "description": "Initial"})
    task = r.json()

    update_response = client.patch(f"/tasks/{task['id']}", json={"description": None})
    assert update_response.status_code == 200
    assert update_response.json()["description"] is None


def test_get_nonexistent_task_returns_structured_error():
    r = client.get("/tasks/nonexistent-id")
    assert r.status_code == 404
    body = r.json()
    assert body["error"] == "not_found"
    assert body["message"] == "Task not found"


def test_complete_task_idempotent():
    r = client.post("/tasks", json={"title": "Read book"})
    task = r.json()

    c1 = client.post(f"/tasks/{task['id']}/complete")
    assert c1.status_code == 200
    assert c1.json()["status"] == "completed"

    c2 = client.post(f"/tasks/{task['id']}/complete")
    assert c2.status_code == 200
    assert c2.json()["status"] == "completed"
