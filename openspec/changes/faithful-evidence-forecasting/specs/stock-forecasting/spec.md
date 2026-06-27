## ADDED Input / Output

**Input:**
- `evidence_list`: List of evidence dicts (from evidence extractor), each with `polarity`, `expected_direction`
- `price_features`: dict containing `price_5d_return` (float)
- `ticker`: str — stock ticker symbol
- `forecast_time`: datetime str — the forecast timestamp

**Output:**
- `prediction`: "UP" | "DOWN" | "HOLD"
- `confidence`: float in [0.0, 1.0]
- `cited_evidence`: list of evidence items supporting the prediction
- `rationale`: str — human-readable explanation of the reasoning
- `confidence_drop`: float — confidence difference when cited evidence is removed

## ADDED Requirements

### Requirement: System SHALL predict stock movement direction
The system SHALL output a prediction of UP, DOWN, or HOLD based on aggregated evidence and price features, along with a confidence score.

#### Scenario: Majority positive evidence
- **WHEN** there are more positive evidence items than negative ones
- **THEN** `prediction` SHALL be "UP"

#### Scenario: Majority negative evidence
- **WHEN** there are more negative evidence items than positive ones
- **THEN** `prediction` SHALL be "DOWN"

#### Scenario: Tie between positive and negative
- **WHEN** positive and negative evidence counts are equal
- **THEN** `prediction` SHALL be "HOLD" and `confidence` SHALL be 0.5

#### Scenario: Price signal integration
- **WHEN** `price_5d_return > 0`
- **THEN** the system SHALL add +0.5 to the positive count before computing the final score

#### Scenario: Negative price signal integration
- **WHEN** `price_5d_return < 0`
- **THEN** the system SHALL add +0.5 to the negative count before computing the final score

### Requirement: System SHALL provide confidence scores within valid range
The confidence score SHALL always be a float in the range [0.0, 1.0].

#### Scenario: Confidence bounds
- **WHEN** a prediction is made for any input
- **THEN** `confidence` SHALL satisfy `0.0 <= confidence <= 1.0`

### Requirement: System SHALL cite evidence used for prediction
The system SHALL output a list of cited evidence items that align with the prediction direction.

#### Scenario: Cited evidence alignment
- **WHEN** `prediction = "UP"`
- **THEN** `cited_evidence` SHALL contain only evidence items with `expected_direction = "UP"`

#### Scenario: Rationale generation
- **WHEN** a prediction is made
- **THEN** `rationale` SHALL be a non-empty string describing the reasoning behind the prediction

### Requirement: System SHALL support confidence drop computation
The system SHALL compute confidence drop by removing cited evidence and re-running the model.

#### Scenario: Confidence drop calculation
- **WHEN** cited evidence is removed from the input and the model re-runs
- **THEN** `confidence_drop` SHALL equal `confidence_original - confidence_without_cited`

### Requirement: System SHALL report prediction accuracy metrics
The system SHALL compute and output overall accuracy and a confusion matrix comparing predictions against actual labels.

#### Scenario: Accuracy computation
- **WHEN** predictions for all forecast groups are compared against actual labels
- **THEN** the system SHALL output `overall_accuracy` as a float in [0.0, 1.0]

#### Scenario: Confusion matrix output
- **WHEN** predictions are evaluated
- **THEN** a 3×3 confusion matrix (UP/DOWN/HOLD) SHALL be generated and saved to `outputs/prediction_results.csv` or displayed in the report
