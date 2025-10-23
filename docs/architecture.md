# Architecture Design

## System Overview

The behavior MCP server sits between Claude and the development environment, monitoring patterns and injecting directives.

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Session                       │
│  (Fresh each time, no memory of past sessions)         │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Tool calls, commands
                 ↓
┌─────────────────────────────────────────────────────────┐
│              Behavior MCP Server                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │  Pattern Detector                                │  │
│  │  - Watches tool call stream                      │  │
│  │  - Counts repetitions                            │  │
│  │  - Matches against known patterns                │  │
│  └─────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌─────────────────────────────────────────────────┐  │
│  │  Directive Injector                              │  │
│  │  - Loads from ~/.claude/CLAUDE.md                │  │
│  │  - Matches context (repo, task, tool)            │  │
│  │  - Injects timely reminders                      │  │
│  └─────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌─────────────────────────────────────────────────┐  │
│  │  Learning System (via Mnemex)                    │  │
│  │  - Records pattern occurrences                   │  │
│  │  - Tracks intervention effectiveness             │  │
│  │  - Persists across Claude sessions               │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│                    Mnemex Graph                         │
│  - Pattern library                                      │
│  - Effectiveness metrics                                │
│  - Context associations                                 │
│  - Reinforcement learnings                              │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Pattern Detector

**Purpose:** Monitor Claude's behavior for known failure patterns

**How it works:**
```python
class PatternDetector:
    def __init__(self):
        self.tool_history = []  # Last N tool calls
        self.patterns = load_patterns()  # From mnemex

    def add_tool_call(self, tool_name, args, result):
        self.tool_history.append({
            'tool': tool_name,
            'args': args,
            'result': result,
            'timestamp': now()
        })

        # Check for pattern matches
        for pattern in self.patterns:
            if pattern.matches(self.tool_history):
                return pattern
        return None
```

**Detection criteria:**

1. **Repetition count**
   - Same tool called N times with similar args
   - Example: `Edit(file.py)` called 3 times in 5 minutes

2. **Tool sequence patterns**
   - Known bad sequences: Edit → Push → CI fail → Edit → Push
   - Good sequences would skip detection

3. **Error signatures**
   - Same error message appearing multiple times
   - Specific error patterns from logs

4. **Time-based patterns**
   - Rapid attempts (< 1 minute between tries)
   - Multiple commits in short window

**Data structure:**
```python
@dataclass
class Pattern:
    id: str
    name: str
    description: str
    trigger_conditions: Callable[[List[ToolCall]], bool]
    intervention: Intervention
    context_filters: Dict[str, Any]  # repo_type, language, etc.
```

### 2. Directive Injector

**Purpose:** Provide timely, context-aware reminders from CLAUDE.md

**How it works:**
```python
class DirectiveInjector:
    def __init__(self):
        self.directives = load_directives()  # From CLAUDE.md parsing

    def inject_for_pattern(self, pattern, context):
        # Find relevant directive
        directive = self.match_directive(pattern, context)

        # Format reminder
        reminder = self.format_reminder(
            pattern=pattern,
            directive=directive,
            context=context
        )

        return reminder
```

**Reminder format:**
```
⚠️ Loop detected: [Pattern name]

[CLAUDE.md quote]

Suggestion: [Specific action to take]
Expected outcome: [What should happen]
```

**Timing strategies:**

1. **Preventive** (preferred)
   - After N-1 attempts, before the Nth
   - Example: After 2 formatting edits, before 3rd

2. **Reactive**
   - After Nth attempt, when loop is clear
   - Example: After 3 failed attempts with same error

3. **Context-triggered**
   - When entering known problem context
   - Example: When CI fails with known error pattern

**Injection methods:**

1. **Tool result augmentation**
   ```python
   original_result = tool.execute(args)
   if pattern_detected:
       augmented_result = f"{original_result}\n\n{reminder}"
       return augmented_result
   ```

2. **Separate MCP resource**
   - Expose `behavior://alerts/current`
   - Claude can query proactively

3. **System message injection** (if supported)
   - Add to context window
   - Most visible but may be intrusive

### 3. Learning System (Mnemex Integration)

**Purpose:** Persist learnings across Claude sessions and improve over time

**Mnemex graph structure:**

```
Node: Pattern
  - id: "black-formatting-loop"
  - name: "Black Formatting Loop"
  - description: "Manual edits instead of running formatter"
  - trigger_count: 5
  - detection_accuracy: 0.8

Node: Intervention
  - id: "black-loop-reminder-v1"
  - message: "Use black file.py instead of guessing"
  - shown_count: 3
  - worked_count: 2
  - effectiveness: 0.67

Node: Context
  - id: "python-test-repo"
  - repo_type: "test"
  - language: "python"
  - tools: ["black", "pytest", "mypy"]

Edges:
  Pattern --[occurs_in]--> Context
  Pattern --[remedied_by]--> Intervention
  Intervention --[effective_in]--> Context
```

**Learning queries:**

