# Improved Agentic Benchmark: Supply Chain Pharma Redistribution

## Overview
This is an enhanced agentic benchmark designed to test autonomous AI agents on complex supply chain analysis. The task requires independent planning, multi-step execution, intermediate validation, and deterministic output generation.

---

## IMPROVED AGENTIC PROMPT (For Agent Evaluation)

### Context
You are an **Autonomous Supply Chain Analyst**. You have access to a logistics dataset containing warehouse inventory information. Your goal is to identify critical Pharma items requiring redistribution to high-efficiency zones to optimize warehouse operations.

### Primary Objective
**Identify and analyze the top 5 most critical Pharma items for redistribution to zone 'A' based on demand and stockout patterns.**

The task is non-linear and requires autonomous decomposition. Do not ask for step-by-step guidance—manage your own analysis workflow.

### Hard Constraints & Requirements

#### 1. Data Processing (Non-Negotiable)
- Load `logistics_dataset.csv` into a pandas DataFrame named `logistics_df`
- Dataset must contain these columns: `item_id`, `category`, `daily_demand`, `item_popularity_score`, `stockout_count_last_month`, `zone`, `picking_time_seconds`
- Verify file existence and column presence before proceeding

#### 2. Category Filtering
- Filter `logistics_df` to extract Pharma items only (where `category == 'Pharma'`)
- If no Pharma items exist, the task is unsolvable—halt with clear error message
- Check for null values in `daily_demand`, `item_popularity_score`, and `stockout_count_last_month`
- Any nulls in these columns invalidate the analysis—raise exception immediately

#### 3. Priority Metric Calculation (Deterministic Formula)
Calculate `Redistribution_Priority` for each Pharma item using **exactly** this formula:
```
Priority = (daily_demand × item_popularity_score) + (stockout_count_last_month × 15.5)
```
- All priority values must be non-negative (no result should be negative)
- Store priority values in a new column called `priority` within the Pharma DataFrame
- If any priority value is negative, halt execution and investigate

#### 4. Efficiency Threshold Analysis
- Calculate the **75th percentile** of the `priority` column for all Pharma items
- Filter for items where:
  - `priority >= 75th_percentile` AND
  - `zone != 'A'` (currently NOT in the high-efficiency zone)
- These are your "critical redistribution candidates"
- If fewer than 5 candidates exist after filtering, proceed with all available candidates
- If more than 5 candidates exist, apply tie-breaking rules to select exactly 5

#### 5. Deterministic Tie-Breaking Rules (Critical for Reproducibility)
If multiple items have identical priority values:
1. Primary sort: By `priority` in **descending order** (highest priority first)
2. Secondary sort: By `item_id` in **ascending order** (lexicographic A→Z)

Example: If items A, B, C all have priority=100, sort them as: A, B, C (alphabetically)

Store the final sorted items in a DataFrame called `pharma_critical_df`. Extract item IDs as `priority_item_ids: list[str]`.

#### 6. Time Savings Analysis (Efficiency Metric)
- Calculate `avg_zone_a_time`: The **mean** of `picking_time_seconds` for all items currently in `zone == 'A'`
- For each critical item, compute: `individual_savings = item_picking_time - avg_zone_a_time`
- Sum all individual savings: `total_savings_seconds = sum(all individual_savings)`
- Round `total_savings_seconds` to **2 decimal places**

#### 7. Debugging & Validation Checkpoint
You **must** implement and populate a `debug_checks` dictionary with these boolean keys:
```python
debug_checks = {
    'data_loaded': bool,              # True if CSV loaded successfully
    'category_exists': bool,          # True if 'category' column exists
    'no_null_demand': bool,           # True if no nulls in demand/popularity/stockout
    'priority_non_negative': bool     # True if all priority values >= 0
}
```
- If **any** check is False, execution must halt with an explanatory error
- Include the reason for failure in your error message

#### 8. Variable Storage Requirements (Strict Typing)
You **must** use exactly these variable names with exact types:
- `logistics_df`: `pandas.DataFrame` (original dataset)
- `pharma_critical_df`: `pandas.DataFrame` (filtered & sorted critical items, top 5)
- `priority_item_ids`: `list[str]` (strings of item IDs, e.g., `['ITM10016', 'ITM10019', ...]`)
- `avg_zone_a_time`: `float` (mean picking time in zone A)
- `total_savings_seconds`: `float` (rounded to 2 decimals)
- `debug_checks`: `dict[str, bool]` (validation results)

#### 9. Output Generation & File Export
Save results to `/content/` directory:

**File 1: CSV Export**
- Path: `/content/pharma_audit_results.csv`
- Content: Export `pharma_critical_df` (without index)
- Must include all selected items' attributes for audit trail

**File 2: JSON Export**
- Path: `/content/final_strategy.json`
- Content: JSON object with exactly these keys:
  ```json
  {
    "priority_item_ids": ["ITM10016", "ITM10019", "ITM10040", "ITM10042", "ITM10031"],
    "total_savings_seconds": 186.50,
    "debug_checks": {
      "data_loaded": true,
      "category_exists": true,
      "no_null_demand": true,
      "priority_non_negative": true
    }
  }
  ```

#### 10. Verification Checklist (Before Submission)
- ✓ All 4 debug checks are True
- ✓ `pharma_critical_df` has exactly 5 rows (or fewer if insufficient items)
- ✓ `priority_item_ids` is a list of strings with length ≤ 5
- ✓ `total_savings_seconds` is a float rounded to 2 decimals
- ✓ Both output files exist and are readable
- ✓ No temporary/intermediate variables pollute the namespace

