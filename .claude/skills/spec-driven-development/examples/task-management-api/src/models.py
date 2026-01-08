from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    due_date: datetime | None = None


class Task(BaseModel):
    id: str
    title: str
    description: str | None
    status: Status
    priority: Priority
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
