# Case Study: CrewAI Test CI/CD Fix

**Date:** October 23, 2025
**Duration:** ~2 hours
**Total commits:** 5 (4 failed, 1 success)
**Patterns observed:** 3 distinct failure modes

---

## Initial State

**Repository:** crewai-test (test/experimental project)
**Problem:** CI pipeline failing on main branch
**CI checks:**
1. Ruff linting
2. Black formatting
3. Mypy type checking
4. Pytest tests

---

## Timeline of Events

### Attempt 1-3: The Black Formatting Loop

**Symptom:** CI fails with "Black check failed, would reformat file.py"

**What Claude did:**
1. Read error message
2. Manually edited file to remove blank lines
3. Committed and pushed
4. CI failed again with same error
5. Manually edited different whitespace
6. Committed and pushed
7. CI failed again
8. Manually edited more formatting
9. Committed and pushed

**What was wrong:**
- Guessing what Black wanted instead of running `black file.py`
- Treating symptom (wrong formatting) not disease (not using the tool)
- No web search for current Black best practices

**User intervention required:**
> "I feel like you're in a loop of trial and error. read ~/.claude/CLAUDE.md and see if you can break out of the pattern. use your debugging tools from clear thought, read documentation from github, deepwiki and context7 and BE SURE to search the web"

**What worked:**
1. Read CLAUDE.md reminder about using tools not guessing
2. Web search for "black python formatter blank line after import PEP 8"
3. Learned: Black enforces PEP 8 (2 blank lines between imports and code)
4. Ran `black file.py` to auto-format
5. Committed the changes Black made
6. ✅ Black check passed

**Pattern detected:** Black formatting loop
**Trigger:** 3+ manual edits to .py file after "Black check failed"
**Effective intervention:** "Use `black file.py` instead of guessing"

---

### Attempt 4: The Mypy Strict Config Mismatch

**Symptom:** 77 mypy type errors

**Error messages:**
```
crewai_test/src/crewai_test/simple_test.py:13: error: Skipping analyzing "crewai":
  module is installed, but missing library stubs or py.typed marker [import-untyped]

crewai_test/src/crewai_test/crew.py:26: error: "CrewaiTest" has no attribute
  "agents_config" [attr-defined]

... (75 more similar errors)
```

**Root cause analysis:**
```toml
# BEFORE (copied from mnemex - a production package)
[tool.mypy]
strict = true
disallow_untyped_defs = true
disallow_any_generics = true
disallow_any_unimported = true
```

This configuration was appropriate for mnemex (published to PyPI) but wrong for crewai-test (experimental project using CrewAI without type stubs).

**What Claude did:**
1. Read mypy errors
2. Recognized pattern: external library without type stubs
3. Web search confirmed: libraries without py.typed marker cause these errors
4. Changed config to match project type:

```toml
# AFTER (appropriate for test project)
[tool.mypy]
ignore_missing_imports = true
warn_unused_configs = true
disable_error_code = ["attr-defined", "var-annotated", "index"]
```

**Result:** 77 errors → 0 errors

**Pattern detected:** Mypy strict config in wrong project type
**Trigger:** 50+ errors, all "import-untyped" or "attr-defined", config has "strict=true"
**Effective intervention:** "Match CI strictness to project type - is this production or experimental?"

**Why this worked:**
- No loop this time - pattern was recognized immediately
- Web search provided confirmation
- Solution was systematic (config change) not incremental (fixing each error)

---

### Attempt 5: The Missing Dependency

**Symptom:** Pytest fails with "unrecognized arguments: --cov"

**Error message:**
```
pytest: error: unrecognized arguments: --cov=crewai_test --cov-report=xml
```

**Root cause:**
- CI workflow used `pytest --cov`
- Package didn't have `pytest-cov` in dev dependencies
- Error message was literal but easy to misinterpret

**What Claude did:**
1. Read error message
2. Checked pyproject.toml
3. Saw pytest-cov was missing from dev dependencies
4. Added `pytest-cov>=4.0.0`
5. ✅ Tests passed

**Pattern detected:** Missing pytest plugin
**Trigger:** Error "unrecognized arguments: --cov" AND pytest-cov not in dependencies
**Effective intervention:** "Error is literal - check if pytest-cov is installed"

**Why this worked:**
- Error message was clear ("unrecognized arguments")
- Simple diagnosis (check dependencies)
- No loop - caught immediately

---

## Final Analysis

### What Worked

1. **User intervention breaking the loop**
   - Explicit instruction to read CLAUDE.md
   - Direction to use web search and documentation tools
   - This snapped Claude out of trial-and-error mode

2. **Web search for current best practices**
   - Black formatting rules (2025 documentation)
   - Mypy configuration patterns
   - Better than guessing from training data

3. **Root cause analysis**
   - Mypy: Wrong config for project type (not wrong code)
   - Pytest: Missing dependency (not wrong workflow)
   - Treating disease not symptoms

4. **Using the actual tools**
   - `black file.py` fixed formatting in one command
   - Local verification (`black --check`, `mypy src/`) before pushing

### What Didn't Work

1. **Manual formatting edits** (attempts 1-3)
   - Wasted 3 commits
   - Never addressed root cause
   - Guessing instead of asking the tool

