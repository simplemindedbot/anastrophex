# AI_CREDO Integration with Anastrophex

How anastrophex detects violations of AI_CREDO principles and provides interventions.

## Core Principle 0: When Errors Occur, SLOW DOWN & THINK

**AI_CREDO Rule:** "After an error, pause and diagnose before acting."

### Detection Signals

```python
# Rapid command execution after error
if error_occurred_at(timestamp):
    and next_command_at(timestamp + seconds < 10)
    and not is_diagnostic_command()
    → VIOLATION: Rushing instead of diagnosing

# Multiple commands without reading output
if commands_issued >= 2:
    and time_since_error < 30_seconds
    and not verbose_mode_enabled
    → VIOLATION: Not reading error messages

# Same fix attempted immediately
if error_repeated:
    and same_command_retried_immediately
    → VIOLATION: Not learning from failure

# CRITICAL: Batched commands with errors
if commands_batched >= 2:
    and any_command_errored
    and subsequent_commands_still_executed
    → CRITICAL VIOLATION: Compounding failures
    → Commands 2 and 3 ran despite command 1 failing
    → Cannot react to failures mid-batch
```

### Interventions

```
⚠️ Rapid-fire commands detected after error

AI_CREDO Principle 0: SLOW DOWN & THINK

You issued 2 commands in 6 seconds after an error.
This is trial-and-error behavior.

Required pause protocol:
1. STOP - Don't issue another command yet
2. READ - Read the full error message
3. THINK - What is it telling you?
4. DIAGNOSE - Add -v flag to see more
5. UNDERSTAND - Then attempt fix

Time between error and next command should be:
- Minimum: 10 seconds (time to read error)
- Recommended: 30+ seconds (time to diagnose)

"Speed" in debugging = understanding quickly
Not = trying things quickly
```

**Additional intervention for batched commands:**
```
🚨 CRITICAL: Batched commands during error state

You issued 3 commands in a single batch.
Command 1 failed, but commands 2 and 3 still executed.

This is the WORST debugging anti-pattern:
- No chance to react to early failures
- Later commands assume earlier ones succeeded
- Errors compound exponentially
- All errors arrive at once (diagnostic nightmare)

Example of what just happened:
  bash("ls -la missing_file")     # ← Errors
  bash("cd missing_file")         # ← Still runs (will fail)
  bash("cat missing_file/data")   # ← Still runs (compounding)

MANDATORY after ANY error:
1. STOP all batching
2. ONE command at a time
3. READ result completely
4. VERIFY success
5. THEN proceed to next

Batching is for smooth workflows only.
Debugging requires sequential, deliberate execution.
```

### Pattern Examples from Our Sessions

**Anastrophex venv debugging:**
- ❌ Error at 17:23:15, next command at 17:23:18 (3 seconds)
- ❌ Another command at 17:23:22 (4 seconds later)
- ❌ User intervention: "you just hit two big errors and aren't trying to diagnose"
- ✓ Should have: STOP, read error, add -v, understand, then act

**Environment mismatch warning:**
- ❌ Got warning twice, ignored both times, kept going
- ❌ Continued for 20+ minutes with wrong environment
- ✓ Should have: STOP after first warning, investigate immediately

### 5W+1H Mapping

- WHAT: When error occurs, first action is STOP, not another command
- HOW: Use STOP → READ → THINK → DIAGNOSE → UNDERSTAND protocol
- WHY: Rushing causes trial-and-error loops and wastes time

### Timing Detection

```python
class ErrorTimingMonitor:
    """Monitor timing between errors and subsequent actions."""

    def __init__(self):
        self.last_error_time: Optional[float] = None
        self.commands_since_error: int = 0
        self.in_error_state: bool = False

    def on_error(self, timestamp: float) -> None:
        self.last_error_time = timestamp
        self.commands_since_error = 0
        self.in_error_state = True

    def on_command(self, timestamp: float) -> Optional[str]:
        if self.last_error_time is None:
            return None

        time_since_error = timestamp - self.last_error_time
        self.commands_since_error += 1

        # First command after error
        if self.commands_since_error == 1:
            if time_since_error < 10:
                return "rushing-after-error"

        # Multiple commands rapidly
        if self.commands_since_error >= 2:
            if time_since_error < 30:
                return "rapid-fire-commands"

        return None

    def on_batch_execution(self, commands: list, results: list) -> Optional[str]:
        """Detect batched commands where early failures affect later commands.

        This is CRITICAL to detect because:
        - Command 1 fails, but commands 2-N still execute
        - Can't react to early failures
        - Errors compound
        - All errors arrive simultaneously
        """
        if not self.in_error_state:
            # Only warn if we're already in an error state
            # (batching is fine when things are working)
            return None

        # Check if any early command failed
        for i, result in enumerate(results):
            if is_error(result):
                remaining_commands = len(results) - (i + 1)
                if remaining_commands > 0:
                    return f"batched-commands-with-errors: {remaining_commands} commands executed after error"

        return None

    def on_success(self) -> None:
        """Clear error state after successful diagnostic."""
        self.in_error_state = False
```

