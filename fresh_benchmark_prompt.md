# Fresh Agentic Benchmark: Inventory Risk Assessment

## Task Overview

You are an **Autonomous Inventory Risk Manager** working for a large warehouse operation. Your job is to identify which items are at highest risk of running out of stock and need emergency restocking.

The task requires you to:
- Analyze inventory data independently
- Calculate risk scores based on multiple factors
- Filter items using complex logic
- Rank items deterministically (reproducibly)
- Generate business-ready reports

**Important**: You must do this autonomously without asking for step-by-step instructions.

---

## The Problem You're Solving

Warehouse managers need to know: "Which items need emergency restocking RIGHT NOW?"

A simple approach (just look at stock level) doesn't work because:
- An item with 1 unit might be OK if demand is 0.1 units/day (30 days left)
- An item with 100 units might be critical if demand is 50 units/day (2 days left)
- Volatile demand items are riskier than stable items
- Items with stockout history deserve more attention

Your task is to identify the true risk items using a mathematical model.

---

## Required Data Source

Load `inventory_dataset.csv` containing:
- `item_id`: Unique item identifier
- `category`: Product category
- `stock_level`: Current units in stock
- `reorder_point`: Minimum stock level target
- `daily_demand`: Average daily units sold
- `demand_std_dev`: Volatility in demand
- `lead_time_days`: Days to receive new order
- `holding_cost_per_unit_day`: Cost per unit per day
- `last_restock_date`: When last restocked
- `stockout_count_last_month`: How many times item ran out last month

---

## Your Objective

Identify and rank the **top 10 highest-risk items** that require emergency restocking.

---

## Step-by-Step Logic (What to Do)

### 1. Load & Validate Data
- Load CSV into pandas DataFrame
- Verify all 10 required columns exist
- Check for null values in numeric columns
- Create `debug_checks` dictionary

### 2. Calculate Safety Stock
This is the minimum stock needed to prevent 99% of stockouts:

```
Safety_Stock = (daily_demand × lead_time_days) + (2.33 × demand_std_dev × √lead_time_days)
```

What this means:
- First part: stock needed for lead time period
- Second part: buffer for safety (2.33 is the math magic for 99% service level)

### 3. Calculate Risk Score
For each item, calculate:

```
Risk_Score = (days_until_stockout × stockout_history) + (safety_violation × 10) + volatility
```

Where:
- `days_until_stockout` = MAX(1, stock_level / daily_demand)
  - How many days until this item runs out
  - Min of 1 day to avoid division issues

- `stockout_history` = stockout_count_last_month
  - Items that ran out before are riskier
  - Multiply by days_until_stockout

- `safety_violation` = 1 if (stock_level < safety_stock), else 0
  - Items below safety level are penalized
  - Multiply by 10 to make it significant

- `volatility` = demand_std_dev / daily_demand
  - High variation = higher risk
  - Normalize by dividing by demand

Round all values to 2 decimal places.

### 4. Apply Risk Threshold
- Calculate **80th percentile** of all risk scores
- Filter items where:
  - `risk_score >= 80th_percentile` AND
  - `stockout_count_last_month > 0` AND
  - `stock_level < reorder_point`

All three conditions must be true.

### 5. Deterministic Ranking (CRITICAL)
Sort filtered items by:
1. **First**: risk_score (highest first - descending)
2. **Then**: stock_level (lowest first - ascending)
3. **Finally**: item_id (A-Z - ascending)

Example: If items A, B, C have same risk_score:
- Compare their stock levels
- Pick lowest stock first
- If still tied, use alphabetical (ITM10001 before ITM10002)

Select top 10 items (or fewer if less than 10 qualify).

### 6. Calculate Emergency Restock Quantity
For each selected item:
```
Restock_Qty = (reorder_point - current_stock) + (daily_demand × 7)
```

This = enough to reach reorder point + 1 week buffer

### 7. Assign Urgency Flag
- "CRITICAL" if stock_level <= 0
- "HIGH" if stock_level < safety_stock
- Otherwise "NORMAL"

### 8. Create Summary Metrics
- `total_emergency_stock_deficit` = sum of all restock quantities (2 decimals)
- `highest_risk_score` = max risk score among selected items (2 decimals)

### 9. Validation Checks
Update debug_checks dictionary:
```python
debug_checks = {
    'data_loaded': True/False,              # CSV loaded?
    'required_columns_exist': True/False,   # All 10 cols?
    'no_null_numeric_values': True/False,   # No nulls?
    'risk_scores_positive': True/False      # All >= 0?
}
```

If any check is False, STOP execution and report error.

---

## Required Variable Names & Types

You MUST use exactly these:

```python
inventory_df: pandas.DataFrame              # Original data
emergency_restock_df: pandas.DataFrame      # Top 10 items
emergency_item_ids: list[str]               # Item IDs, e.g. ['ITM10001', 'ITM10002']
total_emergency_stock_deficit: float        # Sum of quantities
highest_risk_score: float                   # Max risk score
debug_checks: dict[str, bool]               # Validation results
```

---

## File Exports

Save to `/content/` directory:

### File 1: CSV Audit Report
- Path: `/content/emergency_restock_audit.csv`
- Columns: item_id, category, stock_level, reorder_point, risk_score, urgency_flag, days_until_stockout, recommended_restock_quantity
- No index, ordered by risk ranking

### File 2: JSON Strategic Plan
- Path: `/content/emergency_action_plan.json`
- Exact format:
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

---

## Verification Checklist

Before finishing, verify:
- ✓ All 4 debug checks are True
- ✓ emergency_restock_df has ≤ 10 rows
- ✓ emergency_item_ids is list[str], length ≤ 10
- ✓ total_emergency_stock_deficit is float, 2 decimals
- ✓ highest_risk_score is float, 2 decimals
- ✓ Both CSV and JSON files exist in /content/
- ✓ JSON format matches exactly (no extra fields)
- ✓ All risk scores in output are positive

---

## What NOT to Do

- ❌ Ask me for step-by-step guidance
- ❌ Hard-code item IDs or values
- ❌ Use external libraries beyond pandas/numpy/json/os
- ❌ Round to wrong decimals (must be exactly 2)
- ❌ Use single-key sorting (must use 3-key)
- ❌ Include temporary variables in final output
- ❌ Skip the debug checks

---

## Expected Execution Time

- 30-60 seconds total
- Depends on dataset size and agent reasoning time

---

## Success Indicators

✓ All outputs generated
✓ All debug checks pass
✓ JSON schema valid
✓ Items deterministically ranked
✓ No errors or warnings
