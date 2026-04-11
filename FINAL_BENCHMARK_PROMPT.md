# Agentic Benchmark: Inventory Risk Assessment

## The Task

You are an Autonomous Inventory Risk Manager. Identify the top 10 highest-risk products that need emergency restocking based on stockout probability, safety stock violations, and demand volatility.

## What You Need to Do

### 1. Load & Validate Data
- Load `inventory_dataset.csv` as `inventory_df`
- Required columns: `item_id`, `category`, `stock_level`, `reorder_point`, `daily_demand`, `demand_std_dev`, `lead_time_days`, `holding_cost_per_unit_day`, `last_restock_date`, `stockout_count_last_month`
- Check for null values in numeric columns
- Track success in `debug_checks` dictionary

### 2. Calculate Safety Stock & Risk Scores
Calculate safety stock baseline:
```
Safety_Stock = (daily_demand × lead_time_days) + (2.33 × demand_std_dev × √lead_time_days)
```

Calculate risk score for each item:
```
Risk_Score = (days_until_stockout × stockout_frequency) + (safety_violation × 10) + demand_volatility
```

Where:
- `days_until_stockout` = stock_level / daily_demand (minimum 1)
- `stockout_frequency` = stockout_count_last_month
- `safety_violation` = 1 if stock < safety_stock, else 0
- `demand_volatility` = demand_std_dev / daily_demand

All values rounded to 2 decimals.

### 3. Filter for High-Risk Items
Find items where ALL conditions are true:
- risk_score >= 80th percentile of all risk_scores
- stockout_count_last_month > 0 (proven history of problems)
- stock_level < reorder_point (already below threshold)

### 4. Rank & Select Top 10
Sort by:
1. risk_score (highest first)
2. stock_level (lowest first)
3. item_id (A→Z alphabetically)

Take only top 10 items (or all if fewer than 10 qualify).

### 5. Calculate Emergency Metrics
For each item:
- `recommended_restock_quantity` = (reorder_point - stock_level) + (daily_demand × 7)
- `urgency_flag` = "CRITICAL" if stock ≤ 0, else "HIGH"
- `days_to_stockout` = stock_level / daily_demand (rounded to 1 decimal)

### 6. Debug Validation
Create and verify:
```python
debug_checks = {
    'data_loaded': bool,
    'required_columns_exist': bool,
    'no_null_numeric_values': bool,
    'risk_scores_positive': bool
}
```
All values must be True. If any is False, halt execution.

### 7. Variable Storage (Exact Names & Types)
- `inventory_df`: pandas.DataFrame
- `emergency_restock_df`: pandas.DataFrame (≤10 rows)
- `emergency_item_ids`: list[str]
- `total_emergency_stock_deficit`: float (rounded to 2 decimals)
- `highest_risk_score`: float (rounded to 2 decimals)
- `debug_checks`: dict[str, bool]

### 8. Export Results
**File 1**: `/content/emergency_restock_audit.csv`
- Columns: item_id, category, stock_level, reorder_point, risk_score, urgency_flag, days_to_stockout, recommended_restock_quantity
- No index

**File 2**: `/content/emergency_action_plan.json`
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

## Success Criteria

✓ All output files generated
✓ All debug checks pass (True)
✓ JSON schema exact match
✓ Items ranked deterministically (multi-key sort)
✓ Rounding exactly 2 decimals
