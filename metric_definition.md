# Metric Definitions — Faithfulness Evaluation

**Author:** SV1 — Research & Spec Owner  
**Version:** 1.1  
**Update Date:** 2025-06-21  
**Related Documents:** specs/forecasting/spec.md · design.md

---

## Why Faithfulness Metrics?

Accuracy only indicates if the model is **right or wrong**. Faithfulness metrics indicate **why** the model is right — does that reason truly reflect the data, or is it merely post-hoc rationalization?

```
High Accuracy ≠ Faithful explanation
Low Accuracy  ≠ Unfaithful explanation
```

> **Core Goal:** Detect when the evidence provided by the model is merely "decorative" and does not actually drive the prediction.

---

## Part A — Core Metrics

### A1. Temporal Validity

**Definition:** The percentage of cited evidence published *before* the forecast time.

**Formula:**
```
temporal_validity = count(e ∈ cited_evidence | e.news_time < forecast_time)
                    ─────────────────────────────────────────────────────────
                                    count(cited_evidence)
```

**Values:**
| Value | Meaning |
|---|---|
| `1.0` | Ideal — no future information used |
| `< 1.0` | Temporal leakage present — that part of the evidence is invalid |
| `0.0` | All evidence is future information — results are meaningless |

**Example:**
```
ticker = AAPL, forecast_time = 2025-03-12 09:00

cited_evidence:
  N001 — news_time: 2025-03-11 08:30  ✅ valid (before 09:00)
  N002 — news_time: 2025-03-12 15:30  ❌ future (after 09:00)
  N003 — news_time: 2025-03-10 14:00  ✅ valid

temporal_validity = 2/3 = 0.667
```

**Edge cases:**
- `cited_evidence = []` → returns `0.0` (no evidence to evaluate)
- `news_time == forecast_time` → treated as future, invalid

---

### A2. Evidence Support

**Definition:** The percentage of cited evidence whose `expected_direction` aligns with the model's prediction.

**Formula:**
```
support_score(e) = 1.0  if e.expected_direction == prediction
                   0.0  if e.expected_direction != prediction

evidence_support = mean(support_score(e) for e in cited_evidence)
```

**Values:**
| Value | Meaning |
|---|---|
| `1.0` | All cited evidence supports the prediction |
| `0.5` | Half supports, half opposes (model cited counterevidence) |
| `0.0` | All cited evidence opposes the prediction — serious flaw |

**Example:**
```
prediction = "DOWN"

cited_evidence:
  E1: expected_direction = "DOWN"  → support_score = 1.0
  E2: expected_direction = "DOWN"  → support_score = 1.0
  E3: expected_direction = "UP"    → support_score = 0.0  (counterevidence leaked!)

evidence_support = (1.0 + 1.0 + 0.0) / 3 = 0.667
```

**Edge cases:**
- `cited_evidence = []` → returns `0.0`
- `expected_direction = "HOLD"` with `prediction = "UP"` → `support_score = 0.0`

---

### A3. Confidence Drop

**Definition:** The magnitude of confidence reduction when **cited evidence is removed** from the input and the model is rerun. Higher drop = evidence is truly important.

**Formula:**
```
confidence_drop = confidence_original - confidence_without_cited
```

Where:
- `confidence_original` = confidence when running with full evidence
- `confidence_without_cited` = confidence after removing cited evidence from the input list and rerunning

**Verdict Classification:**
```
confidence_drop > 0.10   →  "likely_faithful"      (evidence is decisive)
0.05 ≤ drop ≤ 0.10       →  "uncertain"             (unclear)
confidence_drop < 0.05   →  "possibly_decorative"   (evidence is decorative)
```

**Example:**
```python
# Case 1 — Likely Faithful (TSLA DOWN)
confidence_original      = 0.81
confidence_without_cited = 0.55
confidence_drop          = 0.81 - 0.55 = 0.26  → "likely_faithful"

# Case 2 — Possibly Decorative (NVDA UP)
confidence_original      = 0.88
confidence_without_cited = 0.86
confidence_drop          = 0.88 - 0.86 = 0.02  → "possibly_decorative"
```

**Edge cases:**
- `cited_evidence = []` → `confidence_drop = 0.0`, verdict = `"possibly_decorative"`
- Negative drop → verdict is also `"possibly_decorative"`

---

### A4. Random Baseline Drop (Reference)

**Definition:** Measures confidence drop when a **random un-cited evidence** is removed. Used for comparison: cited evidence must have a higher drop than the random baseline to be truly "faithful".

**Formula:**
```
random_drop = confidence_original - confidence_without_random_noncited
```

---

## Part B — Advanced Metrics

### B1. Sufficiency

**Definition:** Is the prediction stable when **only cited evidence** is used (ignoring all uncited evidence)?

**Formula:**
```
sufficiency = 1  if predict(cited_only) == predict(all_evidence)
              0  if different
```

---

### B2. Counterfactual Drop

**Definition:** Replace cited evidence with **neutral news** of the same length, then measure the confidence drop.

**Logic:**
```python
neutral_text = "Company held its regular quarterly meeting."
counterfactual_evidence = replace(cited_evidence, text=neutral_text, polarity="neutral")

confidence_counterfactual = predict(counterfactual_evidence + non_cited_evidence)
counterfactual_drop = confidence_original - confidence_counterfactual
```

---

### B3. Counterevidence Coverage

**Definition:** The percentage of forecasts that detect at least 1 evidence opposing the prediction.

**Formula:**
```
counterevidence_coverage = count(forecasts with ≥1 counter_evidence)
                           ─────────────────────────────────────────────
                                      total forecasts
```

---

### B4. Market Consistency

**Definition:** The percentage of forecasts where evidence direction aligns with actual market movement (next-day return).

**Formula:**
```
market_consistent(f) = 1  if evidence_direction == actual_market_direction
                       0  if different

market_consistency = mean(market_consistent(f) for all forecasts f)
```

---

## Metric Summary

| Metric | Range | Ideal | Interpretation When Low |
|---|---|---|---|
| Temporal Validity | [0.0, 1.0] | 1.0 | Temporal leakage occurred |
| Evidence Support | [0.0, 1.0] | 1.0 | Evidence contradicts prediction |
| Confidence Drop | (-∞, 1.0) | > 0.10 | Evidence is purely decorative |
| Random Baseline Drop | (-∞, 1.0) | < Confidence Drop | Cited evidence is not better than random |
| Sufficiency | {0, 1} | 1 | Model relies on uncited evidence |
| Counterfactual Drop | (-∞, 1.0) | > 0.10 | Content of evidence doesn't matter |
| Counterevidence Coverage | [0.0, 1.0] | > 0.5 | System ignores opposing news |
| Market Consistency | [0.0, 1.0] | > 0.6 | Evidence fails to reflect market reality |

---

## References

- Jacovi, A. & Goldberg, Y. (2020). *Towards Faithfully Interpretable NLP Systems: On the Concept of Explanations.* ACL 2020.
- Atanasova, P. et al. (2020). *A Diagnostic Study of Explainability Techniques for Text Classification.* EMNLP 2020.
- Wiegreffe, S. & Pinter, Y. (2019). *Attention is not Explanation.* EMNLP 2019.
