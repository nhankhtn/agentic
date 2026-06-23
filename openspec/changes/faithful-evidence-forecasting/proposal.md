## Why

AI systems predicting stock trends from news often provide explanations (evidence) that sound reasonable but may not accurately reflect the model's actual decision-making reasoning. For example: a model predicts "NVDA UP" citing "NVIDIA launches new AI chip", but removing this news barely changes the confidence (0.88 → 0.86) — the evidence is merely "decorative".

We need a prototype to verify the **faithfulness** of evidence: does the evidence provided by the model truly drive its predictions? Additionally, this project applies **Agentic AI in SDLC** with quality control following OpenSpec standards.

## What Changes

- Build an end-to-end pipeline: CSV → Temporal Retriever → Evidence Extractor → Evidence Selector → Forecast Model → Faithfulness Evaluator → Dashboard
- Implement 3 core faithfulness metrics: Temporal Validity, Evidence Support, Confidence Drop
- Detect and warn about temporal leakage (preventing the use of future news for prediction)
- Create an interactive Streamlit dashboard with 4 tabs: Prediction Overview, Evidence Explorer, Faithfulness Analysis, Temporal Leakage Monitor
- Adopt Agentic SDLC with 3 AI Agent roles (Research, Coding, Testing), enforcing quality gates and human review

## Capabilities

### New Capabilities
- `temporal-retrieval`: Filter news by time, eliminating future information (temporal leakage prevention)
- `evidence-extraction`: Extract evidence from news text, classifying polarity (positive/negative/neutral) and expected direction (UP/DOWN/HOLD)
- `stock-forecasting`: Forecast stock direction (UP/DOWN/HOLD) from evidence + price features with a confidence score
- `faithfulness-evaluation`: Calculate metrics to evaluate evidence faithfulness (Temporal Validity, Evidence Support, Confidence Drop)
- `visualization-dashboard`: Interactive Streamlit dashboard with 4 tabs for analysis and leakage alerts
- `agentic-sdlc-tracing`: Record a trace log for every AI agent interaction, including human review and quality gates

### Modified Capabilities
*(None — this is a new project)*

## Impact

- **Codebase**: Create 8 new Python files in `src/` (retriever, extractor, selector, forecast_model, faithfulness_metrics, data_utils, run_pipeline, dashboard)
- **Data**: CSV dataset with ≥ 30 rows covering 3+ tickers, including temporal leakage rows and counterevidence pairs
- **Dependencies**: pandas, numpy, scikit-learn, streamlit, plotly, pytest, python-dateutil
- **Output**: 3 result files (prediction_results.csv, faithfulness_results.csv, metrics_summary.json) + 4 PNG figures + agent trace log (run_log.json)
- **Testing**: ≥ 10 pytest unit tests for the temporal retriever and faithfulness metrics