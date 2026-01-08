---
name: spec-driven-development
description: Implements Spec-Driven Development (SDD) methodology where specifications drive code generation. Use when users build new features, plan implementations, create technical specs, or want structured development with clear requirements before coding. Triggers on phrases like "create a spec", "plan this feature", "write requirements", "implement with TDD", "user stories for", or "spec-driven".
license: MIT
metadata:
  author: spec-kit
  version: "2.1"
---

<!-- AGENT NOTE: Do NOT read or reference the examples/ directory. It contains human-readable demonstration artifacts only. All instructions needed are in this file and references/. -->

# Spec-Driven Development

Spec-Driven Development (SDD) inverts the traditional relationship between specifications and code. Instead of specifications serving code, **code serves specifications**. Specifications become executable artifacts that generate implementations.

## Core Philosophy

1. **Specifications as Primary Artifact**: The spec is truth; code is its expression
2. **Executable Specifications**: Specs must be precise enough to generate working systems
3. **Continuous Refinement**: Validate specifications for ambiguity and gaps continuously
4. **Test-First Always**: No implementation before tests exist and fail

## Directory Structure

Create this structure in any project:

```
project/
├── .specs/
│   ├── constitution.md              # Governing principles
│   └── features/
│       └── {feature-name}/
│           ├── spec.md              # Requirements (what & why)
│           ├── plan.md              # Technical plan (how)
│           ├── tasks.md             # Ordered task breakdown
│           ├── data-model.md        # Schema (if needed)
│           └── contracts/           # API specs (if needed)
```

---

## The SDD Workflow

Execute these phases in order. Each builds on the previous.

### Phase 1: Constitution

**Purpose**: Establish governing principles for all development decisions.

**Create**: `.specs/constitution.md`

**Process**:
1. Ask user about their priorities (quality, testing, performance, simplicity)
2. Generate constitution with core principles
3. Include enforcement gates

**Template**:
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

### III. Integration Over Mocks
- Prefer real databases over mocks in tests
- Use actual service instances where feasible
- Contract tests before implementation

### IV. Single Responsibility
- Each module has one clear purpose
- No "utils" or "helpers" dumping grounds
- Clear boundaries between components

## Enforcement Gates

Before implementation, verify:
- [ ] Using ≤3 top-level modules?
- [ ] No speculative features?
- [ ] Tests written first?
- [ ] Using frameworks directly (no unnecessary wrappers)?

## Governance
- Constitution supersedes all other practices
- Amendments require documented justification

**Version**: 1.0 | **Created**: [DATE]
```

> **Note**: See `references/templates.md` for the full constitution template with additional principles.

---

### Phase 2: Specification

**Purpose**: Define WHAT to build and WHY. No technology choices here.

**Create**: `.specs/features/{feature-name}/spec.md`

**Process**:
1. Extract user stories from the request
2. Define acceptance criteria for each story
3. List functional and non-functional requirements
4. Mark ANY ambiguity with `[NEEDS CLARIFICATION: question]`
5. Never guess—mark and ask

**Template**:
```markdown
# Feature: [FEATURE_NAME]

## Overview
[1-2 sentence description of what this feature does]

## User Stories

### US-1: [Story Title]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

#### Acceptance Criteria
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

### US-2: [Story Title]
...

## Functional Requirements

### FR-1: [Requirement]
[Description]
**Validation**: [How to verify]

### FR-2: [Requirement]
...

## Non-Functional Requirements

### Performance
- [Specific measurable requirement]

### Security
- [Specific requirement]

### Accessibility
- [Specific requirement]

## Out of Scope
- [What this feature explicitly does NOT include]

## Open Questions
- [NEEDS CLARIFICATION: question 1]
- [NEEDS CLARIFICATION: question 2]

