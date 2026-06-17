# Metric Definitions — Faithfulness Evaluation

## Core metrics (A6)

### Temporal Validity
```
temporal_validity = (# cited evidence with news_time < forecast_time) / (# cited evidence)
```
Ideal value: **1.0** (no future information in cited evidence).

### Evidence Support
```
support_score = 1.0 if expected_direction == prediction else 0.0
evidence_support = mean(support_score over cited evidence)
```

### Confidence Drop
```
confidence_drop = confidence_original - confidence_without_cited
```
- Remove cited evidence from input, re-run forecast model.
- `confidence_drop > 0.10` → **likely_faithful**
- `confidence_drop < 0.05` → **possibly_decorative**

### Confidence Drop (Random baseline)
Remove one random **non-cited** evidence item and measure drop. Cited evidence is more faithful if its drop exceeds the random baseline.

## Advanced metrics (optional B1–B3)

- **Sufficiency**: prediction stable when only cited evidence is used.
- **Counterfactual drop**: replace cited evidence with neutral text and measure confidence change.
- **Counterevidence coverage**: fraction of forecasts where counter-direction evidence is detected.
- **Market consistency**: evidence direction aligns with realized next-day return.