```python
# Has this pattern been seen before?
def check_pattern_history(pattern_signature):
    return mnemex.search(
        query=f"pattern:{pattern_signature}",
        type="pattern"
    )

# What intervention works best in this context?
def get_best_intervention(pattern, context):
    return mnemex.query("""
        MATCH (p:Pattern {id: $pattern_id})-[r:remedied_by]->(i:Intervention)
        WHERE i.effectiveness > 0.5
        AND EXISTS {
            MATCH (i)-[:effective_in]->(c:Context)
            WHERE c.repo_type = $context.repo_type
        }
        RETURN i ORDER BY i.effectiveness DESC LIMIT 1
    """)

# Record outcome
def record_outcome(pattern, intervention, worked):
    mnemex.update(f"""
        MATCH (i:Intervention {id: $intervention_id})
        SET i.shown_count += 1
        SET i.worked_count += ${1 if worked else 0}
        SET i.effectiveness = i.worked_count / i.shown_count
    """)
```

**Reinforcement loop:**

```
Session 1:
  1. Pattern detected (Black loop)
  2. No history in mnemex
  3. Use default intervention
  4. Record: "shown, outcome unknown"

Session 2:
  1. Same pattern detected
  2. Query mnemex: "Has this worked before?"
  3. Mnemex: "Used once, outcome unknown"
  4. Use same intervention
  5. This time, user reports it worked
  6. Record: "shown 2, worked 1, effectiveness 0.5"

Session 3:
  1. Same pattern detected
  2. Query mnemex: effectiveness = 0.5
  3. Use intervention (proven somewhat effective)
  4. Monitor outcome
  5. Update effectiveness score
```

## MCP Interface

### Resources (Read-Only)

**1. Pattern Library**
```
behavior://patterns/all
  - List all known patterns
  - Include detection criteria
  - Show effectiveness scores

behavior://patterns/{pattern_id}
  - Detailed pattern information
  - Historical data from mnemex
```

**2. Current Alerts**
```
behavior://alerts/active
  - Currently triggered patterns
  - Pending interventions
  - Context information
```

**3. Directive Index**
```
behavior://directives/all
  - All directives from CLAUDE.md
  - Categorized by type
  - Mapped to patterns
```

### Tools (Interactive)

**1. Report Outcome**
```
report_outcome(
    pattern_id: str,
    intervention_id: str,
    worked: bool,
    notes: str
)
```
Allows Claude or user to report if intervention was effective.

**2. Query Pattern History**
```
query_pattern_history(
    signature: str,
    context: Dict[str, Any]
) -> PatternHistory
```
Check if pattern has been seen before in similar context.

**3. Request Intervention**
```
request_intervention(
    pattern_id: str,
    context: Dict[str, Any]
) -> Intervention
```
Explicitly ask for guidance on a pattern.

## Implementation Phases

### Phase 1: Basic Detection
- Monitor tool call stream
- Detect simple repetition (same tool N times)
- Log to mnemex (no intervention yet)
- Build pattern library from real usage

### Phase 2: Directive Injection
- Parse CLAUDE.md for directives
- Match patterns to directives
- Inject reminders in tool results
- Track if Claude behavior changes

### Phase 3: Learning System
- Record intervention effectiveness
- Query mnemex for historical data
- Adapt interventions based on success rate
- Build context associations

### Phase 4: Advanced Patterns
- Multi-tool sequences
- Time-based patterns
- Context-aware triggers
- Predictive interventions

## Success Metrics

**Primary:**
- **Loop break rate**: % of loops broken before 5 attempts
- **Intervention effectiveness**: % of reminders that change behavior
- **Time saved**: Estimated commits/minutes saved

**Secondary:**
- Pattern detection accuracy
- False positive rate (alerts when no loop exists)
- Coverage (% of failure modes with patterns)

**Qualitative:**
- User satisfaction ("Did this help?")
- Claude learning curve (do patterns reduce over time?)
- Documentation quality (are patterns well-described?)

## Technical Considerations

### Performance
- Tool call monitoring must be lightweight (< 10ms overhead)
- Mnemex queries should be cached
- Pattern matching should be efficient (indexed)

### Privacy
- All data stays local (mnemex is local)
- No external tracking
- User controls what patterns are tracked

### Extensibility
- Easy to add new patterns (YAML or code)
- Pluggable intervention strategies
- Custom context filters

### Testing
- Simulated tool call streams
- Known loop scenarios
- Effectiveness tracking in test environment

## Open Questions

1. **Timing precision**: How do we know WHEN to inject?
   - Too early: Not obvious it's a loop yet
   - Too late: Claude already wasted time

2. **Reminder format**: What actually works?
   - Direct quote from CLAUDE.md?
   - Paraphrased suggestion?
   - Explicit command to run?

3. **False positives**: How to handle?
   - 3 edits might be legitimate refactoring
   - Distinguish loop from valid iteration

4. **Effectiveness measurement**: How to know if it worked?
   - Behavior change?
   - User feedback?
   - Outcome (CI passing)?

5. **Context detection**: How granular?
   - Repo level? (crewai-test vs mnemex)
   - File level? (pyproject.toml vs .py files)
   - Task level? (debugging vs new feature)

---

**Next:** Start with Phase 1 - basic detection and logging. Learn what patterns actually occur in practice before building sophisticated interventions.
