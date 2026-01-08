# Feature: Task Management API

## Overview
A REST API that allows users to create, read, update, and delete tasks with support for due dates, priorities, and completion status.

## User Stories

### US-1: Create a Task
**As a** user
**I want** to create a new task with a title and optional details
**So that** I can track work that needs to be done

#### Acceptance Criteria
- [ ] Given valid task data, when I POST to /tasks, then a new task is created with a unique ID
- [ ] Given a task title, when I create a task, then the task defaults to "pending" status
- [ ] Given invalid data (missing title), when I POST to /tasks, then I receive a 400 error with details

### US-2: List Tasks
**As a** user
**I want** to view all my tasks
**So that** I can see what work is pending

#### Acceptance Criteria
- [ ] Given tasks exist, when I GET /tasks, then I receive a list of all tasks
- [ ] Given no tasks exist, when I GET /tasks, then I receive an empty array
- [ ] Given tasks exist, when I GET /tasks, then tasks are sorted by creation date (newest first)

### US-3: Update a Task
**As a** user
**I want** to update task details or mark it complete
**So that** I can track progress

#### Acceptance Criteria
- [ ] Given a valid task ID, when I PATCH /tasks/:id, then the task is updated
- [ ] Given a valid task ID, when I set status to "completed", then completed_at timestamp is set
- [ ] Given an invalid task ID, when I PATCH /tasks/:id, then I receive a 404 error

### US-4: Delete a Task
**As a** user
**I want** to delete a task
**So that** I can remove tasks I no longer need

#### Acceptance Criteria
- [ ] Given a valid task ID, when I DELETE /tasks/:id, then the task is removed
- [ ] Given an invalid task ID, when I DELETE /tasks/:id, then I receive a 404 error

## Functional Requirements

### FR-1: Task Data Model
A task must contain:
- `id`: Unique identifier
- `title`: Required, non-empty string
- `description`: Optional string
- `status`: One of "pending", "in_progress", "completed"
- `priority`: One of "low", "medium", "high" (defaults to "medium")
- `due_date`: Optional date
- `created_at`: Timestamp
- `updated_at`: Timestamp
- `completed_at`: Timestamp (set when status becomes "completed")

### FR-2: API Endpoints
- `POST /tasks` - Create task
- `GET /tasks` - List all tasks
- `GET /tasks/:id` - Get single task
- `PATCH /tasks/:id` - Update task
- `DELETE /tasks/:id` - Delete task

### FR-3: Filtering and Sorting
- `GET /tasks` supports optional `?status=` query parameter
- Valid status values: "pending", "in_progress", "completed"
- Default sort: by created_at descending (newest first)

## Non-Functional Requirements

### Performance
- API responses under 200ms for typical operations
- Support at least 100 concurrent requests

### Data Persistence
- In-memory storage (data does not persist across restarts)
- Suitable for demo/development purposes

## Out of Scope
- User authentication (single-user API for now)
- Task categories/tags
- Task dependencies
- Recurring tasks
- Real-time updates/websockets

## Open Questions
None - all clarifications resolved.

## Review Checklist
- [x] All user stories have testable acceptance criteria
- [x] No [NEEDS CLARIFICATION] markers remain unresolved
- [x] Requirements are unambiguous
- [x] Success criteria are measurable
- [x] Out of scope is clearly defined
