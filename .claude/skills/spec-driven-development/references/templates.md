# SDD Document Templates (Copy-Paste Ready)

## Constitution Template

```markdown
# [Project Name] Constitution

## Core Principles

### I. Test-First Development (NON-NEGOTIABLE)
All implementation MUST follow TDD:
1. Write tests first
2. Verify tests FAIL (Red)
3. Implement to make tests pass (Green)
4. Refactor while keeping tests green

### II. Simplicity
- Start with minimal viable implementation
- Maximum 3 modules/packages initially
- Additional complexity requires documented justification
- No premature abstractions
- No "utils" dumping grounds

### III. Integration Over Mocks
- Prefer real databases over mocks in tests
- Use actual service instances where feasible
- Contract tests before implementation

### IV. Single Responsibility
- Each module has one clear purpose
- Clear boundaries between components
- Dependencies flow in one direction

### V. Framework Trust
- Use framework features directly
- No unnecessary wrapper layers
- Trust the ecosystem

## Enforcement Gates

Before any implementation, verify:
- [ ] Using ≤3 top-level modules?
- [ ] No speculative "might need" features?
- [ ] Tests written before implementation?
- [ ] Using frameworks directly (no wrappers)?
- [ ] Single model representation (no DTOs unless required)?

## Governance
- Constitution supersedes all other practices
- Amendments require documented justification and team review
- All code reviews must verify constitutional compliance

**Version**: 1.0 | **Created**: [DATE] | **Last Amended**: [DATE]
```

---

## Specification Template

```markdown
# Feature: [FEATURE_NAME]

## Overview
[1-2 sentence description]

## User Stories

### US-1: [Story Title]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

#### Acceptance Criteria
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

### US-2: [Story Title]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

#### Acceptance Criteria
- [ ] Given [context], when [action], then [outcome]

## Functional Requirements

### FR-1: [Requirement Title]
[Description of what the system must do]

**Validation**: [How to verify this is implemented correctly]

### FR-2: [Requirement Title]
[Description]

**Validation**: [Verification method]

## Non-Functional Requirements

### Performance
- Page load time < [X]ms
- API response time < [X]ms under [Y] concurrent users

### Security
- [Specific security requirement]
- [Authentication/authorization requirements]

### Accessibility
- WCAG 2.1 AA compliance
- [Specific accessibility requirements]

## Out of Scope
- [Explicitly excluded feature 1]
- [Explicitly excluded feature 2]

## Open Questions
- [NEEDS CLARIFICATION: question about ambiguous requirement]

## Dependencies
- [External system or feature this depends on]

## Review Checklist
- [ ] All user stories have testable acceptance criteria
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are unambiguous and testable
- [ ] Success criteria are measurable
- [ ] Out of scope clearly defined
- [ ] No technology choices in this document
```

---

## Plan Template

```markdown
# Implementation Plan: [FEATURE_NAME]

## Technology Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | [e.g., TypeScript] | [5.x] | [Type safety, ecosystem] |
| Frontend | [e.g., React] | [18.x] | [Component model, hooks] |
| Backend | [e.g., Express] | [4.x] | [Simplicity, middleware] |
| Database | [e.g., PostgreSQL] | [15.x] | [ACID, JSON support] |
| ORM | [e.g., Prisma] | [5.x] | [Type-safe queries] |
| Testing | [e.g., Vitest] | [1.x] | [Fast, ESM native] |

## Architecture Overview

[Brief description or ASCII diagram]

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API       │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Component Mapping

| Requirement | Component | Location |
|-------------|-----------|----------|
| FR-1 | [ComponentName] | `src/components/` |
| FR-2 | [ServiceName] | `src/services/` |
| US-1 | [FeatureModule] | `src/features/` |

## Implementation Phases

### Phase 1: Foundation
**Goal**: Project setup and infrastructure
**Prerequisites**: None
**Duration Estimate**: [Not time-based, task-based]

**Deliverables**:
1. Project structure with TypeScript config
2. Testing framework configured
3. Database connection established
4. CI pipeline (optional)

**Exit Criteria**:
- [ ] `npm run build` succeeds
- [ ] `npm test` runs (even with no tests)
- [ ] Database connects successfully

### Phase 2: [User Story 1 - Title]
**Goal**: Implement first user story end-to-end
**Prerequisites**: Phase 1 complete

**Deliverables**:
1. Data model for [entities]
2. API endpoints for [resources]
3. UI components for [features]

**Exit Criteria**:
- [ ] All US-1 acceptance criteria pass
- [ ] Integration tests pass

### Phase 3: [User Story 2 - Title]
**Goal**: [Goal]
**Prerequisites**: Phase 2 complete

**Deliverables**:
1. [Deliverable]

**Exit Criteria**:
- [ ] All US-2 acceptance criteria pass

## Pre-Implementation Gates

### Simplicity Gate
- [ ] ≤3 top-level directories in src/?
- [ ] No speculative features planned?
- [ ] No premature abstractions?

### Test-First Gate
- [ ] Test files listed for each component?
- [ ] Contract tests planned for APIs?

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | Low/Med/High | Low/Med/High | [Mitigation strategy] |

## External Dependencies

| Dependency | Version | Purpose | Fallback |
|------------|---------|---------|----------|
| [package] | [^x.x] | [Why needed] | [Alternative if fails] |
```

