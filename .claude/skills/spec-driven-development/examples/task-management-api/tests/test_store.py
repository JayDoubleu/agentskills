import pytest
from datetime import datetime

from src.models import TaskCreate, TaskUpdate, Status, Priority
from src.store import TaskStore


@pytest.fixture
def store():
    return TaskStore()


@pytest.fixture
def sample_task(store):
    return store.create(TaskCreate(title="Sample task"))


class TestTaskStoreCreate:
    def test_create_returns_task_with_id(self, store):
        task = store.create(TaskCreate(title="New task"))
        assert task.id is not None
        assert task.title == "New task"

    def test_create_sets_default_status(self, store):
        task = store.create(TaskCreate(title="New task"))
        assert task.status == Status.PENDING

    def test_create_sets_default_priority(self, store):
        task = store.create(TaskCreate(title="New task"))
        assert task.priority == Priority.MEDIUM

    def test_create_sets_timestamps(self, store):
        task = store.create(TaskCreate(title="New task"))
        assert task.created_at is not None
        assert task.updated_at is not None
        assert task.completed_at is None


class TestTaskStoreGet:
    def test_get_existing_task(self, store, sample_task):
        retrieved = store.get(sample_task.id)
        assert retrieved is not None
        assert retrieved.id == sample_task.id

    def test_get_nonexistent_returns_none(self, store):
        result = store.get("nonexistent-id")
        assert result is None


class TestTaskStoreList:
    def test_list_empty_store(self, store):
        tasks = store.list()
        assert tasks == []

    def test_list_returns_all_tasks(self, store):
        store.create(TaskCreate(title="Task 1"))
        store.create(TaskCreate(title="Task 2"))
        tasks = store.list()
        assert len(tasks) == 2

    def test_list_sorted_by_created_at_desc(self, store):
        task1 = store.create(TaskCreate(title="First"))
        task2 = store.create(TaskCreate(title="Second"))
        tasks = store.list()
        assert tasks[0].id == task2.id
        assert tasks[1].id == task1.id


class TestTaskStoreUpdate:
    def test_update_title(self, store, sample_task):
        updated = store.update(sample_task.id, TaskUpdate(title="Updated title"))
        assert updated is not None
        assert updated.title == "Updated title"

    def test_update_status_to_completed_sets_completed_at(self, store, sample_task):
        updated = store.update(sample_task.id, TaskUpdate(status=Status.COMPLETED))
        assert updated is not None
        assert updated.status == Status.COMPLETED
        assert updated.completed_at is not None

    def test_update_nonexistent_returns_none(self, store):
        result = store.update("nonexistent", TaskUpdate(title="New"))
        assert result is None

    def test_update_changes_updated_at(self, store, sample_task):
        original_updated_at = sample_task.updated_at
        updated = store.update(sample_task.id, TaskUpdate(title="Changed"))
        assert updated.updated_at >= original_updated_at


class TestTaskStoreDelete:
    def test_delete_existing_task(self, store, sample_task):
        result = store.delete(sample_task.id)
        assert result is True
        assert store.get(sample_task.id) is None

    def test_delete_nonexistent_returns_false(self, store):
        result = store.delete("nonexistent")
        assert result is False
