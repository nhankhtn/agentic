# Requirement.md — Final Project
## Faithful Evidence-Centric Financial News Forecasting
### Course: Emerging Technologies | Group: 3 Students | Total Score: 10 + 2 Bonus Points

---

## Phase Overview

| Phase | Name | Main Goal | Related Score |
|-------|-----|----------------|----------------|
| 0 | Kickoff & Planning | Understand problem, assign roles, setup environment | A1 |
| 1 | OpenSpec & Requirements | Write proposal, spec, design, tasks, metric definition | A1, B4 |
| 2 | Data Preparation | Create/collect dataset, group logic, preprocessing | A2, C1 |
| 3 | Temporal Retriever | Module to filter news chronologically | A3 |
| 4 | Evidence Extraction | Module to extract evidence from news | A4 |
| 4.5 | Evidence Selector | Select pro/counter evidence before prediction | A4, B2 |
| 5 | Forecast Model | UP/DOWN/HOLD prediction model | A5 |
| 6 | Faithfulness Metrics | 3 core metrics: Support, Validity, Confidence Drop | A6 |
| 7 | Visualization Dashboard | Dashboard, charts, warnings, live model rerun | A7 |
| 8 | Testing & QA | Test cases, E2E pipeline, test report | A3, A6 |
| 9 | Report & Demo | Write report, record demo, final submission | A7, B4 |
| 10 (Advanced) | Agentic SDLC Maturity | Agent roles, trace log, quality gates, commit log | B4 |
| 11 (Advanced) | Advanced Metrics | Sufficiency, counterfactual, counterevidence, market consistency | B1, B2, B3 |
| 12 (Bonus) | Real Data & GPU | Real data, FinBERT/LSTM | C1, C2 |

**Standard Pipeline (matches assignment):**
```
News + Price → Temporal Retriever → Evidence Extractor → Evidence Selector
  → Forecast Model → Faithfulness Evaluator → Dashboard
```

---

## Phase 0 — Kickoff & Planning

### Goal
Ensure the team understands the problem, divides tasks properly, and prepares a unified working environment before coding.

### Tasks

#### 0.1 Understand the problem
- Read the entire assignment document.
- Fully understand **faithfulness**: does the evidence cited by the model actually impact the prediction?
- Understand the 4 examples: faithful evidence, decorative evidence, temporal leakage, counterevidence.
- All 3 members must understand the end-to-end data flow.

#### 0.2 Task Assignment

| Role | Main Responsibilities |
|---------|----------------|
| **SV1 — Research & Spec Owner** | Write OpenSpec, user stories, metric definitions, report sections 1–3 |
| **SV2 — ML/NLP Engineer** | Create dataset, retriever, extractor, selector, forecast model, pipeline, experiments |
| **SV3 — Visualization & QA** | Dashboard, notebooks, charts, test cases, temporal leakage testing, demo video |

> ⚠️ Note: All 3 members must be able to understand and explain the entire system during the defense.

#### 0.3 Environment Setup
- Create a shared Git repository (GitHub/GitLab).
- Create the project directory structure exactly as requested:
```
agentic/
├── README.md
├── requirements.txt
├── report.pdf
├── demo_video_link.txt
├── openspec/
│   ├── changes/faithful-evidence-forecasting/
│   │   ├── proposal.md
│   │   ├── design.md
│   │   └── tasks.md
│   └── specs/forecasting/spec.md
├── metric_definition.md
├── data/
│   └── sample_news_price.csv
├── src/
│   ├── retriever.py
│   ├── evidence_extractor.py
│   ├── evidence_selector.py
│   ├── forecast_model.py
│   ├── faithfulness_metrics.py
│   ├── run_pipeline.py
│   └── dashboard.py
├── tests/
│   ├── test_temporal_retriever.py
│   └── test_metrics.py
├── notebooks/
│   └── visualization.ipynb
└── outputs/
    ├── prediction_results.csv
    ├── faithfulness_results.csv
    ├── run_log.json
    ├── test_report.md
    └── figures/
```
- Install Python 3.9+ and the libraries in `requirements.txt`: `pandas`, `numpy`, `scikit-learn`, `streamlit`, `jupyter`, `pytest`, `plotly`.
- Agree on data formats and variable naming conventions.
- Maintain a **commit log** (or PR links) as evidence of Agentic SDLC — update continuously, do not wait until the end.

### Deliverables for Phase 0
- [ ] Shared Git repository created with full folder structure.
- [ ] `requirements.txt` created and installable by all members.
- [ ] Clear task assignment documented in `README.md`.
- [ ] Python environment works on everyone's machine.

---

## Phase 1 — OpenSpec & Requirements

### Goal
Write the system specification using the OpenSpec standard, including proposal, design, tasks, and spec. This phase is mandatory, worth **1.0 point (A1)**.

