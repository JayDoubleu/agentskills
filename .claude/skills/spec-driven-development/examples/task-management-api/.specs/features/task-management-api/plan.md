# Implementation Plan: Task Management API

## Technology Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Framework | FastAPI | 0.100+ | Modern, automatic validation, OpenAPI docs |
| Language | Python | 3.11+ | Type hints, async support |
| Testing | pytest | 8.0+ | Standard Python testing, async support |
| HTTP Client | httpx | 0.27+ | Async test client for FastAPI |
| Validation | Pydantic | 2.0+ | Built into FastAPI, great DX |

## Architecture Overview

Simple 3-module structure (per constitution):

```
src/
├── main.py          # FastAPI app, routes
├── models.py        # Pydantic models, Task dataclass
└── store.py         # In-memory storage
tests/
├── conftest.py      # Fixtures
└── test_api.py      # API tests
```

## Component Mapping

| Requirement | Component | Location |
|-------------|-----------|----------|
| FR-1: Task Data Model | Task, TaskCreate, TaskUpdate | `src/models.py` |
| FR-2: API Endpoints | Route handlers | `src/main.py` |
| FR-3: Filtering | Query params in GET /tasks | `src/main.py` |
| Data Persistence | TaskStore class | `src/store.py` |

## Implementation Phases

### Phase 1: Foundation
**Goal**: Project structure with working test setup

**Deliverables**:
1. Project directory structure
2. pyproject.toml with dependencies
3. Empty FastAPI app that starts
4. pytest configured and running

**Exit Criteria**:
- [ ] `uvicorn src.main:app` starts without error
- [ ] `pytest` runs (even with no tests)

### Phase 2: Core CRUD (US-1, US-2, US-3, US-4)
**Goal**: All CRUD operations working with tests

**Deliverables**:
1. Pydantic models for Task
2. In-memory store
3. All 5 endpoints implemented
4. Tests for each endpoint

**Exit Criteria**:
- [ ] All acceptance criteria from spec pass
- [ ] Test coverage for happy path and error cases

### Phase 3: Filtering (FR-3)
**Goal**: Status filtering on list endpoint

**Deliverables**:
1. Query parameter support
2. Tests for filtering

**Exit Criteria**:
- [ ] `GET /tasks?status=pending` returns only pending tasks
- [ ] Invalid status returns 400 error

## Pre-Implementation Gates

### Simplicity Gate (from Constitution)
- [x] ≤3 top-level modules? (main.py, models.py, store.py)
- [x] No speculative features?
- [x] No premature abstractions?

### Test-First Gate (from Constitution)
- [x] Test strategy defined? (pytest + httpx TestClient)
- [x] Contract tests planned? (API endpoint tests)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| UUID collision | Very Low | Low | Use uuid4, statistically impossible |
| Concurrent access bugs | Low | Medium | Single-threaded for demo; document limitation |

## Dependencies

- fastapi >= 0.100.0
- uvicorn >= 0.30.0
- pydantic >= 2.0.0
- pytest >= 8.0.0
- httpx >= 0.27.0
