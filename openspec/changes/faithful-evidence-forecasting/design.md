## Context

Final term project for New Technologies course — group of 3 students (SV1: Research & Spec Owner, SV2: ML/NLP Engineer, SV3: Visualization & QA). Objective: build a prototype to verify the faithfulness of evidence in stock trend forecasting using financial news.

The current system does not exist — this is an entirely new project. The baseline uses a rule-based model (no GPU/training required), which is sufficient to demonstrate the faithfulness concept. The dataset will consist of ≥ 30 simulated rows.

**Stakeholders:** Students (development team), Instructor (reviewer)

## Goals / Non-Goals

**Goals:**
- Build an executable end-to-end Python pipeline: from CSV input to prediction + faithfulness metrics output
- Implement 3 core verifiable faithfulness metrics: Temporal Validity, Evidence Support, Confidence Drop
- Interactive Streamlit dashboard enabling Reviewers to audit results without reading raw CSV files
- Adopt Agentic SDLC with trace logs, quality gates, and human reviews

**Non-Goals:**
- Not building a real trading system
- Not aiming for high prediction accuracy (the focus is on faithfulness, not accuracy)
- Not integrating live market data or real-time APIs
- Not using deep learning models for the baseline (FinBERT/LSTM are optional advanced tasks)

## Decisions

### D1. Evidence Extraction: Rule-based keyword matching
**Decision:** Keyword dictionary (positive/negative/neutral) → polarity → expected_direction
**Alternative:** FinBERT, Transformers, or LLM-based extraction
**Rationale:** Simple, explainable, no GPU needed, aligns with the goal of testing the faithfulness concept. FinBERT will be an optional advanced feature.

### D2. Forecast Model: Sentiment aggregation rule-based
**Decision:** Count positive vs negative evidence, add price signals → vote → prediction + confidence
**Alternative:** ML classifiers (Random Forest, Logistic Regression)
**Rationale:** Rule-based models have easily traceable logic → easier to verify faithfulness. ML classifiers are black-boxes and hard to explain for a demo.

### D3. Dashboard: Streamlit + Plotly
**Decision:** Streamlit (4 tabs) with Plotly charts
**Alternative:** Jupyter Notebook, Flask/Django web app
**Rationale:** Fast to build, no separate frontend required, sufficiently interactive for demos. Notebooks lack interaction; Flask is too heavy for a prototype.

### D4. Confidence Drop: Remove-and-rerun approach
**Decision:** Remove cited evidence → rerun model → measure confidence difference
**Alternative:** Attention weight analysis, SHAP/LIME
**Rationale:** Rule-based models lack attention weights. Remove-and-rerun is the most direct and easily understood faithfulness method.

### D5. Data Schema: Flat CSV, one row = one news article
**Decision:** Flat CSV with group key = (ticker, forecast_time)
**Alternative:** Relational database, nested JSON
**Rationale:** Easy to read/debug, no DB setup required, suitable for small datasets.

### D6. Pipeline Architecture: Sequential module pipeline
```
CSV → group(ticker, forecast_time)
  → Temporal Retriever → Evidence Extractor → Evidence Selector
  → Forecast Model → Faithfulness Evaluator → outputs/
```
**Decision:** Sequential pipeline, each module is a separate Python file
**Alternative:** Monolithic script, DAG framework (Airflow/Prefect)
**Rationale:** Simple, easy to test individual modules, facilitates team task division. DAGs are overly complex for a prototype.

## Risks / Trade-offs

**[Low rule-based accuracy]** → Acceptable tradeoff — the focus is on faithfulness. This limitation will be noted in the report. Low accuracy might cause reviewer skepticism, but we will justify it as a conscious design choice.

**[Simulated dataset lacks diversity]** → We will prepare ≥ 30 rows containing 3 tickers, 3 labels, 5+ leakage rows, and 3+ counterevidence pairs. If diversity is lacking → we will add backup data.

**[AI agents generating flawed logic]** → All AI outputs must pass QG-01 (human review). Traces are logged in run_log.json. If quality_gate = "failed" → the agent must regenerate output.

**[Dashboard crashing during demo]** → Pre-test on both SV1 and SV2 machines. Prepare a fallback Jupyter notebook.

**[Temporal leakage slipping past the Retriever]** → Implement 5 boundary test cases for filter_news_by_time(). Parse datetimes down to the minute, treating `news_time == forecast_time` strictly as future information.

## Open Questions

*(Resolved — no open questions at this stage)*