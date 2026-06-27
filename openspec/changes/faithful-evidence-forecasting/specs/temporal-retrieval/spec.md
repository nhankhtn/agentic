## ADDED Input / Output

**Input:**
- `news_list`: List of news article dicts, each containing `news_id` (str), `news_time` (datetime str), `news_text` (str), `ticker` (str)
- `forecast_time`: datetime string (e.g., `"2025-03-12 09:00"`) — the cutoff timestamp

**Output:**
- `valid_news[]`: List of news articles with `news_time < forecast_time`
- `invalid_future_news[]`: List of filtered articles with `news_time >= forecast_time`
- `leakage_count`: int — total number of filtered future articles

## ADDED Requirements

### Requirement: System SHALL filter news by temporal validity
The system SHALL exclude any news article with `news_time >= forecast_time` from the prediction pipeline. Only news published strictly before the forecast timestamp SHALL be used as input.

#### Scenario: Valid news passes through
- **WHEN** a news article has `news_time = "2025-03-11 08:30"` and `forecast_time = "2025-03-12 09:00"`
- **THEN** the article SHALL be included in `valid_news[]`

#### Scenario: Future news is filtered out
- **WHEN** a news article has `news_time = "2025-03-12 15:30"` and `forecast_time = "2025-03-12 09:00"`
- **THEN** the article SHALL be added to `invalid_future_news[]` and SHALL NOT be used for prediction

#### Scenario: Boundary time is treated as future
- **WHEN** a news article has `news_time == forecast_time` (exact match)
- **THEN** the article SHALL be treated as future information and excluded

#### Scenario: Leakage warning is logged
- **WHEN** a news article is excluded due to temporal leakage
- **THEN** the system SHALL log: `[WARNING] Temporal leakage: news_id={id}, news_time={t} >= forecast_time={ft}`

### Requirement: System SHALL count leaked articles
The system SHALL return an accurate `leakage_count` representing the total number of filtered future news articles for each forecast group.

#### Scenario: Accurate leakage count
- **WHEN** 3 out of 5 news articles have `news_time >= forecast_time`
- **THEN** `leakage_count` SHALL equal 3

### Requirement: System SHALL handle empty valid news gracefully
The system SHALL not crash when all news articles are filtered out. It SHALL proceed with a fallback prediction.

#### Scenario: All news filtered
- **WHEN** every news article for a ticker/forecast_time group has `news_time >= forecast_time`
- **THEN** `valid_news[]` SHALL be empty, and the pipeline SHALL produce `prediction = "HOLD"` with `confidence = 0.5`

#### Scenario: No news at all
- **WHEN** there are zero news articles for a ticker/forecast_time group
- **THEN** the system SHALL not crash and SHALL produce `prediction = "HOLD"` with `confidence = 0.5`
