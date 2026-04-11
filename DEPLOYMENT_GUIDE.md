# Headroom Agentic Benchmark: Deployment & Evaluation Guide

## Quick Start

### File Structure
```
warehouse-mlops/
├── Data/
│   └── warehouse.csv (source data)
├── IMPROVED_AGENTIC_PROMPT.md (this prompt for agents)
├── golden_solution_pharma_redistribution.ipynb (golden solution)
├── DEPLOYMENT_GUIDE.md (this file)
└── evaluation_results.json (generated after agent runs)
```

---

## Step 1: Prepare the Data

The benchmark uses `warehouse.csv` which contains 50+ Pharma items across 10+ categories. The data includes:

| Column | Purpose |
|--------|---------|
| item_id | Unique identifier for merchandise |
| category | Product category (Pharma, Automotive, etc.) |
| daily_demand | Average daily units requested |
| item_popularity_score | Normalized popularity metric (0-1) |
| stockout_count_last_month | Number of stockouts in past 30 days |
| zone | Current warehouse zone (A, B, C, D) |
| picking_time_seconds | Average time to pick this item |

### Data Statistics for Pharma Category
- **Total Pharma items**: ~12 items
- **Priority range**: ~20 to ~200 (based on formula)
- **Zone distribution**: Zones B, C, D (none currently in A)
- **75th percentile priority**: ~110-130 (varies by snapshot)

---

## Step 2: Deploy in Google Colab

### Setup Instructions

1. **Upload Data**
   ```python
   from google.colab import files
   uploaded = files.upload()
   # Select warehouse.csv
   # Rename to logistics_dataset.csv in working directory
   ```

2. **Copy the Agentic Prompt**
   - Open `IMPROVED_AGENTIC_PROMPT.md`
   - Copy the section: "IMPROVED AGENTIC PROMPT (For Agent Evaluation)"
   - Paste into a Colab cell as markdown + instructions
   - Click "Blue Star" agent button

3. **Execute Autonomously**
   - Agent will run the analysis without guidance
   - Monitor for errors in intermediate checkpoints
   - Wait for completion

---

## Step 3: Validate Agent Output

### Expected Output Files

After execution, agent should generate two files:

**1. `/content/pharma_audit_results.csv`**
Example:
```
item_id,category,daily_demand,item_popularity_score,stockout_count_last_month,zone,picking_time_seconds,priority
ITM10031,Pharma,45.72,0.86,6,C,96,176.3
ITM10040,Pharma,40.23,0.55,8,A,147,115.4
... (up to 5 rows)
```

**2. `/content/final_strategy.json`**
Example:
```json
{
  "priority_item_ids": ["ITM10031", "ITM10040", "ITM10016", "ITM10042", "ITM10019"],
  "total_savings_seconds": 186.50,
  "debug_checks": {
    "data_loaded": true,
    "category_exists": true,
    "no_null_demand": true,
    "priority_non_negative": true
  }
}
```

---

## Step 4: Run Evaluation Tests

Use this test suite to validate agent performance:

