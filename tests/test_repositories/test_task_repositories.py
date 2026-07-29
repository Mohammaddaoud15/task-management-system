from app.models.task import Task, TaskPriority, TaskStatus
from app.models.user import User
from app.repositories.task_repositories import TaskRepository
from app.repositories.user_repositories import UserRepository


def create_user(db):
    repository = UserRepository(db)

    return repository.create(
        User(
            full_name="Mohamed",
            email="mohamed@test.com",
            hashed_password="hashed_password",
        )
    )


def test_create_task(db):
    user = create_user(db)

    repository = TaskRepository(db)

    task = Task(
        title="Finish testing",
        description="Write repository tests",
        priority=TaskPriority.HIGH,
        owner_id=user.id,
    )

    created_task = repository.create(task)

    assert created_task.id is not None
    assert created_task.title == "Finish testing"


def test_get_task_by_id(db):
    user = create_user(db)

    repository = TaskRepository(db)

    task = repository.create(
        Task(
            title="Task",
            owner_id=user.id,
        )
    )

    found_task = repository.get_by_id(task.id)

    assert found_task is not None
    assert found_task.id == task.id


def test_get_missing_task(db):
    repository = TaskRepository(db)

    assert repository.get_by_id(9999) is None


def test_get_all_tasks_by_owner(db):
    user1 = create_user(db)

    repository = TaskRepository(db)

    repository.create(Task(title="Task 1", owner_id=user1.id))
    repository.create(Task(title="Task 2", owner_id=user1.id))

    tasks = repository.get_all_by_owner(user1.id)

    assert len(tasks) == 2


def test_update_task(db):
    user = create_user(db)

    repository = TaskRepository(db)

    task = repository.create(
        Task(
            title="Old Title",
            owner_id=user.id,
        )
    )

    task.title = "New Title"
    task.status = TaskStatus.DONE

    repository.update(task)

    updated = repository.get_by_id(task.id)

    assert updated.title == "New Title"
    assert updated.status == TaskStatus.DONE


def test_delete_task(db):
    user = create_user(db)

    repository = TaskRepository(db)

    task = repository.create(
        Task(
            title="Delete Me",
            owner_id=user.id,
        )
    )

    repository.delete(task)

    assert repository.get_by_id(task.id) is None