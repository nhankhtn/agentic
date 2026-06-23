# Spec — Faithful Evidence-Centric Financial News Forecasting

**Version:** 1.0  
**Created Date:** 2025-06-21  
**Author:** SV1 — Research & Spec Owner  
**Status:** Draft  
**Related Documents:** proposal.md · design.md · tasks.md · metric_definition.md

---

## 1. System Overview

### 1.1 Purpose

This specification outlines the **functional requirements**, **Acceptance Criteria**, **Quality Gates**, and **AI Agent roles** for the stock trend forecasting system with faithful evidence checks.

### 1.2 Scope

| In Scope | Out of Scope |
|---|---|
| UP / DOWN / HOLD predictions from financial news | Real-world stock trading |
| Evidence faithfulness verification | Financial investment recommendations |
| Temporal leakage detection and warning | Real-time precise price forecasting |
| Interactive result visualization dashboard | Live market data integration |

### 1.3 Actors (Users)

| Actor | Description |
|---|---|
| **Researcher** | Students/researchers analyzing the faithfulness of the model |
| **Reviewer** | Instructors/TAs evaluating the system output |
| **System** | Automated Python data processing pipeline |

---

## 2. User Stories & Acceptance Criteria

### US-01 — Temporal Filtering

> **As a** Researcher,  
> **I want** the system to automatically filter out news articles published after `forecast_time`,  
> **So that** predictions are never based on future information (no temporal leakage).

#### Acceptance Criteria

| ID | Condition | Expected Result |
|----|---|---|
| AC-01-01 | News with `news_time < forecast_time` | Included in `valid_news[]` |
| AC-01-02 | News with `news_time >= forecast_time` | Filtered to `invalid_future_news[]`, log WARNING |
| AC-01-03 | Input has 0 valid news | System does not crash; returns prediction="HOLD", confidence=0.5 |
| AC-01-04 | News with `news_time == forecast_time` | Treated as FUTURE NEWS, filtered out |
| AC-01-05 | Log warning format | `[WARNING] Temporal leakage: news_id={id}, news_time={t} >= forecast_time={ft}` |
| AC-01-06 | Output `leakage_count` | Exactly matches the number of filtered news |

**Definition of Done:** All 6 ACs pass via `pytest tests/test_temporal_retriever.py -v`

---

### US-02 — Evidence Extraction

> **As a** Researcher,  
> **I want** the system to extract key evidence phrases from news text and classify their sentiment,  
> **So that** I can see what specific signals drive the model's prediction.

#### Acceptance Criteria

| ID | Condition | Expected Result |
|----|---|---|
| AC-02-01 | News contains negative keywords (miss, weak, decline...) | `polarity = "negative"`, `expected_direction = "DOWN"` |
| AC-02-02 | News contains positive keywords (beat, strong, growth...) | `polarity = "positive"`, `expected_direction = "UP"` |
| AC-02-03 | News lacks clear keywords | `polarity = "neutral"`, `expected_direction = "HOLD"` |
| AC-02-04 | Very short news (< 5 words) | Returns empty evidence `[]`, log WARNING |
| AC-02-05 | Full dataset coverage | ≥ 80% of news extracts at least 1 evidence |
| AC-02-06 | Output completeness | `evidence_text`, `polarity`, `expected_direction`, `confidence` all populated |

**Definition of Done:** ≥ 80% coverage when running on `data/sample_news_price.csv`

---

### US-03 — Stock Movement Forecasting

> **As a** Researcher,  
> **I want** the system to predict stock movement direction (UP/DOWN/HOLD) with a confidence score,  
> **So that** I can evaluate the model's accuracy alongside its faithfulness.

#### Acceptance Criteria

