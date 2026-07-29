import uuid
from datetime import UTC, datetime, timedelta

import pytest

from app.dependencies import get_current_user
from app.main import app
from app.models.user import User


@pytest.fixture
def authed_client(client, db):
    test_user = User(
        full_name="Test User",
        email=f"{uuid.uuid4()}@test.com",
        hashed_password="fake_hash",
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    app.dependency_overrides[get_current_user] = lambda: test_user

    yield client

    app.dependency_overrides.clear()


def test_create_task_success(authed_client):
    payload = {
        "title": "Router Task",
        "description": "Created via API",
        "priority": "HIGH",
        "due_date": (
            datetime.now(UTC) + timedelta(days=1)
        ).isoformat(),
    }

    response = authed_client.post("/tasks/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["priority"] == payload["priority"]


def test_create_task_unauthorized(client):
    response = client.post(
        "/tasks/",
        json={"title": "Sneaky Task"},
    )

    assert response.status_code == 401


def test_get_tasks_success(authed_client):
    authed_client.post("/tasks/", json={"title": "Task 1"})
    authed_client.post("/tasks/", json={"title": "Task 2"})

    response = authed_client.get("/tasks/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    titles = {task["title"] for task in data}

    assert "Task 1" in titles
    assert "Task 2" in titles


def test_get_tasks_unauthorized(client):
    response = client.get("/tasks/")

    assert response.status_code == 401


def test_get_task_by_id_success(authed_client):
    create = authed_client.post(
        "/tasks/",json={"title": "Specific Task"},
    )

    task_id = create.json()["id"]

    response = authed_client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Specific Task"


def test_get_task_not_found(authed_client):
    response = authed_client.get("/tasks/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found."


def test_get_task_unauthorized(client):
    response = client.get("/tasks/1")

    assert response.status_code == 401


def test_update_task_success(authed_client):
    response = authed_client.post(
        "/tasks/",
        json={
            "title": "Old Title",
            "status": "PENDING",
        },
    )

    task_id = response.json()["id"]

    update_payload = {
        "title": "New Title",
        "status": "IN_PROGRESS",
    }

    response = authed_client.patch(
        f"/tasks/{task_id}",
        json=update_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Title"
    assert data["status"] == "IN_PROGRESS"


def test_update_task_not_found(authed_client):
    response = authed_client.patch(
        "/tasks/9999",
        json={"title": "New Title"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Task not found."


def test_update_task_unauthorized(client):
    response = client.patch(
        "/tasks/1",
        json={"title": "New Title"},
    )

    assert response.status_code == 401


def test_delete_task_success(authed_client):
    response = authed_client.post(
        "/tasks/",
        json={"title": "Task to delete"},
    )

    task_id = response.json()["id"]

    response = authed_client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204

    get_response = authed_client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404


def test_delete_task_not_found(authed_client):
    response = authed_client.delete("/tasks/9999")

    assert response.status_code == 400
    assert response.json()["detail"] == "Task not found."


def test_delete_task_unauthorized(client):
    response = client.delete("/tasks/1")

    assert response.status_code == 401