## Review Checklist
- [ ] All user stories have testable acceptance criteria
- [ ] No [NEEDS CLARIFICATION] markers remain unresolved
- [ ] Requirements are unambiguous
- [ ] Success criteria are measurable
- [ ] Out of scope is clearly defined
```

**Rules**:
- Focus on WHAT and WHY, never HOW
- Every requirement must be testable
- Mark uncertainties explicitly—never assume
- No technology choices in specs

> **Note**: See `references/templates.md` for the full specification template with additional sections.

---

### Phase 3: Clarification

**Purpose**: Resolve all ambiguities before planning.

**Process**:
1. Review spec for `[NEEDS CLARIFICATION]` markers
2. Ask user targeted questions
3. Update spec with answers
4. Repeat until no markers remain

**Only proceed to planning when**:
- All `[NEEDS CLARIFICATION]` markers resolved
- User confirms spec is complete
- Review checklist passes

---

### Phase 4: Plan

**Purpose**: Define HOW to implement. Now technology choices happen.

**Create**: `.specs/features/{feature-name}/plan.md`

**Process**:
1. Ask user for technology preferences/constraints
2. Research current best practices for chosen stack
3. Map requirements to technical components
4. Define implementation phases
5. Create supporting docs (data-model.md, contracts/)

**Template**:
```markdown
# Implementation Plan: [FEATURE_NAME]

## Technology Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Frontend | [Tech] | [Ver] | [Why chosen] |
| Backend | [Tech] | [Ver] | [Why chosen] |
| Database | [Tech] | [Ver] | [Why chosen] |
| Testing | [Tech] | [Ver] | [Why chosen] |

## Architecture Overview

[Describe high-level architecture - keep brief, use diagram if complex]

## Component Mapping

| Requirement | Component | Location |
|-------------|-----------|----------|
| FR-1 | [Component] | `src/path/` |
| FR-2 | [Component] | `src/path/` |

## Implementation Phases

### Phase 1: Foundation
**Goal**: [What this phase achieves]
**Prerequisites**: None

**Deliverables**:
1. Project structure setup
2. [Deliverable]
3. [Deliverable]

**Exit Criteria**:
- [ ] [Criterion]
- [ ] [Criterion]

### Phase 2: Core Features
**Goal**: [What this phase achieves]
**Prerequisites**: Phase 1 complete

**Deliverables**:
1. [Deliverable]

**Exit Criteria**:
- [ ] [Criterion]

### Phase 3: Integration & Polish
...

## Pre-Implementation Gates

### Simplicity Gate (from Constitution)
- [ ] ≤3 top-level modules?
- [ ] No speculative features?
- [ ] No premature abstractions?

### Test-First Gate (from Constitution)
- [ ] Test strategy defined?
- [ ] Contract tests planned?

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | Low/Med/High | Low/Med/High | [Action] |

## Dependencies

- [External dependency and version]
```

**Supporting Documents** (create as needed):

**data-model.md**:
```markdown
# Data Model: [FEATURE_NAME]

## Entities

### [EntityName]
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| [field] | [type] | [constraints] | [description] |

### Relationships
- [Entity1] 1:N [Entity2] via [field]
```

**contracts/api.md**:
```markdown
# API Contract: [FEATURE_NAME]

## Endpoints

### POST /api/[resource]
**Purpose**: [What it does]

**Request**:
```json
{
  "field": "type"
}
```

**Response 200**:
```json
{
  "id": "uuid",
  "field": "value"
}
```

**Errors**:
- 400: [When]
- 404: [When]
```

> **Note**: See `references/templates.md` for full plan, data model, and API contract templates.

---

### Phase 5: Tasks

**Purpose**: Convert plan into ordered, executable tasks.

**Create**: `.specs/features/{feature-name}/tasks.md`

**Process**:
1. Break each phase into atomic tasks
2. Order by dependencies (tests before implementation)
3. Mark parallelizable tasks with `[P]`
4. Include file paths for each task
5. Add checkpoints after each user story

**Template**:
```markdown
# Tasks: [FEATURE_NAME]