### Tasks

#### 1.1 Write `proposal.md`
Contents:
- **Problem**: Stock trend prediction from verified evidence.
- **Motivation**: Why accuracy isn't enough, why we need faithful evidence.
- **Scope**: What the team will and will not build.
- **Expected Results**: Prototype, dashboard, report, demo.
- **Timeline**: Schedule for each phase.

#### 1.2 Write `design.md`
Contents:
- **Architecture diagram**: draw the pipeline from input to output.
- **Data schema**: Describe JSON/CSV structure for input/output.
- **Module descriptions**: Retriever, Extractor, **Selector**, Model, Metrics, Dashboard — responsibilities and interfaces.
- **Data grouping flow**: Flat CSV → group by `(ticker, forecast_time)` → pipeline per group.
- **Dashboard design**: What tabs/charts are included.
- **Technology decisions**: Chosen libraries and reasons.

#### 1.3 Write `tasks.md`
- List all specific tasks (data creation, modules, tests...).
- For each task, record: owner, deadline, status (TODO/IN PROGRESS/DONE).
- Note which AI agent assists which task (e.g., using ChatGPT to generate test cases).

#### 1.4 Write `specs/forecasting/spec.md`
Contents:
- **Input specification**: Detailed description of each input field.
- **Output specification**: Detailed description of each output field, including faithfulness fields.
- **Functional requirements**: Features the system must have.
- **Non-functional requirements**: Minimum accuracy, processing speed, etc.
- **Acceptance criteria** in Given/When/Then format.

- **AI Agent Usage**: Explicitly state where AI agents are used in the SDLC.
- **Quality gate**: Every AI output must pass human review before merging (documented in `tasks.md`).

#### 1.5 Write `metric_definition.md` (SV1)
Formally define the metrics, formulas, and thresholds:
- Temporal Validity, Evidence Support, Confidence Drop (A6).
- Sufficiency, Counterfactual Drop, Counterevidence Coverage, Market Consistency (B1–B3, if doing advanced).
- Thresholds: `confidence_drop > 0.1` → likely faithful; `< 0.05` → possibly decorative.

#### 1.6 Begin Agent Trace Log (B4 — ongoing)
- Create `outputs/run_log.json` starting in Phase 1.
- Each AI interaction must log: `run_id`, `agent_role`, `task`, `human_review`, `quality_gate`.
- Save the **commit log** (or `outputs/commit_log.md` summarizing reviewed PRs/commits) as A1 evidence.

### Deliverables for Phase 1
- [ ] `proposal.md` — complete.
- [ ] `design.md` — architecture diagram (including Evidence Selector).
- [ ] `tasks.md` — assignments, timelines, quality gates.
- [ ] `spec.md` — clear acceptance criteria.
- [ ] `metric_definition.md` — metrics and thresholds.
- [ ] `outputs/run_log.json` — at least 1 entry.

---

## Phase 2 — Data Preparation

### Goal
Create or collect a dataset sufficient to run the entire pipeline. Mandatory phase, **1.0 point (A2)**. Using real data yields a **+1.0 bonus point (C1)**.

### Tasks

#### 2.1 Create simulated dataset (minimum — mandatory)
At least **30 rows**, containing:
`ticker`, `forecast_time`, `news_id`, `news_time`, `news_title`, `news_text`, `price_5d_return`, `volume_change`, `label` (UP/DOWN/HOLD).

**Dataset requirements:**
- At least 3 different tickers.
- All 3 labels present.
- **At least 5 rows with news_time > forecast_time** (to test temporal leakage).
- Clear positive, negative, and neutral news.
- At least 2–3 counterevidence groups (same ticker, same `forecast_time`, both good and bad news).

#### 2.2 Group data by `(ticker, forecast_time)`
CSV is flat, but the pipeline processes **forecast groups**. Group keys: `(ticker, forecast_time)`. `label` and `price_features` must be consistent within the group.

#### 2.3 Data Preprocessing
- Standardize datetimes (ISO 8601).
- Drop rows missing critical data.
- Validate labels (UP/DOWN/HOLD only).

#### 2.4 Descriptive Statistics
Table showing group count, row count, label distribution, leakage count, and ticker breakdown.

#### 2.5 (Bonus C1) Real Data
- Use **Yahoo Finance** and **Kaggle / Financial PhraseBank**.
- Determine labels based on actual `return_next_day`.
- At least **300 samples**, must handle temporal leakage.

### Deliverables for Phase 2
- [ ] `data/sample_news_price.csv` — ≥30 rows.
- [ ] Dataset statistics table.
- [ ] (Bonus) Real data fetching script.

---

## Phase 3 — Temporal Retriever

### Goal
Build a module to filter news chronologically, preventing **future information leakage**. Worth **1.0 point (A3)**.

### Tasks

