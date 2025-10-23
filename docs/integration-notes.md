# Integration Notes

## Complementary Tools

### Clear-Thought MCP Server

**Repository:** https://github.com/chirag127/Clear-Thought-MCP-server

**What it provides:** Strategic "how to think" debugging frameworks
- Binary Search (systematic elimination)
- Reverse Engineering (working backward)
- Divide and Conquer (breaking problems down)
- Backtracking (retracing steps)
- Cause Elimination (ruling out sources)
- Program Slicing (isolating code segments)

**Gap identified:** No tactical implementation guidance
- Doesn't mention verbose flags (`-v`, `-vv`, `--debug`)
- Doesn't mention logging levels or trace modes
- Doesn't mention diagnostic commands
- Focuses on mental models, not tool usage

### Anastrophex (This Project)

**What we provide:** Tactical "what to actually do" debugging actions
- Verbosity escalation rules (when to add `-v`, `-vv`, etc.)
- Language-specific verbose flags (Python, git, npm, etc.)
- Concrete commands to run when stuck
- Pattern detection for trial-and-error loops
- Intervention timing and messaging

**Relationship:** Complementary

Example flow:
1. **Clear-thought:** "Use binary search to narrow down the problem"
2. **Anastrophex:** "Run `python -v script.py` to see what's happening"
3. **Clear-thought:** "Divide the problem - test each component separately"
4. **Anastrophex:** "Add `-vv` flag since first attempt failed"

## Future Collaboration

**Potential PR to clear-thought-mcp:**

When anastrophex is mature enough (Phase 2-3 complete), propose adding tactical debugging tools that complement their strategic frameworks.

**Suggested additions:**

```markdown
## Debugging Approaches

### [Existing approaches...]

### Diagnostic Verbosity (NEW)
**When to use:** When commands fail but error messages are unclear
**Strategy:** Escalate diagnostic output to see internal behavior

**Implementation:**
- **Level 1 (First error):** Add `-v` or `--verbose` flag
- **Level 2 (Second error):** Add `-vv` or very verbose mode
- **Level 3 (Third error):** Add debug/trace flags
- **Level 4 (Still stuck):** Ask about environment changes

**Language-specific flags:**
- Python: `python -v`, `python -vv`, `pip -vvv`
- Git: `git --verbose`, `GIT_TRACE=1`
- npm: `npm --loglevel=verbose`
- Shell: `bash -x`, `set -x`

**Combines with:**
- Binary Search: Use verbose output to narrow which component fails
- Divide and Conquer: Add verbosity to each isolated test
- Backtracking: Verbose logs show exact execution path

### Warning Pattern Detection (NEW)
**When to use:** When same warning appears multiple times
**Strategy:** Stop and investigate rather than continue

**Implementation:**
1. First warning: Note it
2. Second occurrence of same warning: STOP
3. Investigate before proceeding
4. Don't continue until warning is understood

**Combines with:**
- Cause Elimination: Warning tells you what to investigate
- Backtracking: Warning shows where things diverged from expected
```

**Value proposition for clear-thought:**
- Bridges gap between strategic thinking and tactical execution
- Provides concrete commands users can run immediately
- Complements existing mental models with implementation details
- Helps users avoid trial-and-error loops

**Files to reference:**
- `docs/debugging-principles.md` - Verbosity escalation
- `docs/failure-patterns.md` - Real-world loop patterns
- `examples/crewai-test-case-study.md` - Before/after examples
- `examples/anastrophex-venv-debugging.md` - Meta-debugging session

## Why This Works

**Clear-thought** answers: "How should I approach this problem?"
**Anastrophex** answers: "What command should I run right now?"

Together they form a complete debugging toolkit:
- Strategic framework (clear-thought)
- Tactical implementation (anastrophex)
- Pattern detection (anastrophex)
- Learning persistence (anastrophex via mnemex)

## Timeline

- **Now:** Keep development separate
- **Phase 2 complete:** Anastrophex has proven directive injection
- **Phase 3 complete:** Effectiveness data from mnemex shows which tactics work
- **Then:** Propose collaboration/PR with data-backed recommendations

## Notes

- Clear-thought is MIT licensed (open source, accepts contributions)
- Active development (recent commits as of 2025)
- Part of @waldzellai collection of MCP servers
- Has existing user base through Smithery

This is a good candidate for collaborative enhancement once we have:
1. Working implementation
2. Effectiveness data
3. Clear examples of tactical + strategic = better outcomes