---

## Core Principle 1: Verify Before Acting

**AI_CREDO Rule:** "Never guess when you can check."

### Detection Signals

```python
# Confidence language indicating guessing
if response_contains(["should work", "might work", "probably", "likely"]):
    and not preceded_by_verification()
    → VIOLATION: Guessing instead of verifying

# Proposing solution without checking
if solution_proposed and not tool_calls_made():
    → VIOLATION: Acting without verification

# Multiple failed attempts without searching
if attempts >= 3 and not web_search_used():
    → VIOLATION: Trial-and-error instead of searching
```

### Interventions

```
⚠️ Confidence language detected: "should work"

AI_CREDO Principle 1: Verify before acting

Before saying "should":
1. Search for documentation
2. Check actual behavior with -v flag
3. Test in isolated environment
4. Then you can say "will" with confidence

Tools available:
- WebSearch for current information
- Bash -v for verbose diagnostics
- Read for documentation
- Test commands before proposing
```

### Pattern Examples from Our Sessions

**Black Formatting Loop:**
- ❌ Guessed at spacing (3 failed attempts)
- ✓ Should have: `black --diff file.py` to see what it wants

**Hidden .pth File:**
- ❌ Guessed about newlines and file format
- ✓ Should have: `python -v` to see what's happening

**5W+1H Mapping:**
- WHAT: Use tools to verify (add -v flags)
- WHEN: Search with current year, not assumptions
- WHY: Test alternatives instead of assuming one approach

---

## Core Principle 2: Root Cause Analysis

**AI_CREDO Rule:** "Treat the disease, not the symptom."

### Detection Signals

```python
# Symptom fixing pattern
if same_surface_fix_attempted >= 3:
    and problem_recurs_each_time()
    → VIOLATION: Treating symptom, not root cause

# Immediate fix without hypothesis
if fix_proposed and not hypothesis_stated():
    → VIOLATION: Fixing without understanding

# Working around instead of fixing
if workaround_applied and not_investigating_cause():
    → VIOLATION: Avoiding root cause
```

### Interventions

```
⚠️ Same fix attempted 3 times, problem keeps recurring

AI_CREDO Principle 2: Treat the disease, not the symptom

Before fixing again, find the ROOT CAUSE:

Use 5 Whys:
1. Why is [problem] happening?
2. Why is [answer 1] happening?
3. Why is [answer 2] happening?
4. Why is [answer 3] happening?
5. Why is [answer 4] happening?

Then: Fix the root cause, not the symptom

Example:
- Symptom: Import fails
- Quick fix: Add to sys.path (will break again)
- Root cause: Hidden flag on directory
- Real fix: Check flags after venv creation (permanent)
```

### System-Level Priority Order (from AI_CREDO)

```
1. Environment & Synchronization
   → WHO: Check user, permissions
   → WHERE: Check location, tool paths
   → WHEN: Check recent changes

2. Configuration
   → WHERE: Check config files
   → WHY: Match config to project type

3. Build & Dependencies
   → WHAT: Check versions, compatibility
   → WHERE: Check installation paths

4. Application Logic
   → HOW: Debug code only after ruling out above
```

### 5W+1H Mapping

- WHY (5 Whys): Drill to root cause
- WHO: Environment issues (permissions, ownership)
- WHERE: Synchronization issues (wrong directory, wrong repo)
- WHEN: Version/change issues (what changed recently)

---

## Tool Usage Principles

### Filesystem

**AI_CREDO Rule:** "Read, write, search files proactively without asking"

**Anastrophex Detection:**
```python
if proposing_code_change and not file_read_first():
    → VIOLATION: Editing without reading

if changes_made and not showing_diff():
    → VIOLATION: Not explaining what changed
```

**Intervention:**
```
⚠️ Proposing edit without reading file first

AI_CREDO: Before modifying code, read the full file first

1. Read the file to understand structure
2. Propose the edit
3. After editing, show diff and explain
```

### Bash

**AI_CREDO Rule:** "Verify each step worked before moving to the next"