| ID | Condition | Expected Result |
|----|---|---|
| AC-03-01 | Input has more positive than negative evidence | `prediction = "UP"` |
| AC-03-02 | Input has more negative than positive evidence | `prediction = "DOWN"` |
| AC-03-03 | Input has equal positive and negative evidence | `prediction = "HOLD"`, `confidence = 0.5` |
| AC-03-04 | `price_5d_return > 0` | Add +0.5 to positive_count before calculation |
| AC-03-05 | `price_5d_return < 0` | Add +0.5 to negative_count before calculation |
| AC-03-06 | `confidence` range | Always within `[0.0, 1.0]` |
| AC-03-07 | `cited_evidence` | List of evidence aligning with prediction (not empty if valid news exists) |
| AC-03-08 | `rationale` | Non-empty string describing prediction reasoning |

**Definition of Done:** Pipeline runs on full dataset without exceptions; `prediction_results.csv` exists with correct schema.

---

### US-04 — Faithfulness Evaluation

> **As a** Researcher,  
> **I want** the system to compute faithfulness metrics (Temporal Validity, Evidence Support, Confidence Drop),  
> **So that** I can distinguish models that give correct predictions for the right reasons vs. wrong reasons.

#### Acceptance Criteria

| ID | Condition | Expected Result |
|----|---|---|
| AC-04-01 | All cited evidence has `news_time < forecast_time` | `temporal_validity = 1.0` |
| AC-04-02 | ≥ 1 cited evidence has `news_time >= forecast_time` | `temporal_validity < 1.0` |
| AC-04-03 | All cited evidence aligns with prediction | `evidence_support = 1.0` |
| AC-04-04 | `confidence_drop > 0.10` | `faithful_verdict = "likely_faithful"` |
| AC-04-05 | `confidence_drop` in range `[0.05, 0.10]` | `faithful_verdict = "uncertain"` |
| AC-04-06 | `confidence_drop < 0.05` | `faithful_verdict = "possibly_decorative"` |
| AC-04-07 | Empty cited evidence `[]` | `temporal_validity = 0.0`, `evidence_support = 0.0`, `confidence_drop = 0.0` |
| AC-04-08 | Output file | `faithfulness_results.csv` exists with correct schema after pipeline run |

**Definition of Done:** All 8 ACs pass via `pytest tests/test_metrics.py -v`

---

### US-05 — Dashboard Visualization

> **As a** Reviewer,  
> **I want** an interactive dashboard showing predictions, evidence, faithfulness metrics, and leakage warnings,  
> **So that** I can audit the system's behavior without reading raw CSV files.

#### Acceptance Criteria

| ID | Condition | Expected Result |
|----|---|---|
| AC-05-01 | `streamlit run src/dashboard.py` | App runs without import errors |
| AC-05-02 | Tab 1 — Prediction Overview | Shows table, UP/DOWN/HOLD bar chart, 4 metric cards |
| AC-05-03 | Tab 2 — Evidence Explorer | Prediction dropdown, evidence table, red banner on leakage |
| AC-05-04 | Tab 3 — Faithfulness Analysis | Confidence drop bar chart, verdict table, radar chart |
| AC-05-05 | Tab 4 — Temporal Leakage Monitor | Filtered news table, warning if `leakage_rate > 0` |
| AC-05-06 | Temporal leakage warning | Displays ⚠️ red banner when `invalid_future_news` exists |
| AC-05-07 | Static figures | 4 PNG files exist in `outputs/figures/` after pipeline run |

**Definition of Done:** Dashboard runs on SV1 and SV2 machines; 4 PNG files exist.

---

### US-06 — Agentic SDLC Traceability

> **As a** Reviewer,  
> **I want** to see a log of all AI agent activities with human review outcomes,  
> **So that** I can verify that AI assistance was used responsibly with proper quality gates.

#### Acceptance Criteria

