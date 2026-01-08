# Agent Skills

A collection of portable [Agent Skills](https://agentskills.io) for AI coding assistants.

## What Are Agent Skills?

Agent Skills are self-contained packages of instructions, templates, and resources that AI agents load dynamically to improve performance on specific tasks. They follow the open [agentskills.io](https://agentskills.io/specification) specification and work across multiple platforms including Claude Code, Cursor, VS Code, and others.

## Skills in This Repository

| Skill | Description |
|-------|-------------|
| [spec-driven-development](.claude/skills/spec-driven-development/) | Structured methodology where specifications drive code generation |

## Installation

### Claude Code (Global)

```bash
cp -r .claude/skills/* ~/.claude/skills/
```

### Project-Level

```bash
cp -r .claude/skills/* /path/to/project/.claude/skills/
```

## Structure

```
.claude/skills/
└── {skill-name}/
    ├── SKILL.md        # Required - skill definition
    ├── references/     # Optional - supporting docs
    ├── scripts/        # Optional - automation
    └── README.md       # Optional - skill documentation
```

## Creating New Skills

Each skill must have:
- A `SKILL.md` file with YAML frontmatter (`name`, `description`)
- Directory name matching the `name` field
- Clear trigger keywords in the description

See [agentskills.io/specification](https://agentskills.io/specification) for the full spec.

## License

MIT
