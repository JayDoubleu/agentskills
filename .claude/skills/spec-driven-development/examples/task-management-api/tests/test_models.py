import pytest
from datetime import datetime
from pydantic import ValidationError

from src.models import Task, TaskCreate, TaskUpdate, Status, Priority


class TestTaskCreate:
    def test_valid_task_create_minimal(self):
        task = TaskCreate(title="Buy groceries")
        assert task.title == "Buy groceries"
        assert task.description is None
        assert task.priority == Priority.MEDIUM
        assert task.due_date is None

    def test_valid_task_create_full(self):
        due = datetime(2026, 12, 31)
        task = TaskCreate(
            title="Complete project",
            description="Finish the API",
            priority=Priority.HIGH,
            due_date=due,
        )
        assert task.title == "Complete project"
        assert task.description == "Finish the API"
        assert task.priority == Priority.HIGH
        assert task.due_date == due

    def test_task_create_missing_title_fails(self):
        with pytest.raises(ValidationError):
            TaskCreate()

    def test_task_create_empty_title_fails(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="")


class TestTaskUpdate:
    def test_all_fields_optional(self):
        update = TaskUpdate()
        assert update.title is None
        assert update.description is None
        assert update.status is None
        assert update.priority is None
        assert update.due_date is None

    def test_partial_update(self):
        update = TaskUpdate(status=Status.COMPLETED, priority=Priority.LOW)
        assert update.status == Status.COMPLETED
        assert update.priority == Priority.LOW


class TestTask:
    def test_task_has_all_fields(self):
        now = datetime.now()
        task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test task",
            description="A test",
            status=Status.PENDING,
            priority=Priority.MEDIUM,
            due_date=None,
            created_at=now,
            updated_at=now,
            completed_at=None,
        )
        assert task.id == "123e4567-e89b-12d3-a456-426614174000"
        assert task.title == "Test task"
        assert task.status == Status.PENDING


class TestEnums:
    def test_status_values(self):
        assert Status.PENDING == "pending"
        assert Status.IN_PROGRESS == "in_progress"
        assert Status.COMPLETED == "completed"

    def test_priority_values(self):
        assert Priority.LOW == "low"
        assert Priority.MEDIUM == "medium"
        assert Priority.HIGH == "high"
