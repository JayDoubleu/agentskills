# AgentSkills Project Constitution

## Core Principles

### I. Test-First Development (NON-NEGOTIABLE)
All implementation MUST follow TDD:
1. Write tests first
2. Verify tests FAIL (Red)
3. Implement to make tests pass (Green)
4. Refactor while keeping tests green

### II. Rapid Iteration
- Favor working software over perfect architecture
- Start with the simplest thing that works
- Iterate based on real feedback, not speculation
- Time-box decisions - if unsure after 5 minutes, pick and move on

### III. Simplicity
- Maximum 3 modules/packages initially
- No premature abstractions
- Additional complexity requires documented justification
- Delete code rather than comment it out

### IV. Minimal Viable Implementation
- Build only what's needed NOW
- No "future-proofing" without immediate use case
- Features earn their complexity through demonstrated need

### V. Integration Over Mocks
- Prefer real dependencies in tests where feasible
- Contract tests before implementation
- Mocks only for external services or slow operations

## Enforcement Gates

Before implementation, verify:
- [ ] Using ≤3 top-level modules?
- [ ] No speculative features?
- [ ] Tests written first?
- [ ] Simplest solution chosen?

## Governance
- Constitution supersedes all other practices
- Amendments require documented justification

**Version**: 1.0 | **Created**: 2026-01-08