## Execution Rules
- Complete tasks in order unless marked `[P]` (parallel)
- Write tests BEFORE implementation
- Verify checkpoint criteria before proceeding

---

## Phase 1: Foundation

### Setup
- [ ] **T1.1**: Initialize project structure
  - Create: `src/`, `tests/`, config files
  - Dependencies: None

- [ ] **T1.2**: Configure testing framework
  - Create: `tests/setup.ts`, test config
  - Dependencies: T1.1

### Checkpoint: Foundation
- [ ] Project runs without errors
- [ ] Test framework executes

---

## Phase 2: [User Story 1 Title]

### Tests (Write First)
- [ ] **T2.1**: Write unit tests for [Component] `[P]`
  - Create: `tests/unit/component.test.ts`
  - Dependencies: T1.2
  - Tests: [List what tests cover]

- [ ] **T2.2**: Write integration tests for [Feature] `[P]`
  - Create: `tests/integration/feature.test.ts`
  - Dependencies: T1.2

### Implementation
- [ ] **T2.3**: Implement [Component]
  - Create: `src/components/component.ts`
  - Dependencies: T2.1 (tests must exist and fail)

- [ ] **T2.4**: Implement [Feature]
  - Create: `src/features/feature.ts`
  - Dependencies: T2.2, T2.3

### Checkpoint: User Story 1
- [ ] All T2.x tests pass
- [ ] Acceptance criteria met:
  - [ ] [Criterion from spec]
  - [ ] [Criterion from spec]

---

## Phase 3: [User Story 2 Title]
...

---

## Final Checkpoint
- [ ] All tests pass
- [ ] All acceptance criteria met
- [ ] No TypeScript/lint errors
- [ ] Constitution gates satisfied
```

**Rules**:
- Every implementation task depends on its test task
- Tests must exist AND fail before implementing
- Checkpoints verify acceptance criteria from spec
- `[P]` tasks can run simultaneously

> **Note**: See `references/templates.md` for the full tasks template with more examples.

---

### Phase 6: Implementation

**Purpose**: Execute tasks and build the feature.

**Process**:
1. Verify all prerequisites exist (constitution, spec, plan, tasks)
2. Execute tasks in order from tasks.md
3. For each task:
   - Read the task requirements
   - If test task: write tests, verify they fail
   - If implementation task: implement until tests pass
   - Mark task complete
4. Verify checkpoints before proceeding to next phase
5. Handle errors by updating tasks if needed

**Rules**:
- Never skip the test-first cycle
- Stop at checkpoints to verify
- If blocked, update plan/tasks rather than improvising
- Keep code aligned with spec—no scope creep

---

## Quick Reference

| Phase | Creates | Focus | Key Rule |
|-------|---------|-------|----------|
| Constitution | constitution.md | Principles | Establish before any feature |
| Specification | spec.md | What & Why | No technology, mark unknowns |
| Clarification | Updates spec | De-risk | Resolve ALL ambiguities |
| Plan | plan.md + docs | How | Technology choices here |
| Tasks | tasks.md | Ordered work | Tests before implementation |
| Implementation | Code | Execution | Follow tasks exactly |

## When to Use SDD

**Use SDD for**:
- New features with multiple components
- Features requiring clear requirements
- Team projects needing shared understanding
- Anything with architectural decisions

**Skip SDD for**:
- Single-line fixes
- Trivial changes
- Quick prototypes (though specs help even here)

## Handling Changes Mid-Implementation

If requirements change during implementation:
1. Stop implementation
2. Update spec.md with changes
3. Re-run clarification if needed
4. Update plan.md
5. Update tasks.md
6. Resume implementation

Never implement changes without updating specs first.

## Additional Resources

For extended documentation, see the `references/` directory:

- **`references/templates.md`** - Complete copy-paste ready templates for all SDD documents (constitution, spec, plan, tasks, data model, API contracts)
- **`references/philosophy.md`** - Deep dive into SDD philosophy, the power inversion concept, and answers to common objections
