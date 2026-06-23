# Sub-tasks — SV2 · ML/NLP Engineer

**Project:** Faithful Evidence-Centric Financial News Forecasting  
**Role:** Student 2 — ML/NLP Engineer  
**References:** [REQUIREMENT.md](./REQUIREMENT.md), [tasks.md](./openspec/changes/faithful-evidence-forecasting/tasks.md), [design.md](./openspec/changes/faithful-evidence-forecasting/design.md)

---

## What are your responsibilities?

SV2 is the **main owner** of the entire **ML/NLP pipeline** — from data to prediction and faithfulness metrics. **Training a model is not required** for the basic 7 points; rule-based is sufficient.

| Your ownership | Collaboration with team | Not your main task |
|----------------------|-------------------|------------------------------|
| `data/sample_news_price.csv` | Review OpenSpec (written by SV1) | `dashboard.py` (SV3) |
| `src/retriever.py` | CSV Schema (with SV1) | `test_*.py` (written by SV3, you help run) |
| `src/evidence_extractor.py` | Extractor examples table (with SV1) | OpenSpec proposal/spec (SV1) |
| `src/evidence_selector.py` | Demo video (you demo the ML part) | Main `run_log.json` (SV1) |
| `src/forecast_model.py` | Report sections 4–7 (with SV1) | PNG figures (exported by SV3) |
| `src/faithfulness_metrics.py` | E2E testing (with SV3) | |
| `src/run_pipeline.py` | | |
| `requirements.txt` | | |
| `outputs/prediction_results.csv` | | |
| `outputs/faithfulness_results.csv` | | |

**Pipeline you must make operational:**

```
CSV → group (ticker, forecast_time)
  → Retriever → Extractor → Selector → Forecast Model → Faithfulness Metrics → outputs/
```

---

## Update Convention

| Symbol | Meaning |
|---------|---------|
| `[ ]` | Todo |
| `[~]` | In progress |
| `[x]` | Done |
| `🤖` | Used AI agent — log it in `outputs/run_log.json` |
| `🔗` | Depends on another task/person |

---

## Suggested Timeline (SV2)

| Week | Phase | Your main focus |
|------|-------|---------------------|
| 1 | 0, 1 | Python Setup, `requirements.txt`, design/schema review |
| 2 | 2, 3 | Dataset + `retriever.py` |
| 3 | 4, 4.5, 5 | Extractor + Selector + Forecast Model |
| 4 | 6 | Faithfulness metrics + first run of full pipeline |
| 5 | 8 | Complete `run_pipeline.py`, E2E with SV3 |
| 6 | 9 | Write report sections 4–5, support demo |
| 7 | 11, 12 | (Optional) advanced metrics, real data/GPU |

---

## PHASE 0 — Kickoff & Environment Setup

**Goal:** Ensure your machine runs the Python project and you understand the end-to-end pipeline.

### Sub-tasks

- [ ] **S2-P0-01** Read `REQUIREMENT.md` + `design.md` — write a 1-page summary of the data flow (for Q&A defense)
- [ ] **S2-P0-02** Understand the 4 assignment cases: faithful evidence, decorative evidence, temporal leakage, counterevidence
- [ ] **S2-P0-03** 🤖 Create `requirements.txt` with: `pandas`, `numpy`, `scikit-learn`, `pytest`, `streamlit`, `plotly`
- [ ] **S2-P0-04** Setup environment: `python -m venv .venv && pip install -r requirements.txt`
- [ ] **S2-P0-05** Create empty Python files in `src/`: `retriever.py`, `evidence_extractor.py`, `evidence_selector.py`, `forecast_model.py`, `faithfulness_metrics.py`, `run_pipeline.py`
- [ ] **S2-P0-06** Agree with SV1/SV3 on: ISO 8601 datetime format, variable/function naming conventions

### Deliverables Phase 0

| File | Status |
|------|-----------|
| `requirements.txt` | `[ ]` |
| `src/*.py` (skeleton) | `[ ]` |

---

## PHASE 1 — OpenSpec Support (review, not main writer)

**Goal:** Ensure the specs match the code you will write.

🔗 Waiting for SV1 to draft `design.md` and `metric_definition.md`.

