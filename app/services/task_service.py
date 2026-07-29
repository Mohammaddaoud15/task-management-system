from sqlalchemy.orm import Session

from app.core.logging import logger
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

        task = self.task_repository.create(task)

        logger.info(
            "Task '%s' created by user %s",
            task.title,
            current_user.email,
        )

        return task

    def get_task(
        self,
        task_id: int,
        current_user: User,
    ) -> Task:
        task = self.task_repository.get_by_id(task_id)

        if not task:
            logger.warning(
                "User %s requested non-existent task %s",
                current_user.email,
                task_id,
            )
            raise ValueError("Task not found.")

        if task.owner_id != current_user.id:
            logger.warning(
                "User %s attempted to access task %s owned by another user",
                current_user.email,
                task_id,
            )
            raise ValueError("You do not own this task.")

        logger.info(
            "User %s retrieved task %s",
            current_user.email,
            task.id,
        )

        return task

    def get_tasks(self, current_user: User) -> list[Task]:
        tasks = self.task_repository.get_all_by_owner(current_user.id)

        logger.info(
            "User %s retrieved %d task(s)",
            current_user.email,
            len(tasks),
        )

        return tasks

    def update_task(
        self,
        task_id: int,
        request: TaskUpdate,
        current_user: User,
    ) -> Task:
        task = self.task_repository.get_by_id(task_id)

        if not task:
            logger.warning(
                "User %s attempted to update non-existent task %s",
                current_user.email,
                task_id,
            )
            raise ValueError("Task not found.")

        if task.owner_id != current_user.id:
            logger.warning(
                "User %s attempted to update task %s owned by another user",
                current_user.email,
                task_id,
            )
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

        task = self.task_repository.update(task)

        logger.info(
            "Task %s updated by user %s",
            task.id,
            current_user.email,
        )

        return task

    def delete_task(
        self,
        task_id: int,
        current_user: User,
    ) -> None:
        task = self.task_repository.get_by_id(task_id)

        if not task:
            logger.warning(
                "User %s attempted to delete non-existent task %s",
                current_user.email,
                task_id,
            )
            raise ValueError("Task not found.")

        if task.owner_id != current_user.id:
            logger.warning(
                "User %s attempted to delete task %s owned by another user",
                current_user.email,
                task_id,
            )
            raise ValueError("You do not own this task.")

        logger.info(
            "Task %s deleted by user %s",
            task.id,
            current_user.email,
        )

        self.task_repository.delete(task)