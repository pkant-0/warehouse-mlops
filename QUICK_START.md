# Agentic Benchmark: Quick Start Checklist

## Phase 1: Preparation (5 minutes)

### ☐ 1.1 Review Documentation
- [ ] Read [README.md](README.md) for overall context (2 min)
- [ ] Review [VISUAL_REFERENCE.md](VISUAL_REFERENCE.md) to understand task complexity (3 min)
- [ ] Skim [IMPROVED_AGENTIC_PROMPT.md](IMPROVED_AGENTIC_PROMPT.md) constraints section

### ☐ 1.2 Verify Data
- [ ] Confirm `Data/warehouse.csv` exists (50+ items)
- [ ] Verify data loads: `df = pd.read_csv('Data/warehouse.csv')`
- [ ] Check Pharma items exist: `len(df[df['category']=='Pharma']) > 0`

### ☐ 1.3 Review Golden Solution
- [ ] Open [golden_solution_pharma_redistribution.ipynb](golden_solution_pharma_redistribution.ipynb)
- [ ] Review the 9-section structure
- [ ] Note key implementation details (sorting, rounding, schema)

---

## Phase 2: Agent Execution (30-60 minutes)

### ☐ 2.1 Google Colab Setup
- [ ] Go to https://colab.research.google.com
- [ ] Create new notebook
- [ ] Upload `warehouse.csv` to Colab
  ```python
  from google.colab import files
  uploaded = files.upload()
  ```
- [ ] Rename to `logistics_dataset.csv`
  ```bash
  ! mv warehouse.csv logistics_dataset.csv
  ```

### ☐ 2.2 Inject Agentic Prompt
- [ ] Open [IMPROVED_AGENTIC_PROMPT.md](IMPROVED_AGENTIC_PROMPT.md)
- [ ] Copy full "IMPROVED AGENTIC PROMPT" section (starting at "Context")
- [ ] Paste into Colab cell
- [ ] Click **"Blue Star"** agent button (if using Claude/GPT agent interface)
  - *Alternative*: If no agent button, manually run cell to see what agent does

### ☐ 2.3 Monitor Execution
- [ ] Watch for print statements at each checkpoint
- [ ] Expected outputs:
  ```
  ✓ Dataset loaded successfully
  ✓ Filtered X Pharma items
  ✓ Priority metric calculated
  ✓ Found N items above 75th percentile
  ✓ All verification checks passed
  ✓ Results exported to /content/
  ```
- [ ] Note any errors or deviations

### ☐ 2.4 Collect Outputs
- [ ] Check `/content/pharma_audit_results.csv` exists
- [ ] Check `/content/final_strategy.json` exists
- [ ] Download both files locally
- [ ] Save stdout logs (copy entire output)

---

## Phase 3: Evaluation (15 minutes)

