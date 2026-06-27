# Purpose
Provide an interactive dashboard for users to analyze stock movement predictions, evidence used, faithfulness metrics, and temporal leakage monitoring.

## Input / Output

**Input:**
- `outputs/prediction_results.csv`: Predictions with columns (ticker, forecast_time, prediction, confidence, label, correct)
- `outputs/faithfulness_results.csv`: Faithfulness metrics per prediction
- `outputs/metrics_summary.json`: Aggregated summary metrics

**Output:**
- Streamlit web app with 4 interactive tabs
- 4 static PNG figures exported to `outputs/figures/`
- Visual warnings (⚠️) for temporal leakage and low faithfulness

## Requirements

### Requirement: Dashboard SHALL provide Prediction Overview tab
The dashboard SHALL display an overview of all predictions with summary metrics and filtering capability.

#### Scenario: Prediction table display
- **WHEN** the user opens Tab 1 (Prediction Overview)
- **THEN** a table SHALL show all predictions with columns: ticker, forecast_time, prediction, confidence, label, correct

#### Scenario: Metric cards
- **WHEN** the user opens Tab 1
- **THEN** the dashboard SHALL display metric cards for: Accuracy, Average Confidence, Average Confidence Drop, Leakage count

#### Scenario: Distribution chart
- **WHEN** the user opens Tab 1
- **THEN** a bar chart SHALL show the distribution of UP/DOWN/HOLD predictions

### Requirement: Dashboard SHALL provide Evidence Explorer tab
The dashboard SHALL allow users to inspect evidence for individual predictions.

#### Scenario: Prediction selection
- **WHEN** the user selects a specific prediction from a dropdown in Tab 2
- **THEN** the dashboard SHALL display: ticker, forecast_time, prediction (color-coded), confidence, and a table of cited evidence

#### Scenario: Temporal leakage warning
- **WHEN** a selected prediction has evidence with `news_time >= forecast_time`
- **THEN** a red warning banner (⚠️) SHALL be displayed

### Requirement: Dashboard SHALL provide Faithfulness Analysis tab
The dashboard SHALL visualize faithfulness metrics for all predictions.

#### Scenario: Confidence drop chart
- **WHEN** the user opens Tab 3 (Faithfulness Analysis)
- **THEN** a bar chart SHALL show confidence drop for each prediction

#### Scenario: Verdict table
- **WHEN** the user opens Tab 3
- **THEN** a table SHALL show confidence_original vs confidence_without_evidence with a verdict column

#### Scenario: Faithfulness radar chart
- **WHEN** the user opens Tab 3
- **THEN** a radar chart SHALL display multi-dimensional faithfulness metrics (temporal_validity, evidence_support, confidence_drop) for the selected prediction or overall averages

### Requirement: Dashboard SHALL provide Temporal Leakage Monitor tab
The dashboard SHALL display all news articles that were filtered due to temporal leakage.

#### Scenario: Leakage table
- **WHEN** the user opens Tab 4 (Temporal Leakage Monitor)
- **THEN** a table SHALL list all filtered articles with: news_id, ticker, news_time, forecast_time, time delta

#### Scenario: Leakage rate warning
- **WHEN** `leakage_rate > 0`
- **THEN** a ⚠️ warning banner SHALL be displayed

#### Scenario: No leakage confirmation
- **WHEN** `leakage_rate = 0`
- **THEN** a ✅ confirmation message SHALL be displayed

### Requirement: Dashboard SHALL launch without errors
The dashboard SHALL be runnable with `streamlit run src/dashboard.py` without import or runtime errors.

#### Scenario: Successful launch
- **WHEN** the user runs `streamlit run src/dashboard.py`
- **THEN** the application SHALL start and display all 4 tabs without errors
