# Tasks: Task Management API

## Execution Rules
- Complete tasks in order unless marked `[P]` (parallel)
- Write tests BEFORE implementation (TDD)
- Verify checkpoint criteria before proceeding

---

## Phase 1: Foundation

### Setup
- [ ] **T1.1**: Create project structure
  - Create: `src/`, `tests/`, `pyproject.toml`
  - Dependencies: None

- [ ] **T1.2**: Configure pyproject.toml with dependencies
  - Edit: `pyproject.toml`
  - Dependencies: T1.1
  - Add: fastapi, uvicorn, pydantic, pytest, httpx

- [ ] **T1.3**: Create minimal FastAPI app
  - Create: `src/__init__.py`, `src/main.py`
  - Dependencies: T1.2
  - Just health check endpoint for now

- [ ] **T1.4**: Configure pytest with test client fixture
  - Create: `tests/__init__.py`, `tests/conftest.py`
  - Dependencies: T1.3

### Checkpoint: Foundation
- [ ] `pytest` runs without errors
- [ ] `uvicorn src.main:app` starts
- [ ] Health check endpoint responds

---

## Phase 2: Core CRUD

### T2.1-T2.4: Models & Store (Tests First)
- [ ] **T2.1**: Write tests for Pydantic models `[P]`
  - Create: `tests/test_models.py`
  - Dependencies: T1.4
  - Tests: Task, TaskCreate, TaskUpdate validation

- [ ] **T2.2**: Write tests for TaskStore `[P]`
  - Create: `tests/test_store.py`
  - Dependencies: T1.4
  - Tests: create, get, list, update, delete operations

- [ ] **T2.3**: Implement Pydantic models
  - Create: `src/models.py`
  - Dependencies: T2.1 (tests must FAIL first)

- [ ] **T2.4**: Implement TaskStore
  - Create: `src/store.py`
  - Dependencies: T2.2, T2.3 (tests must FAIL first)

### Checkpoint: Models & Store
- [ ] All model tests pass
- [ ] All store tests pass

### T2.5-T2.14: API Endpoints (Tests First)

#### Create Task (US-1)
- [ ] **T2.5**: Write tests for POST /tasks
  - Edit: `tests/test_api.py`
  - Dependencies: T2.4
  - Tests: valid create, missing title (400), default status

- [ ] **T2.6**: Implement POST /tasks
  - Edit: `src/main.py`
  - Dependencies: T2.5 (tests must FAIL first)

#### List Tasks (US-2)
- [ ] **T2.7**: Write tests for GET /tasks
  - Edit: `tests/test_api.py`
  - Dependencies: T2.6
  - Tests: list all, empty list, sorted by created_at

- [ ] **T2.8**: Implement GET /tasks
  - Edit: `src/main.py`
  - Dependencies: T2.7 (tests must FAIL first)

#### Get Single Task
- [ ] **T2.9**: Write tests for GET /tasks/{id}
  - Edit: `tests/test_api.py`
  - Dependencies: T2.8
  - Tests: found, not found (404)

- [ ] **T2.10**: Implement GET /tasks/{id}
  - Edit: `src/main.py`
  - Dependencies: T2.9 (tests must FAIL first)

#### Update Task (US-3)
- [ ] **T2.11**: Write tests for PATCH /tasks/{id}
  - Edit: `tests/test_api.py`
  - Dependencies: T2.10
  - Tests: update fields, complete sets completed_at, not found (404)

- [ ] **T2.12**: Implement PATCH /tasks/{id}
  - Edit: `src/main.py`
  - Dependencies: T2.11 (tests must FAIL first)

#### Delete Task (US-4)
- [ ] **T2.13**: Write tests for DELETE /tasks/{id}
  - Edit: `tests/test_api.py`
  - Dependencies: T2.12
  - Tests: successful delete (204), not found (404)

- [ ] **T2.14**: Implement DELETE /tasks/{id}
  - Edit: `src/main.py`
  - Dependencies: T2.13 (tests must FAIL first)

### Checkpoint: Core CRUD
- [ ] All US-1 acceptance criteria pass
- [ ] All US-2 acceptance criteria pass
- [ ] All US-3 acceptance criteria pass
- [ ] All US-4 acceptance criteria pass

---

## Phase 3: Filtering (FR-3)

- [ ] **T3.1**: Write tests for status filtering
  - Edit: `tests/test_api.py`
  - Dependencies: T2.14
  - Tests: filter by each status, invalid status (400)

- [ ] **T3.2**: Implement status filtering
  - Edit: `src/main.py`
  - Dependencies: T3.1 (tests must FAIL first)

### Checkpoint: Filtering
- [ ] `GET /tasks?status=pending` works
- [ ] `GET /tasks?status=in_progress` works
- [ ] `GET /tasks?status=completed` works
- [ ] Invalid status returns 400

---

## Final Checkpoint
- [ ] All tests pass (`pytest`)
- [ ] No type errors (`mypy src/` if configured)
- [ ] All acceptance criteria from spec.md met
- [ ] Constitution gates satisfied
- [ ] API matches contracts/api.md
