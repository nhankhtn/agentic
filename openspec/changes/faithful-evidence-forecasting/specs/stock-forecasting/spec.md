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
