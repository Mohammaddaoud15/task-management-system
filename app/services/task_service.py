from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.repositories.task_repositories import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.task_repository = TaskRepository(db)

    def create_task(
        self,
        request: TaskCreate,
        current_user: User,
    ) -> Task:
        task = Task(
            title=request.title,
            description=request.description,
            priority=request.priority,
            due_date=request.due_date,
            owner_id=current_user.id,
        )
        return self.task_repository.create(task)

    def get_task(
        self,
        task_id: int,
        current_user: User,
    ) -> Task:
        task = self.task_repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")

        if task.owner_id != current_user.id:
            raise ValueError("You do not own this task.")

        return task

    def get_tasks(self, current_user: User) -> list[Task]:
        return self.task_repository.get_all_by_owner(current_user.id)

    def update_task(
        self,
        task_id: int,
        request: TaskUpdate,
        current_user: User,
    ) -> Task:
        task = self.task_repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")

        if task.owner_id != current_user.id:
            raise ValueError("You do not own this task.")

        if request.title:
            task.title = request.title

        if request.description:
            task.description = request.description

        if request.status:
            task.status = request.status

        if request.priority:
            task.priority = request.priority

        if request.due_date:
            task.due_date = request.due_date

        return self.task_repository.update(task)

    def delete_task(
        self,
        task_id: int,
        current_user: User,
    ) -> None:
        task = self.task_repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")

        if task.owner_id != current_user.id:
            raise ValueError("You do not own this task.")

        self.task_repository.delete(task)
