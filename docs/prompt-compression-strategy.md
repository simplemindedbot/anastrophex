# Prompt Compression Strategy for Anastrophex

## Problem Statement

As we build out anastrophex with comprehensive rules, frameworks, and architectural guidance, we face token budget constraints:

**Current token usage concerns:**
- CLAUDE.md: ~2-3K tokens (debugging principles, tool usage, CI/CD best practices)
- AI_CREDO.md: ~1-2K tokens (verification rules, root cause analysis)
- cognitive-model.md: ~1K tokens (ADHD symptoms, neuroanatomical mappings)
- 5w1h-framework.md: ~2K tokens (systematic debugging)
- ai-credo-integration.md: ~3K tokens (detection signals, interventions)
- integration-notes.md: ~2K tokens (mnemex + clear-thought integration)

**Total: ~10-13K tokens just for guidance documents**

This doesn't include:
- Actual code context
- Conversation history
- Tool results
- File contents being worked on

**Goal:** Reduce guidance token usage by 60-80% while maintaining effectiveness.

---

## Approach 1: LLMLingua Prompt Compression

### Technology

**LLMLingua-2** (Microsoft Research, 2024)
- Trained via data distillation from GPT-4
- BERT-level encoder for token classification
- Achieves 3x-20x compression with minimal performance loss
- Task-agnostic (works on any prompt type)
- 3x-6x faster than LLMLingua v1

### Application to Anastrophex

**Compress static guidance documents:**

```python
from llmlingua import PromptCompressor

compressor = PromptCompressor(
    model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
    use_llmlingua2=True
)

# Example: Compress CLAUDE.md
original_credo = read_file("~/.claude/CLAUDE.md")  # ~2000 tokens
compressed = compressor.compress_prompt(
    original_credo,
    rate=0.25,  # Keep 25% of tokens (75% compression)
    force_tokens=['\n', '?', '!']  # Preserve structure
)
# Result: ~500 tokens, maintains key directives
```

**What gets compressed:**
- Verbose explanations → core directives
- Repeated concepts → single mentions
- Examples → compressed or removed
- Formatting → minimal structure retained

**What's preserved:**
- Critical rules ("verify before acting")
- Detection patterns ("should" = guessing)
- Key interventions ("STOP protocol")
- Essential structure (sections, hierarchy)

### Integration Strategy

```python
# Load compressed versions into context
anastrophex_context = {
    "core_principles": compress(AI_CREDO, rate=0.2),  # 80% reduction
    "debugging_framework": compress(5W1H, rate=0.3),  # 70% reduction
    "adhd_patterns": compress(cognitive_model, rate=0.4),  # 60% reduction
}

# Keep full versions in mnemex for reference
mnemex.store({
    "full_documentation": {
        "ai_credo": original_AI_CREDO,
        "5w1h": original_5W1H,
        "cognitive_model": original_cognitive_model
    }
})

# Lazy load details only when needed
if pattern_detected("rushing-after-error"):
    intervention = mnemex.retrieve("interventions/stop-protocol")
```

### Expected Savings

| Document | Original | Compressed (25%) | Savings |
|----------|----------|------------------|---------|
| CLAUDE.md | 2000 | 500 | 1500 |
| AI_CREDO.md | 1500 | 375 | 1125 |
| cognitive-model.md | 1000 | 250 | 750 |
| 5w1h-framework.md | 2000 | 500 | 1500 |
| ai-credo-integration.md | 3000 | 750 | 2250 |
| integration-notes.md | 2000 | 500 | 1500 |
| **Total** | **11,500** | **2,875** | **8,625 (75%)** |

---

## Approach 2: Symbolic Logic Notation

### Concept

Represent detection rules in formal logic for extreme compactness.

**Example current rule (natural language):**
```
If error occurred and command issued within 10 seconds
and command is not diagnostic, then rushing violation detected.

Intervention: STOP protocol
```

