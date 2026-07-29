from datetime import UTC, datetime, timedelta

import pytest

from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService


def create_user_helper(db, email: str = "user1@test.com") -> User:
    user = User(
        full_name="Test User",
        email=email,
        hashed_password="fake_hashed_password"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_create_task(db):
    service = TaskService(db)
    user = create_user_helper(db)

    request = TaskCreate(
        title="My First Task",
        description="Testing the creation logic",
        priority="HIGH",
        due_date=datetime.now(UTC) + timedelta(days=2)
    )

    task = service.create_task(request, user)

    assert task.id is not None
    assert task.title == request.title
    assert task.description == request.description
    assert task.owner_id == user.id


def test_get_task_success(db):
    service = TaskService(db)
    user = create_user_helper(db)
    request = TaskCreate(title="Target Task", description="To be retrieved")
    
    created_task = service.create_task(request, user)
    retrieved_task = service.get_task(created_task.id, user)

    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Target Task"


def test_get_task_not_found(db):
    service = TaskService(db)
    user = create_user_helper(db)

    with pytest.raises(ValueError, match="Task not found"):
        service.get_task(task_id=9999, current_user=user)


def test_get_task_unauthorized_owner(db):
    service = TaskService(db)
    user1 = create_user_helper(db, email="user1@test.com")
    user2 = create_user_helper(db, email="user2@test.com")

    request = TaskCreate(title="User 1 Secret Task")
    task = service.create_task(request, current_user=user1)

    with pytest.raises(ValueError, match="You do not own this task"):
        service.get_task(task.id, current_user=user2)


def test_get_tasks_list(db):
    service = TaskService(db)
    user1 = create_user_helper(db, email="user1@test.com")
    user2 = create_user_helper(db, email="user2@test.com")

    service.create_task(TaskCreate(title="Task A"), current_user=user1)
    service.create_task(TaskCreate(title="Task B"), current_user=user1)
    
    service.create_task(TaskCreate(title="Task C"), current_user=user2)

    user1_tasks = service.get_tasks(current_user=user1)

    assert len(user1_tasks) == 2
    assert user1_tasks[0].title in ["Task A", "Task B"]
    assert user1_tasks[1].title in ["Task A", "Task B"]


def test_update_task_success(db):
    service = TaskService(db)
    user = create_user_helper(db)
    
    task = service.create_task(
        TaskCreate(title="Old Title", description="Old Description"), 
        current_user=user
    )

    update_request = TaskUpdate(title="New Title", status="DONE")
    updated_task = service.update_task(task.id, update_request, current_user=user)

    assert updated_task.title == "New Title"
    assert updated_task.status == "DONE"
    assert updated_task.description == "Old Description" 


def test_update_task_unauthorized(db):
    service = TaskService(db)
    user1 = create_user_helper(db, email="user1@test.com")
    user2 = create_user_helper(db, email="user2@test.com")

    task = service.create_task(TaskCreate(title="Original"), current_user=user1)
    update_request = TaskUpdate(title="Hacked")

    with pytest.raises(ValueError, match="You do not own this task"):
        service.update_task(task.id, update_request, current_user=user2)


def test_delete_task_success(db):
    service = TaskService(db)
    user = create_user_helper(db)
    
    task = service.create_task(TaskCreate(title="To be deleted"), current_user=user)
    
    service.delete_task(task.id, current_user=user)

    with pytest.raises(ValueError, match="Task not found"):
        service.get_task(task.id, current_user=user)


def test_delete_task_unauthorized(db):
    service = TaskService(db)
    user1 = create_user_helper(db, email="user1@test.com")
    user2 = create_user_helper(db, email="user2@test.com")

    task = service.create_task(TaskCreate(title="Do not delete"), current_user=user1)

    with pytest.raises(ValueError, match="You do not own this task"):
        service.delete_task(task.id, current_user=user2)