# NEW Agentic Benchmark: Inventory Risk Assessment & Emergency Restocking

## Overview
This is an autonomous benchmark designed to test AI agents on complex inventory risk analysis. The task requires independent planning, risk calculation, threshold analysis, deterministic ranking, and business metric computation.

---

## AGENTIC PROMPT (For Agent Evaluation)

### Context
You are an **Autonomous Inventory Risk Manager**. Your goal is to identify high-risk products that are approaching critical stockout conditions and require immediate emergency restocking actions.

### Primary Objective
**Identify and rank the top 10 highest-risk inventory items that require emergency restocking, based on stockout probability, safety stock violation, and demand volatility.**

The task is non-linear and requires autonomous planning. Do not ask for step-by-step guidance—manage your own analysis workflow.

---

## Hard Constraints & Requirements

### 1. Data Loading & Validation
- Load `inventory_dataset.csv` into a pandas DataFrame named `inventory_df`
- Required columns: `item_id`, `category`, `stock_level`, `reorder_point`, `daily_demand`, `demand_std_dev`, `lead_time_days`, `holding_cost_per_unit_day`, `last_restock_date`, `stockout_count_last_month`
- Verify file existence and all columns present
- Check for null values in all numeric columns

### 2. Safety Stock Violation Detection
Calculate safety stock baseline:
```
Safety_Stock = (daily_demand × lead_time_days) + (2.33 × demand_std_dev × sqrt(lead_time_days))
```
- This represents the minimum buffer to prevent 99% of stockouts
- For each item, check if: `current_stock_level < safety_stock_baseline`
- Flag items violating safety stock as **HIGH RISK**

### 3. Stockout Probability Calculation (Deterministic)
Calculate stockout risk for each item:
```
Risk_Score = (days_until_stockout × stockout_frequency_weight) + (safety_violation_penalty × 10) + (demand_volatility_factor)
```

Where:
- `days_until_stockout`: MAX(1, stock_level / daily_demand)
- `stockout_frequency_weight`: stockout_count_last_month (items with history are riskier)
- `safety_violation_penalty`: 1 if stock < safety_stock, 0 otherwise
- `demand_volatility_factor`: demand_std_dev / daily_demand (normalized volatility)

All components rounded to 2 decimal places.

### 4. Efficiency Analysis: Holding Cost Impact
- For each item, calculate: `potential_holding_cost = stock_level × holding_cost_per_unit_day × days_until_reorder`
- This identifies items with high carrying costs that should be prioritized for reduction
- Include this in the final audit for business context

### 5. Risk Threshold & Multi-Condition Filtering
- Calculate the **80th percentile** of risk_score across ALL items
- Filter for items where:
  - `risk_score >= 80th_percentile` AND
  - `stockout_count_last_month > 0` (proven history of problems) AND
  - `stock_level < reorder_point` (already below reorder threshold)
- If fewer than 10 items meet criteria, include all qualifying items
- If more than 10 items meet criteria, apply tie-breaking to select exactly 10

### 6. Deterministic Ranking & Tie-Breaking Rules (Critical for Reproducibility)
Sort the filtered items using multi-key ordering:
1. **Primary**: By `risk_score` in **descending order** (highest risk first)
2. **Secondary**: By `stock_level` in **ascending order** (lowest stock first)
3. **Tertiary**: By `item_id` in **ascending order** (lexicographic A→Z)

Example: If items have same risk_score, prioritize the one with lower stock. If still tied, use item_id alphabetically.

Store results in DataFrame called `emergency_restock_df`. Extract item IDs as `emergency_item_ids: list[str]`.

### 7. Emergency Action Planning
For each item in emergency_restock_df, calculate:
- `recommended_restock_quantity = (reorder_point - current_stock_level) + (daily_demand × 7)` (enough to cover reorder point + 1 week demand)
- `urgency_flag`: "CRITICAL" if stock_level <= 0, "HIGH" if stock_level < safety_stock
- `days_to_stockout`: MAX(1, stock_level / daily_demand), rounded to 1 decimal place

### 8. Validation & Debug Checks
You **must** implement and populate a `debug_checks` dictionary:
```python
debug_checks = {
    'data_loaded': bool,                    # CSV loaded successfully
    'required_columns_exist': bool,        # All 10 columns present
    'no_null_numeric_values': bool,        # No nulls in numeric columns
    'risk_scores_positive': bool           # All risk scores >= 0
}
```
- If **any** check is False, execution must halt with explanatory error
- All checks must be True before proceeding to export

### 9. Variable Storage Requirements (Strict Typing)
You **must** use exactly these variable names and types:
- `inventory_df`: `pandas.DataFrame` (original dataset)
- `emergency_restock_df`: `pandas.DataFrame` (filtered & ranked, ≤10 items)
- `emergency_item_ids`: `list[str]` (item ID strings, e.g., `['ITM10001', 'ITM10005', ...]`)
- `total_emergency_stock_deficit`: `float` (sum of all restock_quantity values, rounded to 2 decimals)
- `highest_risk_score`: `float` (max risk_score from emergency_restock_df, rounded to 2 decimals)
- `debug_checks`: `dict[str, bool]` (validation results)

### 10. Output Generation & File Export
Save all results to `/content/` directory:

**File 1: Audit CSV**
- Path: `/content/emergency_restock_audit.csv`
- Content: emergency_restock_df with columns: item_id, category, stock_level, reorder_point, risk_score, urgency_flag, days_to_stockout, recommended_restock_quantity
- No index, proper column ordering