**Symbolic logic representation:**
```
E ∧ (t < 10s) ∧ ¬D → V(rushing) → I(stop)

Where:
  E = error_occurred
  t = time_since_error
  D = is_diagnostic_command
  V(x) = violation(x)
  I(x) = intervention(x)
```

### Full Notation System

**Predicates:**
- `E` = error occurred
- `W` = warning seen
- `C` = command executed
- `D` = diagnostic command
- `V` = verified/searched
- `B` = batched commands
- `P` = pattern matched

**Temporal operators:**
- `t < n` = time since event < n seconds
- `t > n` = time since event > n seconds
- `cnt(x) ≥ n` = count of x >= n

**Logic operators:**
- `∧` = AND
- `∨` = OR
- `¬` = NOT
- `→` = IMPLIES
- `↔` = IF AND ONLY IF

**Quantifiers:**
- `∀` = for all
- `∃` = there exists

### Pattern Library (Compact)

```
# Core violations
rushing:      E ∧ (t < 10s) ∧ ¬D → V(rushing)
batching:     E ∧ B ∧ (cnt(C) ≥ 2) → V(batching-critical)
repetition:   cnt(same_cmd) ≥ 3 ∧ ¬V → V(loop)
warning:      cnt(W_same) ≥ 2 ∧ ¬investigated → V(ignored-warning)
confidence:   contains("should"|"might"|"probably") ∧ ¬V → V(guessing)

# Composite rules
severe_loop:  V(loop) ∧ (t_loop > 5min) ∧ cnt(V(loop)) ≥ 2 → I(user-intervention)
escalation:   V(rushing) ∧ ¬response → wait(10s) → V(rushing) → I(force-stop)
```

### Human-Readable Mapping

Keep symbolic rules in code, maintain translation table:

```python
RULES = {
    "rushing": {
        "logic": "E ∧ (t < 10s) ∧ ¬D → V(rushing)",
        "description": "Command within 10s of error without diagnostics",
        "intervention": "stop-protocol",
        "severity": "warning"
    },
    "batching": {
        "logic": "E ∧ B ∧ (cnt(C) ≥ 2) → V(batching-critical)",
        "description": "Multiple commands batched during error state",
        "intervention": "force-sequential",
        "severity": "critical"
    }
}
```

### Token Savings

Natural language rule: ~50-100 tokens
Symbolic notation: ~10-15 tokens
**Savings: 80-85% per rule**

With 50+ rules: ~2500 tokens → ~500 tokens

---

## Approach 3: Structured XML/Tags

### Hierarchical Rule Representation

```xml
<anastrophex-rules version="1.0">

  <rule id="rushing-after-error" severity="warning">
    <detect>
      <and>
        <event type="error"/>
        <timing since="error" max="10s"/>
        <not><command type="diagnostic"/></not>
      </and>
    </detect>
    <violation type="rushing"/>
    <intervention ref="stop-protocol"/>
  </rule>

  <rule id="batched-commands-error" severity="critical">
    <detect>
      <and>
        <state>error_active</state>
        <commands mode="batch" count-min="2"/>
      </and>
    </detect>
    <violation type="batching-critical"/>
    <intervention ref="force-sequential"/>
  </rule>

  <intervention id="stop-protocol">
    <message>⚠️ Error occurred - SLOW DOWN</message>
    <actions>
      <block-execution duration="10s"/>
      <require-diagnostic/>
      <show-guidance ref="stop-read-think"/>
    </actions>
  </intervention>

</anastrophex-rules>
```

### Benefits

1. **Machine-parseable**: Direct XML parsing
2. **Hierarchical**: Natural nesting of conditions
3. **Reference-based**: Interventions defined once, referenced many times
4. **Extensible**: Add new attributes without breaking existing rules
5. **Validatable**: Can use XML schema for validation

### Integration with Code

