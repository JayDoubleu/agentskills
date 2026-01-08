# Spec-Driven Development Skill

A portable Agent Skill implementing Spec-Driven Development (SDD) methodology for AI-assisted coding.

## Origin

This skill was extracted and adapted from [github/spec-kit](https://github.com/github/spec-kit), a toolkit for Spec-Driven Development. The original spec-kit provides a CLI tool (`specify`) that bootstraps projects with SDD templates for various AI coding assistants.

## How It Was Produced

1. **Research Phase**: Analyzed the agentskills.io specification to understand the standard format for portable AI skills (SKILL.md with YAML frontmatter, directory structure, progressive disclosure patterns).

2. **Extraction**: Studied the spec-kit repository to understand the SDD methodology:
   - `spec-driven.md` - Core philosophy
   - `templates/` - Document templates (constitution, spec, plan, tasks)
   - `memory/constitution.md` - Governing principles approach
   - Slash commands workflow (`/speckit.constitution`, `/speckit.specify`, etc.)

3. **Initial Skill Creation**: Created a skill that referenced spec-kit's `/speckit.*` commands. This worked but had a dependency on projects initialized with the `specify` CLI.

4. **Standalone Refactoring**: Rewrote the skill to be fully portable:
   - Removed all `/speckit.*` command dependencies
   - Embedded complete templates and instructions inline
   - Changed directory structure from `.specify/` to generic `.specs/`
   - Added reference files for progressive disclosure

5. **Validation**: Ran the skill through a validator to ensure compliance with agentskills.io spec. Applied fixes for minor issues:
   - Updated description to third person
   - Added explicit pointers to reference files
   - Added Resources section

## What's Included

```
spec-driven-development/
├── SKILL.md              # Complete SDD workflow (493 lines)
├── README.md             # This file
├── references/
│   ├── philosophy.md     # Deep dive on SDD philosophy
│   └── templates.md      # Copy-paste ready templates
└── examples/
    └── task-management-api/  # Complete worked example
```

## Examples

The `examples/` directory contains complete worked examples demonstrating the SDD workflow.

### task-management-api

A REST API for task management built using the full SDD workflow. Demonstrates:

- **All 6 phases**: Constitution through Implementation
- **Clarification in action**: 3 ambiguities identified and resolved via user questions
- **TDD workflow**: Tests written before implementation, verified to fail, then code written to pass
- **Constitution adherence**: 3-module limit, rapid iteration focus

**Structure:**
```
examples/task-management-api/
├── .specs/
│   ├── constitution.md                    # Project principles
│   └── features/task-management-api/
│       ├── spec.md                        # Requirements (WHAT & WHY)
│       ├── plan.md                        # Technical plan (HOW)
│       ├── tasks.md                       # Ordered task breakdown
│       ├── data-model.md                  # Schema definition
│       └── contracts/api.md               # API contract
├── src/
│   ├── main.py                            # FastAPI app + routes
│   ├── models.py                          # Pydantic models
│   └── store.py                           # In-memory storage
├── tests/
│   ├── test_api.py                        # API endpoint tests
│   ├── test_models.py                     # Model validation tests
│   └── test_store.py                      # Store operation tests
└── pyproject.toml
```

**Results:** 42 tests, 5 CRUD endpoints + filtering, Python/FastAPI stack

## The SDD Methodology

SDD inverts the traditional relationship between specifications and code:

1. **Constitution** - Establish governing principles
2. **Specification** - Define WHAT and WHY (no technology)
3. **Clarification** - Resolve all ambiguities
4. **Plan** - Define HOW (technology choices)
5. **Tasks** - Ordered, test-first task breakdown
6. **Implementation** - Execute tasks

Key principles:
- Specifications are the primary artifact; code serves specs
- Test-first development is non-negotiable
- Mark ambiguities with `[NEEDS CLARIFICATION]` - never guess
- Simplicity gates prevent over-engineering

## Usage

The skill triggers automatically when Claude detects phrases like:
- "create a spec"
- "plan this feature"
- "write requirements"
- "implement with TDD"
- "user stories for"
- "spec-driven"

Or explicitly reference SDD methodology in your request.

## Version History

- **2.1** - Standalone version with reference pointers, third-person description
- **2.0** - Fully standalone, removed spec-kit dependencies
- **1.0** - Initial version with spec-kit command references

## License

MIT

## Credits

- Original SDD methodology from [github/spec-kit](https://github.com/github/spec-kit)
- Skill format follows [agentskills.io](https://agentskills.io) specification