---

## Tasks Template

```markdown
# Tasks: [FEATURE_NAME]

## Execution Rules
1. Complete tasks in listed order unless marked `[P]` (parallelizable)
2. Write tests BEFORE implementation code
3. Verify checkpoint criteria before proceeding to next phase
4. Update this file if tasks need modification

---

## Phase 1: Foundation

- [ ] **T1.1**: Initialize project
  - Run: `npm init`, configure TypeScript, ESLint
  - Create: `src/`, `tests/`, `tsconfig.json`
  - Dependencies: None

- [ ] **T1.2**: Configure testing framework
  - Install: vitest (or jest)
  - Create: `vitest.config.ts`, `tests/setup.ts`
  - Dependencies: T1.1

- [ ] **T1.3**: Setup database connection
  - Install: prisma (or chosen ORM)
  - Create: `prisma/schema.prisma`, connection config
  - Dependencies: T1.1

### Checkpoint: Foundation Complete
- [ ] `npm run build` succeeds
- [ ] `npm test` executes without error
- [ ] Database connection verified

---

## Phase 2: [User Story Title]

### Tests First
- [ ] **T2.1**: Write [Component] unit tests `[P]`
  - Create: `tests/unit/component.test.ts`
  - Cover: [list test scenarios]
  - Dependencies: T1.2

- [ ] **T2.2**: Write [API] integration tests `[P]`
  - Create: `tests/integration/api.test.ts`
  - Cover: [list test scenarios]
  - Dependencies: T1.2, T1.3

### Implementation
- [ ] **T2.3**: Implement [Component]
  - Create: `src/components/Component.tsx`
  - Dependencies: T2.1 *(tests must exist and FAIL)*

- [ ] **T2.4**: Implement [API endpoint]
  - Create: `src/api/resource.ts`
  - Dependencies: T2.2 *(tests must exist and FAIL)*

- [ ] **T2.5**: Wire up [integration]
  - Modify: `src/index.ts`
  - Dependencies: T2.3, T2.4

### Checkpoint: User Story Complete
- [ ] All T2.x tests PASS
- [ ] Acceptance criteria verified:
  - [ ] [AC from spec]
  - [ ] [AC from spec]

---

## Final Checkpoint

- [ ] All tests pass: `npm test`
- [ ] Build succeeds: `npm run build`
- [ ] No lint errors: `npm run lint`
- [ ] All acceptance criteria from spec verified
- [ ] Constitution gates satisfied
```

---

## Data Model Template

```markdown
# Data Model: [FEATURE_NAME]

## Entities

### User
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | String | Unique, Not Null | User email |
| name | String | Not Null | Display name |
| createdAt | DateTime | Not Null, Default NOW | Creation timestamp |
| updatedAt | DateTime | Not Null, Auto-update | Last modification |

### [EntityName]
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| [field] | [Type] | [Constraints] | [Description] |

## Relationships

- User 1:N [Entity] (via userId foreign key)
- [Entity1] N:M [Entity2] (via join table)

## Indexes

| Table | Columns | Type | Rationale |
|-------|---------|------|-----------|
| users | email | Unique | Login lookup |
| [table] | [columns] | [Type] | [Why needed] |

## Migrations Strategy

1. Create tables in dependency order
2. Add indexes after data population
3. Use transactions for multi-table changes
```

---

## API Contract Template

```markdown
# API Contract: [FEATURE_NAME]

## Base URL
`/api/v1`

## Authentication
[Describe auth mechanism - Bearer token, session, etc.]

## Endpoints

### Create [Resource]
`POST /resources`

**Purpose**: Create a new resource

**Request Headers**:
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "name": "string (required, 1-100 chars)",
  "description": "string (optional, max 500 chars)"
}
```

**Response 201 Created**:
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string | null",
  "createdAt": "ISO8601 datetime"
}
```

**Errors**:
- `400 Bad Request`: Invalid input (validation errors in body)
- `401 Unauthorized`: Missing or invalid token
- `409 Conflict`: Resource already exists

### Get [Resource]
`GET /resources/:id`

**Response 200 OK**:
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string | null",
  "createdAt": "ISO8601 datetime"
}
```

**Errors**:
- `404 Not Found`: Resource does not exist

### List [Resources]
`GET /resources`

**Query Parameters**:
- `page` (integer, default: 1)
- `limit` (integer, default: 20, max: 100)
- `sort` (string: "createdAt" | "name", default: "createdAt")
- `order` (string: "asc" | "desc", default: "desc")

**Response 200 OK**:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

## Error Response Format

All errors follow this structure:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [
      { "field": "name", "message": "Required" }
    ]
  }
}
```
```
