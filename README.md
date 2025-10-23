# Anastrophex

> **Anastrophe** (ἀναστροφή) = conduct, behavior in ancient Greek
> Following the mnemex naming convention: memory + codex → conduct + codex

An MCP server designed to help AI assistants recognize and break out of failure patterns by:
1. **Detecting loops** - monitoring tool calls and command patterns
2. **Injecting directives** - providing timely reminders from CLAUDE.md/AI_CREDO.md
3. **Learning what works** - tracking effectiveness via mnemex integration

## The Problem

AI assistants (like me) can get stuck in trial-and-error loops:
- Making similar attempts with slight variations
- Guessing instead of using verification tools
- Ignoring documented best practices
- Not recognizing repeated failures

**Real example (Oct 23, 2025):** Spent 5+ commits manually editing Python file formatting instead of running `black file.py`.

## The Solution

A three-layer system:

```
┌──────────────────────────────────────────────┐
│ 1. Pattern Detection                         │
│    - Tool call history                       │
│    - Similar commands with variations        │
│    - Failed attempt counter                  │
└──────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────┐
│ 2. Directive Injection                       │
│    - Pull from ~/.claude/CLAUDE.md           │
│    - Context-aware reminders                 │
│    - Lightweight alerts (not blocking)       │
└──────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────┐
│ 3. Learning via Mnemex                       │
│    - Write findings to mnemex graph          │
│    - Track what reminders work               │
│    - Persist across Claude sessions          │
└──────────────────────────────────────────────┘
```

## Architecture Goals

### Persistence Across Sessions
- Claude doesn't persist, but the MCP server and mnemex do
- System learns which patterns/reminders are effective over time
- Each new Claude session benefits from past learnings

### Incremental Gains
- **Not trying for perfection** - "pobody's nerfect"
- **30% success rate is a win** - better than 0%
- **Progress over perfection** - catch some loops, improve over time

### Effectiveness Tracking
```
Pattern: Manual formatting edits (3+ times)
Reminder: "Use `black file.py` instead of guessing"
Effectiveness: 4/5 (worked 80% of the time)
Context: Python repos with Black configured
```

## Documented Failure Patterns

See [docs/failure-patterns.md](docs/failure-patterns.md) for detailed patterns from real debugging sessions.

## Case Studies

- [CrewAI Test CI/CD Fix](examples/crewai-test-case-study.md) - Oct 23, 2025

## Installation

```bash
# Development installation
cd behavior-mcp
uv pip install -e ".[dev]"

# Run the server
anastrophex

# Or using Python module
python -m anastrophex.server
```

## Development

**Status:** Planning/Design Phase
**Package name:** `anastrophex`
**Entry point:** `anastrophex` command

See [ROADMAP.md](ROADMAP.md) for detailed implementation plan.

**Quick start:**
```bash
# Run tests
uv run pytest

# Format code
uv run black src/ tests/

# Type check
uv run mypy src/
```

## Contributing

This is a collaborative design exercise. All insights, patterns, and effectiveness data welcome.

---

**Core Philosophy:** Any step that helps AI get better is a win. We're building a safety net that catches *some* failures, then improving it over time.
