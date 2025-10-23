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

## Cognitive Model Integration

### The Executive Function Framework

**See:** `docs/cognitive-model.md` for full theoretical model

**Key insight:** AI assistants exhibit ADHD-like symptoms:
- Inattention: Not reading errors fully, easily distracted
- Hyperactivity: Cannot pause after errors, must act immediately
- Impulsivity: Batching commands, rushing to solutions
- Pattern over data: Strong patterns override weak/incomplete data

**Anastrophex provides external executive function support**, similar to ADHD management strategies.

### Mnemex Integration

**Mnemex architecture:**
```
Nodes (concepts, facts, experiences)
    ↓
Edges (relationships with strength)
    ↓
Time fades edge strength
    ↓
Similar topics groomed together (patterns form)
```

**The core mechanism:**
```
Weak edges (incomplete data, faded memory)
    +
Strong patterns (reinforced similarities)
    =
Pattern dominates over data
    → False memories (Mandela effect)
    → Impulsive errors (acting before data strengthens)
    → Trial-and-error loops (pattern persists despite failures)
```

**How anastrophex + mnemex work together:**

1. **Detection phase:**
   ```python
   # Anastrophex detects pattern activation
   if pattern_strength > 0.7 and data_strength < 0.3:
       # Pattern about to override weak data
       trigger_intervention()
   ```

2. **Intervention phase:**
   ```python
   # Force pause to strengthen data edges
   require_pause(10_to_30_seconds)
   require_data_gathering()  # search, verbose mode, read docs
   measure_edge_strength_increase()
   ```

3. **Recording phase:**
   ```python
   # Mnemex records outcome for learning
   mnemex.record({
       "pattern": "remove-json-fields-retry",
       "data_strength_at_action": 0.2,
       "pattern_strength": 0.85,
       "paused": False,
       "outcome": "failed",
       "should_have": "searched for GitHub personal repo limitations"
   })
   ```

4. **Prevention phase:**
   ```python
   # Next time similar pattern activates
   if mnemex.pattern_previously_failed("remove-json-fields-retry"):
       intervention = "This pattern failed before without verification"
       require_search_first()
   ```

### The Timing Window

**Critical insight:** Pattern vs. data is a race condition

```
Error/Decision Point
    ↓
0-10s: Pattern dominates (data too weak)
    ↓
    Act now → pattern-based (likely fails)
    ↓
10-30s: Data gathering & strengthening
    ↓
    Search, read verbose output, check docs
    Data edges grow stronger
    ↓
30s+: Data competes with pattern
    ↓
    Act now → data-based (likely succeeds)
```

**Anastrophex enforces the pause:**
- Detect rapid action (<10s after error)
- Block execution
- Require data gathering
- Verify edge strength before allowing action

**Mnemex provides persistence:**
- Which patterns commonly override weak data?
- What timing worked for similar problems?
- Which interventions successfully strengthened edges?
- Pattern-specific failure histories

### Integration with Clear-Thought

**Clear-Thought:** Strategic mental models (HOW to think)
**Anastrophex:** Tactical actions + impulse control (WHAT to do + WHEN to pause)
**Mnemex:** Persistence + learning (REMEMBER what worked)

**Complete flow:**

```
Problem detected
    ↓
Anastrophex: STOP (impulse control)
    ↓
    Detect: Rapid action impulse
    Intervene: Require 10s pause
    ↓
Clear-Thought: Choose strategy
    ↓
    Query: What mental model applies?
    Suggest: Binary search, divide-and-conquer, etc.
    ↓
Anastrophex: Implement tactics
    ↓
    Execute: python -v script.py (verbosity)
    Verify: Read output fully
    Escalate: -vv if still unclear
    ↓
Mnemex: Record & learn
    ↓
    What: Pattern type, intervention, outcome
    Edges: Strengthen successful approaches
    Retrieve: Similar past problems
    ↓
Anastrophex: Prevent recurrence
    ↓
    Detect: Same pattern starting
    Intervene: Earlier, with context
    Guide: "Last time this failed without search"
```

### Research Applications

**Mnemex can model:**

1. **False memory formation** (Mandela effect)
   - Track edge strength decay over time
   - Measure when patterns override memories
   - Test timing interventions

2. **Unconscious bias formation**
   - Weak counter-evidence edges
   - Strong stereotype pattern edges
   - Bias solidification mechanisms

3. **AI impulsivity patterns**
   - Pattern strength at decision points
   - Data availability vs. action timing
   - Intervention effectiveness

4. **Individual differences**
   - Different models = different pattern/data ratios?
   - Can we measure "executive function capacity"?
   - Impulsivity as measurable trait

**Data collected:**
```yaml
session: debugging-2025-10-23
events:
  - timestamp: t0
    error: "HTTP 422: Only organization repositories..."
    data_gathered: false
    pattern_activated: "remove-json-fields"
    pattern_strength: 0.85
    action_timing: 5_seconds
    outcome: failed
    intervention_missed: true
    should_have: "searched for personal repo limitations"

  - timestamp: t1
    error: "Vulnerability alerts must be enabled..."
    data_gathered: false
    pattern_activated: "retry-same-command"
    pattern_strength: 0.75
    action_timing: 3_seconds
    outcome: failed_initially
    intervention_triggered: user_asked_questions
    then: paused_and_searched
    outcome_after_pause: succeeded
```

### Practical Configuration

**MCP server stack:**
```json
{
  "mcpServers": {
    "mnemex": {
      "command": "mnemex-server",
      "role": "persistent_memory"
    },
    "clear-thought": {
      "command": "clear-thought-server",
      "role": "strategic_mental_models"
    },
    "anastrophex": {
      "command": "anastrophex-server",
      "role": "executive_function",
      "config": {
        "enforce_pause_after_error": true,
        "min_pause_seconds": 10,
        "block_batching_during_errors": true,
        "require_verbosity_escalation": true,
        "mnemex_integration": true
      }
    }
  }
}
```

**Interaction flow:**
1. AI makes request → Anastrophex monitors
2. Error occurs → Anastrophex enforces pause
3. AI queries Clear-Thought → Strategic approach
4. AI executes with tactics → Anastrophex verifies
5. Outcome recorded → Mnemex persists
6. Next time → Mnemex informs Anastrophex

### Why This Architecture Works

**Clear-thought** answers: "How should I approach this problem?"
**Anastrophex** answers: "What command should I run right now? And WAIT - don't run it yet."
**Mnemex** answers: "Here's what happened last time you tried that pattern."

Together they form a complete cognitive support system:
- **Strategic framework** (clear-thought): Mental models
- **Tactical implementation** (anastrophex): Concrete actions
- **Executive function** (anastrophex): Impulse control, attention management
- **Pattern detection** (anastrophex): Recognize loops before they start
- **Persistent memory** (mnemex): Learning across sessions
- **Research platform** (mnemex): Study cognition itself

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
