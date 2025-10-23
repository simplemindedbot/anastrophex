# Debugging Principles for Anastrophex

General debugging guidelines derived from real debugging sessions.

## Core Principle 1: When Errors Occur, SLOW DOWN & THINK

**Rule:** When you encounter an error, STOP before trying another command.

### The STOP Protocol

```
ERROR DETECTED
    ↓
STOP  - Don't immediately run another command
    ↓
READ  - Read the entire error message carefully
    ↓
THINK - What is this error actually saying?
    ↓
PLAN  - What diagnostic will reveal the cause?
    ↓
EXECUTE ONE diagnostic step with verbosity
    ↓
READ the output before proceeding
```

### Why This Matters

**Observed pattern from real sessions:**
- Error occurs at 17:23:15
- Next command at 17:23:18 (3 seconds later)
- Another command at 17:23:22 (4 seconds later)
- User intervention: "you just hit two big errors and aren't trying to diagnose but are still issuing commands"

**Rapid-fire commands indicate:**
- Not reading error messages
- Guessing instead of diagnosing
- About to enter trial-and-error loop
- Missing obvious clues

**Anastrophex Detection:**
```python
def detect_rushing_after_error():
    """Detect when commands are issued too quickly after errors."""
    if time_since_error < 10_seconds:
        if new_command_issued and not diagnostic_command:
            return True  # Rushing, not diagnosing
    return False
```

**Intervention:**
```
⚠️ Error just occurred - slow down

You issued a command 3 seconds after an error.
This suggests you didn't fully read the error message.

Before proceeding:
1. Read the error message completely
2. Run with -v flag to see more
3. Understand what failed
4. Then decide on fix

Rushing → trial-and-error loop
Pausing → targeted fix
```

---

## Core Principle 2: Escalate Verbosity on Errors

**Rule:** Once you hit an error, switch to verbose mode on ALL subsequent commands.

### Why This Works

When standard commands fail, you need to see what's happening under the hood:
- Python: Add `-v` or `-vv` flags
- Git: Add `--verbose` or `GIT_TRACE=1`
- Package managers: Add `-v` or `--verbose`
- Shell commands: Add `set -x` or individual `-v` flags

**Example from anastrophex debugging:**

❌ **What happened:**
```bash
# Import failed
python -c "import anastrophex"  # ModuleNotFoundError

# Tried fixing format, newlines, etc. (all failed)
# Spent 30+ minutes guessing

# Finally used verbose mode
python -v -c "import anastrophex" 2>&1 | grep pth
# Output: "Skipping hidden .pth file"
# ✅ Found root cause immediately
```

✅ **What should have happened:**
```bash
# Import failed
python -c "import anastrophex"  # ModuleNotFoundError

# IMMEDIATELY switch to verbose mode (don't guess)
python -v -c "import anastrophex" 2>&1 | grep pth
# Output: "Skipping hidden .pth file"
# ✅ Root cause found in <1 minute
```

### Implementation for Anastrophex

```python
def detect_error_without_verbose():
    """Detect when commands fail but verbose mode not used."""
    if command_failed and not used_verbose_flag:
        return True
    return False

def intervention():
    return """
⚠️ Command failed - switch to verbose mode

You've tried the command multiple times without success.
Before trying fixes, SEE what's actually happening.

For the failed command, add verbose flags:
- Python: python -v or python -vv
- pip: pip -v or pip -vvv
- git: git --verbose or GIT_TRACE=1
- pytest: pytest -vv
- npm: npm --loglevel=verbose

Verbose output shows:
- What files are being processed
- What's being skipped and why
- Internal state and decisions
- Exact error locations

Then: Read the verbose output BEFORE trying fixes.
"""
```

## Verbosity Escalation Ladder

1. **First error:** Run with `-v` (verbose)
2. **Second error:** Run with `-vv` (very verbose)
3. **Third error:** Add debug flags (`-vvv`, `--debug`, `DEBUG=1`)
4. **Fourth error:** Add tracing (`set -x`, `GIT_TRACE`, strace)

**Never repeat a failing command more than twice without increasing verbosity.**

## Language-Specific Verbose Flags