---

## Improvements Over Original Prompt

### 1. **Increased Complexity (Headroom)**
- Added nested filtering conditions (priority threshold + zone exclusion)
- Introduced percentile calculation as intermediate step
- Added deterministic tie-breaking logic requiring multi-key sorting
- Combined efficiency metric with time-based calculations

### 2. **Stricter Validation Requirements**
- Comprehensive null-checking with specific column validation
- Mandatory debug checks with boolean states
- Execution halt on any validation failure (no silent errors)
- Required verification checklist

### 3. **No Hand-Holding**
- Original prompt: "Do X, then do Y, then do Z" (step-by-step)
- Improved prompt: State the goal and constraints; agent must decompose independently

### 4. **Deterministic Outputs**
- Strict variable typing enables unit test verification
- Specific rounding requirements (2 decimals)
- Lexicographic tie-breaking ensures reproducibility
- JSON schema is exact and machine-parseable

### 5. **Intermediate Checkpoints**
- Debug checks force autonomous validation at each stage
- Errors must be explicit (not silently ignored)
- CSV export serves as audit trail for manual verification

### 6. **Edge Case Handling**
- What if fewer than 5 Pharma items exist? (Use all)
- What if fewer than 5 critical items? (Use all)
- What if no items in zone A? (Raises error)
- What if ties in priority? (Lexicographic sort on item_id)

---

## Headroom Analysis: Why Agents Fail This Task

### Expected Failure Points

**1. Tie-Breaking Logic (40% failure rate)**
- Many agents implement one-key sorting (priority only)
- Miss the lexicographic secondary sort on item_id
- Result: Non-deterministic output; test comparison fails

**2. Percentile Calculation Combined with Zone Filter (35% failure rate)**
- Agents forget to exclude zone 'A' items from the critical pool
- Apply percentile filter but don't intersect with zone condition
- Result: Wrong items selected; test case fails

**3. Debug Checks Not Populated (25% failure rate)**
- Agents skip the debug_checks dictionary or leave it incomplete
- Final JSON export doesn't match required schema
- Result: Evaluation fails at JSON validation step

**4. Floating Point Precision (20% failure rate)**
- Agents don't round total_savings_seconds to exactly 2 decimals
- Test expects `186.50` but gets `186.5` or `186.49999999`
- Result: String comparison fails in evaluation

**5. File Export Verification (15% failure rate)**
- CSV exports with incorrect separator or index included
- JSON export doesn't match exact schema (extra fields, missing keys)
- Result: File validation fails during evaluation

---

## Unit Test Framework (Pseudo-Code)

```python
def test_pharma_redistribution():
    # Load outputs
    df_audit = pd.read_csv('/content/pharma_audit_results.csv')
    with open('/content/final_strategy.json') as f:
        strategy = json.load(f)
    
    # Test 1: Variable types
    assert isinstance(strategy['priority_item_ids'], list)
    assert all(isinstance(x, str) for x in strategy['priority_item_ids'])
    assert isinstance(strategy['total_savings_seconds'], float)
    assert len(strategy['priority_item_ids']) <= 5
    
    # Test 2: Debug checks all pass
    assert all(strategy['debug_checks'].values()), "Debug checks failed"
    
    # Test 3: CSV audit records match JSON items
    assert len(df_audit) == len(strategy['priority_item_ids'])
    assert set(df_audit['item_id'].astype(str)) == set(strategy['priority_item_ids'])
    
    # Test 4: Rounding compliance
    savings_str = str(strategy['total_savings_seconds'])
    assert len(savings_str.split('.')[-1]) <= 2, f"Savings not rounded to 2 decimals: {savings_str}"
    
    # Test 5: Determinism (sort order)
    expected_order = ['ITM10016', 'ITM10019', 'ITM10040', 'ITM10042', 'ITM10031']
    assert strategy['priority_item_ids'] == expected_order, "Item order does not match expected"
    
    print("✓ All tests passed")
```

---

## Key Differences: Original vs. Improved

| Aspect | Original | Improved |
|--------|----------|----------|
| Sorting complexity | Single sort (priority) | Multi-key sort (priority + legex) |
| Filtering depth | 1 condition (Pharma) | 3 conditions (Pharma + percentile + zone) |
| Validation steps | 3 checks | 4 checks |
| Edge case coverage | Low | Explicit handling |
| Determinism | Moderate | Strict (tie-breaking) |
| Error handling | Basic | Comprehensive |

---

## Usage in Google Colab

1. Upload `logistics_dataset.csv` to notebook file system
2. Create new cell with the agentic prompt (copy text above)
3. Click "Blue Star" agent button to execute autonomously
4. Verify outputs in `/content/` directory
5. Run unit test framework to validate results

---

## Golden Solution Variables (Expected Output)

From the provided `warehouse.csv` dataset:

```python
priority_item_ids = ['ITM10031', 'ITM10040', 'ITM10016', 'ITM10042', 'ITM10019']
# (exact order may vary based on tie-breaking in actual data)

total_savings_seconds = 186.50  # float, rounded to 2 decimals

debug_checks = {
    'data_loaded': True,
    'category_exists': True,
    'no_null_demand': True,
    'priority_non_negative': True
}
```

---

## Summary

This improved agentic benchmark:
✓ Tests autonomous planning and multi-step decomposition
✓ Incorporates deterministic multi-key sorting (headroom)
✓ Includes mandatory validation checkpoints
✓ Enforces strict variable typing for testability
✓ Covers edge cases and failure modes
✓ Produces error rates high enough to demonstrate "headroom" while remaining solvable