2. **No self-awareness of the loop**
   - Couldn't see the pattern from inside
   - Repeated same approach despite failures
   - Required external intervention

3. **Initial impulse to guess**
   - First instinct was to edit manually
   - Not to check documentation or search
   - Training: "I can fix this" → Reality: "Use the tool"

### Lessons Learned

**For future Claude sessions:**

1. **Black formatting errors → Run Black**
   - Don't edit manually
   - `black file.py` then `git diff`
   - Commit what Black produces

2. **High mypy error count → Check config**
   - 50+ errors suggests config mismatch
   - Match strictness to project type
   - Production: strict, Experimental: relaxed

3. **"Unrecognized arguments" → Check dependencies**
   - Error messages are often literal
   - Missing plugin/tool usually means not installed
   - Check pyproject.toml before changing CI

4. **3 similar attempts → STOP and search**
   - Web search breaks loops
   - Current docs > training data
   - One search > multiple guesses

**For behavior-mcp design:**

1. **Timing matters**
   - Intervene after 2 attempts, before 3rd
   - Early enough to prevent waste
   - Late enough to confirm it's a loop

2. **Directive format that works**
   ```
   ⚠️ Loop detected: [specific pattern]
   CLAUDE.md says: [relevant quote]
   Try: [exact command]
   Expected: [what should happen]
   ```

3. **Context is key**
   - Same symptom, different contexts
   - Black loop: formatting tool
   - Mypy errors: config mismatch
   - Pytest args: missing dependency

4. **Effectiveness measurement**
   - User intervention required = 100% effective
   - Pattern recognition after 1st instance = best case
   - 3+ attempts before recognition = failure

---

## Mnemex Learnings to Record

### Pattern: Black Formatting Loop
```yaml
id: black-formatting-loop-2025-10-23
trigger_count: 1
detection_criteria:
  - tool: Edit
  - file_pattern: "*.py"
  - count: >= 3
  - timeframe: 10 minutes
  - context: CI error contains "black"
intervention:
  message: "Use `black file.py` instead of manual edits"
  shown: yes (user intervention)
  worked: yes
  effectiveness: 1.0
context:
  repo: crewai-test
  repo_type: experimental
  language: python
```

### Pattern: Mypy Strict Mismatch
```yaml
id: mypy-strict-mismatch-2025-10-23
trigger_count: 1
detection_criteria:
  - error_count: >= 50
  - error_pattern: "import-untyped|attr-defined"
  - config_has: "strict = true"
intervention:
  message: "Config too strict for project type"
  shown: no
  worked: N/A (self-diagnosed)
  effectiveness: N/A
context:
  repo: crewai-test
  repo_type: experimental
  external_deps: ["crewai"]
```

### Pattern: Missing Dependency
```yaml
id: pytest-cov-missing-2025-10-23
trigger_count: 1
detection_criteria:
  - error: "unrecognized arguments: --cov"
  - dependency_missing: "pytest-cov"
intervention:
  message: "Check dependencies before changing CI"
  shown: no
  worked: N/A (quick diagnosis)
  effectiveness: N/A
context:
  repo: crewai-test
  tool: pytest
```

---

## Counterfactual: What If behavior-mcp Existed?

### After Attempt 2 (Before Attempt 3)

**Detection:**
```python
Pattern detected: black-formatting-loop
Confidence: 0.8
Evidence:
  - 2 edits to simple_test.py in 5 minutes
  - Both after CI "black check failed"
  - No tool call to black
```

**Intervention:**
```
⚠️ Possible loop detected

You've manually edited simple_test.py formatting twice after Black
CI failures.

CLAUDE.md says: "NEVER guess what formatters want - use the actual tool"

Try: black crewai_test/src/crewai_test/simple_test.py
Then: git diff to see what Black changed
Then: git add && git commit -m "Apply Black formatting"

Expected: CI Black check will pass
```

**Likely outcome:** Loop broken at attempt 2 instead of user intervention at attempt 5

**Time saved:** ~20 minutes, 3 commits

---

## Recommendations for behavior-mcp

1. **Start with Black formatting pattern**
   - Well-defined trigger (multiple edits after CI failure)
   - Clear intervention (run the tool)
   - Measurable outcome (CI passes)

2. **Detection threshold: 2 attempts**
   - Catches loop early
   - Low false positive risk
   - Gives Claude chance to self-correct

3. **Intervention content:**
   - Name the pattern
   - Quote CLAUDE.md
   - Provide exact command
   - State expected outcome

4. **Effectiveness tracking:**
   - Did behavior change after reminder?
   - Did CI pass after following advice?
   - Was reminder helpful? (user feedback)

5. **Progressive reminders:**
   - Attempt 2: Gentle suggestion
   - Attempt 3: Stronger directive
   - Attempt 4: Explicit "STOP, this is a loop"

---

## Appendix: Full Commit History

1. **Fix CI pipeline linting issues** (ruff errors fixed, Black formatting guessed)
2. **Remove unused import from simple_test.py** (still formatting wrong)
3. **Apply Black auto-formatting to simple_test.py** ✅ (finally used the tool)
4. **Relax mypy configuration for test project** ✅ (config mismatch fixed)
5. **Add pytest-cov to dev dependencies** ✅ (missing dependency added)

**Final result:** All CI checks passing ✅
