# Anastrophex Implementation Roadmap

## Phase 1: Pattern Detection (Weeks 1-2)

**Goal:** Basic loop detection without intervention

### Tasks
- [ ] Set up Python MCP server boilerplate
- [ ] Implement tool call monitoring/logging
- [ ] Create `PatternDetector` class with simple repetition counter
- [ ] Define Pattern data structure (ID, name, trigger_count, detection_criteria)
- [ ] Implement Black formatting loop detection (3+ Edit calls to .py files)
- [ ] Log detected patterns to mnemex
- [ ] Write tests for pattern matching logic

### Success Criteria
- Server runs and monitors tool calls
- Correctly identifies Black formatting loop in test scenarios
- Logs pattern occurrences to mnemex graph
- No false positives on legitimate multi-file edits

---

## Phase 2: Directive Injection (Weeks 3-4)

**Goal:** Inject timely reminders from CLAUDE.md

### Tasks
- [ ] Parse CLAUDE.md to extract directives
- [ ] Create directive-to-pattern mappings
- [ ] Implement `DirectiveInjector` class
- [ ] Design reminder format (⚠️ Loop detected template)
- [ ] Inject reminders via tool result augmentation
- [ ] Add MCP resource: `anastrophex://alerts/active`
- [ ] Test timing: trigger after N-1 attempts, before Nth

### Success Criteria
- Reminders appear in tool results when pattern detected
- CLAUDE.md directives correctly matched to patterns
- Timing prevents 3rd attempt (intervene after 2nd)
- Reminders include: pattern name, CLAUDE.md quote, specific command, expected outcome

---

## Phase 3: Learning System (Weeks 5-6)

**Goal:** Track effectiveness and persist learnings

### Tasks
- [ ] Design mnemex graph schema (Pattern, Intervention, Context nodes)
- [ ] Implement effectiveness tracking (shown_count, worked_count)
- [ ] Create `record_outcome()` function
- [ ] Query mnemex for pattern history
- [ ] Implement `get_best_intervention()` for context matching
- [ ] Add MCP tool: `report_outcome(pattern_id, intervention_id, worked, notes)`
- [ ] Build effectiveness dashboard (query from mnemex)

### Success Criteria
- Interventions recorded with effectiveness scores
- Historical data persists across Claude sessions
- Best intervention selected based on past success
- Can query: "Has this pattern been seen before in this context?"

---

## Phase 4: Advanced Patterns (Weeks 7-8)

**Goal:** Multi-tool sequences and context-aware triggers

### Tasks
- [ ] Implement multi-tool sequence detection (Edit → Push → CI fail → Edit)
- [ ] Add time-based pattern matching (rapid attempts < 1 minute)
- [ ] Create context filters (repo_type, language, tool_name)
- [ ] Add trial-and-error pattern (same error 2+ times, no WebSearch)
- [ ] Implement mypy config mismatch detection (50+ errors + strict=true)
- [ ] Add missing dependency pattern (unrecognized arguments + dependency check)
- [ ] Progressive reminders (gentle → stronger → explicit STOP)

### Success Criteria
- 5+ patterns implemented and tested
- Context-aware triggering (Python repos vs others)
- Progressive reminder escalation works
- Low false positive rate (<10%)

---

## Future Enhancements

### Phase 5: Proactive Interventions
- Detect context entry (starting CI debugging) and surface relevant patterns
- Predict potential loops before they start
- Suggest tools proactively based on task context

### Phase 6: User Feedback Loop
- Add thumbs up/down on reminders
- Adjust effectiveness scores based on explicit feedback
- A/B test reminder formats

### Phase 7: Cross-Session Memory
- "Last time you worked on this repo, X pattern occurred"
- Session-to-session continuity through mnemex
- Build user-specific pattern library

---

## Success Metrics

### Primary Metrics (Track from Day 1)
- **Loop break rate**: % of loops broken before attempt 5
- **Intervention effectiveness**: % of reminders that change behavior
- **Time saved**: Estimated commits/minutes saved per session

### Secondary Metrics (Phase 3+)
- Pattern detection accuracy
- False positive rate
- Pattern coverage (% of failure modes with patterns)
- Time to detect (how quickly patterns are identified)

### Qualitative Metrics (Ongoing)
- User satisfaction ("Did this help?")
- Claude learning curve (do patterns reduce over time?)
- Documentation quality (are patterns well-described?)

---

## Development Guidelines

### Testing Strategy
- Simulated tool call streams for pattern detection
- Known loop scenarios from case studies
- Effectiveness tracking in test environment
- Integration tests with mock MCP client

### Performance Requirements
- Tool call monitoring: < 10ms overhead
- Mnemex queries: cached, indexed
- Pattern matching: efficient (indexed by signature)

### Privacy & Control
- All data stays local (mnemex is local)
- No external tracking
- User controls what patterns are tracked
- Easy to disable patterns or interventions

---

## MVP Definition

**Minimum Viable Product (End of Phase 2):**
1. Detects Black formatting loop (3+ manual edits)
2. Injects reminder with CLAUDE.md quote + specific command
3. Logs to mnemex (no effectiveness tracking yet)
4. MCP resource to view active alerts

**Why this is valuable:**
- Addresses real, observed failure mode
- Demonstrates full pipeline (detect → inject → log)
- Provides immediate value in Python development
- Foundation for adding more patterns

---

## Open Questions

1. **Timing precision**: How do we know WHEN to inject?
   - Current plan: After N-1 attempts, before Nth
   - Need to measure: too early vs too late trade-offs

2. **Reminder format**: What actually works?
   - Test multiple formats
   - A/B test with effectiveness tracking

3. **False positives**: How to handle?
   - 3 edits might be legitimate refactoring
   - Add context filters (CI failure present?)
   - Allow user to dismiss/ignore patterns

4. **Effectiveness measurement**: How to know if it worked?
   - Behavior change (did Claude run the suggested tool?)
   - Outcome (did CI pass after following advice?)
   - User feedback (explicit thumbs up/down)
   - Combination of all three?

5. **Context detection**: How granular?
   - Repo level? (crewai-test vs mnemex)
   - File level? (pyproject.toml vs .py files)
   - Task level? (debugging vs new feature)
   - Start broad, refine based on data

---

## Resources Needed

- Python 3.10+ environment
- MCP SDK (`mcp` package)
- Mnemex running and accessible
- Test corpus: crewai-test case study as baseline
- GitHub CI/CD logs for additional pattern examples

---

## Notes

- Start small: One pattern (Black loop) working end-to-end is better than 5 patterns half-implemented
- Measure everything: Effectiveness data is the core value proposition
- Iterate based on real usage: Build what actually helps, not what sounds good
- "Pobody's nerfect": 30% success rate is a huge win over 0%
