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
