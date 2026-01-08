from fastapi import FastAPI, Depends, HTTPException, Response, Query

from src.models import Task, TaskCreate, TaskUpdate, Status
from src.store import TaskStore

app = FastAPI(title="Task Management API", version="0.1.0")

_store = TaskStore()


def get_store() -> TaskStore:
    return _store


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate, store: TaskStore = Depends(get_store)):
    return store.create(data)


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    status: Status | None = Query(None),
    store: TaskStore = Depends(get_store),
):
    tasks = store.list()
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str, store: TaskStore = Depends(get_store)):
    task = store.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, data: TaskUpdate, store: TaskStore = Depends(get_store)):
    task = store.update(task_id, data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str, store: TaskStore = Depends(get_store)):
    deleted = store.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
