# Anastrophex Development TODO

SMART Tasks: Specific, Measurable, Achievable, Relevant, Time-bound

---

## Phase 1: AI_CREDO Parsing & Modularization

### Task 1.1: Parse AI_CREDO.md into Functional Chunks
**Status:** 🔴 Not Started
**Priority:** P0 (Critical)
**Owner:** TBD
**Due:** Day 1

**Objective:** Break AI_CREDO.md into individually callable modules for selective loading.

**Acceptance Criteria:**
- [ ] Create `ai_credo_parser.py` that extracts distinct sections
- [ ] Each section represented as structured data (dict/class)
- [ ] Sections identified:
  - `verify_before_acting` (lines 1-12)
  - `root_cause_analysis` (lines 14-30)
  - `tool_usage` (lines 32-56)
  - `working_approach` (lines 58-76)
  - `loop_detection` (lines 78-98)
  - `communication` (lines 100-117)
  - `brainstorming` (lines 119-134)
  - `plan_mode` (lines 136-148)
  - `cicd_practices` (lines 150-232)
- [ ] Unit test: Parse full file, verify 9 sections extracted
- [ ] Unit test: Each section contains expected key phrases

**Success Metric:** Parser extracts all 9 sections with 100% accuracy

---

### Task 1.2: Create Structured Schema for CREDO Sections
**Status:** 🔴 Not Started
**Priority:** P0 (Critical)
**Owner:** TBD
**Due:** Day 1

**Objective:** Define data structures for parsed CREDO sections.

**Acceptance Criteria:**
- [ ] Create `credo_schema.py` with dataclasses/Pydantic models
- [ ] Schema includes:
  ```python
  @dataclass
  class CredoSection:
      id: str
      title: str
      principle: str
      detection_patterns: List[str]
      interventions: List[str]
      examples: List[str]
      line_range: Tuple[int, int]
  ```
- [ ] Validate against actual AI_CREDO.md content
- [ ] JSON serializable for storage/transmission

**Success Metric:** All 9 sections fit schema, validate successfully

---

### Task 1.3: Implement Selective Section Loader
**Status:** 🔴 Not Started
**Priority:** P0 (Critical)
**Owner:** TBD
**Due:** Day 2

**Objective:** Load only relevant CREDO sections based on detected pattern.

**Acceptance Criteria:**
- [ ] Create `credo_loader.py` with selective loading
- [ ] Function signature: `load_section(pattern: str) -> CredoSection`
- [ ] Pattern mapping:
  - `rushing` → `verify_before_acting` + `loop_detection`
  - `batching` → `verify_before_acting` + `working_approach`
  - `cicd_error` → `cicd_practices` + `tool_usage`
  - `loop` → `loop_detection` + `root_cause_analysis`
