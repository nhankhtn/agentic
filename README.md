# Faithful Evidence-Centric Financial News Forecasting

Prototype pipeline for stock movement forecasting from financial news with **evidence faithfulness** checks.

## Quick start (Makefile)

```bash
cd agentic

# First time: setup + run all + check results
make setup
make all
make check

# Or step by step
make data       # generate sample dataset
make pipeline   # run pipeline → outputs/
make test       # pytest
make figures    # export PNG to outputs/figures/
make dashboard  # open Streamlit UI
```

View all commands: `make help`

### Check results

After `make pipeline`, quick check:

```bash
make check
```

Or view files directly:

```bash
cat outputs/metrics_summary.json          # accuracy, confusion matrix, mean metrics
head outputs/prediction_results.csv       # predictions per group
head outputs/faithfulness_results.csv     # faithfulness metrics
cat outputs/dataset_stats.json            # dataset statistics
ls outputs/figures/                       # exported PNG charts
```

### Quick start (manual)

```bash
cd agentic
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_sample_data.py
python src/run_pipeline.py
pytest tests/ -v
streamlit run src/dashboard.py
```

## Pipeline

```
CSV → group (ticker, forecast_time)
  → Temporal Retriever → Evidence Extractor → Evidence Selector
  → Forecast Model → Faithfulness Metrics → outputs/
```

## Project structure

```
agentic/
├── data/sample_news_price.csv
├── src/
│   ├── data_utils.py
│   ├── retriever.py
│   ├── evidence_extractor.py
│   ├── evidence_selector.py
│   ├── forecast_model.py
│   ├── faithfulness_metrics.py
│   ├── run_pipeline.py
│   └── dashboard.py
├── tests/
├── outputs/
│   ├── prediction_results.csv
│   ├── faithfulness_results.csv
│   └── metrics_summary.json
└── openspec/
```

## Team roles

| Member | Role |
|--------|------|
| SV1 | Research & Spec Owner |
| SV2 | ML/NLP Engineer |
| SV3 | Visualization & QA |

## Outputs

- `outputs/prediction_results.csv` — predictions per forecast group
- `outputs/faithfulness_results.csv` — temporal validity, evidence support, confidence drop
- `outputs/metrics_summary.json` — accuracy, confusion matrix, mean metrics

## Notes

- Baseline model is **rule-based** (no GPU / training required for core deliverables).
- Temporal leakage: news with `news_time >= forecast_time` is excluded.
- Faithfulness: high `confidence_drop` after removing cited evidence suggests faithful explanations.