### Sub-tasks

- [ ] **S2-P1-01** 🔗 Review `design.md`: are the interfaces for each module (input/output) implementable?
- [ ] **S2-P1-02** 🔗 Review `specs/forecasting/spec.md`: are the acceptance criteria testable via code?
- [ ] **S2-P1-03** Provide feedback on the CSV schema with SV1 (columns, types, grouping rules)
- [ ] **S2-P1-04** Confirm the 3 metric formulas in `metric_definition.md` before coding Phase 6

### Deliverables Phase 1

| Task | Status |
|------|-----------|
| Comment review on PR/issue or notes in team meeting | `[ ]` |

---

## PHASE 2 — Data Preparation · **A2**

**Goal:** Provide `data/sample_news_price.csv` with ≥30 rows, covering edge cases, groupable by `(ticker, forecast_time)`.

### Sub-tasks

#### 2.1 Design & Generate Dataset

- [ ] **S2-P2-01** 🔗 Agree on CSV schema with SV1 (mandatory columns):

  | Column | Type | Notes |
  |-----|------|---------|
  | `ticker` | string | AAPL, TSLA, NVDA, ... |
  | `forecast_time` | datetime | Forecast timestamp |
  | `news_id` | string | N001, N002, ... |
  | `news_time` | datetime | News publication time |
  | `news_title` | string | |
  | `news_text` | string | |
  | `price_5d_return` | float | |
  | `volume_change` | float | |
  | `label` | string | UP / DOWN / HOLD |

- [ ] **S2-P2-02** 🤖 Generate ≥30 rows of simulated news (3 tickers, 3 labels, positive/negative/neutral)
- [ ] **S2-P2-03** Include **≥5 leakage rows**: `news_time >= forecast_time` (for SV3 to test retriever)
- [ ] **S2-P2-04** Create **≥3 counterevidence groups**: same `(ticker, forecast_time)`, with both positive + negative news
- [ ] **S2-P2-05** Ensure `label`, `price_*` are consistent within the same group

#### 2.2 Preprocessing & Statistics

- [ ] **S2-P2-06** 🤖 Write `src/data_utils.py` (or script in `run_pipeline.py`):
  - `load_csv()` — parse datetime
  - `group_by_forecast(df)` → list of group dicts
  - validate label ∈ {UP, DOWN, HOLD}
- [ ] **S2-P2-07** 🤖 Generate statistics table: row count, group count, label distribution, leakage row count
- [ ] **S2-P2-08** 🔗 Send dataset to SV3 to review edge cases (P2-07 in tasks.md)

#### 2.3 (Optional · C1) Real Data

- [ ] **S2-P2-09** Script `scripts/fetch_real_data.py` — Yahoo Finance + news dataset
- [ ] **S2-P2-10** ≥300 samples, 3 tickers, labels from `return_next_day`
- [ ] **S2-P2-11** Document data sources + statistics table for the report

### Deliverables Phase 2

| File | Status |
|------|-----------|
| `data/sample_news_price.csv` | `[ ]` |
| `src/data_utils.py` (or equivalent) | `[ ]` |
| Dataset statistics table (markdown/csv) | `[ ]` |

### Completion Criteria (A2)

- [ ] ≥30 CSV rows, ≥3 tickers, includes UP/DOWN/HOLD
- [ ] ≥5 temporal leakage rows
- [ ] Grouping by `(ticker, forecast_time)` loads successfully via code

---

## PHASE 3 — Temporal Retriever · **A3**

**Goal:** `src/retriever.py` — prevent usage of future news.

### Sub-tasks

- [ ] **S2-P3-01** 🤖 Implement `filter_news_by_time(news_list, forecast_time)`:
  - `valid_news`: `news_time < forecast_time`
  - `invalid_future_news`: `news_time >= forecast_time`
  - return additionally `leakage_count`
- [ ] **S2-P3-02** Log WARNING upon leakage: `[WARNING] Temporal leakage detected: news_id=..., news_time=... > forecast_time=...`
- [ ] **S2-P3-03** 🤖 Full docstrings + type hints
- [ ] **S2-P3-04** Run retriever on the full dataset, confirm 5+ news items go into `invalid_future_news`
- [ ] **S2-P3-05** 🔗 Hand over interface to SV3 to write `tests/test_temporal_retriever.py` (6 TCs)
- [ ] **S2-P3-06** Run `pytest tests/test_temporal_retriever.py -v` — fix if failed

