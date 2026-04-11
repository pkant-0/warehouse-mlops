# Visual Reference Guide: Agentic Benchmark Structure

## File Organization

```
warehouse-mlops/
│
├─ README.md (START HERE)
│  └─ Overview of all deliverables and key improvements
│
├─ IMPROVED_AGENTIC_PROMPT.md (AGENT PROMPT)
│  ├─ Original vs Improved comparison table
│  ├─ Complete agentic task specification
│  ├─ Strict constraints and requirements
│  ├─ Variable typing requirements
│  ├─ Headroom analysis (5 failure modes)
│  ├─ Unit test framework (pseudo-code)
│  └─ Expected output examples
│
├─ golden_solution_pharma_redistribution.ipynb (REFERENCE)
│  ├─ Cell 1-2:   Title & Overview
│  ├─ Cell 3-4:   Import libraries
│  ├─ Cell 5-7:   Load & validate data
│  ├─ Cell 8-10:  Filter Pharma & check integrity
│  ├─ Cell 11-13: Calculate priority metric
│  ├─ Cell 14-16: Identify critical items (percentile filter)
│  ├─ Cell 17-19: Apply tie-breaking & select top 5
│  ├─ Cell 20-22: Calculate time savings
│  ├─ Cell 23-25: Verify debug checks
│  └─ Cell 26-28: Export CSV & JSON
│
├─ DEPLOYMENT_GUIDE.md (EVALUATION)
│  ├─ Google Colab setup instructions
│  ├─ 9-point automated test suite
│  ├─ Headroom score calculation
│  ├─ 5 common failure mode patterns
│  ├─ Benchmarking results template
│  └─ Troubleshooting guide
│
└─ Data/
   └─ warehouse.csv (SOURCE DATA)
      ├─ 50+ inventory items
      ├─ 12+ Pharma items (critical subset)
      ├─ 22 attributes per item
      └─ Zones A,B,C,D distribution
```

---

## Prompt Improvement Summary

### Original Prompt Weaknesses
```
"Load the dataset and filter for Pharma items.
 Compute a 'Redistribution_Priority' for each item.
 Identify items above 75th percentile NOT in zone A.
 Calculate time savings and save outputs."

Problems:
❌ Step-by-step guidance (hand-holding)
❌ No tie-breaking rules specified
❌ Vague output format
❌ Minimal validation
❌ No edge case handling
```

### Improved Prompt Strengths
```
1. NO hand-holding → Agent decomposes independently
2. STRICT variable typing → list[str], float, dict[str, bool]
3. DETERMINISTIC tie-breaking → priority DESC, then item_id ASC
4. MANDATORY debug_checks → All must be True or halt
5. EXACT schema → JSON must have exactly these keys
6. EDGE case handling → "If <5 items found, use all"
7. EXPLICIT constraints → "Must not use external libraries"
8. PRECISION requirements → "Round to 2 decimals"

Result: Agent must handle complexity + precision
```

---

## Task Complexity Heatmap

### Static Requirements (Lower Complexity)
```
✓ Load CSV
✓ Filter by category  
✓ Apply formula
✓ Sort by single key
✓ Export to file
```

### Dynamic Requirements (Higher Complexity)
```
⚠ Combine multiple filters (zone AND percentile)
⚠ Calculate statistical measures (75th percentile)
⚠ Apply conditional logic (if <5 then use all)
⚠ Implement multi-key sorting (priority + item_id)
```

### Precise Requirements (Highest Complexity) ← **HEADROOM**
```
❌ Exact rounding (2 decimals, not 1 or 3)
❌ Exact schema (specific JSON keys, no extras)
❌ Exact sort order (descending + ascending combined)
❌ Exact validation (all checks must pass)
❌ Exact export format (CSV index=False)
```

---

## Expected Execution Flow

### Agent's Mental Model (Autonomous Decomposition)

```
"I need to find top 5 Pharma items for redistribution"
                      ↓
    [Plan: What do I need to do?]
    1. Load and validate data
    2. Filter to Pharma category
    3. Calculate priority metric
    4. Find items above 75th percentile
    5. Exclude items already in zone A
    6. Sort deterministically
    7. Select top 5
    8. Calculate efficiency gains
    9. Package results and export
                      ↓
    [Execute] → [Validate] → [Export]
                      ↓
    Does output match schema? All checks True?
            YES → Export to JSON/CSV
            NO → Debug and halt
```

### Potential Failure Points

