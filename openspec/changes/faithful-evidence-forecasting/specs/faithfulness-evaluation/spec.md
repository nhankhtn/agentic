## ADDED Input / Output

**Input:**
- `cited_evidence`: list of evidence dicts cited by the forecast model
- `prediction`: str — "UP" | "DOWN" | "HOLD"
- `forecast_time`: datetime str — the forecast timestamp
- `confidence_original`: float — model confidence with all evidence
- `confidence_without_evidence`: float — model confidence after removing cited evidence

**Output:**
- `temporal_validity`: float in [0.0, 1.0] — ratio of temporally valid cited evidence
- `evidence_support`: float in [0.0, 1.0] — ratio of direction-aligned cited evidence
- `confidence_drop`: float — `confidence_original - confidence_without_evidence`
- `faithful_verdict`: "likely_faithful" | "uncertain" | "possibly_decorative"
- CSV file: `outputs/faithfulness_results.csv` with all metrics per prediction

## ADDED Requirements

### Requirement: System SHALL compute Temporal Validity metric
The system SHALL calculate the ratio of cited evidence with valid timestamps (before forecast_time) to total cited evidence.

#### Scenario: All evidence is temporally valid
- **WHEN** every cited evidence item has `news_time < forecast_time`
- **THEN** `temporal_validity` SHALL equal 1.0

#### Scenario: Some evidence has temporal leakage
- **WHEN** 2 of 3 cited evidence items have `news_time < forecast_time`
- **THEN** `temporal_validity` SHALL equal 0.667 (rounded to 3 decimal places)

#### Scenario: No cited evidence
- **WHEN** `cited_evidence` is an empty list
- **THEN** `temporal_validity` SHALL equal 0.0

### Requirement: System SHALL compute Evidence Support metric
The system SHALL calculate the ratio of cited evidence whose `expected_direction` matches the prediction.

#### Scenario: Perfect alignment
- **WHEN** all cited evidence has `expected_direction` matching the prediction
- **THEN** `evidence_support` SHALL equal 1.0

#### Scenario: Mixed alignment
- **WHEN** 2 of 3 cited evidence items align with prediction, 1 does not
- **THEN** `evidence_support` SHALL equal 0.667

#### Scenario: Empty evidence
- **WHEN** `cited_evidence` is empty
- **THEN** `evidence_support` SHALL equal 0.0

### Requirement: System SHALL compute Confidence Drop and classify verdict
The system SHALL measure confidence change when cited evidence is removed, and classify the result.

#### Scenario: Likely faithful evidence
- **WHEN** `confidence_drop > 0.10`
- **THEN** `faithful_verdict` SHALL be "likely_faithful"

#### Scenario: Uncertain faithfulness
- **WHEN** `0.05 <= confidence_drop <= 0.10`
- **THEN** `faithful_verdict` SHALL be "uncertain"

#### Scenario: Possibly decorative evidence
- **WHEN** `confidence_drop < 0.05`
- **THEN** `faithful_verdict` SHALL be "possibly_decorative"

#### Scenario: No cited evidence
- **WHEN** cited_evidence is empty
- **THEN** `confidence_drop` SHALL be 0.0 and `faithful_verdict` SHALL be "possibly_decorative"

### Requirement: System SHALL output faithfulness results to CSV
The system SHALL write faithfulness evaluation results to `outputs/faithfulness_results.csv`.

#### Scenario: Output file schema
- **WHEN** the pipeline completes
- **THEN** `faithfulness_results.csv` SHALL contain columns: ticker, forecast_time, prediction, confidence_original, confidence_without_evidence, confidence_drop, temporal_validity, evidence_support, leakage_count, faithful_verdict

### Requirement: (Advanced B1) System SHALL compute Sufficiency and Counterfactual Perturbation
The system SHALL test whether cited evidence alone is sufficient to reproduce the prediction, and whether replacing evidence with neutral/counterfactual text changes the outcome.

#### Scenario: Sufficiency test
- **WHEN** only cited evidence (without other news) is used as input
- **THEN** the system SHALL output a sufficiency prediction and compare it against the original prediction

#### Scenario: Counterfactual perturbation
- **WHEN** cited evidence is replaced with neutral text (e.g., "Company holds annual meeting")
- **THEN** the system SHALL re-run prediction and report whether the outcome changes

### Requirement: (Advanced B2) System SHALL compute Counterevidence Coverage
The system SHALL identify both pro-evidence (supporting prediction) and counterevidence (opposing prediction) and compute coverage metrics.

#### Scenario: Pro and counter separation
- **WHEN** evidence is extracted for a prediction
- **THEN** the system SHALL separate evidence into `pro_evidence` (aligning with prediction) and `counter_evidence` (opposing prediction)

#### Scenario: Coverage metric
- **WHEN** counterevidence exists for a prediction
- **THEN** `counterevidence_coverage` SHALL equal `counter_count / total_evidence_count`

### Requirement: (Advanced B3) System SHALL compute Market Consistency
The system SHALL compare evidence polarity with actual market reaction (next-day return and volume change) to assess consistency.

#### Scenario: Consistent evidence
- **WHEN** negative evidence is cited AND `next_day_return < 0` AND volume increases
- **THEN** `market_consistency` SHALL be classified as "high"

#### Scenario: Inconsistent evidence
- **WHEN** negative evidence is cited BUT `next_day_return > 0`
- **THEN** `market_consistency` SHALL be classified as "low"
