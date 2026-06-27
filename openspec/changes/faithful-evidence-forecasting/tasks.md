## 1. Project Setup & OpenSpec

- [ ] 1.1 Initialize project repository with directory structure (data/, src/, tests/, outputs/, openspec/)
- [ ] 1.2 Create requirements.txt with dependencies (pandas, numpy, scikit-learn, streamlit, plotly, pytest, python-dateutil)
- [ ] 1.3 Run `openspec init` and configure Antigravity skills
- [ ] 1.4 Create README.md with quick start instructions

## 2. Dataset Preparation

- [ ] 2.1 Design CSV schema matching input spec (ticker, forecast_time, news_id, news_time, news_title, news_text, price_5d_return, volume_change, label)
- [ ] 2.2 Generate ≥30 rows of simulated data with 3+ tickers (AAPL, TSLA, NVDA) and all 3 labels (UP, DOWN, HOLD)
- [ ] 2.3 Include ≥5 rows with temporal leakage (news_time >= forecast_time) for testing
- [ ] 2.4 Include ≥3 counterevidence pairs (same ticker + date, both positive and negative news)
- [ ] 2.5 Write data validation script to check nulls, datetime parsing, and label distribution

## 3. Temporal Retriever (src/retriever.py)

- [ ] 3.1 Implement `filter_news_by_time(news_list, forecast_time)` → returns (valid_news, invalid_future_news, leakage_count)
- [ ] 3.2 Add WARNING log for each filtered article: `[WARNING] Temporal leakage: news_id={id}, news_time={t} >= forecast_time={ft}`
- [ ] 3.3 Write docstrings and type hints for retriever.py
- [ ] 3.4 Write ≥5 unit tests in tests/test_temporal_retriever.py (valid pass, future filtered, boundary filtered, empty input, all filtered)
- [ ] 3.5 Run pytest and verify all tests pass

## 4. Evidence Extraction (src/evidence_extractor.py)

- [ ] 4.1 Build keyword dictionary: negative → DOWN, positive → UP, neutral → HOLD
- [ ] 4.2 Implement `extract_evidence(news_text, news_id)` → returns list of evidence dicts
- [ ] 4.3 Handle edge cases: very short text (<5 words), no keywords found
- [ ] 4.4 Verify ≥80% extraction coverage on the full dataset
- [ ] 4.5 Write docstrings and type hints for evidence_extractor.py

## 5. Forecast Model (src/forecast_model.py)

- [ ] 5.1 Implement `predict(evidence_list, price_features, ticker, forecast_time)` → returns prediction dict
- [ ] 5.2 Implement `compute_confidence_drop(evidence_list, price_features, cited_evidence, ticker, forecast_time)` → returns drop value
- [ ] 5.3 Integrate price_5d_return signal (+0.5 to positive/negative count)
- [ ] 5.4 Run predict on full dataset and save to outputs/prediction_results.csv
- [ ] 5.5 Compute accuracy and confusion matrix using sklearn.metrics
- [ ] 5.6 Save accuracy and 3×3 confusion matrix (UP/DOWN/HOLD) to outputs/ or report
- [ ] 5.7 Write docstrings and type hints for forecast_model.py

## 6. Faithfulness Metrics (src/faithfulness_metrics.py)

- [ ] 6.1 Implement `temporal_validity(cited_evidence, forecast_time)` → float
- [ ] 6.2 Implement `evidence_support(cited_evidence, prediction)` → float
- [ ] 6.3 Implement `confidence_drop(original, without)` → float + verdict classifier
- [ ] 6.4 Run metrics on full dataset and save to outputs/faithfulness_results.csv
- [ ] 6.5 Write ≥5 unit tests in tests/test_metrics.py (boundary values, empty lists, verdict classification)
- [ ] 6.6 (Advanced B1) Implement sufficiency test and counterfactual perturbation
- [ ] 6.7 (Advanced B2) Implement counterevidence_coverage()
- [ ] 6.8 (Advanced B3) Implement market_consistency()

## 7. Dashboard (src/dashboard.py)

- [ ] 7.1 Setup Streamlit app skeleton with 4 tabs
- [ ] 7.2 Build Tab 1 — Prediction Overview (table + bar chart + metric cards)
- [ ] 7.3 Build Tab 2 — Evidence Explorer (dropdown + evidence table + leakage warning banner)
- [ ] 7.4 Build Tab 3 — Faithfulness Analysis (confidence drop bar chart + verdict table)
- [ ] 7.5 Build Tab 4 — Temporal Leakage Monitor (filtered articles table + warning/confirmation)
- [ ] 7.6 Export 4 static PNG figures to outputs/figures/
- [ ] 7.7 Test dashboard on multiple machines (cross-machine compatibility)

## 8. Testing & QA

- [ ] 8.1 Finalize test_temporal_retriever.py (≥5 tests, all pass)
- [ ] 8.2 Finalize test_metrics.py (≥5 tests, all pass)
- [ ] 8.3 Run end-to-end pipeline test on full dataset (no runtime errors)
- [ ] 8.4 Test edge case: ticker with no news articles
- [ ] 8.5 Test edge case: all news filtered due to temporal leakage
- [ ] 8.6 Verify output files match expected schema (prediction_results.csv, faithfulness_results.csv, metrics_summary.json)

## 9. Agent Trace & Documentation

- [ ] 9.1 Create outputs/run_log.json with ≥6 entries covering 3 agent roles (Research, Coding, Testing)
- [ ] 9.2 Add ≥1 reflection entry in run_log.json where agent self-evaluates output quality and suggests improvements
- [ ] 9.3 Write metric_definition.md with formulas, examples, and interpretation guide
- [ ] 9.4 Write report sections 1-3 (introduction, research gap, agentic SDLC design)
- [ ] 9.5 Write report sections 4-5 (dataset description, pipeline technical details)
- [ ] 9.6 Write report sections 6-7 (metric results, experimental analysis)
- [ ] 9.7 Write report sections 8-9 (case analysis, limitations — at least 3 specific limitations)
- [ ] 9.8 Finalize and export report as PDF (5-8 pages)
- [ ] 9.9 Record demo video (~5 minutes) and create demo_video_link.txt
- [ ] 9.10 Final submission checklist review