#### 3.1 Write `src/retriever.py`
Implement `filter_news_by_time(news_list, forecast_time)`. Compare timestamps down to the minute. Separate `valid_news` and `invalid_future_news`.

#### 3.2 Write `tests/test_temporal_retriever.py`
Write at least **6 test cases**:
- Valid news (before forecast)
- Future news (after forecast)
- Exact match (equals forecast) -> rejected
- Mixed news
- Empty list
- All leakage list

#### 3.3 Create temporal leakage warnings
Log warning if any news is dropped: `[WARNING] Temporal leakage detected...`. Return `leakage_count`.

### Deliverables for Phase 3
- [ ] `src/retriever.py` — runs successfully with docstrings.
- [ ] `tests/test_temporal_retriever.py` — 6 tests pass.
- [ ] Temporal leakage warning logs function properly.

---

## Phase 4 — Evidence Extraction

### Goal
Extract evidence from news text and classify sentiment direction. Worth **1.0 point (A4)**.

### Tasks

#### 4.1 Write `src/evidence_extractor.py`
Input text, output list of evidence dictionaries: `evidence_text`, `polarity`, `expected_direction`, `confidence`.
**Minimum (rule-based):**
- Negative keywords → DOWN
- Positive keywords → UP
- Neutral keywords → HOLD

#### 4.2 Test evidence extractor
Prepare **5 correct and 5 edge-case examples** for the report.

#### 4.3 Handle edge cases
- Ambiguous/no keyword → neutral (HOLD).
- Both positive and negative → extract both, let Evidence Selector decide.
- Too short (< 10 words) → log warning, assign neutral.

### Deliverables for Phase 4
- [ ] `src/evidence_extractor.py` — runs on the dataset.
- [ ] 10-example table in the report.
- [ ] Coverage ≥ 80%.

---

## Phase 4.5 — Evidence Selector

### Goal
Select and classify evidence before the Forecast Model. Supports separating pro/counter evidence.

### Tasks

#### 4.5.1 Write `src/evidence_selector.py`
Implement `select_evidence(all_evidence, prediction_direction=None)`.
Outputs: `pro_evidence`, `counter_evidence`, `cited_evidence` (top-k by confidence).

#### 4.5.2 Test selector
Ensure it correctly groups pro and counter evidence when both positive and negative news exist in the same group.

### Deliverables for Phase 4.5
- [ ] `src/evidence_selector.py` — runs per group.
- [ ] `design.md` updated with Selector interface.

---

## Phase 5 — Forecast Model

### Goal
Build the UP/DOWN/HOLD prediction model with explanations. Worth **1.0 point (A5)**. Rule-based model is sufficient.

### Tasks

#### 5.1 Write `src/forecast_model.py`
Implement `predict(ticker, forecast_time, valid_news, price_features, cited_evidence=None)`.
Calculate score based on positive/negative evidence counts and price signals. Output prediction, confidence, cited evidence, and rationale.

#### 5.2 Model Evaluation
Calculate Accuracy, Confusion Matrix, Precision, Recall, F1.

#### 5.3 Explain a specific prediction
Select 1 prediction for the report, detailing the rationale, evidence, and confidence.

#### 5.4 Save Results
Save to `outputs/prediction_results.csv`.

### Deliverables for Phase 5
- [ ] `src/forecast_model.py` — predicts the entire dataset.
- [ ] `outputs/prediction_results.csv` — full columns.
- [ ] Accuracy and confusion matrix table.
- [ ] 1 detailed case explanation in the report.

---

## Phase 6 — Faithfulness Metrics

### Goal
Compute the **3 core faithfulness metrics**. This is the **most crucial part**. Worth **1.0 point (A6)**.

### Tasks

#### 6.1 Write `src/faithfulness_metrics.py`
**Metric 1 — Temporal Validity**: cited evidence before forecast_time.
**Metric 2 — Evidence Support**: cited evidence aligns with prediction.
**Metric 3 — Confidence Drop**: `confidence_original - confidence_without_cited_evidence`. Check if drop > 0.1 (likely faithful) or < 0.05 (possibly decorative). Also compute `confidence_drop_random` for baseline comparison.

#### 6.2 Save Faithfulness Results
Save to `outputs/faithfulness_results.csv`.

#### 6.3 Aggregated Metrics Table
Compute the mean of each metric across the entire dataset for the dashboard.

### Deliverables for Phase 6
- [ ] `src/faithfulness_metrics.py` — computes 3 metrics + random baseline.
- [ ] `outputs/faithfulness_results.csv` — full columns.
- [ ] Summary table of average metrics.

---

## Phase 7 — Visualization Dashboard

### Goal
Build an interactive dashboard (Streamlit recommended). Worth **1.0 point (A7)**.

### Tasks

