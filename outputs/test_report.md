# Test Report

**Date:** 2026-06-16  
**Command:** `pytest tests/ -v`

## Summary

| Suite | Tests | Passed | Failed |
|-------|-------|--------|--------|
| test_temporal_retriever.py | 6 | 6 | 0 |
| test_metrics.py | 6 | 6 | 0 |
| **Total** | **12** | **12** | **0** |

## End-to-end pipeline

- Command: `python src/run_pipeline.py`
- Input: `data/sample_news_price.csv` (36 rows, 25 forecast groups)
- Outputs: `prediction_results.csv`, `faithfulness_results.csv`, `metrics_summary.json`
- Accuracy: **96%**
- Mean temporal validity: **1.0**

## Edge cases verified

- Empty news list → retriever returns empty valid/invalid lists
- All news leakage → valid_news empty, pipeline fallback HOLD/low confidence
- No cited evidence → confidence_drop = 0