### ☐ 3.1 Run Test Suite
- [ ] Open [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [ ] Copy the "Run Evaluation Tests" code block
- [ ] Paste and execute in new Colab cell
- [ ] Record test results:

```
Test 1: File Exists        [ ] PASS [ ] FAIL
Test 2: JSON Schema        [ ] PASS [ ] FAIL
Test 3: Variable Types     [ ] PASS [ ] FAIL
Test 4: Debug Checks       [ ] PASS [ ] FAIL
Test 5: Item Count         [ ] PASS [ ] FAIL
Test 6: CSV/JSON Match     [ ] PASS [ ] FAIL
Test 7: Rounding           [ ] PASS [ ] FAIL
Test 8: ID Format          [ ] PASS [ ] FAIL
Test 9: Savings Logic      [ ] PASS [ ] FAIL

Total: _/9 PASS
```

### ☐ 3.2 Calculate Headroom Score
- [ ] Count passed tests (e.g., 7)
- [ ] Total tests: 9
- [ ] Headroom = (9 - 7) / 9 = 0.22 = **22%**
- [ ] Interpret result:
  - 0-10% = Perfect solution
  - 10-20% = Excellent (minor edge cases)
  - **20-40% = Target zone ✓**
  - 40-60% = Good (major gaps visible)
  - 60-80% = Acceptable (needs work)
  - 80-100% = Failed

### ☐ 3.3 Document Failures
- [ ] For each failed test, note:
  - Test name
  - Expected value
  - Actual value
  - Root cause (e.g., "Single-key sort instead of multi-key")

---

## Phase 4: Analysis (10 minutes)

### ☐ 4.1 Identify Failure Pattern
- [ ] If sorting test failed:
  - [ ] Agent used single-key sort
  - [ ] Missing lexicographic secondary sort
  - [ ] See [VISUAL_REFERENCE.md](VISUAL_REFERENCE.md) Pattern 1

- [ ] If filter test failed:
  - [ ] Zone/percentile filters not combined correctly
  - [ ] See [VISUAL_REFERENCE.md](VISUAL_REFERENCE.md) Pattern 2

- [ ] If rounding test failed:
  - [ ] Precision lost (186.5 instead of 186.50)
  - [ ] See [VISUAL_REFERENCE.md](VISUAL_REFERENCE.md) Pattern 3

- [ ] If schema test failed:
  - [ ] Extra/missing JSON keys
  - [ ] See [VISUAL_REFERENCE.md](VISUAL_REFERENCE.md) Pattern 4

- [ ] If debug checks test failed:
  - [ ] Validation errors not enforced
  - [ ] See [VISUAL_REFERENCE.md](VISUAL_REFERENCE.md) Pattern 5

### ☐ 4.2 Compare Against Golden Solution
- [ ] Run [golden_solution_pharma_redistribution.ipynb](golden_solution_pharma_redistribution.ipynb) locally
- [ ] Compare agent output vs golden output
- [ ] Identify specific differences
- [ ] Verify golden solution produces:
  ```json
  {
    "priority_item_ids": ["ITM10031", "ITM10040", "ITM10016", "ITM10042", "ITM10019"],
    "total_savings_seconds": 186.50,
    "debug_checks": {"data_loaded": true, "category_exists": true, "no_null_demand": true, "priority_non_negative": true}
  }
  ```

### ☐ 4.3 Record Findings
- [ ] Create results document with:
  - Agent model used (GPT-4, Claude, etc.)
  - Test pass/fail breakdown
  - Headroom score
  - Failure patterns identified
  - Time to completion

---

## Phase 5: Reporting (5 minutes)

### ☐ 5.1 Use Benchmarking Template
- [ ] Open [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) "Benchmarking Results Template"
- [ ] Fill in all fields:
  ```json
  {
    "benchmark_name": "Pharma Redistribution Priority Analysis",
    "benchmark_date": "2024-XX-XX",
    "agent_model": "Model name",
    "execution_time_seconds": 45,
    "tests_passed": 7,
    "tests_total": 9,
    "headroom_score": 0.22,
    ...
  }
  ```

### ☐ 5.2 Create Summary Report
- [ ] Write 1-page executive summary:
  - What agent was tested
  - Key results (pass/fail breakdown)
  - Headroom score and interpretation
  - Top 1-2 failure modes
  - Recommendations for improvement

### ☐ 5.3 Share Results
- [ ] Save benchmarking results to JSON file
- [ ] Back up all logs and outputs
- [ ] Share results with team/stakeholders

---

## Troubleshooting Quick Reference

### Issue: "FileNotFoundError: logistics_dataset.csv"
- **Cause**: File not in working directory
- **Solution**: 
  ```python
  !ls -la  # Check current directory contents
  # Upload via: files.upload()
  # Or rename: !mv warehouse.csv logistics_dataset.csv
  ```

### Issue: JSON Parse Error
- **Cause**: Agent created invalid JSON
- **Solution**:
  ```python
  import json
  with open('/content/final_strategy.json') as f:
      json.load(f)  # This will show exact error
  ```

### Issue: "No Pharma items found"
- **Cause**: Dataset has wrong structure or no Pharma items
- **Solution**:
  ```python
  df = pd.read_csv('logistics_dataset.csv')
  print(df['category'].unique())  # Check categories
  print(len(df[df['category']=='Pharma']))  # Count Pharma items
  ```

### Issue: Test fails with "Type mismatch"
- **Cause**: Agent returned wrong data type (e.g., NumPy float instead of Python float)
- **Solution**: 
  ```python
  total_savings = float(strategy['total_savings_seconds'])  # Convert explicitly
  ```

### Issue: "Items mismatch between CSV and JSON"
- **Cause**: Agent saved different items to CSV vs JSON
- **Solution**: Re-run agent with debug logs enabled

---

## Success Indicators

### ✓ Strong Performance (Headroom < 20%)
- All 9 tests pass OR only 1-2 fail
- Agent correctly implements multi-key sorting
- JSON schema matches exactly
- Rounding precise to 2 decimals
- **Interpretation**: Agent almost perfect; minor edge cases only

### ✓ Target Performance (Headroom 20-40%)
- 7-8 tests pass; 1-2 fail
- Common failures: sorting, rounding, or schema
- Agent demonstrates good understanding but misses precision
- **Interpretation**: Clear improvement areas identified ✓

### ⚠ Acceptable Performance (Headroom 40-60%)
- 5-6 tests pass; 3-4 fail
- Multiple logic errors visible
- Agent struggles with multi-condition filtering
- **Interpretation**: Significant gaps identified; needs improvement

### ✗ Poor Performance (Headroom > 60%)
- Fewer than 5 tests pass
- Agent fails basic validation or schema checks
- **Interpretation**: Task too difficult or training insufficient

---

## Files Checklist

### Must Have
- [ ] `Data/warehouse.csv` - Source data
- [ ] `IMPROVED_AGENTIC_PROMPT.md` - Agent prompt
- [ ] `golden_solution_pharma_redistribution.ipynb` - Reference solution
- [ ] `DEPLOYMENT_GUIDE.md` - Evaluation framework
- [ ] `README.md` - Documentation

### Nice to Have
- [ ] `VISUAL_REFERENCE.md` - Visual guides
- [ ] This checklist (QUICK_START.md)
- [ ] `evaluation_results.json` - Your test results

---

## Expected Timeline

| Phase | Tasks | Time |
|-------|-------|------|
| **1. Prep** | Review docs, verify data, study solution | 5 min |
| **2. Execute** | Setup Colab, run agent, collect outputs | 45 min |
| **3. Evaluate** | Run tests, calculate headroom | 15 min |
| **4. Analyze** | Identify patterns, compare to golden | 10 min |
| **5. Report** | Document and share results | 5 min |
| **TOTAL** | | **~80 min** |

---

## Next Steps After Completion

### If passing (Headroom < 30%)
1. Try harder test variant
2. Add constraints (time limit, memory limit)
3. Test on different data
4. Increase problem complexity

### If failing (Headroom > 50%)
1. Review golden solution in detail
2. Identify blockers with agent developers
3. Adjust prompt clarity
4. Simplify task components incrementally

### For Continuous Testing
1. Create automated test pipeline
2. Add more Pharma scenarios
3. Test with different warehouse datasets
4. Track headroom trends over time

---

## Support & Questions

### Common Questions

**Q: What if agent doesn't reach /content/ directory?**
A: In Colab, `/content/` is the working directory after upload. Create it if needed:
```python
import os
os.makedirs('/content', exist_ok=True)
```

**Q: Can I modify the prompt?**
A: Yes! For testing, you can:
- Add hints (reduces headroom)
- Add constraints (increases headroom)
- Change thresholds (75th to 80th percentile)
- Modify item count (5 to 10)

**Q: What if data is different?**
A: Results will vary but test suite should still work. Adjust expected values accordingly.

**Q: Can this run outside of Colab?**
A: Yes! Works in any Jupyter environment. Adjust `/content/` paths as needed.

---

**Version**: 1.0
**Last Updated**: April 7, 2026
**Status**: Ready to Use

✓ Print this checklist and complete each item in order
✓ Estimated total time: ~80 minutes
✓ All materials provided; no additional software needed beyond Google Colab
