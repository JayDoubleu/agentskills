import pytest
from fastapi.testclient import TestClient

from src.main import app, get_store
from src.store import TaskStore


@pytest.fixture
def client():
    store = TaskStore()
    app.dependency_overrides[get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_tasks(client):
    client.post("/tasks", json={"title": "Task 1", "priority": "low"})
    client.post("/tasks", json={"title": "Task 2", "priority": "high"})
    client.post("/tasks", json={"title": "Task 3", "priority": "medium"})
    return client


class TestCreateTask:
    def test_create_task_valid(self, client):
        response = client.post("/tasks", json={"title": "Buy groceries"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["id"] is not None
        assert data["status"] == "pending"
        assert data["priority"] == "medium"

    def test_create_task_with_all_fields(self, client):
        response = client.post(
            "/tasks",
            json={
                "title": "Complete project",
                "description": "Finish the API",
                "priority": "high",
                "due_date": "2026-12-31T23:59:59",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Complete project"
        assert data["description"] == "Finish the API"
        assert data["priority"] == "high"

    def test_create_task_missing_title(self, client):
        response = client.post("/tasks", json={})
        assert response.status_code == 422

    def test_create_task_empty_title(self, client):
        response = client.post("/tasks", json={"title": ""})
        assert response.status_code == 422


class TestListTasks:
    def test_list_tasks_empty(self, client):
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_returns_all(self, client_with_tasks):
        response = client_with_tasks.get("/tasks")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 3

    def test_list_tasks_sorted_by_created_at_desc(self, client_with_tasks):
        response = client_with_tasks.get("/tasks")
        tasks = response.json()
        assert tasks[0]["title"] == "Task 3"
        assert tasks[2]["title"] == "Task 1"


class TestGetTask:
    def test_get_task_exists(self, client):
        create_response = client.post("/tasks", json={"title": "Test task"})
        task_id = create_response.json()["id"]

        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Test task"

    def test_get_task_not_found(self, client):
        response = client.get("/tasks/nonexistent-id")
        assert response.status_code == 404


class TestUpdateTask:
    def test_update_task_title(self, client):
        create_response = client.post("/tasks", json={"title": "Original"})
        task_id = create_response.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={"title": "Updated"})
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"

    def test_update_task_status_to_completed(self, client):
        create_response = client.post("/tasks", json={"title": "Test"})
        task_id = create_response.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={"status": "completed"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["completed_at"] is not None

    def test_update_task_not_found(self, client):
        response = client.patch("/tasks/nonexistent", json={"title": "New"})
        assert response.status_code == 404


class TestDeleteTask:
    def test_delete_task_exists(self, client):
        create_response = client.post("/tasks", json={"title": "To delete"})
        task_id = create_response.json()["id"]

        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client):
        response = client.delete("/tasks/nonexistent")
        assert response.status_code == 404


class TestFilterByStatus:
    def test_filter_by_pending(self, client):
        client.post("/tasks", json={"title": "Task 1"})
        create_response = client.post("/tasks", json={"title": "Task 2"})
        task_id = create_response.json()["id"]
        client.patch(f"/tasks/{task_id}", json={"status": "completed"})

        response = client.get("/tasks?status=pending")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Task 1"

    def test_filter_by_completed(self, client):
        client.post("/tasks", json={"title": "Task 1"})
        create_response = client.post("/tasks", json={"title": "Task 2"})
        task_id = create_response.json()["id"]
        client.patch(f"/tasks/{task_id}", json={"status": "completed"})

        response = client.get("/tasks?status=completed")
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["status"] == "completed"

    def test_filter_by_in_progress(self, client):
        create_response = client.post("/tasks", json={"title": "Task 1"})
        task_id = create_response.json()["id"]
        client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})

        response = client.get("/tasks?status=in_progress")
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["status"] == "in_progress"

    def test_filter_invalid_status(self, client):
        response = client.get("/tasks?status=invalid")
        assert response.status_code == 422
