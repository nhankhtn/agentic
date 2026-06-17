.PHONY: help setup install data pipeline run test figures dashboard check clean all

PYTHON   ?= python3
VENV     := .venv
BIN      := $(VENV)/bin
PY       := $(BIN)/python
PIP      := $(BIN)/pip
PYTEST   := $(BIN)/pytest

INPUT    ?= data/sample_news_price.csv
OUTPUT   ?= outputs

help: ## Hiển thị danh sách lệnh
	@echo "Faithful Evidence Forecasting — Makefile"
	@echo ""
	@grep -E '^[a-zA-Z0-9_.-]+:.*##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Ví dụ nhanh:"
	@echo "  make setup && make all && make check"

setup: $(VENV)/bin/activate ## Tạo venv + cài dependencies
	$(PIP) install -r requirements.txt
	@echo "✓ Setup xong. Chạy: source $(VENV)/bin/activate"

install: setup ## Alias của setup

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)

data: setup ## Sinh dataset mẫu (data/sample_news_price.csv)
	$(PY) scripts/generate_sample_data.py

pipeline: setup ## Chạy pipeline end-to-end
	$(PY) src/run_pipeline.py --input $(INPUT) --output-dir $(OUTPUT)

run: pipeline ## Alias của pipeline

test: setup ## Chạy pytest
	$(PYTEST) tests/ -v

figures: pipeline ## Export biểu đồ PNG vào outputs/figures/
	$(PY) scripts/export_figures.py

dashboard: setup ## Mở Streamlit dashboard
	$(BIN)/streamlit run src/dashboard.py

check: ## In tóm tắt kết quả từ outputs/
	@$(PY) -c "\
import json, sys; \
from pathlib import Path; \
out = Path('$(OUTPUT)'); \
required = ['prediction_results.csv', 'faithfulness_results.csv', 'metrics_summary.json', 'dataset_stats.json']; \
missing = [f for f in required if not (out / f).exists()]; \
print('=== Kiểm tra output files ==='); \
[print(f'  [OK]  {f}') for f in required if (out / f).exists()]; \
[print(f'  [MISSING] {f}') for f in missing]; \
sys.exit(1 if missing else 0); \
" && $(PY) -c "\
import json; \
from pathlib import Path; \
import pandas as pd; \
out = Path('$(OUTPUT)'); \
m = json.loads((out / 'metrics_summary.json').read_text()); \
pred = pd.read_csv(out / 'prediction_results.csv'); \
faith = pd.read_csv(out / 'faithfulness_results.csv'); \
stats = json.loads((out / 'dataset_stats.json').read_text()); \
print(); \
print('=== Dataset ==='); \
print(f'  Rows CSV      : {stats[\"total_rows\"]}'); \
print(f'  Forecast groups: {stats[\"forecast_groups\"]}'); \
print(f'  Tickers       : {\", \".join(stats[\"tickers\"])}'); \
print(f'  Leakage rows  : {stats[\"temporal_leakage_rows\"]}'); \
print(); \
print('=== Predictions ==='); \
print(f'  Groups        : {len(pred)}'); \
print(f'  Accuracy      : {m[\"accuracy\"]:.1%}'); \
print(f'  Correct       : {pred[\"correct\"].sum()}/{len(pred)}'); \
print(f'  Distribution  : {dict(pred[\"prediction\"].value_counts().astype(int))}'); \
print(); \
print('=== Faithfulness (mean) ==='); \
print(f'  Confidence drop : {m[\"mean_confidence_drop\"]:.4f}'); \
print(f'  Temporal valid. : {m[\"mean_temporal_validity\"]:.4f}'); \
print(f'  Evidence support: {m[\"mean_evidence_support\"]:.4f}'); \
print(); \
print('=== Verdicts ==='); \
print(f'  {dict(faith[\"faithful_verdict\"].value_counts().astype(int))}'); \
print(); \
print('=== Confusion matrix (UP/DOWN/HOLD) ==='); \
labels = m['confusion_matrix_labels']; \
cm = m['confusion_matrix']; \
print('       pred ' + '  '.join(f'{l:>5}' for l in labels)); \
[print(f'  true {labels[i]:>4}  ' + '  '.join(f'{v:>5}' for v in row)) for i, row in enumerate(cm)]; \
print(); \
print('Xem chi tiết:'); \
print(f'  cat $(OUTPUT)/prediction_results.csv'); \
print(f'  cat $(OUTPUT)/faithfulness_results.csv'); \
"

all: data pipeline test figures check ## Setup + data + pipeline + test + figures + check

clean: ## Xóa venv, cache, outputs (giữ data/)
	rm -rf $(VENV) .pytest_cache
	rm -rf $(OUTPUT)/prediction_results.csv $(OUTPUT)/faithfulness_results.csv
	rm -rf $(OUTPUT)/metrics_summary.json $(OUTPUT)/dataset_stats.json
	rm -rf $(OUTPUT)/figures/*.png