| ID | Condition | Expected Result |
|----|---|---|
| AC-06-01 | `outputs/run_log.json` exists | File exists and parses as valid JSON |
| AC-06-02 | Entry count | ≥ 6 entries in the JSON array |
| AC-06-03 | Agent roles represented | Includes at least 3 roles: `Research Agent`, `Coding Agent`, `Testing Agent` |
| AC-06-04 | Each entry has required fields | `run_id`, `task_id`, `timestamp`, `agent_role`, `tool_used`, `task`, `input_summary`, `output_summary`, `human_review`, `quality_gate` |
| AC-06-05 | `quality_gate` value | All entries are either `"passed"` or `"failed"` (no blanks) |
| AC-06-06 | `human_review` value | `"accepted"`, `"accepted with edits"`, or `"rejected"` |

**Definition of Done:** File exists, parses correctly, has ≥ 6 entries, covers 3 roles.

---

## 3. Input / Output Schema

### 3.1 Input Schema — `data/sample_news_price.csv`

```
ticker         : string          — Stock ticker (e.g., AAPL, TSLA, NVDA)
forecast_time  : datetime string — ISO 8601, YYYY-MM-DD HH:MM (e.g., 2025-03-12 09:00)
news_id        : string          — Unique ID (e.g., N001)
news_time      : datetime string — ISO 8601, YYYY-MM-DD HH:MM
news_title     : string          — News title
news_text      : string          — News body text
price_5d_return: float           — 5-day return rate (e.g., -0.02)
volume_change  : float           — (Optional) Trading volume change
label          : string          — Actual label: UP | DOWN | HOLD
```

**Constraints:**
- `ticker` must not be empty
- `forecast_time` and `news_time` must parse to minute-level datetimes
- `label` accepts only 3 values: `UP`, `DOWN`, `HOLD`
- Dataset must have ≥ 30 rows, ≥ 3 unique tickers, ≥ 5 temporal leakage rows

### 3.2 Output Schema — `prediction_results.csv`

```json
{
  "ticker":          "string  — Stock ticker",
  "forecast_time":   "string  — Forecast timestamp",
  "prediction":      "string  — UP | DOWN | HOLD",
  "confidence":      "float   — [0.0, 1.0]",
  "rationale":       "string  — Natural language explanation",
  "cited_evidence":  "list    — List of cited evidence",
  "label":           "string  — Actual label",
  "correct":         "boolean — prediction == label"
}
```

### 3.3 Output Schema — `faithfulness_results.csv`

```json
{
  "ticker":                      "string",
  "forecast_time":               "string",
  "prediction":                  "string  — UP | DOWN | HOLD",
  "confidence_original":         "float   — confidence with full evidence",
  "confidence_without_evidence": "float   — confidence after dropping cited evidence",
  "confidence_drop":             "float   — original - without",
  "temporal_validity":           "float   — [0.0, 1.0]",
  "evidence_support":            "float   — [0.0, 1.0]",
  "leakage_count":               "int     — number of filtered news items",
  "faithful_verdict":            "string  — likely_faithful | uncertain | possibly_decorative"
}
```

### 3.4 Output Schema — `outputs/run_log.json`

```json
[
  {
    "run_id":         "string  — e.g., R001",
    "task_id":        "string  — e.g., P3-01",
    "timestamp":      "string  — YYYY-MM-DD HH:MM:SS",
    "agent_role":     "string  — Research Agent | Coding Agent | Testing Agent",
    "tool_used":      "string  — ChatGPT | Cursor | GitHub Copilot | Claude | Antigravity",
    "task":           "string  — Short task description",
    "input_summary":  "string  — Summary of prompt given to agent",
    "output_summary": "string  — Summary of agent's output",
    "human_review":   "string  — accepted | accepted with edits | rejected",
    "quality_gate":   "string  — passed | failed",
    "notes":          "string  — (Optional) Additional notes"
  }
]
```

---

## 4. Quality Gates

Quality Gates are mandatory **human-led** checkpoints before AI-assisted code merges into the main branch.

