# Purpose
Extract key evidence phrases from news articles and classify their sentiment polarity and expected stock direction.

## Input / Output

**Input:**
- `news_text`: str — full text content of a news article
- `news_id`: str — unique identifier for the article

**Output:**
- List of evidence dicts, each containing:
  - `evidence_text` (str): the extracted phrase
  - `polarity` ("positive" | "negative" | "neutral")
  - `expected_direction` ("UP" | "DOWN" | "HOLD")
  - `confidence` (float): extraction confidence score

## Requirements

### Requirement: System SHALL extract evidence from news text
The system SHALL extract key evidence phrases from each valid news article and classify their sentiment polarity and expected stock direction.

#### Scenario: Negative keyword detection
- **WHEN** a news article contains keywords such as "miss", "weak", "decline", "drop", "loss", "recall", "layoff"
- **THEN** the system SHALL assign `polarity = "negative"` and `expected_direction = "DOWN"`

#### Scenario: Positive keyword detection
- **WHEN** a news article contains keywords such as "beat", "strong", "growth", "launch", "surge", "profit", "record"
- **THEN** the system SHALL assign `polarity = "positive"` and `expected_direction = "UP"`

#### Scenario: Neutral or ambiguous text
- **WHEN** a news article has equal positive and negative keywords, or no relevant keywords
- **THEN** the system SHALL assign `polarity = "neutral"` and `expected_direction = "HOLD"`

#### Scenario: Very short news text
- **WHEN** a news article text is shorter than 5 words
- **THEN** the system SHALL return an empty evidence list `[]` for that article

### Requirement: System SHALL provide structured evidence output
Each extracted evidence item SHALL contain all required fields for downstream processing.

#### Scenario: Complete evidence fields
- **WHEN** evidence is successfully extracted from a news article
- **THEN** the output SHALL contain: `evidence_text` (string), `polarity` ("positive" | "negative" | "neutral"), `expected_direction` ("UP" | "DOWN" | "HOLD"), and `confidence` (float)

### Requirement: System SHALL achieve minimum extraction coverage
The evidence extractor SHALL extract at least one evidence item from a minimum percentage of valid news articles.

#### Scenario: Coverage threshold
- **WHEN** the extractor runs on the entire `data/sample_news_price.csv` dataset
- **THEN** at least 80% of valid news articles SHALL produce at least 1 evidence item

### Requirement: System SHALL provide validation examples
The evidence extractor SHALL be validated with concrete correct and incorrect extraction examples.

#### Scenario: Minimum validation examples
- **WHEN** the evidence extractor is tested
- **THEN** at least 5 examples SHALL be documented showing correct extractions (keyword → polarity → direction) and incorrect/edge-case extractions
