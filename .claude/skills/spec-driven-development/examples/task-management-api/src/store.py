from datetime import datetime
from uuid import uuid4

from src.models import Task, TaskCreate, TaskUpdate, Status


class TaskStore:
    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def create(self, data: TaskCreate) -> Task:
        now = datetime.now()
        task = Task(
            id=str(uuid4()),
            title=data.title,
            description=data.description,
            status=Status.PENDING,
            priority=data.priority,
            due_date=data.due_date,
            created_at=now,
            updated_at=now,
            completed_at=None,
        )
        self._tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list(self) -> list[Task]:
        tasks = list(self._tasks.values())
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def update(self, task_id: str, data: TaskUpdate) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        task_dict = task.model_dump()
        task_dict.update(update_data)
        task_dict["updated_at"] = datetime.now()

        if data.status == Status.COMPLETED and task.completed_at is None:
            task_dict["completed_at"] = datetime.now()

        updated_task = Task(**task_dict)
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