| Gate ID | Trigger | Reviewer | Pass Criteria |
|---|---|---|---|
| **QG-01** | After AI generates module code | SV2 or SV3 | Code runs, logic matches `design.md`, no magic hardcoded values |
| **QG-02** | After AI generates test cases | SV3 | Tests pass, ≥ 1 edge case included, meaningful assertions (not just assert True) |
| **QG-03** | Before merging OpenSpec docs | SV2 and SV3 | Readable content; measurable acceptance criteria |
| **QG-04** | Final pipeline run before submission | Full Team | No runtime errors; output files exist with correct schema; `leakage_rate` is accurate |
| **QG-05** | Before recording demo video | SV1 lead | All `pytest tests/ -v` pass; dashboard loads in < 10 seconds |

**Quality Gate Rules:**
1. All AI-assisted code **must** pass at least **QG-01** before use.
2. Review results must be logged in `outputs/run_log.json` (`human_review` and `quality_gate`).
3. If `quality_gate = "failed"`, the AI agent must regenerate the output; **gates cannot be skipped**.

---

## 5. AI Agent Roles in SDLC

### 5.1 Agent Distribution Map

```
SDLC Phase          AI Agent Role           Human Responsibility
─────────────────────────────────────────────────────────────────
Requirements    →   Research Agent      →   Verify user stories are testable
Design          →   Research Agent      →   Choose design fitting team capabilities
Implementation  →   Coding Agent        →   Read code, run tests, QG-01
Testing         →   Testing Agent       →   Check edge cases in tests, QG-02
Evaluation      →   Research Agent      →   Avoid overclaiming; document limitations
Documentation   →   Coding Agent        →   Verify docstrings match actual code
```

### 5.2 Detailed Roles

#### Research Agent
- **Tasks:** Aggregate literature, suggest metrics, explain concepts, create sample user stories
- **Example:** "Explain the difference between prediction accuracy and explanation faithfulness"
- **Restrictions:** Cannot make final system design or dataset selections

#### Coding Agent
- **Tasks:** Generate Python code, suggest refactoring, explain algorithms, write docstrings
- **Example:** "Write the `filter_news_by_time()` function according to this spec"
- **Restrictions:** Cannot alter business logic without human review

#### Testing Agent
- **Tasks:** Generate test cases, suggest edge cases, review test coverage
- **Example:** "Create 5 test cases for `filter_news_by_time()` including boundary conditions"
- **Restrictions:** Cannot validate test passes without actual execution

### 5.3 General Principles

> ⚠️ **CRITICAL:** All AI Agent outputs must undergo human review. Never use AI-generated content or code without reading, understanding, and verifying it.

- Log every AI usage in `outputs/run_log.json`
- Do not let the agent autonomously decide parameters that affect experiment outcomes (e.g., confidence drop thresholds, keyword lists)
- If AI generates flawed code, fix it manually and log `human_review = "accepted with edits"`

---

## 6. Non-functional Requirements

| Requirement | Criteria |
|---|---|
| **Performance** | Pipeline processes ≤ 1000 rows in < 30 seconds |
| **Correctness** | Zero future information bypasses the Temporal Retriever |
| **Reproducibility** | Running pipeline twice on same input → identical output |
| **Portability** | Runs on Python 3.10+ across Windows, macOS, Linux |
| **Readability** | All functions have docstrings and complete type hints |
| **Testability** | ≥ 10 test cases; `pytest tests/ -v` passes without extra config |

---

## 7. Ethical Constraints & System Limitations

- The system is for **educational and research purposes only**.
- Results **must not be used** for real-world financial trading recommendations.
- Small/simulated dataset — results are not representative of real markets.
- Simple rule-based model — low accuracy is expected; focus is on faithfulness.
- Keyword-based evidence extraction may fail on ambiguous or sarcastic news.

---

## 8. Change History

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0 | 2025-06-21 | SV1 | Initial version — 6 user stories, 4 schemas, 5 quality gates |

---

*This document belongs to the OpenSpec workflow — Specification Phase. After team review and approval (QG-03), it advances to Implementation.*