**File 2: Strategic JSON**
- Path: `/content/emergency_action_plan.json`
- Exact schema:
```json
{
  "emergency_item_ids": ["ITM10001", "ITM10005", ...],
  "total_emergency_stock_deficit": 1250.50,
  "highest_risk_score": 45.78,
  "debug_checks": {
    "data_loaded": true,
    "required_columns_exist": true,
    "no_null_numeric_values": true,
    "risk_scores_positive": true
  }
}
```

### 11. Verification Checklist (Before Submission)
- ✓ All 4 debug checks are True
- ✓ emergency_restock_df has ≤ 10 rows
- ✓ emergency_item_ids is list[str] with ≤ 10 items
- ✓ total_emergency_stock_deficit is float, rounded 2 decimals
- ✓ highest_risk_score is float, rounded 2 decimals
- ✓ Both output files exist and readable
- ✓ No temporary variables in final namespace

---

## Headroom Analysis: Expected Failure Points

**Pattern 1: Multi-Condition Filter Logic (45% failure)**
- Forget to combine all 3 conditions (usually miss stockout_count > 0)
- Apply filters sequentially instead of using AND operator
- Result: Wrong items selected

**Pattern 2: Risk Score Calculation (35% failure)**
- Wrong formula implementation (missing components or wrong weights)
- Forget to round intermediate values to 2 decimals
- Result: Incorrect risk rankings

**Pattern 3: Multi-Key Sorting (40% failure)**
- Apply single-key sort only (risk_score)
- Miss secondary sort by stock_level and tertiary by item_id
- Result: Different item order; audit comparison fails

**Pattern 4: Safety Stock Formula (30% failure)**
- Mathematical error in square root calculation
- Wrong interpretation of 2.33 constant (z-score for 99% service level)
- Result: Incorrect safety stock baseline

**Pattern 5: JSON Schema (20% failure)**
- Extra fields or wrong field names
- Missing debug_checks object
- Type mismatch (string instead of float)
- Result: Schema validation fails

---

## Success Indicators

### Perfect Execution (Headroom < 10%)
- All 4 debug checks True
- All 10 items ranked correctly
- JSON schema matches exactly
- File exports successful

### Target Execution (Headroom 25-35%)
- 7-8 debug checks True (or 4/4 but minor calculation errors)
- 8-10 items identified correctly
- JSON mostly correct (minor rounding discrepancies)
- Specific failure: Usually sorting or risk calculation error

### Acceptable Execution (Headroom 40-50%)
- 3-4 debug checks True
- 5-8 items identified
- JSON schema mostly correct
- Multiple logic errors visible

---

## Unit Test Framework (Pseudo-Code)

```python
def validate_emergency_restock_output():
    """Comprehensive validation of agent output."""
    
    tests_passed = 0
    
    # Test 1: Files exist
    assert os.path.exists('/content/emergency_restock_audit.csv'), "CSV not found"
    assert os.path.exists('/content/emergency_action_plan.json'), "JSON not found"
    tests_passed += 1
    
    # Test 2: Load outputs
    df_audit = pd.read_csv('/content/emergency_restock_audit.csv')
    with open('/content/emergency_action_plan.json') as f:
        action_plan = json.load(f)
    tests_passed += 1
    
    # Test 3: JSON schema
    required_keys = {'emergency_item_ids', 'total_emergency_stock_deficit', 'highest_risk_score', 'debug_checks'}
    assert required_keys.issubset(action_plan.keys()), "Missing JSON keys"
    tests_passed += 1
    
    # Test 4: Types correct
    assert isinstance(action_plan['emergency_item_ids'], list), "Item IDs not list"
    assert all(isinstance(x, str) for x in action_plan['emergency_item_ids']), "Item IDs not strings"
    assert isinstance(action_plan['total_emergency_stock_deficit'], float), "Stock deficit not float"
    assert isinstance(action_plan['highest_risk_score'], float), "Risk score not float"
    tests_passed += 1
    
    # Test 5: Debug checks all True
    assert all(action_plan['debug_checks'].values()), "Debug checks failed"
    tests_passed += 1
    
    # Test 6: Item count <= 10
    assert len(action_plan['emergency_item_ids']) <= 10, "Too many items"
    tests_passed += 1
    
    # Test 7: CSV/JSON consistency
    csv_items = set(df_audit['item_id'].astype(str))
    json_items = set(action_plan['emergency_item_ids'])
    assert csv_items == json_items, "Items mismatch between CSV and JSON"
    tests_passed += 1
    
    # Test 8: Rounding compliance (2 decimals)
    deficit_str = f"{action_plan['total_emergency_stock_deficit']:.2f}"
    risk_str = f"{action_plan['highest_risk_score']:.2f}"
    assert action_plan['total_emergency_stock_deficit'] == float(deficit_str), "Stock deficit rounding"
    assert action_plan['highest_risk_score'] == float(risk_str), "Risk score rounding"
    tests_passed += 1
    
    # Test 9: Item IDs valid format
    for item_id in action_plan['emergency_item_ids']:
        assert item_id.startswith('ITM'), f"Invalid item ID format: {item_id}"
    tests_passed += 1
    
    print(f"✓ All tests passed ({tests_passed}/9)")
    return True
```

---

## Evaluation Criteria

### Tests (9 Total)
1. Output files exist
2. JSON loads successfully
3. JSON schema valid
4. Variable types correct
5. Debug checks all true
6. Item count ≤ 10
7. CSV/JSON consistency
8. Rounding compliance
9. Item ID format valid

### Pass Rate Target
- **70-80%** (7-8 tests pass)
- Expected headroom: **20-30%**

### Failure Modes
If tests fail, check:
- Sorting order (multi-key sort missing?)
- Filter logic (all 3 conditions applied?)
- Risk calculation (formula implemented correctly?)
- Rounding precision (exactly 2 decimals?)
- JSON schema (exact keys, no extras?)
