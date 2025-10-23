# The 5W+1H Debugging Framework

Systematic approach to debugging that prevents trial-and-error loops by asking the right questions in order.

## Core Rule: When Errors Occur, SLOW DOWN & THINK

**Before doing anything after an error:**

```
⚠️ ERROR OCCURRED

STOP  → Don't immediately try another command
READ  → Read the error message completely
THINK → Consider what it's actually telling you
PLAN  → Decide on diagnostic approach (5W+1H)
THEN  → Execute one diagnostic step at a time
```

**Anti-pattern to avoid:**
```
Error → Try fix 1 → Error → Try fix 2 → Error → Try fix 3...
[Rapid-fire attempts without understanding]
```

**Correct pattern:**
```
Error → STOP → Read error → Add -v → Read verbose output → Understand → Fix
[Deliberate, diagnostic approach]
```

This principle applies to ALL dimensions of 5W+1H. Rushing leads to:
- Skipping important diagnostic output
- Missing obvious clues in error messages
- Repeating failed approaches
- Not noticing warnings
- Trial-and-error loops

**CRITICAL: Batched commands are even worse**

When you issue multiple commands in parallel (e.g., 3 bash calls at once):
- If command 1 errors, commands 2 and 3 STILL EXECUTE
- No opportunity to react to early failures
- Later commands may depend on earlier ones succeeding
- Errors compound exponentially
- All errors arrive simultaneously (diagnostic chaos)

**Rule:** After ANY error, switch to ONE command at a time.

Batching is for smooth workflows. Debugging requires sequential execution.

**Slow down. One step at a time. Understand before acting.**

---

## Framework Overview

When a command fails or behavior is unexpected, work through these questions systematically:

```
WHO → WHAT → WHERE → WHEN → WHY → HOW
```

Each question builds on the previous, creating a complete diagnostic picture before attempting fixes.

---

## WHO: Permissions and Identity

**Question:** Who is running this? Who should be running it? Who owns the resources?

### Checks to Run

```bash
# Who am I?
whoami
id

# Who owns this file/directory?
ls -l file.txt
ls -ld directory/

# What are the permissions?
ls -la

# Am I in the right group?
groups

# Should this run as sudo?
# (Check if error mentions permissions, access denied, etc.)
```

### Common Issues

- ✗ Running as wrong user (need sudo or specific user)
- ✗ File owned by different user/group
- ✗ SSH key belongs to different user
- ✗ Git configured with wrong identity
- ✗ Venv created by different user

### Interventions

```
⚠️ Permission denied error detected

WHO checks:
1. whoami → Are you the right user?
2. ls -l → Who owns the file causing the error?
3. groups → Are you in the required group?

If running as wrong user:
- sudo command (if you need root)
- su - username (if you need different user)
- Fix ownership: chown -R user:group path/
```

### Pattern Detection

```python
if error_contains(["permission denied", "access denied", "EACCES"]):
    run_who_checks()
```

---

## WHAT: Actions and Diagnostics

**Question:** What should I do to diagnose this? What information do I need?

### Diagnostic Actions

```bash
# ESCALATE VERBOSITY (Most important!)
command -v        # Verbose mode
command -vv       # Very verbose
command --debug   # Debug mode
command --trace   # Trace execution

# CHECK ERROR MESSAGES AS THEY ARRIVE
# Don't wait until all errors accumulate
# Read each error immediately and adjust

# SLOW DOWN
# Don't rush through multiple commands
# One diagnostic at a time
# Verify each result before proceeding
```

### The Verbosity Ladder

```
1st error  → Add -v
2nd error  → Add -vv
3rd error  → Add --debug/trace
4th error  → Check WHO/WHERE/WHEN
5th error  → Question WHY (is this the right approach?)
```

### Common Issues

- ✗ Skipping verbose output
- ✗ Batch running multiple commands without reading results
- ✗ Ignoring warnings and continuing
- ✗ Not reading error messages carefully
- ✗ Guessing at solutions instead of diagnosing

### Interventions

```
⚠️ Command failed without verbose mode

WHAT you should do:
1. Run with -v flag to see what's happening
2. Read the verbose output completely
3. Identify the exact failure point
4. Then attempt fix

Don't guess. See what's actually happening first.
```

### Pattern Detection

```python
if command_failed and not used_verbose_flag:
    suggest_verbosity()

if same_error_count >= 2 and not increased_verbosity:
    force_verbosity_escalation()
```

---

## WHERE: Location and Context