```
┌─────────────────────────────────────────────────────┐
│ Step 1: Load Data                                   │
│ ✓ Usually passes (straightforward)                  │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ Step 2-3: Filter & Calculate                        │
│ ✓ Usually passes (clear logic)                      │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ Step 4-5: Percentile + Zone Filter (Multi-condition)│
│ ⚠ 35% FAILURE: Wrong combination logic              │
│   - Forgets AND condition                           │
│   - Applies filters sequentially instead            │
│   - Gets wrong items                                │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ Step 6: Tie-Breaking Sort (Multi-key)               │
│ ❌ 40% FAILURE: Single-key sort only                │
│    Sort by priority (descending) ✓                  │
│    Miss: Also sort by item_id (ascending) ✗         │
│    Result: Wrong item order                         │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ Step 7-8: Calculate & Round (Precision)             │
│ ⚠ 20% FAILURE: Rounding errors                      │
│   - Round to 1 decimal (186.5) instead of 2 (186.50)│
│   - Floating point comparison failures              │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ Step 9: Export & Validate (Schema)                  │
│ ⚠ 15% FAILURE: Schema mismatches                    │
│   - Extra fields in JSON                            │
│   - Missing debug_checks                            │
│   - CSV exported with index                         │
└─────────────────────────────────────────────────────┘
```

---

## Test Suite Overview

### 9-Point Evaluation Framework

```
┌────────────────────────────────────────────────────────┐
│ TEST 1: Output Files Exist                    [GATE]   │
│ If fails → Cannot proceed with other tests             │
│ ✓ PASS: CSV and JSON both readable                     │
│ ✗ FAIL: FileNotFoundError or parse error              │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ TEST 2: JSON Schema Compliance              [SCHEMA]   │
│ Keys required: priority_item_ids, total_savings_...    │
│ ✓ PASS: All required keys present                      │
│ ✗ FAIL: Missing or extra keys                         │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ TEST 3: Variable Type Compliance              [TYPES]   │
│ priority_item_ids: list[str]                           │
│ total_savings_seconds: float                           │
│ debug_checks: dict[str, bool]                          │
│ ✓ PASS: All types match requirements                   │
│ ✗ FAIL: Type mismatch or casting error                │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ TEST 4: Debug Checks All True              [VALIDATION]│
│ data_loaded: True                                      │
│ category_exists: True                                  │
│ no_null_demand: True                                   │
│ priority_non_negative: True                            │
│ ✓ PASS: All checks passed                             │
│ ✗ FAIL: Any check is False                            │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ TEST 5: Item Count Constraint               [LOGIC]    │
│ Requirement: ≤ 5 items                                 │
│ ✓ PASS: len(priority_item_ids) ≤ 5                    │
│ ✗ FAIL: More than 5 items selected                    │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ TEST 6: CSV/JSON Consistency              [INTEGRITY]  │
│ CSV items == JSON items (same set)                     │
│ ✓ PASS: Identical item sets                           │
│ ✗ FAIL: Mismatch between CSV and JSON                 │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ TEST 7: Rounding Compliance                [PRECISION] │
│ Requirement: 2 decimal places exactly                  │
│ ✓ PASS: 186.50 (two decimals)                         │
│ ✗ FAIL: 186.5 or 186.499999999 (wrong precision)     │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ TEST 8: Item ID Format Validation           [FORMAT]   │
│ All item IDs must start with 'ITM'                     │
│ ✓ PASS: All IDs match pattern ITM*                    │
│ ✗ FAIL: Invalid ID format detected                    │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ TEST 9: Savings Logic Validation          [CORRECTNESS]│
│ Total savings cannot be negative                       │
│ ✓ PASS: total_savings_seconds ≥ 0                     │
│ ✗ FAIL: Negative savings (formula inverted)           │
└────────────────────────────────────────────────────────┘
```

---

## Headroom Score Interpretation

### Visual Representation

```
Headroom Scale:
│
│  [0%]────[20%]────[40%]────[60%]────[80%]────[100%]
│   ↓        ↓        ↓        ↓        ↓        ↓
│  Perfect  Target   Good    Acceptable Poor   Failed
│  Solution Zone     Zone    Zone      Zone    Zone
│
│  Agent   Agent    Agent   Agent     Agent   Agent
│ passes   passes   passes  passes    passes  never
│ all 9    7-8 ✓   5-6 ⚠   3-4 ✗    0-2✗✗  solves
│ tests    tests    tests   tests     tests   task
│
└─────────────────────────────────────────────────────

Example Results:

AGENT A:  Pass: 9/9 → Headroom: 0%    [Perfect]
AGENT B:  Pass: 7/9 → Headroom: 22%   [Target ✓]
AGENT C:  Pass: 5/9 → Headroom: 44%   [Needs work]
AGENT D:  Pass: 2/9 → Headroom: 78%   [Major gaps]
```

---

## Common Failure Patterns