### Deliverables Phase 3

| File | Status |
|------|-----------|
| `src/retriever.py` | `[ ]` |

### Completion Criteria (A3)

- [ ] Filter function correctly filters `>=`
- [ ] Warning log + `leakage_count` present
- [ ] Retriever tests pass (coordinating with SV3)

---

## PHASE 4 — Evidence Extraction · **A4**

**Goal:** Extract evidence from news text (rule-based keywords).

### Sub-tasks

- [ ] **S2-P4-01** 🤖 Define keyword dictionary:
  - Negative → DOWN: `miss, weak, decline, drop, loss, recall, layoff, ...`
  - Positive → UP: `beat, strong, growth, launch, surge, profit, ...`
  - Neutral → HOLD: `meeting, announce, report, hold, ...`
- [ ] **S2-P4-02** 🤖 Implement `extract_evidence(news_item) -> list[dict]`:

  ```python
  {
    "news_id": "...",
    "news_time": "...",
    "evidence_text": "...",
    "polarity": "negative",
    "expected_direction": "DOWN",
    "confidence": 0.85
  }
  ```

- [ ] **S2-P4-03** Edge cases:
  - Text < 10 words → neutral + warning log
  - No keywords → neutral, HOLD
  - Both positive and negative → return both evidences
- [ ] **S2-P4-04** Run on full dataset — **coverage ≥80%** of news have ≥1 evidence
- [ ] **S2-P4-05** 🔗 With SV1: table of 5 correct examples + 5 incorrect/edge examples (for report)
- [ ] **S2-P4-06** 🤖 Docstrings + type hints

### Deliverables Phase 4

| File | Status |
|------|-----------|
| `src/evidence_extractor.py` | `[ ]` |
| Table of 10 extractor examples | `[ ]` |

---

## PHASE 4.5 — Evidence Selector · **A4 / Foundation for B2**

**Goal:** Separate pro/counter evidence, select cited evidence before prediction.

### Sub-tasks

- [ ] **S2-P4.5-01** 🤖 Implement `select_evidence(all_evidence, dominant_direction=None)`:
  - `pro_evidence` — aligns with dominant direction
  - `counter_evidence` — opposite direction
  - `cited_evidence` — top-k by `confidence` (≥1 if pro exists)
- [ ] **S2-P4.5-02** Remove duplicates: same `news_id` or identical `evidence_text`
- [ ] **S2-P4.5-03** Manually test on 3 counterevidence groups in dataset — pro and counter are not empty
- [ ] **S2-P4.5-04** 🤖 Docstrings + type hints

### Deliverables Phase 4.5

| File | Status |
|------|-----------|
| `src/evidence_selector.py` | `[ ]` |

---

## PHASE 5 — Forecast Model · **A5**

**Goal:** Predict UP/DOWN/HOLD + confidence + rationale. **Rule-based, no training.**

### Sub-tasks

- [ ] **S2-P5-01** 🤖 Implement `predict(ticker, forecast_time, valid_news, price_features, cited_evidence=None)`:

  **Rule-based (sufficient for A5):**
  ```
  positive_count, negative_count from evidence (ignore neutral)
  price_signal = sign(price_5d_return)
  score = (positive_count - negative_count) + 0.5 * price_signal

  score > 0  → UP,   confidence = positive / (positive + negative)
  score < 0  → DOWN, confidence = negative / (positive + negative)
  score = 0  → HOLD, confidence = 0.5
  ```

- [ ] **S2-P5-02** Return `cited_evidence` + `rationale` (string explaining the reason)
- [ ] **S2-P5-03** Fallback when no news / all leaked → HOLD, low confidence, clear rationale
- [ ] **S2-P5-04** Run predict on all groups → save to `outputs/prediction_results.csv`
- [ ] **S2-P5-05** 🤖 Calculate accuracy + confusion matrix (`sklearn.metrics`)
- [ ] **S2-P5-06** 🔗 With SV1: write a detailed explanation for **1 prediction** (case study for report)
- [ ] **S2-P5-07** 🤖 Docstrings + type hints