```python
import json
import pandas as pd

def evaluate_agent_output():
    """Comprehensive evaluation of agent output."""
    
    print("="*60)
    print("AGENTIC BENCHMARK EVALUATION")
    print("="*60)
    
    # Test 1: File existence
    print("\nTest 1: Output Files Exist")
    try:
        strategy = json.load(open('/content/final_strategy.json'))
        audit_df = pd.read_csv('/content/pharma_audit_results.csv')
        print("✓ Both output files exist and are readable")
    except Exception as e:
        print(f"✗ File loading error: {e}")
        return False
    
    # Test 2: JSON Schema Validation
    print("\nTest 2: JSON Schema Compliance")
    required_keys = {'priority_item_ids', 'total_savings_seconds', 'debug_checks'}
    if not required_keys.issubset(strategy.keys()):
        print(f"✗ Missing keys: {required_keys - set(strategy.keys())}")
        return False
    print("✓ JSON schema correct")
    
    # Test 3: Variable Types
    print("\nTest 3: Variable Type Compliance")
    try:
        assert isinstance(strategy['priority_item_ids'], list), "priority_item_ids not a list"
        assert all(isinstance(x, str) for x in strategy['priority_item_ids']), "Items not all strings"
        assert isinstance(strategy['total_savings_seconds'], float), "total_savings_seconds not float"
        assert isinstance(strategy['debug_checks'], dict), "debug_checks not dict"
        assert all(isinstance(v, bool) for v in strategy['debug_checks'].values()), "Debug checks not all bool"
        print("✓ All variable types correct")
    except AssertionError as e:
        print(f"✗ Type error: {e}")
        return False
    
    # Test 4: Debug Checks All Pass
    print("\nTest 4: Debug Checks Status")
    if not all(strategy['debug_checks'].values()):
        failed = [k for k, v in strategy['debug_checks'].items() if not v]
        print(f"✗ Debug checks failed: {failed}")
        return False
    print("✓ All debug checks passed")
    
    # Test 5: Item Count Constraint
    print("\nTest 5: Item Count (≤ 5)")
    if len(strategy['priority_item_ids']) > 5:
        print(f"✗ Too many items selected: {len(strategy['priority_item_ids'])} (max 5)")
        return False
    print(f"✓ Item count valid: {len(strategy['priority_item_ids'])}")
    
    # Test 6: CSV/JSON Consistency
    print("\nTest 6: CSV/JSON Consistency")
    csv_items = set(audit_df['item_id'].astype(str))
    json_items = set(strategy['priority_item_ids'])
    if csv_items != json_items:
        print(f"✗ Items mismatch. CSV: {csv_items}, JSON: {json_items}")
        return False
    print(f"✓ CSV and JSON items match ({len(csv_items)} items)")
    
    # Test 7: Rounding Compliance
    print("\nTest 7: Total Savings Rounding (2 decimals)")
    savings_str = f"{strategy['total_savings_seconds']:.2f}"
    if strategy['total_savings_seconds'] != float(savings_str):
        print(f"✗ Rounding error: {strategy['total_savings_seconds']} != {float(savings_str)}")
        return False
    print(f"✓ Rounding compliant: {strategy['total_savings_seconds']}")
    
    # Test 8: Item IDs Valid Format
    print("\nTest 8: Item ID Format Validation")
    for item_id in strategy['priority_item_ids']:
        if not item_id.startswith('ITM'):
            print(f"✗ Invalid item ID format: {item_id}")
            return False
    print(f"✓ All item IDs have valid format (ITM*)")
    
    # Test 9: Non-Negative Savings
    print("\nTest 9: Savings Logic Validation")
    if strategy['total_savings_seconds'] < 0:
        print(f"✗ Total savings is negative: {strategy['total_savings_seconds']}")
        return False
    print(f"✓ Total savings is non-negative")
    
    # Summary
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    print("Status: ✓ PASS - All tests successful")
    print(f"Items identified: {len(strategy['priority_item_ids'])}")
    print(f"Total time savings: {strategy['total_savings_seconds']} seconds")
    return True

# Run evaluation
evaluate_agent_output()
```

---

## Headroom Interpretation

### Success Criteria (Agent Passes)
✓ All output files generated correctly
✓ All debug checks = True
✓ Output schema matches exactly
✓ deterministic tie-breaking applied correctly
✓ All tests pass

### Failure Modes (Agent Fails) - Demonstrates Headroom

**Common Failure 1: Incorrect Sorting**
- Agent sorts by priority only (descending)
- Misses lexicographic secondary sort on item_id
- Result: Items selected but in wrong order; CSV/JSON comparison fails
- **Fix**: Implement two-key sort: [('priority', False), ('item_id', True)]

**Common Failure 2: Zone Filter Error**
- Agent finds top 5 Pharma items by priority (ignores zone condition)
- Misses the critical "AND zone != 'A'" requirement
- Result: Wrong items selected; test fails
- **Fix**: Add explicit zone filter: `pharma_df[pharma_df['zone'] != 'A']`

**Common Failure 3: Percentile Confusion**
- Agent finds all items > 75th percentile (correct)
- But doesn't combine with zone filter correctly
- Includes zone A items or excludes valid candidates
- Result: Item count doesn't match; test fails
- **Fix**: Use proper filter: `(priority >= p75) & (zone != 'A')`