- [ ] Lazy loading (don't load all sections upfront)
- [ ] Cache loaded sections for session

**Success Metric:** Load time <10ms per section, memory usage <1KB per section

---

## Phase 2: Prompt Compression POC

### Task 2.1: Install and Configure LLMLingua-2
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 2

**Objective:** Set up LLMLingua-2 for prompt compression testing.

**Acceptance Criteria:**
- [ ] Install: `pip install llmlingua`
- [ ] Test basic compression with sample text
- [ ] Verify compression rates: 0.2, 0.25, 0.3, 0.4
- [ ] Document installation steps in `docs/setup.md`

**Success Metric:** Successfully compress 1000-token text to 250 tokens

---

### Task 2.2: Compress AI_CREDO Sections
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 2

**Objective:** Compress each AI_CREDO section at multiple rates, measure quality.

**Acceptance Criteria:**
- [ ] Compress each of 9 sections at rates: 0.2, 0.25, 0.3
- [ ] Create comparison table:
  ```
  Section | Original | 0.2 | 0.25 | 0.3 | Quality Score
  --------|----------|-----|------|-----|---------------
  verify  | 200      | 40  | 50   | 60  | ?
  ```
- [ ] Manual quality review: Do compressed versions preserve key directives?
- [ ] Store compressed versions in `compressed/ai_credo/`
- [ ] Document findings in `docs/compression-analysis.md`

**Success Metric:** Find optimal compression rate per section (preserves 90%+ meaning)

---

### Task 2.3: Implement Symbolic Logic Rule Notation
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 3

**Objective:** Define symbolic notation for detection rules, create parser.

**Acceptance Criteria:**
- [ ] Create `symbolic_rules.py` with notation definition
- [ ] Document notation in `docs/symbolic-notation.md`:
  - Predicates: E (error), W (warning), C (command), D (diagnostic), V (verified)
  - Temporal: t<n, t>n, cnt(x)≥n
  - Logic: ∧, ∨, ¬, →, ↔
- [ ] Implement 10 core rules in symbolic form:
  ```python
  RULES = {
      "rushing": "E ∧ (t<10s) ∧ ¬D → V(rushing)",
      "batching": "E ∧ B ∧ (cnt(C)≥2) → V(batching)",
      # ... 8 more
  }
  ```
- [ ] Create evaluator: `evaluate_rule(rule_logic: str, context: dict) -> bool`
- [ ] Unit tests: Verify each rule evaluates correctly

**Success Metric:** 10 rules defined, evaluator passes all tests

---

### Task 2.4: Create XML Intervention Schema
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 3

**Objective:** Define XML structure for interventions, implement parser.

**Acceptance Criteria:**
- [ ] Create `interventions.xml` with schema:
  ```xml
  <interventions>
    <intervention id="stop-protocol">
      <message>⚠️ Error occurred - SLOW DOWN</message>
      <actions>
        <block-execution duration="10s"/>
        <require-diagnostic/>
      </actions>
    </intervention>
  </interventions>
  ```
- [ ] Create XML schema validation (XSD)
- [ ] Implement parser: `parse_interventions(xml_path: str) -> Dict[str, Intervention]`
- [ ] Convert 5 key interventions to XML
- [ ] Unit tests: Parse, validate, retrieve interventions

**Success Metric:** XML validates, parser extracts all interventions correctly

---

### Task 2.5: Measure Token Savings
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 3

**Objective:** Quantify token reduction from all compression approaches.

**Acceptance Criteria:**
- [ ] Create `token_counter.py` using tiktoken or similar
- [ ] Count tokens for:
  - Original AI_CREDO.md: ~2000 tokens
  - Compressed sections (0.25 rate): ~500 tokens
  - Symbolic rules: ~100 tokens
  - XML interventions: ~200 tokens
  - Total compressed: ~800 tokens
- [ ] Calculate savings: (2000 - 800) / 2000 = 60%
- [ ] Document in `docs/compression-results.md`

**Success Metric:** Achieve 60%+ token reduction with acceptable quality

---

## Phase 3: Pattern Detection System

### Task 3.1: Implement Timing Monitor
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 4

**Objective:** Track timing between errors and subsequent commands.

**Acceptance Criteria:**
- [ ] Create `timing_monitor.py` with class:
  ```python
  class TimingMonitor:
      def on_error(self, timestamp: float)
      def on_command(self, timestamp: float) -> Optional[str]
      def on_batch_execution(self, commands: List) -> Optional[str]
  ```
- [ ] Detect patterns:
  - Commands within 10s of error
  - Multiple commands within 30s
  - Batched commands during error state
- [ ] Unit tests: Simulate various timing scenarios
- [ ] Integration test: Monitor real tool calls

**Success Metric:** Detects 100% of timing violations in test suite

---

### Task 3.2: Implement Confidence Language Detector
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 4

**Objective:** Detect hyperbolic/uncertain language in responses.

**Acceptance Criteria:**
- [ ] Create `language_detector.py`
- [ ] Pattern matching for:
  - Confidence words: "should", "might", "probably", "likely"
  - Superlatives: "brilliant", "amazing", "groundbreaking"
  - Excessive exclamation marks (>2 in paragraph)
  - Sycophancy: "absolutely right", "great insight"
- [ ] Scoring system: Low/Medium/High severity
- [ ] Unit tests: Test sentences with/without violations
- [ ] False positive rate <5%

**Success Metric:** Detects 95%+ of confidence language patterns

---

### Task 3.3: Implement Loop Detector
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 5

**Objective:** Detect trial-and-error loops and repeated failures.

**Acceptance Criteria:**
- [ ] Create `loop_detector.py`
- [ ] Track:
  - Same command attempted 3+ times
  - Same error occurred 3+ times
  - Same fix attempted without success
  - 5+ tool calls without progress
  - User corrections on same topic (2+)
- [ ] Maintain session history (last N actions)
- [ ] Provide loop type classification
- [ ] Unit tests: Simulate various loop scenarios

**Success Metric:** Detects loops before 4th repetition, <1% false positives

---

### Task 3.4: Implement Pattern Orchestrator
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 5

**Objective:** Coordinate all pattern detectors, determine interventions.

**Acceptance Criteria:**
- [ ] Create `pattern_orchestrator.py`
- [ ] Integrate:
  - TimingMonitor
  - LanguageDetector
  - LoopDetector
  - Symbolic rule evaluator
- [ ] Priority system (CRITICAL > WARNING > INFO)
- [ ] Intervention selection based on pattern type
- [ ] Debouncing (don't re-trigger same intervention <5min)
- [ ] Unit tests: Multiple simultaneous patterns

**Success Metric:** Correctly prioritizes and triggers interventions

---

## Phase 4: MCP Server Implementation

### Task 4.1: Create Base MCP Server Structure
**Status:** 🔴 Not Started
**Priority:** P0 (Critical)
**Owner:** TBD
**Due:** Day 6

**Objective:** Implement basic MCP server with core protocol support.

**Acceptance Criteria:**
- [ ] Update `src/anastrophex/server.py`
- [ ] Implement MCP protocol handlers:
  - `list_resources()` - available CREDO sections
  - `read_resource()` - load specific section
  - `list_tools()` - pattern detection tools
  - `call_tool()` - run pattern detection
- [ ] Resource URIs:
  - `anastrophex://credo/verify-before-acting`
  - `anastrophex://credo/loop-detection`
  - etc.
- [ ] Tool: `detect_pattern(context: dict) -> Violation`
- [ ] Unit tests for all handlers

**Success Metric:** MCP protocol compliance, all tests pass

---

### Task 4.2: Integrate Pattern Detection into MCP
**Status:** 🔴 Not Started
**Priority:** P0 (Critical)
**Owner:** TBD
**Due:** Day 6

**Objective:** Wire pattern detection system into MCP server.

**Acceptance Criteria:**
- [ ] MCP tool: `check_violations(tool_history: List[dict])`
- [ ] Returns list of detected violations with:
  - Pattern type
  - Severity
  - Recommended intervention
  - Relevant CREDO section
- [ ] Tool: `get_intervention(violation_id: str)`
- [ ] Integration test: Call from MCP client

**Success Metric:** MCP client can detect patterns and retrieve interventions

---

### Task 4.3: Add Mnemex Integration
**Status:** 🔴 Not Started
**Priority:** P2 (Medium)
**Owner:** TBD
**Due:** Day 7

**Objective:** Record violations and interventions to mnemex for learning.

**Acceptance Criteria:**
- [ ] Create `mnemex_recorder.py`
- [ ] Record to mnemex after each violation:
  ```python
  mnemex.record({
      "pattern": "rushing-after-error",
      "timestamp": timestamp,
      "context": context,
      "intervention": intervention_id,
      "effectiveness": None  # will be updated later
  })
  ```
- [ ] Query mnemex: `has_pattern_failed_before(pattern: str)`
- [ ] Update effectiveness after user feedback
- [ ] Integration test: Write to mnemex, query back

**Success Metric:** All violations recorded, queryable from mnemex

---

### Task 4.4: Create Configuration System
**Status:** 🔴 Not Started
**Priority:** P2 (Medium)
**Owner:** TBD
**Due:** Day 7

**Objective:** Allow users to configure anastrophex behavior.

**Acceptance Criteria:**
- [ ] Create `config.yaml` with settings:
  ```yaml
  anastrophex:
    timing:
      min_pause_seconds: 10
      max_pause_seconds: 30
    detection:
      enable_rushing: true
      enable_batching: true
      enable_loops: true
      enable_language: true
    compression:
      use_compressed: true
      compression_rate: 0.25
    mnemex:
      enabled: true
      record_all: false  # or only successful interventions
  ```
- [ ] Config validation
- [ ] Hot reload (no restart needed)
- [ ] Environment variable overrides

**Success Metric:** All settings configurable, validated, overridable

---

## Phase 5: Testing & Validation

### Task 5.1: Create Test Suite from Real Sessions
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 8

**Objective:** Build comprehensive tests from documented debugging sessions.

**Acceptance Criteria:**
- [ ] Extract test cases from:
  - `examples/crewai-test-case-study.md`
  - `examples/anastrophex-venv-debugging.md`
  - GitHub API error session (documented today)
- [ ] Create fixture: Simulated tool call history
- [ ] Test scenarios:
  - Rushing after error (should detect)
  - Batched commands with errors (should detect CRITICAL)
  - Loop detection (3+ failed attempts)
  - Hyperbole detection ("This is brilliant!")
  - No false positives on normal workflow
- [ ] Minimum 20 test cases, 50+ assertions

**Success Metric:** 100% test pass rate, <5% false positive rate

---

### Task 5.2: Benchmark Token Usage
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 8

**Objective:** Measure actual token usage in real debugging scenario.

**Acceptance Criteria:**
- [ ] Simulate debugging session with:
  - Original full CREDO: Count tokens
  - Compressed selective loading: Count tokens
- [ ] Scenarios:
  - Simple error (1 pattern): Load 1 section
  - Complex debugging (3 patterns): Load 3 sections
  - Full session (all patterns): Compare to loading everything
- [ ] Document in `docs/benchmark-results.md`
- [ ] Graphs: Token usage over time

**Success Metric:** Compressed approach uses 60%+ fewer tokens

---

### Task 5.3: Quality Validation
**Status:** 🔴 Not Started
**Priority:** P1 (High)
**Owner:** TBD
**Due:** Day 9

**Objective:** Verify compressed/symbolic versions maintain effectiveness.

**Acceptance Criteria:**
- [ ] A/B test: Same debugging scenario with:
  - Full natural language CREDO
  - Compressed + symbolic version
- [ ] Measure:
  - Time to detect pattern
  - Accuracy of intervention selection
  - User-perceived quality (manual review)
- [ ] Criteria: Compressed performs within 10% of original
- [ ] Document findings

**Success Metric:** Compressed version ≥90% as effective as original

---

## Phase 6: Documentation & Deployment

### Task 6.1: Write User Documentation
**Status:** 🔴 Not Started
**Priority:** P2 (Medium)
**Owner:** TBD
**Due:** Day 10

**Objective:** Create comprehensive user-facing documentation.

**Acceptance Criteria:**
- [ ] Update `README.md` with:
  - What anastrophex does
  - How to install
  - How to configure
  - Example usage
- [ ] Create `docs/user-guide.md`:
  - Pattern types explained
  - Intervention descriptions
  - Configuration options
  - Troubleshooting
- [ ] Create `docs/architecture.md`:
  - System components
  - Data flow diagrams
  - Extension points
- [ ] API documentation (autodoc from code)

**Success Metric:** User can install and use without additional help

---

### Task 6.2: Create Installation Script
**Status:** 🔴 Not Started
**Priority:** P2 (Medium)
**Owner:** TBD
**Due:** Day 10

**Objective:** Automated installation and setup.

**Acceptance Criteria:**
- [ ] Create `install.sh` that:
  - Checks Python version (≥3.10)
  - Installs dependencies
  - Downloads LLMLingua models
  - Compresses CREDO sections
  - Tests installation
- [ ] Works on macOS and Linux
- [ ] Idempotent (can run multiple times)
- [ ] Progress reporting

**Success Metric:** Fresh install completes in <5 minutes

---

### Task 6.3: CI/CD Pipeline
**Status:** 🔴 Not Started
**Priority:** P2 (Medium)
**Owner:** TBD
**Due:** Day 11

**Objective:** Automated testing and deployment.

**Acceptance Criteria:**
- [ ] GitHub Actions workflow:
  ```yaml
  name: Tests
  on: [push, pull_request]
  jobs:
    test:
      strategy:
        matrix:
          python: [3.10, 3.11, 3.12]
  ```
- [ ] Run on each PR:
  - Unit tests (pytest)
  - Type checking (mypy)
  - Linting (ruff)
  - Format check (black)
- [ ] Coverage reporting (>80% target)
- [ ] Auto-publish to PyPI on tag

**Success Metric:** All checks pass, auto-deploy works

---

## Phase 7: Integration & Polish

### Task 7.1: Clear-Thought Integration
**Status:** 🔴 Not Started
**Priority:** P2 (Medium)
**Owner:** TBD
**Due:** Day 12

**Objective:** Coordinate with Clear-Thought MCP for complete debugging support.

**Acceptance Criteria:**
- [ ] Document integration in `docs/integration-notes.md`
- [ ] Example workflow:
  - Clear-Thought: Suggests "binary search" strategy
  - Anastrophex: Enforces verbosity, detects loops
  - Mnemex: Records what worked
- [ ] Test combined usage
- [ ] Consider PR to clear-thought with tactical additions

**Success Metric:** Documented integration, tested workflow

---

### Task 7.2: Neuroanatomical Model Refinement
**Status:** 🔴 Not Started
**Priority:** P3 (Low)
**Owner:** TBD
**Due:** Day 13

**Objective:** Refine cognitive model based on implementation learnings.

**Acceptance Criteria:**
- [ ] Review `docs/cognitive-model.md`
- [ ] Add sections based on what we learned:
  - Actual timing windows observed
  - Pattern frequencies
  - Intervention effectiveness data
- [ ] Update predictions with actual results
- [ ] Add research section: "What we discovered"

**Success Metric:** Model updated with empirical findings

---

### Task 7.3: Performance Optimization
**Status:** 🔴 Not Started
**Priority:** P3 (Low)
**Owner:** TBD
**Due:** Day 14

**Objective:** Optimize for speed and memory efficiency.

**Acceptance Criteria:**
- [ ] Profile pattern detection code
- [ ] Optimize hot paths:
  - Rule evaluation <1ms
  - Section loading <10ms
  - Mnemex writes async (don't block)
- [ ] Memory usage <50MB for server
- [ ] Benchmark before/after

**Success Metric:** 50%+ speed improvement, no memory leaks

---

## Ongoing Tasks

### Maintain Documentation
**Status:** 🟢 Ongoing
**Priority:** P1 (High)
**Owner:** All contributors

**Activities:**
- Update docs with each code change
- Keep examples current
- Document new patterns discovered
- Update compression analysis as we learn

---

### Collect Pattern Examples
**Status:** 🟢 Ongoing
**Priority:** P2 (Medium)
**Owner:** All users

**Activities:**
- Record debugging sessions where anastrophex helped
- Document false positives (refine detection)
- Share intervention effectiveness
- Build pattern library

---

### Research & Experimentation
**Status:** 🟢 Ongoing
**Priority:** P3 (Low)
**Owner:** Research team

**Activities:**
- Test compression rates
- Try different symbolic notations
- Explore new pattern types
- Validate neuroanatomical predictions

---

## Metrics Dashboard

### Code Quality
- [ ] Test coverage: 80%+ (target)
- [ ] Type coverage: 90%+ (mypy strict)
- [ ] Linting: 0 errors (ruff)
- [ ] Format: 100% (black)

### Performance
- [ ] Pattern detection: <10ms per check
- [ ] Section loading: <50ms
- [ ] Memory usage: <50MB resident
- [ ] Token savings: 60%+

### Effectiveness
- [ ] False positive rate: <5%
- [ ] Detection accuracy: >95%
- [ ] User satisfaction: TBD (feedback)
- [ ] Intervention success: TBD (from mnemex)

---

## Priority Legend
- **P0 (Critical):** Blocking, must complete first
- **P1 (High):** Core functionality, high value
- **P2 (Medium):** Important but not blocking
- **P3 (Low):** Nice to have, future work

## Status Legend
- 🔴 **Not Started**
- 🟡 **In Progress**
- 🟢 **Complete**
- ⏸️ **Blocked**
- 🔵 **Under Review**

---

**Last Updated:** 2025-10-23
**Next Review:** After Phase 1 completion