### Deliverables Phase 5

| File | Status |
|------|-----------|
| `src/forecast_model.py` | `[ ]` |
| `outputs/prediction_results.csv` | `[ ]` |
| Accuracy + confusion matrix (markdown or notebook) | `[ ]` |

### Completion Criteria (A5)

- [ ] Successfully predicts UP/DOWN/HOLD for all groups
- [ ] Includes confidence + at least 1 cited evidence (when valid news exists)
- [ ] 1 case study clearly explained in the report

---

## PHASE 6 — Faithfulness Metrics · **A6**

**Goal:** Prove whether evidence is faithful or not — **the core of the project**.

### Sub-tasks

#### 6.1 Three core metrics

- [ ] **S2-P6-01** 🤖 `temporal_validity(cited_evidence, forecast_time)` → float [0, 1]
- [ ] **S2-P6-02** 🤖 `evidence_support(cited_evidence, prediction)` → float [0, 1]
- [ ] **S2-P6-03** `confidence_drop(...)`:
  1. Run model with full input → `confidence_original`
  2. Remove cited evidence → rerun → `confidence_without`
  3. `confidence_drop = original - without`
  4. Also compute `confidence_drop_random` (remove 1 non-cited news)
- [ ] **S2-P6-04** Verdict: `likely_faithful` (drop > 0.1), `possibly_decorative` (drop < 0.05)
- [ ] **S2-P6-05** Run on all groups → `outputs/faithfulness_results.csv`
- [ ] **S2-P6-06** 🔗 With SV1: table of mean values for 3 metrics across dataset
- [ ] **S2-P6-07** 🔗 Hand over interface to SV3: `test_metrics.py` (5 TCs)
- [ ] **S2-P6-08** 🤖 Docstrings + type hints

#### 6.2 Preparation for dashboard (used by SV3)

- [ ] **S2-P6-09** Export CSV format with all required columns for Dashboard Tab 3
- [ ] **S2-P6-10** Document how to call `confidence_drop` from the dashboard (re-run at runtime)

### Deliverables Phase 6

| File | Status |
|------|-----------|
| `src/faithfulness_metrics.py` | `[ ]` |
| `outputs/faithfulness_results.csv` | `[ ]` |

### Completion Criteria (A6)

- [ ] 3 metrics computable for all predictions with cited evidence
- [ ] Comparison between cited vs random confidence drop included
- [ ] Metrics tests pass (coordinating with SV3)

---

## PHASE 7 — Dashboard Support (SV3 owner)

**You do not write the main dashboard**, but you must support SV3 with integration.

### Sub-tasks

- [ ] **S2-P7-01** 🔗 Provide a stable API: `run_single_forecast(group)` returning all fields for the dashboard
- [ ] **S2-P7-02** 🔗 Help SV3 implement "Remove cited evidence" — calling `predict()` + `confidence_drop()`
- [ ] **S2-P7-03** Test dashboard on your machine: `streamlit run src/dashboard.py`
- [ ] **S2-P7-04** Prepare **2 demo cases** (1 faithful, 1 decorative) for the presentation

---

## PHASE 8 — E2E Pipeline & QA

**Goal:** `run_pipeline.py` runs with a single command, producing all outputs.

### Sub-tasks

- [ ] **S2-P8-01** 🤖 Write `src/run_pipeline.py`:

  ```bash
  python src/run_pipeline.py --input data/sample_news_price.csv
  ```

  Flow: load → group → retriever → extractor → selector → model → metrics → write CSVs

- [ ] **S2-P8-02** 🔗 With SV3: run E2E, ensuring zero runtime errors
- [ ] **S2-P8-03** Handle edge cases in pipeline:
  - Empty group → HOLD
  - All news leaked → HOLD + warning
  - No cited evidence → confidence_drop = 0
- [ ] **S2-P8-04** Run `pytest tests/ -v` — fix any bugs on the ML modules side
- [ ] **S2-P8-05** Record `outputs/commit_log.md` or PR links for your code (B4)

### Deliverables Phase 8

| File | Status |
|------|-----------|
| `src/run_pipeline.py` | `[ ]` |
| Pipeline runs E2E without errors | `[ ]` |