```python
import xml.etree.ElementTree as ET

class AnastrophexRules:
    def __init__(self, xml_path):
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()

    def check_violation(self, context):
        for rule in self.root.findall('rule'):
            if self.evaluate_conditions(rule.find('detect'), context):
                return self.get_intervention(rule.find('intervention'))
        return None
```

### Token Efficiency

- Rules compressed into structured format
- No repeated explanatory text
- References instead of duplication
- Clear hierarchy reduces nesting tokens

**Estimated savings: 40-50% vs. natural language**

---

## Hybrid Strategy: Best of All Approaches

### Three-Tier System

**Tier 1: Ultra-Compact Rules (Symbolic Logic)**
```python
DETECTION_RULES = {
    "rushing": "E ∧ (t<10s) ∧ ¬D → V",
    "batching": "E ∧ B ∧ (n≥2) → V_crit",
    "loop": "cnt(cmd)≥3 ∧ ¬V → V_loop"
}
# ~100 tokens for 20+ rules
```

**Tier 2: Structured Metadata (XML)**
```xml
<interventions>
  <i id="stop">Block 10s, require diagnostic</i>
  <i id="seq">Force sequential execution</i>
  <i id="5why">Trigger root cause analysis</i>
</interventions>
<!-- ~200 tokens for all interventions -->
```

**Tier 3: Compressed Documentation (LLMLingua)**
```python
compressed_docs = {
    "adhd_model": llmlingua.compress(cognitive_model, rate=0.2),
    "frameworks": llmlingua.compress(frameworks, rate=0.25),
    "principles": llmlingua.compress(principles, rate=0.3)
}
# ~3000 tokens for all background theory
```

### Load Strategy

```python
# Always in context (minimal tokens)
core_rules = load_symbolic_rules()  # ~100 tokens
interventions = load_interventions_xml()  # ~200 tokens

# Loaded on-demand
if violation_detected:
    guidance = get_compressed_guidance(violation_type)  # ~100-200 tokens

if user_asks_why:
    theory = mnemex.retrieve("cognitive-model/full")  # from persistent storage
```

### Total Token Budget

| Component | Tokens | Load Strategy |
|-----------|--------|---------------|
| Symbolic rules | 100 | Always loaded |
| Intervention metadata | 200 | Always loaded |
| Compressed frameworks | 1000 | Lazy load by section |
| Full documentation | 0 | In mnemex, not in context |
| **Active context** | **~1300** | **vs. 11,500 currently** |

**Savings: ~89% reduction in guidance token usage**

---

## Implementation Plan

### Phase 1: Infrastructure (Tomorrow's POC)

1. **Install LLMLingua-2**
   ```bash
   pip install llmlingua
   ```

2. **Create compression script**
   - Read all guidance documents
   - Compress with various rates (0.2, 0.25, 0.3)
   - Compare outputs for quality
   - Select optimal compression rates

3. **Define symbolic notation**
   - Document all predicates and operators
   - Create translation layer
   - Write test rules in both formats

4. **Create XML schema**
   - Define rule structure
   - Define intervention structure
   - Validate against current patterns

### Phase 2: Migration

1. **Convert existing patterns**
   - AI_CREDO rules → symbolic + XML
   - 5W+1H framework → compressed + structured
   - Cognitive model → compressed reference

2. **Build loader system**
   - Parse symbolic rules
   - Parse XML interventions
   - Load compressed docs on-demand

3. **Integration with anastrophex MCP**
   - Rules loaded at server start
   - Violations detected via symbolic evaluation
   - Interventions retrieved from XML
   - Full context from mnemex when needed

### Phase 3: Validation

1. **Test compression quality**
   - Do compressed docs maintain effectiveness?
   - Run test cases from debugging sessions
   - Measure intervention accuracy

2. **Measure token savings**
   - Before/after token counts
   - Context window utilization
   - Performance impact