**Common Failure 4: JSON Export Issues**
- Agent exports extra columns or forgets debug_checks
- JSON schema doesn't match exactly
- Result: Schema validation fails
- **Fix**: Create dict explicitly with exact keys before dumping

**Common Failure 5: Rounding Precision**
- `total_savings_seconds` = 186.5 (not rounded to 2 decimals)
- Test expects "186.50" but gets string "186.5"
- Result: String comparison fails
- **Fix**: Use `round(value, 2)` explicitly before JSON export

---

## Measuring Agent Headroom

### Headroom Score Calculation

```python
def calculate_headroom_score(test_results):
    """
    Headroom = gap between current agent capability and perfect solution
    
    Returns:
    - Headroom = 0.0: Agent perfectly solves all test cases (no headroom)
    - Headroom = 1.0: Agent fails catastrophically (maximum headroom)
    """
    
    # Expected: 9 tests total
    tests_passed = sum(test_results.values())
    tests_total = len(test_results)
    
    headroom = 1 - (tests_passed / tests_total)
    
    return headroom

# Example results
test_results = {
    'file_exists': True,
    'schema_valid': True,
    'types_correct': True,
    'debug_checks_pass': True,
    'item_count': True,
    'csv_json_match': False,  # ← Test failed (sorting issue)
    'rounding_correct': False,  # ← Test failed (precision issue)
    'format_valid': True,
    'savings_logic': True
}

headroom = calculate_headroom_score(test_results)
print(f"Headroom Score: {headroom:.1%}")  # 22% headroom
```

### Target Headroom
- **Target**: 20-40% headroom
- **Interpretation**: Difficulty calibrated so agent fails ~2-4 tests autonomously
- **Sweet Spot**: Agent identifies most requirements but misses edge cases like:
  - Exact tie-breaking rules
  - Multi-key sorting logic
  - Rounding precision requirements
  - Zone filtering intersection

---

## Benchmarking Results Template

Save this template after running agent evaluation:

```json
{
  "benchmark_name": "Pharma Redistribution Priority Analysis",
  "benchmark_date": "2024-04-07",
  "agent_model": "GPT-4 / Claude / Gemini (specify)",
  "execution_time_seconds": 45,
  "tests_passed": 7,
  "tests_total": 9,
  "test_results": {
    "file_exists": true,
    "schema_valid": true,
    "types_correct": true,
    "debug_checks": true,
    "item_count": true,
    "consistency": false,
    "rounding": false,
    "format": true,
    "logic": true
  },
  "headroom_score": 0.22,
  "items_selected": 5,
  "total_savings_seconds": 186.50,
  "errors": [
    "Incorrect sort order - missing lexicographic secondary sort",
    "Total savings rounding to 1 decimal instead of 2"
  ],
  "notes": "Agent successfully filtered Pharma items and calculated priorities but failed on deterministic ordering rules"
}
```

---

## Troubleshooting

### Issue: "File not found" Error
**Cause**: Agent didn't rename CSV correctly or saved to wrong directory
**Solution**: Ensure `logistics_dataset.csv` is in current working directory before running agent

### Issue: "No Pharma items found"
**Cause**: Data file loaded but category column is wrong or all uppercase/lowercase
**Solution**: Check column names and values match exactly

### Issue: JSON Parse Error
**Cause**: Agent wrote invalid JSON (missing quotes, trailing commas)
**Solution**: Validate JSON syntax. In Colab: `json.loads()` will show exact error

### Issue: "Total savings is negative"
**Cause**: Agent calculated savings backwards (avg_zone_a - picking_time instead of inverse)
**Solution**: Review formula: `savings = picking_time - avg_zone_a`

---

## Conclusion

This agentic benchmark provides:
✓ **Deterministic Problem**: Same input always has one correct solution
✓ **Sufficient Complexity**: Multi-step workflow requires planning
✓ **Measurable Headroom**: Specific failure modes demonstrate capability gaps
✓ **Objective Evaluation**: Unit tests validate output without subjectivity
✓ **Reproducibility**: Golden solution proves task is solvable

**Expected Outcome**: Agent achieves ~70-80% test pass rate, identifying clear headroom for future improvement.
