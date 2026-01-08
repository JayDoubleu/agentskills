# Roast Review

A code review skill that uses Google Gemini to "roast" your codebase, then has Claude validate and translate the findings into actionable feedback.

## How It Works

1. **Pack** - Uses [repomix](https://github.com/yamadashy/repomix) to bundle your repo into a single file
2. **Roast** - Sends the bundle to Gemini with a prompt to brutally critique the code
3. **Validate** - Claude reads each flagged `file:line` to verify the issue exists (catches hallucinations)
4. **Translate** - Harsh criticism is rewritten as constructive, prioritized recommendations

## Why "Roast"?

When asked to roast code, LLMs surface the most glaring issues - the things that would stand out to any developer. This is a useful heuristic for finding high-priority problems quickly.

## Usage

In Claude Code, just ask:

```
roast this repo
```

Or be more specific:

```
roast the src directory
quick roast (uses faster model)
```

## Requirements

### Environment Variable

```bash
export GEMINI_API_KEY="your-api-key"
```

### Dependencies

```bash
# Python SDK for Gemini
pip install google-genai

# Repo packer (or use npx)
npm install -g repomix
```

## Supported Models

| Model | Best For | Input Cost | Output Cost |
|-------|----------|------------|-------------|
| `gemini-3-pro-preview` | Most thorough (default) | $2.00/1M | $12.00/1M |
| `gemini-3-flash-preview` | Fast, good quality | $0.15/1M | $0.60/1M |
| `gemini-2.5-pro` | High quality, large context | $1.25/1M | $10.00/1M |
| `gemini-2.5-flash` | Balanced | $0.15/1M | $0.60/1M |

## Output Format

The skill reports token usage and cost, then presents validated findings:

```
Token usage: 45,231 input, 2,847 output, 48,078 total
Estimated cost: $0.0432 (gemini-3-pro-preview)

## Validated Issues

### Critical Issues
- **[src/auth.py:45]** ✅ VERIFIED - SQL injection vulnerability → Use parameterized queries

### High Priority
- **[src/api.py:120-130]** ✅ VERIFIED - No rate limiting → Add rate limiter middleware

### Unverified Issues
- **[src/utils.py:99]** ❌ NOT FOUND - File exists but line 99 is a comment, not the claimed issue
```

## Validation Statuses

- ✅ **VERIFIED** - Issue confirmed at the specified location
- ⚠️ **PARTIAL** - Issue exists but at different line or in modified form
- ❌ **NOT FOUND** - File missing, line out of range, or code doesn't match claim
- 🤔 **SUBJECTIVE** - Style/opinion matter, not an objective problem

## Caching

Repomix output is cached in `/tmp/repomix-{hash}.txt`. The roast script uses `--no-cache` flag if you need to regenerate.

## Standalone Script Usage

The underlying script can be used directly:

```bash
# Basic usage
python3 scripts/repo_query.py "What does this repo do?"

# With specific model
python3 scripts/repo_query.py --model gemini-2.5-pro "Find security issues"

# Output to file
python3 scripts/repo_query.py --output review.md "Review this code"

# Target subdirectory
python3 scripts/repo_query.py --repo src/ "Analyze the source code"

# Quiet mode (for automation)
python3 scripts/repo_query.py -q --output out.md "query"
```

## License

MIT
