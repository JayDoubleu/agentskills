---
name: roast-review
description: Roast a repository to identify issues, then translate to constructive feedback. Use when user wants code review, wants to find problems, asks to "roast" their code, or wants honest feedback about their codebase.
allowed-tools: Bash(python*:*), Read
---

# Roast Review Skill

This skill performs a code review by asking Gemini to "roast" the codebase, then translating the roast into actionable feedback.

## Why This Works

When asked to "roast" code, LLMs surface the most glaring issues - the things that would stand out to any developer. This is a useful heuristic for finding high-priority problems.

## Configuration

### Supported Models

| Model | Best For |
|-------|----------|
| `gemini-3-pro-preview` | Most thorough analysis (recommended) |
| `gemini-3-flash-preview` | Fast, good quality |
| `gemini-2.5-pro` | High quality, large context |
| `gemini-2.5-flash` | Default, balanced |

### Repomix Caching

The script caches repomix output in `{tempdir}/repomix-{hash}.txt`. Use `--no-cache` to regenerate.

## Execution Steps

### Step 1: Determine Scope

Ask the user what to roast:
- Entire repository (default)
- Specific directory (e.g., `src/`, `tests/`)

### Step 2: Run the Roast

```bash
# Set target and output paths
TARGET_DIR="$(pwd)"  # or "$(pwd)/src" for specific directory
ROAST_OUTPUT="/tmp/roast-$(echo -n "$TARGET_DIR" | md5sum | cut -c1-12).md"

# Run the roast (use --repo for subdirectory)
python3 ${CLAUDE_SKILL_DIR}/scripts/repo_query.py --quiet --model gemini-3-pro-preview --output "$ROAST_OUTPUT" \
  "Roast this repo. Be brutally honest about what's wrong. For EVERY issue, include the specific file path and line number(s) in the format 'file.py:123' or 'file.py:100-150'. Point out bad practices, code smells, missing features, poor organization, security issues, and anything else problematic."
```

### Step 3: Report Token Usage

The script outputs token usage and cost. Report this to the user:
```
Token usage: X input, Y output, Z total
Estimated cost: $0.XXXX (model-name)
```

### Step 4: Read and Present Results

1. Use Read tool to get the roast from `$ROAST_OUTPUT`
2. Present the roast to the user
3. Translate each issue into constructive feedback with this format:

```
## Code Review Summary

### Critical Issues
- **[file:line]** Issue description → Recommendation

### High Priority
- **[file:line]** Issue description → Recommendation

### Medium Priority
- **[file:line]** Issue description → Recommendation

### Low Priority
- **[file:line]** Issue description → Recommendation

### Positive Observations
- What's good about the codebase
```

For each roasted issue:
- Extract the file:line reference
- Rewrite harshly-worded criticism as constructive feedback
- Add specific, actionable recommendation
- Prioritize by severity

### Step 5: Validate Flagged Issues

**IMPORTANT**: Gemini may hallucinate file paths, line numbers, or issues that don't exist. You MUST validate each flagged issue.

For each issue with a `file:line` reference:

1. Use the Read tool to read the flagged file at the specified line(s)
2. Verify the issue actually exists in the code
3. Mark each issue with a validation status:

```
## Validated Issues

### Critical Issues
- **[file:line]** ✅ VERIFIED - Issue description → Recommendation
- **[file:line]** ❌ NOT FOUND - Gemini claimed X but the code shows Y

### Unverified Issues
- Issues where file/line couldn't be located or code differs significantly
```

Validation criteria:
- ✅ **VERIFIED**: The code at that location clearly shows the described issue
- ⚠️ **PARTIAL**: The issue exists but at a different line or in modified form
- ❌ **NOT FOUND**: File doesn't exist, line is out of range, or code doesn't match the claim
- 🤔 **SUBJECTIVE**: The "issue" is a style/opinion matter, not an objective problem

If more than 30% of issues fail validation, warn the user that the roast may be unreliable and suggest re-running with a different model.

## Examples

**User**: "Roast this repo"
**Action**: Run on current directory, read output, present with recommendations

**User**: "Roast the src directory"
**Action**: Run with `--repo src/`, read output, present with recommendations

**User**: "Quick roast"
**Action**: Use `--model gemini-2.5-flash` for faster results

## Requirements

- `GEMINI_API_KEY` environment variable
- `google-genai`: `pip install google-genai`
- `repomix`: `npm install -g repomix` (or via npx)