**Question:** Where am I? Where should I be? Where else is this happening?

### Checks to Run

```bash
# Where am I?
pwd

# Am I in the right directory?
ls -la  # Check if expected files are here
git remote -v  # Check repo context

# Where is the actual file/command?
which python
readlink /path/to/symlink

# Where is this installed?
pip show package
npm list package
brew list package

# Is this a global issue?
# Search: "package-name error-message 2025"
# Check GitHub issues
# Check other projects
```

### Common Issues

- ✗ Wrong working directory (expected ~/project, in ~/project/subdir)
- ✗ Wrong repository (expected repo-A, in repo-B)
- ✗ Tool not in PATH
- ✗ Symlink pointing to wrong location
- ✗ Using wrong Python/Node/etc. (pyenv vs mise vs system)
- ✗ Problem is specific to this repo's configuration

### Real Example: Anastrophex venv

```bash
# WHERE is Python?
which python
# → /Users/sc/.pyenv/shims/python (pyenv)

# WHERE is the venv's Python?
readlink .venv/bin/python
# → /Users/sc/.local/share/uv/python/... (uv!)

# WHERE should it be?
mise where python
# → /Users/sc/.local/share/mise/installs/python/3.12.11

# ✗ MISMATCH! Venv using wrong Python distribution
```

### Interventions

```
⚠️ Tool behaving unexpectedly

WHERE checks:
1. pwd → Are you in the right directory?
2. which tool → Is this the right installation?
3. readlink symlink → Is this pointing where you expect?
4. Search "tool version error" → Is this a known issue?

If in wrong location:
- cd to correct directory
- Update symlinks
- Recreate with correct tool
```

### Pattern Detection

```python
if tool_succeeds_elsewhere and fails_here:
    check_where_context()

if expected_file_missing:
    verify_current_directory()
```

---

## WHEN: Temporal Context

**Question:** When did this start? When was this working? What's changed?

### Checks to Run

```bash
# What's today's date?
date
date +%Y  # What year for searches?

# When was this file last modified?
ls -lt file.txt
stat file.txt

# When was this working?
git log --since="1 week ago"
git log -p file.txt  # When did this file change?

# What changed recently?
git diff HEAD~5..HEAD
git log --oneline --graph

# How old is my knowledge?
# (Check your training cutoff - search with recent year)
```

### Common Issues