#### 7.1 Write `src/dashboard.py`
Must support re-running the model at runtime when "Remove cited evidence" or "Remove random evidence" is clicked to show live confidence drops.
Tabs:
1. **Prediction Overview**: Data table, distribution chart, metric cards.
2. **Evidence Explorer**: Dropdown, detailed evidence table, leakage red warning.
3. **Faithfulness Analysis**: Confidence drop charts, radar chart (3 metrics), verdict table.
4. **Temporal Leakage Monitor**: Table of filtered news.

#### 7.2 Static Figures
Export PNG charts to `outputs/figures/`.

#### 7.3 Dashboard Demo Script (5 mins)
Prepare a demo flow for the presentation showing predictions, leakage warnings, and live confidence drops.

### Deliverables for Phase 7
- [ ] `src/dashboard.py` — runs successfully.
- [ ] `notebooks/visualization.ipynb` — for data exploration.
- [ ] `outputs/figures/` — 4 PNG charts.
- [ ] Dashboard supports live prediction rerun.
- [ ] Demo script written in `README.md`.

---

## Phase 8 — Testing & QA

### Goal
End-to-end pipeline testing, ensuring no major errors.

### Tasks

#### 8.1 Complete `tests/test_temporal_retriever.py`
#### 8.2 Write `tests/test_metrics.py`
5 tests covering metrics edge cases.
#### 8.3 Write `src/run_pipeline.py`
End-to-end orchestrator script.
#### 8.4 E2E Check
Run pipeline entirely on `data/sample_news_price.csv` without runtime errors.
#### 8.5 Edge Cases
Handle empty groups, fully leaked groups, HOLD fallbacks.
#### 8.6 Write `outputs/test_report.md`
Summarize pytest results and bugs fixed.

### Deliverables for Phase 8
- [ ] `src/run_pipeline.py` — error-free.
- [ ] Tests pass (Retriever + Metrics).
- [ ] `outputs/test_report.md`.

---

## Phase 9 — Report & Demo

### Goal
Write a 5–8 page report and record a 5-minute video demo.

### Tasks

#### 9.1 Write `report.pdf` (5–8 pages)
Include Introduction, Gap, Design, Data, Pipeline, Metrics, Results, Case Analysis, and Limitations.
#### 9.2 Write `README.md`
Installation, run commands, team members.
#### 9.3 Record demo video (~5 mins)
Upload to Drive/YouTube and put link in `demo_video_link.txt`.
#### 9.4 Pre-submission Checklist
Ensure all files, tests, reports, and logs are complete. No future information must be used in the experiments.

### Deliverables for Phase 9
- [ ] `report.pdf`
- [ ] `README.md`
- [ ] `demo_video_link.txt`

---

## Phase 10 (Advanced) — Agentic SDLC Maturity

### Goal
Implement 3 agent roles with trace log, quality gates, and reflections. **0.75 points (B4)**. Must be done continuously from Phase 1.

### Tasks
- Define Research Agent, Coding Agent, Testing Agent.
- Maintain `outputs/run_log.json` (≥6 entries, 2 per role).
- Implement human reviews (quality gates).
- Write a 200+ word reflection in the report.

---

## Phase 11 (Advanced) — Advanced Metrics

### Goal
Implement advanced metrics in `faithfulness_metrics.py`. **2.25 points (B1+B2+B3)**.

### Tasks
- **B1 (0.75)**: Sufficiency test + Counterfactual perturbation.
- **B2 (0.75)**: Counterevidence coverage (from the Selector module).
- **B3 (0.75)**: Market consistency (compare evidence vs actual post-forecast returns) + bull/bear regime analysis.
- Update `outputs/faithfulness_results.csv` with these new columns.

---

## Phase 12 (Bonus) — Real Data & GPU

### Goal
Earn up to 2 bonus points by using real data or advanced models.

### Tasks
- **C1 (+1.0)**: Real data (Yahoo Finance, >300 samples).
- **C2 (+1.0)**: GPU Model (FinBERT, LSTM) compared against the rule-based baseline.

---

## Summary Timeline

| Week | Phase | Main Tasks |
|------|-------|----------------|
| 1 | 0, 1 | Setup, OpenSpec, `metric_definition.md`, `run_log.json` start |
| 2 | 2, 3 | Dataset + grouping, Temporal Retriever + tests |
| 3 | 4, 4.5, 5 | Evidence Extractor, **Selector**, Forecast Model |
| 4 | 6, 7 | Faithfulness Metrics (A6), Dashboard + figures |
| 5 | 8 | `run_pipeline.py`, pytest, `test_report.md` |
| 6 | 9, 10, 11 | Report, demo, B4 reflection, advanced metrics |
| 7 | 12, Buffer | Real data/GPU, bug fixes, review, submit |

---

*This document is based on the final project requirements for the Emerging Technologies course.*