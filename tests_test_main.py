import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_tasks():
    from main import _tasks
    _tasks.clear()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_get_task():
    response = client.post("/tasks", json={"title": "Study math", "description": "Algebra assignment"})
    assert response.status_code == 201
    task = response.json()

    get_response = client.get(f"/tasks/{task['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == task

def test_list_tasks_is_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_update_task():
    response = client.post("/tasks", json={"title": "Study math"})
    task = response.json()

    update_response = client.put(f"/tasks/{task['id']}", json={"completed": true})
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

def test_delete_task():
    response = client.post("/tasks", json={"title": "Study math"})
    task = response.json()

    delete_response = client.delete(f"/tasks/{task['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task['id']}")
    assert get_response.status_code == 404