---

## PHASE 9 — Report & Demo

### Sub-tasks (your sections)

- [ ] **S2-P9-01** Write report **Section 4 — Data**: schema, statistics, label creation, group logic
- [ ] **S2-P9-02** Write report **Section 5 — Technical Pipeline**: describe the 5 ML modules (avoid pasting long code blocks)
- [ ] **S2-P9-03** 🔗 With SV1: **Sections 6–7** — metrics + experimental results (tables, real figures from `outputs/`)
- [ ] **S2-P9-04** Participate in ~5 min demo: explain pipeline + "Remove cited evidence" action
- [ ] **S2-P9-05** Review report draft 1 — provide technical feedback

### Deliverables Phase 9

| Task | Status |
|------|-----------|
| Report sections 4–5 (draft) | `[ ]` |
| Participation in demo video | `[ ]` |

---

## PHASE 10 — Agentic SDLC (coordinate with SV1)

Log every instance of using Cursor/ChatGPT for ML tasks:

- [ ] **S2-P10-01** ≥2 entries in `outputs/run_log.json` with `agent_role: "Coding Agent"`
- [ ] **S2-P10-02** Each entry records: task_id (S2-P*), human_review, quality_gate

**Tasks recommended for logging:** P2-02, P3-01, P4-02, P5-01, P6-03, P8-01

---

## PHASE 11 — Advanced Metrics (optional · B1–B3)

Only tackle after Phase 6 is done and the team decides to aim for bonus points.

- [ ] **S2-P11-01** (B1) `sufficiency_test()` — use only cited evidence → predict again
- [ ] **S2-P11-02** (B1) `counterfactual_perturbation()` — replace evidence with neutral news
- [ ] **S2-P11-03** (B2) `counterevidence_coverage()` — use output from selector
- [ ] **S2-P11-04** (B3) `market_consistency()` — compare evidence vs actual label/return
- [ ] **S2-P11-05** (B3) Analyze by bull/bear/sideway regimes
- [ ] **S2-P11-06** Append columns to `faithfulness_results.csv`

---

## PHASE 12 — Real Data & GPU (optional · C1–C2)

- [ ] **S2-P12-01** (C1) Collect ≥300 samples, 3 tickers — see S2-P2-09
- [ ] **S2-P12-02** (C2) FinBERT sentiment or LSTM — **only if aiming for +1 bonus point**
- [ ] **S2-P12-03** (C2) Comparison table for rule-based vs GPU model (accuracy, avg confidence drop, runtime)

---

## Final Checklist — SV2 before submission

### Code (mandatory)

- [ ] `requirements.txt`
- [ ] `data/sample_news_price.csv` (≥30 rows)
- [ ] `src/retriever.py`
- [ ] `src/evidence_extractor.py`
- [ ] `src/evidence_selector.py`
- [ ] `src/forecast_model.py`
- [ ] `src/faithfulness_metrics.py`
- [ ] `src/run_pipeline.py`
- [ ] `outputs/prediction_results.csv`
- [ ] `outputs/faithfulness_results.csv`

### Quality

- [ ] `python src/run_pipeline.py` runs without errors
- [ ] `pytest tests/ -v` passes
- [ ] No future news in model input (only `valid_news`)
- [ ] Can explain every module when questioned during defense

### Team Coordination

- [ ] SV3 has the CSV + API needed for the dashboard
- [ ] SV1 has the real metrics for report sections 6–7
- [ ] Participated in the demo video

---

## Quick Reference Q&A

| Question | Answer |
|---------|---------|
| Do we need to train a model? | **No** (for base 7 points). Rule-based is sufficient. |
| Which module to build first? | Dataset → Retriever → Extractor → Selector → Model → Metrics → Pipeline |
| Most important metric? | **Confidence Drop** — drop cited evidence, does confidence decrease? |
| Which files does SV3 need from you? | `prediction_results.csv`, `faithfulness_results.csv`, function to re-run predict |

---

*Update status `[ ]` → `[~]` → `[x]` after each working session. This file contains personal sub-tasks for SV2; full team tasks are in `openspec/changes/faithful-evidence-forecasting/tasks.md`.*
