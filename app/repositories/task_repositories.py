from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        output = select(Task).where(Task.id == task_id)
        return self.db.scalar(output)

    def get_all_by_owner(self, owner_id: int) -> list[Task]:
        output = select(Task).where(Task.owner_id == owner_id)
        return list(self.db.scalars(output))

    def update(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