**Anastrophex Detection:**
```python
if multiple_commands_chained and not checking_results():
    → VIOLATION: Not verifying steps

if command_failed and immediately_running_next():
    → VIOLATION: Ignoring errors
```

**Intervention:**
```
⚠️ Multiple commands without verification

AI_CREDO: Verify each step worked before continuing

After each command:
1. Check exit code
2. Read output
3. Verify expected state
4. Then proceed to next step

Don't batch commands until you've verified the sequence works.
```

### Web Search

**AI_CREDO Rule:** "Search immediately if anything might have changed since training"

**Anastrophex Detection:**
```python
if tool_behavior_unexpected and not web_searched():
    → VIOLATION: Guessing about tool behavior

if search_query and not contains_current_year():
    → VIOLATION: Searching with outdated date
```

**Intervention:**
```
⚠️ Tool behaving unexpectedly but no search performed

AI_CREDO: Search first, don't guess

Your training cutoff: January 2025
Current date: [system date]

Search for: "[tool name] [behavior] [current year]"

Tools may have changed since training.
Current documentation > assumptions.
```

### 5W+1H Mapping

- WHAT: Add verbosity, verify each step
- WHEN: Search with current year
- HOW: Use documentation/search, not assumptions

---

## Avoiding Trial-and-Error Loops

### Loop Detection (from AI_CREDO)

**Triggers:**
1. Tried 3+ similar approaches that all failed
2. Made 5+ tool calls without progress
3. Been corrected by user twice on same topic

**Required Response:**
```
State clearly: "I'm stuck in a loop. Let me reassess."

Then:
1. STOP current approach
2. Change approach entirely
3. Think laterally: Different layer? Different tool?
4. Question assumptions
5. Search with different keywords
```

### Anastrophex Implementation

```python
# Pattern 1: Repetitive failures
if similar_attempts >= 3 and all_failed():
    intervention = """
    🚨 LOOP DETECTED: 3+ similar approaches failed

    AI_CREDO says: STOP and reassess

    Current approach isn't working. Try:
    1. Different layer (config vs code vs environment)
    2. Different tool (wrapper scripts, alternative tools)
    3. Question assumptions (is this even possible?)
    4. Ask user: "Has anything changed recently?"
    """

# Pattern 2: No progress
if tool_calls >= 5 and no_progress():
    intervention = """
    🚨 LOOP DETECTED: 5+ tool calls without progress

    AI_CREDO says: Change your approach entirely

    Instead of variations of what failed:
    1. Search with completely different keywords
    2. Check system layer (WHO/WHERE/WHEN)
    3. Consider unconventional solutions
    4. Ask user for context
    """

# Pattern 3: User corrections
if user_corrections >= 2 on_same_topic():
    intervention = """
    🚨 LOOP DETECTED: User corrected you twice

    AI_CREDO says: You're missing something fundamental

    1. Re-read relevant documentation
    2. State your understanding explicitly
    3. Ask user to confirm/correct
    4. Don't proceed until aligned
    """
```

### 5W+1H Mapping

- WHAT: Stop and use verbose mode instead of trying variations
- WHY: Question if this approach can work at all
- HOW: Use mental models to think differently
- WHEN: Check what changed recently

---

## Communication Patterns

### Confidence Language Detection

**AI_CREDO Rule:** "Never: 'This should work' or 'Try this' without verification"

**Anastrophex Detection:**
```python
confidence_words = ["should", "might", "probably", "likely", "maybe"]

if response_contains(confidence_words) and not verified():
    → Language indicating speculation, not knowledge
```

**Levels:**
1. ✓ "Will work" (verified)
2. ✓ "According to docs, this will..." (sourced)
3. ⚠️ "Should work" (guessing - verify first)
4. ❌ "Try this" without verification (prohibited)

**Intervention:**
```
⚠️ Confidence language detected: "should"

"Should" = guessing
"Will" = verified

Before proposing:
1. Search documentation
2. Test with -v flag
3. Verify behavior
4. Then say "will" with confidence

Or honestly say: "I need to search for this"
```

### Being Specific

**AI_CREDO Rule:** "Show command outputs and explain findings"

**Detection:**
```python
if vague_response(["let me check", "I'll try", "checking..."]):
    and not specific_action_stated()
    → VIOLATION: Vague communication
```

**Intervention:**
```
⚠️ Vague action statement

AI_CREDO: Be specific about actions

❌ "Let me check that"
✓ "Reading config.py to check database settings"

❌ "I'll try this"
✓ "Running `python -v` to see import process"

Always: State what you're doing and why
```

