# Data Model: Task Management API

## Entities

### Task
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| title | string | Required, min 1 char | Task title |
| description | string | Optional | Task details |
| status | enum | "pending", "in_progress", "completed" | Current state (default: "pending") |
| priority | enum | "low", "medium", "high" | Priority level (default: "medium") |
| due_date | datetime | Optional | When task is due |
| created_at | datetime | Auto-set on create | Creation timestamp |
| updated_at | datetime | Auto-set on update | Last modification timestamp |
| completed_at | datetime | Auto-set when completed | Completion timestamp |

## Pydantic Models

### TaskCreate (Request body for POST)
- title: str (required)
- description: str | None
- priority: Priority = "medium"
- due_date: datetime | None

### TaskUpdate (Request body for PATCH)
- title: str | None
- description: str | None
- status: Status | None
- priority: Priority | None
- due_date: datetime | None

### Task (Response model)
- All fields from entity table