### Python
```bash
python -v script.py           # Trace imports
python -vv script.py          # More detailed tracing
python -m module -v           # Verbose mode for module
pytest -vv                    # Very verbose test output
pip install -v package        # Verbose install
pip install -vvv package      # Very verbose (shows subprocess calls)
```

### Git
```bash
git command --verbose
GIT_TRACE=1 git command
GIT_TRACE_PACKET=1 git clone  # Network debugging
GIT_CURL_VERBOSE=1 git push   # HTTPS debugging
```

### Shell/Bash
```bash
bash -x script.sh            # Print commands before execution
set -x; command; set +x      # Trace single command
sh -v script.sh              # Print lines as they're read
```

### Package Managers
```bash
npm install --loglevel=verbose
yarn --verbose
cargo build --verbose
make VERBOSE=1
```

## Debugging Escalation Pattern

```
Error occurs
    ↓
Run with -v (verbose)
    ↓
Read verbose output carefully
    ↓
Still failing?
    ↓
Run with -vv (very verbose)
    ↓
Read output carefully
    ↓
Still failing?
    ↓
Add debug/trace flags
    ↓
Read output carefully
    ↓
Still failing?
    ↓
ASK USER: "Has anything changed recently?"
```

**Key:** Actually READ the verbose output before trying fixes!

## Anti-Pattern: Trial and Error Without Verbosity

❌ **Bad debugging sequence:**
```
1. Command fails
2. Guess what's wrong
3. Try fix #1
4. Still fails
5. Guess again
6. Try fix #2
7. Still fails
8. Guess again
9. Try fix #3
... (repeat 10+ times)
```

✅ **Good debugging sequence:**
```
1. Command fails
2. Run with -v flag
3. Read verbose output
4. Identify actual cause
5. Apply correct fix
6. Success
```

## Examples from Real Sessions

### Example 1: Black Formatting Loop (crewai-test)
**Without verbosity:**
- 3 manual edits
- 3 commits
- 20+ minutes wasted

**With verbosity:**
```bash
black --diff file.py  # Shows exactly what Black wants
black file.py         # Apply it
git commit            # Done
```

### Example 2: Hidden site-packages (anastrophex)
**Without verbosity:**
- Checked .pth file format
- Tried adding newlines
- Tested splitlines()
- Checked file permissions
- ~30 minutes of guessing

**With verbosity:**
```bash
python -v -c "import package" 2>&1 | grep pth
# Output: "Skipping hidden .pth file"
# Root cause found in 30 seconds
```

### Example 3: Environment Mismatch (anastrophex)
**What happened:**
- Got warning twice
- Ignored both times
- Continued with wrong venv

**With attention to warnings:**
```bash
# See warning once
uv pip install -e .
# warning: `VIRTUAL_ENV=/Users/sc/.venv` does not match

# STOP. Investigate immediately
echo $VIRTUAL_ENV
readlink .venv/bin/python
# Found mismatch, fixed it
```

## Verbosity Best Practices

1. **Enable early:** Don't wait until you're stuck
2. **Read carefully:** Verbose output tells you what's happening
3. **Save output:** `command -v 2>&1 | tee debug.log`
4. **Search in output:** Use grep/search to find relevant parts
5. **Compare runs:** Diff verbose output from working vs broken states

## Anastrophex Pattern Detection

Detect these sequences and intervene:

```python
patterns = [
    {
        "name": "error-without-verbose",
        "detect": lambda: (
            command_failed_count >= 2 and
            not any_verbose_flags_used
        ),
        "intervention": "Switch to verbose mode before trying more fixes"
    },
    {
        "name": "repeated-failures",
        "detect": lambda: (
            same_command_failed >= 3 and
            no_verbosity_increase
        ),
        "intervention": "Increase verbosity: try -vv or --debug"
    },
    {
        "name": "ignored-warnings",
        "detect": lambda: (
            same_warning_appeared >= 2 and
            no_action_taken
        ),
        "intervention": "STOP. Investigate this warning before continuing"
    }
]
```

## Remember

> "Visibility before fixes. Understand before changing."

When something fails:
1. STOP guessing
2. ADD verbosity
3. READ output
4. THEN fix

The verbose flag is free. Guessing wastes time.