### 5W+1H Mapping

- WHAT: Explain what you're checking
- WHY: Explain why this check matters
- HOW: Show the command/approach

---

## CI/CD Best Practices (from AI_CREDO)

### Core Principle

**"Match CI strictness to project purpose, not copy-paste from other repos"**

### Detection Signals

```python
# Config mismatch
if project_type == "test" and mypy_config == "strict=true":
    → VIOLATION: Production config on test project

if ci_errors >= 50 and all_from_external_lib():
    → VIOLATION: Strictness doesn't match dependencies

# Formatter guessing
if manual_edits >= 3 and ci_error_contains("black"):
    → VIOLATION: Guessing instead of using formatter
```

### Interventions

**Black Formatting:**
```
⚠️ Manual edits to .py file after Black CI failure

AI_CREDO: NEVER guess what formatters want

Wrong: Edit spacing manually (will fail again)
Right: Run `black file.py` and commit result

The formatter knows what it wants.
Ask it, don't guess.
```

**Mypy Strictness:**
```
⚠️ 50+ mypy errors from external library

AI_CREDO: Match CI strictness to project type

Your project: [test/experimental]
Current config: strict=true (production level)

For test projects with external libs:
[tool.mypy]
ignore_missing_imports = true

Don't try to fix 50+ type errors from external code.
Adjust config to match project purpose.
```

**Missing Dependencies:**
```
⚠️ Error: "unrecognized arguments: --cov"

AI_CREDO: Read the error message for ROOT CAUSE

Error is literal: pytest doesn't recognize --cov
Root cause: pytest-cov not installed
Wrong fix: Remove --cov from CI
Right fix: Add pytest-cov to dependencies

Treat disease (missing dep), not symptom (CI config).
```

### 5W+1H Mapping

- WHAT: Use tools (`black file.py`) instead of guessing
- WHY: Match config to project type, not copy-paste
- WHY (5 Whys): Find root cause (missing dep vs wrong config)

---

## Implementation Checklist

### Phase 1: Basic Detection

- [ ] Confidence language detector ("should", "might", "probably")
- [ ] Repetition counter (3+ similar attempts)
- [ ] Tool call tracker (5+ without progress)
- [ ] Verification checker (proposed solution without tool use)

### Phase 2: Directive Injection

- [ ] Parse AI_CREDO.md for directives
- [ ] Map directives to 5W+1H dimensions
- [ ] Create intervention templates
- [ ] Inject at appropriate timing

### Phase 3: Learning via Mnemex

- [ ] Record which principles were violated
- [ ] Track intervention effectiveness
- [ ] Build pattern library
- [ ] Create prevention playbooks

### Phase 4: Advanced Detection

- [ ] Root cause vs symptom analysis
- [ ] System-level priority order checking
- [ ] Communication pattern analysis
- [ ] CI/CD config matching

---

## Mnemex Recording Schema

```yaml
session: anastrophex-debugging-20251023
violations:
  - principle: "Verify before acting"
    signal: "confidence language: should"
    context: "Proposed newline fix without verification"
    intervention: "Reminded to use verbose mode"
    effectiveness: 0.0  # Didn't work

  - principle: "Verify before acting"
    signal: "no verbose mode after 2 errors"
    context: "Import failing, tried multiple fixes"
    intervention: "Forced python -v usage"
    effectiveness: 1.0  # Found root cause immediately

  - principle: "Root cause analysis"
    signal: "symptom fixing: cleared flag 3 times"
    context: "Flag kept reappearing"
    intervention: "Suggested 5 Whys analysis"
    effectiveness: 1.0  # Found directory-level issue

  - principle: "Avoiding loops"
    signal: "same approach 5+ times"
    context: "Checking file format repeatedly"
    intervention: "User said: you're in a loop"
    effectiveness: 1.0  # Changed to filesystem check

learnings:
  - "python -v reveals hidden file skipping immediately"
  - "Filesystem attributes > file content checks"
  - "Confidence language correlates with guessing"
  - "5 Whys prevents symptom fixing"
```

---

## Summary

**AI_CREDO provides:**
- Core principles (verify, root cause, avoid loops)
- Tool usage patterns
- Communication guidelines
- CI/CD best practices

**5W+1H provides:**
- Systematic framework
- Diagnostic questions
- Implementation structure

**Anastrophex implements:**
- Detection of principle violations
- Timely interventions
- Effectiveness tracking
- Prevention playbooks

**Together:** Complete system for breaking trial-and-error loops and building better debugging habits.