- ✗ Searching with old dates (using 2023 when it's 2025)
- ✗ Not knowing when the issue started
- ✗ Not checking if something changed recently
- ✗ Using outdated documentation
- ✗ Assuming training data is current

### Real Example: Python 3.12 Hidden Files

```bash
# WHEN did this behavior change?
# → Python 3.12 added hidden file check for .pth files
# → This is new behavior, not in Python 3.11

# Search with correct year:
# ✗ "python .pth files 2023" (old results)
# ✓ "python .pth files 2025" (current results)
```

### Interventions

```
⚠️ Searching for documentation

WHEN checks:
1. date +%Y → What year is it?
2. Add current year to search: "tool problem 2025"
3. Check "what's new" in recent versions
4. Compare behavior to when it last worked

Your knowledge cutoff: January 2025
Always search with 2025 or later for current info.
```

### Pattern Detection

```python
if web_search_query and not contains_current_year(query):
    suggest_adding_year()

if environment_changed_recently:
    check_what_changed()
```

---

## WHY: Root Cause and Alternatives

**Question:** Why are we getting this error? Why this approach? Why not something simpler?

### Questions to Ask

**Surface vs. Root:**
- Is this the real problem or just a symptom?
- What's the underlying cause?
- Have we treated the disease or just the symptom?

**Necessity:**
- Do we need to fix this specific error?
- Can we simplify the approach?
- Is there a workaround?
- Can we loosen the requirements?

**Context:**
- Why is this configured so strictly?
- Is this a production package or a test project?
- Does the CI configuration match the project type?

### Common Alternatives

Instead of fixing the error, consider:

**Simplify:**
- Remove the underscore instead of fighting hidden flags
- Use simpler tool instead of complex one
- Skip optional feature that's causing issues

**Loosen:**
- Relax mypy strictness for test projects
- Set CI to `continue-on-error: true`
- Use `ignore_missing_imports = true`

**Workaround:**
- Use different command/tool
- Change configuration
- Adjust expectations

### Real Examples

**Example 1: Hidden .pth file**
- ❌ Fix: Figure out why hidden flag is set
- ✓ Workaround: Remove underscore from filename
- ✓ Simpler: Clear hidden flag with chflags

**Example 2: Mypy 77 errors**
- ❌ Fix: Add type annotations for external library
- ✓ Root cause: Config too strict for test project
- ✓ Solution: `ignore_missing_imports = true`

**Example 3: Black formatting**
- ❌ Fix: Manually edit spacing 3 times
- ✓ Root cause: Guessing instead of using tool
- ✓ Solution: `black file.py` (one command)

### Interventions

```
⚠️ Multiple attempts to fix same error

WHY questions:
1. Is this the root cause or a symptom?
2. Do we need to fix this specific error?
3. Can we simplify the approach?
4. Can we loosen the requirement?

Consider:
- Changing configuration instead of code
- Using different tool/approach
- Questioning if this check is necessary for this project type
```

### Pattern Detection

```python
if same_fix_attempted >= 3:
    question_why_this_approach()

if project_type != config_strictness:
    suggest_loosening_config()
```

---

## WHY (Deep Dive): The 5 Whys Technique

**Question:** Why is this *really* happening? (Root cause analysis)

The "5 Whys" technique drills down from symptom to root cause by repeatedly asking "why" about each answer.

### The Technique

```
Problem: [Observable symptom]
  ↓ Why?
Answer 1: [Immediate cause]
  ↓ Why?
Answer 2: [Underlying cause]
  ↓ Why?
Answer 3: [Deeper cause]
  ↓ Why?
Answer 4: [Systemic cause]
  ↓ Why?
Answer 5: [Root cause]
```

**Rule:** Stop when you reach something actionable that prevents recurrence.

### Real Example 1: Hidden .pth File

```
Problem: Import fails with ModuleNotFoundError

Why? → Package not in sys.path

Why? → .pth file not being processed

Why? → Python skipping it as "hidden"

Why? → site-packages directory has UF_HIDDEN flag

Why? → [Unknown - requires investigation]
        Could be: venv creation tool set it
                  Inherited from parent directory
                  Specific to mise's Python build

Root Cause: Filesystem attribute on directory
Actionable: Check for hidden flag after venv creation
Prevention: Add to venv creation workflow
```

**Lessons:**
- Stop at "Python skipping as hidden" = symptom fixing (clear the flag)
- Continue to "directory has flag" = root cause (why does directory have it?)
- Investigation needed: Why does mise/venv set this flag?

### Real Example 2: Black Formatting Loop

```
Problem: CI keeps failing on Black formatting

Why? → File formatting doesn't match Black's rules

Why? → Manual edits don't match what Black wants

Why? → Guessing at formatting instead of using Black

Why? → Not following directive: "use the tool, don't guess"

Why? → Directive not surfaced at the right time

Root Cause: No intervention when loop starts
Actionable: Detect 2+ manual edits to .py after Black CI failure
Prevention: Anastrophex pattern detection + intervention
```

### Real Example 3: Mypy 77 Errors

```
Problem: 77 mypy errors from external library

Why? → Library has no type stubs

Why? → External package (CrewAI) doesn't provide types

Why? → Config requires strict typing for all imports

Why? → Config copied from production package (mnemex)

Why? → Didn't match config strictness to project type

Root Cause: Config mismatch (production config on test project)
Actionable: Check project type before setting mypy strictness
Prevention: Template configs by project type, not copy-paste
```

### Real Example 4: Venv Using Wrong Python

```
Problem: Package installed but won't import

Why? → .pth file not being processed

Why? → uv's Python has .pth file bugs

Why? → Venv created with uv's Python, not mise's

Why? → `python -m venv` used first Python in PATH

Why? → Didn't use explicit path to mise's Python

Root Cause: Relying on shell PATH resolution instead of explicit paths
Actionable: Use $(mise where python)/bin/python3 -m venv .venv
Prevention: Always use explicit paths with version managers
```

### How Deep to Go

**Stop when you find:**
1. Something you can fix permanently
2. Something that prevents recurrence
3. A systemic issue, not a one-time glitch
4. A decision point where you chose wrong option

**Don't stop when you find:**
1. Just a symptom
2. Something you can only work around
3. An effect, not a cause
4. "It just happened" (keep asking why)

### 5 Whys + 5W+1H Integration

The frameworks work together:

```
WHAT: Command failed
  ↓
Add -v verbosity → See error message
  ↓
WHERE: Verify we're in right location → We are
  ↓
WHEN: Check if anything changed → Switched to mise yesterday
  ↓
WHY (5 Whys):
  Why fail? → Wrong Python
  Why wrong Python? → Venv created with uv's Python
  Why uv's Python? → PATH pointed to it
  Why PATH wrong? → Didn't use explicit mise path
  Why not explicit? → Assumed `python` command was mise

Root Cause: Shell PATH assumptions instead of explicit paths
  ↓
HOW: Mental model: "Explicit paths over shell resolution"
     Playbook: Always verify `which` matches `mise where`
```

### Template for 5 Whys

When stuck on a problem:

```markdown
## 5 Whys Analysis

**Problem:** [Observable symptom]

**Why 1:** Why is [problem] happening?
**Answer 1:** [Immediate cause]

**Why 2:** Why is [answer 1] happening?
**Answer 2:** [Underlying cause]

**Why 3:** Why is [answer 2] happening?
**Answer 3:** [Deeper cause]

**Why 4:** Why is [answer 3] happening?
**Answer 4:** [Systemic cause]

**Why 5:** Why is [answer 4] happening?
**Answer 5:** [Root cause]

**Root Cause:** [Final answer]
**Actionable Fix:** [What to do now]
**Prevention:** [How to prevent in future]
**Mental Model:** [What rule to remember]
```

### Anastrophex Integration

**When to trigger 5 Whys:**
```python
if same_symptom_fix_attempted >= 3:
    start_5_whys_analysis()

if workaround_applied_but_not_root_cause:
    suggest_5_whys()
```

**How to guide the user:**
```
⚠️ You've fixed the symptom 3 times but it keeps recurring

Let's do 5 Whys to find the root cause:

Problem: [Import fails]
Why? [Your answer]
  ↓
Why? [Next why based on your answer]
  ↓
... (continue until root cause)

Then: Fix the root cause, not the symptom
```

**Recording in mnemex:**
```yaml
pattern: import-failure-hidden-pth
five_whys:
  - why: "Package not in sys.path"
  - why: ".pth file not processed"
  - why: "Python skipping as hidden"
  - why: "Directory has UF_HIDDEN flag"
  - why: "Unknown - venv creation set it"
root_cause: "Filesystem attribute on directory"
symptom_fix: "chflags nohidden (fixes once)"
root_cause_fix: "Check flag after venv creation (prevents recurrence)"
prevention: "Add to venv creation workflow"
```

### Common Pitfalls

**❌ Stopping too early:**
```
Problem: Import fails
Why? → .pth file not processed
Fix: Manually add to sys.path

[STOPPED AT SYMPTOM - will recur next time]
```

**✓ Going deep enough:**
```
Problem: Import fails
Why? → .pth file not processed
Why? → Hidden flag set
Why? → Directory created with flag
Why? → venv tool sets it
Fix: Change venv creation process

[REACHED ROOT - won't recur]
```

**❌ Asking "how" instead of "why":**
```
Problem: Import fails
How did this happen? → I created a venv
[WRONG QUESTION - doesn't lead to root cause]
```

**✓ Focusing on causation:**
```
Problem: Import fails
Why did this happen? → .pth not processed
Why wasn't it processed? → Hidden flag
[RIGHT QUESTIONS - follows causal chain]
```

### Benefits

1. **Prevents recurrence:** Fix root cause, not symptoms
2. **Saves time:** One deep fix > many surface fixes
3. **Builds knowledge:** Root causes become prevention rules
4. **Complements 5W+1H:** WHO/WHAT/WHERE/WHEN gather data, WHY analyzes it
5. **Creates playbooks:** Root cause patterns → mnemex entries

---

## HOW: Strategy and Mental Models

**Question:** How should I think about this? How do similar problems get solved?

### Integration Points

**Clear-Thought MCP Server:**
- Binary Search → Narrow down which component fails
- Divide and Conquer → Isolate and test parts separately
- Reverse Engineering → Work backward from error
- Backtracking → Retrace steps to find divergence
- Cause Elimination → Rule out possibilities
- Program Slicing → Focus on relevant code

**Mnemex Playbooks:**
- Has this pattern been seen before?
- What intervention worked last time?
- What's the effectiveness score?
- Are we in similar context?

**Established Patterns:**
- From `docs/failure-patterns.md`
- From `docs/debugging-principles.md`
- From case studies

### Mental Model Selection

**For Format/Tool Issues:**
- "Don't guess what the tool wants - use the tool"
- Black formatting → `black file.py`
- Import sorting → `isort file.py`
- Type checking → `mypy --show-error-codes`

**For Configuration Issues:**
- "Match strictness to project type"
- Production → strict checks
- Test/experimental → relaxed checks
- Prototype → minimal checks

**For Environment Issues:**
- "Explicit paths over shell resolution"
- Don't rely on `which`
- Use full paths to tools
- Verify symlink targets

### How to Apply Mental Models

1. **Identify pattern type** (format, config, environment, etc.)
2. **Select mental model** from clear-thought or established patterns
3. **Apply tactical actions** from WHO/WHAT/WHERE/WHEN
4. **Check mnemex** for historical effectiveness
5. **Execute with verbosity** to verify

### Interventions

```
⚠️ Stuck on complex problem

HOW to approach:
1. Check mnemex: Have we seen this before?
2. Select mental model from clear-thought
3. Apply verbosity to see what's happening
4. Use divide-and-conquer to isolate issue

Example:
- Mental model: Binary Search
- Tactic: Run each component with -v
- Find: Which specific step fails
- Fix: Address that one step
```

### Pattern Detection

```python
if problem_is_complex:
    query_mnemex_for_similar()
    suggest_mental_model()

if no_historical_pattern:
    suggest_clear_thought_framework()
```

---

## Putting It All Together

### Debugging Workflow

When a command fails:

```
1. WHO   → Check permissions, user, ownership
2. WHAT  → Add -v, read output, slow down
3. WHERE → Verify location, context, installation
4. WHEN  → Check dates, recent changes, version
5. WHY   → Question approach, consider alternatives
6. HOW   → Apply mental model, check mnemex
```

**Don't skip steps.** Each question builds context for the next.

### Example: Import Fails After Install

```bash
# WHO: Check user and permissions
whoami                    # → sc
ls -la .venv/            # → owned by sc ✓

# WHAT: Add verbosity
python -v -c "import pkg" # → "Skipping hidden .pth file"
                          # ✅ Found the issue!

# WHERE: Check installation
readlink .venv/bin/python # → points to uv's python
mise where python         # → points to mise's python
                          # ✗ Mismatch!

# WHEN: When did this change?
git log .venv/           # → created today
                         # → switched from pyenv to mise yesterday
                         # ✅ Context found!

# WHY: Why is .pth hidden?
ls -lO .venv/lib/.../site-packages/
                         # → directory has "hidden" flag
                         # Can we just remove the flag?
                         # Yes! Simpler than debugging why it's set.

# HOW: Mental model
# → Clear-thought: Cause Elimination
# → Eliminated: file format, content, permissions
# → Found: filesystem attribute
# → Mnemex: No prior pattern for this
# → New pattern to record
```

### Integration with Anastrophex

**Pattern Detection:**
- Monitor for WHO issues (permission errors)
- Monitor for WHAT issues (no verbosity, rushing)
- Monitor for WHERE issues (wrong directory/tool)
- Monitor for WHEN issues (searching old years)
- Monitor for WHY issues (fixing symptoms not causes)
- Monitor for HOW issues (no mental model applied)

**Interventions:**
- Inject WHO checks when permission errors occur
- Force WHAT (verbosity) after 2nd failed attempt
- Verify WHERE when tool location seems wrong
- Add WHEN (year) to search queries automatically
- Question WHY after 3+ similar fix attempts
- Suggest HOW (mental model) for complex problems

**Mnemex Recording:**
```yaml
pattern:
  who_issues: [permission_denied, wrong_user]
  what_issues: [no_verbosity, rushed_execution]
  where_issues: [wrong_directory, wrong_tool]
  when_issues: [outdated_search, version_change]
  why_issues: [symptom_fixing, config_mismatch]
  how_issues: [no_mental_model, no_playbook]
```

---

## Benefits of 5W+1H

1. **Systematic:** Prevents skipping important checks
2. **Memorable:** Easy to remember and apply
3. **Comprehensive:** Covers tactical and strategic
4. **Integrative:** Works with clear-thought and mnemex
5. **Teachable:** Clear framework for interventions
6. **Detectable:** Each dimension has clear signals

---

## Next Steps for Anastrophex

1. **Implement WHO detection** (permission errors)
2. **Implement WHAT enforcement** (verbosity escalation)
3. **Implement WHERE verification** (directory/tool checks)
4. **Implement WHEN awareness** (date injection in searches)
5. **Implement WHY questioning** (simplification suggestions)
6. **Integrate HOW** (clear-thought + mnemex)

Each dimension becomes a monitoring point and intervention trigger.
