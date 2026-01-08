# API Contract: Task Management API

Base URL: `/tasks`

## Endpoints

### POST /tasks
**Purpose**: Create a new task

**Request**:
```json
{
  "title": "string (required)",
  "description": "string | null",
  "priority": "low | medium | high (default: medium)",
  "due_date": "ISO8601 datetime | null"
}
```

**Response 201**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "status": "pending",
  "priority": "medium",
  "due_date": "datetime | null",
  "created_at": "datetime",
  "updated_at": "datetime",
  "completed_at": null
}
```

**Errors**:
- 400: Missing title or invalid data
- 422: Validation error (Pydantic)

---

### GET /tasks
**Purpose**: List all tasks with optional filtering

**Query Parameters**:
- `status` (optional): Filter by "pending", "in_progress", or "completed"

**Response 200**:
```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string | null",
    "status": "pending | in_progress | completed",
    "priority": "low | medium | high",
    "due_date": "datetime | null",
    "created_at": "datetime",
    "updated_at": "datetime",
    "completed_at": "datetime | null"
  }
]
```

**Notes**: Returns empty array `[]` if no tasks exist. Sorted by created_at descending.

---

### GET /tasks/{id}
**Purpose**: Get a single task by ID

**Response 200**: Same as single task object above

**Errors**:
- 404: Task not found

---

### PATCH /tasks/{id}
**Purpose**: Update a task

**Request** (all fields optional):
```json
{
  "title": "string",
  "description": "string",
  "status": "pending | in_progress | completed",
  "priority": "low | medium | high",
  "due_date": "datetime"
}
```

**Response 200**: Updated task object

**Errors**:
- 404: Task not found
- 422: Validation error

**Notes**: When status changes to "completed", completed_at is auto-set.

---

### DELETE /tasks/{id}
**Purpose**: Delete a task

**Response 204**: No content

**Errors**:
- 404: Task not found