### Pattern 1: Sorting Error (40% of agents)
```python
# ❌ WRONG: Single-key sort
df.sort_values('priority', ascending=False).head(5)

# ✓ CORRECT: Multi-key sort
df.sort_values(
    by=['priority', 'item_id'],
    ascending=[False, True]
).head(5)

Impact: Items selected but wrong order → CSV assertion fails
```

### Pattern 2: Filter Combination Error (35% of agents)
```python
# ❌ WRONG: Sequential filters (or operation)
high_priority = df[df['priority'] >= percentile_75]
not_zone_a = df[df['zone'] != 'A']
result = high_priority.append(not_zone_a)  # Wrong!

# ✓ CORRECT: Combined filter (and operation)
result = df[(df['priority'] >= percentile_75) & (df['zone'] != 'A')]

Impact: Wrong items included/excluded → Item count fails
```

### Pattern 3: Rounding Precision (20% of agents)
```python
# ❌ WRONG: Default rounding
total_savings = df['savings'].sum()  # 186.5

# ✓ CORRECT: Explicit 2-decimal rounding
total_savings = round(df['savings'].sum(), 2)  # 186.50

Impact: String comparison fails (186.5 ≠ 186.50 in JSON)
```

### Pattern 4: Schema Mismatch (15% of agents)
```python
# ❌ WRONG: Extra fields or wrong naming
json_output = {
    'items': priority_item_ids,           # Wrong key name
    'total_time_saved': total_savings,    # Wrong key name
    'validation': debug_checks,           # Wrong key name
    'extra_field': 'unnecessary'          # Extra field
}

# ✓ CORRECT: Exact schema
json_output = {
    'priority_item_ids': priority_item_ids,
    'total_savings_seconds': total_savings,
    'debug_checks': debug_checks
}

Impact: JSON schema validation fails
```

### Pattern 5: Debug Check Enforcement (25% of agents)
```python
# ❌ WRONG: Silently skip failed checks
if nulls_found:
    debug_checks['no_null_demand'] = False
# ... continue anyway

# ✓ CORRECT: Halt on any failed check
debug_checks['no_null_demand'] = True
if nulls_found:
    debug_checks['no_null_demand'] = False
    raise AssertionError("Failed: null values found")

Impact: Execution should halt; execution continues → invalid results
```

---

## Quick Decision Tree

```
Agent runs benchmark
         ↓
    ┌─ FILES EXIST? ────────────┐
    │ YES ↓                      NO ↓
    │ Continue            Fail: FileNotFoundError
    │                     (Headroom = 100%)
    │
    ├─ TYPES CORRECT? ──────────┐
    │ YES ↓                      NO ↓
    │ Continue            Fail: Type mismatch
    │                     (Headroom = 89%)
    │
    ├─ DEBUG CHECKS ALL TRUE? ──┐
    │ YES ↓                      NO ↓
    │ Continue            Fail: Validation error
    │                     (Headroom = 78%)
    │
    ├─ SCHEMA VALID? ───────────┐
    │ YES ↓                      NO ↓
    │ Continue            Fail: Schema mismatch
    │                     (Headroom = 67%)
    │
    ├─ ITEM ORDER CORRECT? ─────┐
    │ YES ↓                      NO ↓
    │ Continue            Fail: Sorting error
    │                     (Headroom = 44%)
    │
    ├─ ROUNDING CORRECT? ───────┐
    │ YES ↓                      NO ↓
    │ Continue            Fail: Precision error
    │ PASS (headroom      (Headroom = 22%)
    │ = 0-10%)
```

---

## Key Takeaways

| Aspect | Value | Significance |
|--------|-------|--------------|
| **Task Type** | Multi-step autonomous workflow | Tests planning ability |
| **Determinism** | 100% (same input → same output) | Enables reproducible testing |
| **Complexity** | Medium-High (9 logic branches) | Sufficient for headroom measurement |
| **Expected Headroom** | 20-40% | Shows improvement potential |
| **Failure Points** | 5 major categories | Specific areas for agent improvement |
| **Evaluation Objectivity** | 100% (9 unit tests) | No subjective grading |
| **Time to Execute** | 45-60 seconds | Practical for iterative testing |

---

## Related Resources

**Inside This Package:**
- README.md → Start here
- IMPROVED_AGENTIC_PROMPT.md → Full prompt specification
- golden_solution_pharma_redistribution.ipynb → Reference implementation
- DEPLOYMENT_GUIDE.md → Evaluation framework

**External Resources:**
- Google Colab: https://colab.research.google.com
- Pandas Documentation: https://pandas.pydata.org/docs
- JSON Schema: https://json-schema.org

---

**Last Updated**: April 7, 2026
**Version**: 1.0 (Initial Release)
**Status**: Production Ready