3. **Iterate on compression rates**
   - Find sweet spot for each doc type
   - Balance compression vs. information loss

---

## Expected Benefits

### Token Efficiency

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Guidance docs | 11,500 | 1,300 | 89% reduction |
| Context available for code | ~8,000 | ~18,200 | 128% increase |
| Rules definition | 2,500 | 300 | 88% reduction |

### Other Benefits

1. **Faster inference**: Fewer tokens to process
2. **More context space**: Room for actual code and conversation
3. **Clearer rules**: Symbolic logic is unambiguous
4. **Maintainable**: XML structure easier to edit than prose
5. **Portable**: Compressed docs work with any LLM
6. **Scalable**: Can add many more rules without token explosion

### Risks to Mitigate

1. **Over-compression**: May lose nuance
   - **Mitigation**: Test various compression rates
   - **Fallback**: Keep full docs in mnemex

2. **Symbolic logic opacity**: Harder for humans to read
   - **Mitigation**: Maintain translation table
   - **Documentation**: Clear notation guide

3. **Compression latency**: LLMLingua adds processing time
   - **Mitigation**: Pre-compress, cache results
   - **Acceptable**: One-time cost at deployment

4. **XML verbosity**: Could be worse than compact notation
   - **Mitigation**: Use references, avoid duplication
   - **Compare**: Benchmark against alternatives

---

## POC Success Criteria

Tomorrow's proof-of-concept should demonstrate:

1. ✅ **LLMLingua compression**
   - Compress CLAUDE.md, AI_CREDO.md
   - Compare 0.2, 0.25, 0.3 compression rates
   - Verify key directives preserved

2. ✅ **Symbolic rule notation**
   - Define 5-10 core rules in symbolic form
   - Create Python evaluator
   - Show equivalent natural language

3. ✅ **XML intervention structure**
   - Define schema for interventions
   - Convert 3-5 interventions to XML
   - Parse and retrieve in code

4. ✅ **Token count comparison**
   - Measure before/after for each approach
   - Calculate total savings
   - Document trade-offs

5. ✅ **Quality validation**
   - Run compressed rules against test cases
   - Verify interventions still fire correctly
   - Ensure no critical information lost

---

## References

**LLMLingua Resources:**
- Paper: https://arxiv.org/abs/2403.12968
- GitHub: https://github.com/microsoft/LLMLingua
- Docs: https://llmlingua.com

**Symbolic Logic:**
- First-order logic (FOL) for rule representation
- Temporal logic for time-based conditions
- Modal logic for possibility/necessity

**XML Standards:**
- XML Schema for validation
- XPath for querying
- XSLT for transformation (if needed)

---

## Open Questions

1. **Optimal compression rates by document type?**
   - Theoretical docs (cognitive-model) might compress more
   - Practical rules (AI_CREDO) might need higher fidelity

2. **Symbolic notation extensions needed?**
   - Do we need probabilistic logic (confidence levels)?
   - Should we include fuzzy logic for "approximately"?

3. **Runtime performance?**
   - How fast is symbolic rule evaluation?
   - Does XML parsing add latency?

4. **Integration with other tools?**
   - Should mnemex use same compression?
   - Can clear-thought benefit from symbolic notation?

5. **Human maintainability?**
   - Will we still be able to easily edit rules?
   - Need tooling for symbolic ↔ natural language conversion?

---

## Next Steps

**Tomorrow:**
1. Build POC demonstrating all three approaches
2. Measure token savings and quality
3. Select winning combination
4. Create implementation roadmap

**This Week:**
1. Migrate core rules to chosen format
2. Integrate with anastrophex MCP server
3. Test in real debugging sessions
4. Document notation for contributors

**Next Week:**
1. Extend to all guidance documents
2. Build tooling for rule management
3. Create compression pipeline
4. Measure impact on debugging effectiveness

---

This document represents the conceptual plan. Implementation tomorrow will validate assumptions and refine the approach.
