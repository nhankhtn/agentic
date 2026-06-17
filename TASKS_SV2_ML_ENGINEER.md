# Sub-tasks — SV2 · ML/NLP Engineer

**Đồ án:** Faithful Evidence-Centric Financial News Forecasting  
**Vai trò:** Sinh viên 2 — ML/NLP Engineer  
**Tài liệu tham chiếu:** [REQUIREMENT.md](./REQUIREMENT.md), [tasks.md](./openspec/changes/faithful-evidence-forecasting/tasks.md), [design.md](./openspec/changes/faithful-evidence-forecasting/design.md)

---

## Bạn chịu trách nhiệm gì?

SV2 là **owner chính** của toàn bộ **pipeline ML/NLP** — từ dữ liệu đến prediction và faithfulness metrics. **Không bắt buộc train model** cho 7 điểm cơ bản; rule-based là đủ.

| Thuộc về bạn (owner) | Phối hợp với nhóm | Không phải việc chính của bạn |
|----------------------|-------------------|------------------------------|
| `data/sample_news_price.csv` | Review OpenSpec (SV1 viết) | `dashboard.py` (SV3) |
| `src/retriever.py` | Schema CSV (cùng SV1) | `test_*.py` (SV3 viết, bạn hỗ trợ chạy) |
| `src/evidence_extractor.py` | Bảng ví dụ extractor (cùng SV1) | OpenSpec proposal/spec (SV1) |
| `src/evidence_selector.py` | Demo video (bạn demo phần ML) | `run_log.json` chính (SV1) |
| `src/forecast_model.py` | Báo cáo phần 4–7 (cùng SV1) | Figures PNG (SV3 export) |
| `src/faithfulness_metrics.py` | E2E test (cùng SV3) | |
| `src/run_pipeline.py` | | |
| `requirements.txt` | | |
| `outputs/prediction_results.csv` | | |
| `outputs/faithfulness_results.csv` | | |

**Pipeline bạn phải làm chạy được:**

```
CSV → group (ticker, forecast_time)
  → Retriever → Extractor → Selector → Forecast Model → Faithfulness Metrics → outputs/
```

---

## Quy ước cập nhật

| Ký hiệu | Ý nghĩa |
|---------|---------|
| `[ ]` | Chưa làm |
| `[~]` | Đang làm |
| `[x]` | Xong |
| `🤖` | Có dùng AI agent — ghi vào `outputs/run_log.json` |
| `🔗` | Phụ thuộc task/người khác |

---

## Timeline gợi ý (SV2)

| Tuần | Phase | Focus chính của bạn |
|------|-------|---------------------|
| 1 | 0, 1 | Setup Python, `requirements.txt`, review design/schema |
| 2 | 2, 3 | Dataset + `retriever.py` |
| 3 | 4, 4.5, 5 | Extractor + Selector + Forecast Model |
| 4 | 6 | Faithfulness metrics + chạy full pipeline lần 1 |
| 5 | 8 | `run_pipeline.py` hoàn chỉnh, E2E với SV3 |
| 6 | 9 | Viết báo cáo phần 4–5, hỗ trợ demo |
| 7 | 11, 12 | (Tùy chọn) metric nâng cao, dữ liệu thật/GPU |

---

## PHASE 0 — Khởi động & Setup môi trường

**Mục tiêu:** Máy bạn chạy được Python project; hiểu pipeline end-to-end.

### Sub-tasks

- [ ] **S2-P0-01** Đọc `REQUIREMENT.md` + `design.md` — tóm tắt 1 trang luồng dữ liệu (để phản biện)
- [ ] **S2-P0-02** Hiểu 4 case đề bài: faithful evidence, decorative evidence, temporal leakage, counterevidence
- [ ] **S2-P0-03** 🤖 Tạo `requirements.txt` với: `pandas`, `numpy`, `scikit-learn`, `pytest`, `streamlit`, `plotly`
- [ ] **S2-P0-04** Cài môi trường: `python -m venv .venv && pip install -r requirements.txt`
- [ ] **S2-P0-05** Tạo file Python rỗng trong `src/`: `retriever.py`, `evidence_extractor.py`, `evidence_selector.py`, `forecast_model.py`, `faithfulness_metrics.py`, `run_pipeline.py`
- [ ] **S2-P0-06** Thống nhất với SV1/SV3: format datetime ISO 8601, naming convention biến/hàm

### Deliverables Phase 0

| File | Trạng thái |
|------|-----------|
| `requirements.txt` | `[ ]` |
| `src/*.py` (skeleton) | `[ ]` |

---

## PHASE 1 — Hỗ trợ OpenSpec (review, không viết chính)

**Mục tiêu:** Đảm bảo spec khớp code bạn sẽ viết.

🔗 Chờ SV1 draft `design.md` và `metric_definition.md`.

### Sub-tasks

- [ ] **S2-P1-01** 🔗 Review `design.md`: interface từng module (input/output) có implement được không?
- [ ] **S2-P1-02** 🔗 Review `specs/forecasting/spec.md`: acceptance criteria có test được bằng code không?
- [ ] **S2-P1-03** Góp ý schema CSV với SV1 (cột, kiểu, quy tắc group)
- [ ] **S2-P1-04** Xác nhận công thức 3 metric trong `metric_definition.md` trước khi code Phase 6

### Deliverables Phase 1

| Việc | Trạng thái |
|------|-----------|
| Comment review trên PR/issue hoặc ghi chú trong họp nhóm | `[ ]` |

---

## PHASE 2 — Chuẩn bị dữ liệu · **A2**

**Mục tiêu:** `data/sample_news_price.csv` ≥30 dòng, đủ edge case, group được theo `(ticker, forecast_time)`.

### Sub-tasks

#### 2.1 Thiết kế & tạo dataset

- [ ] **S2-P2-01** 🔗 Thống nhất schema CSV với SV1 (cột bắt buộc):

  | Cột | Kiểu | Ghi chú |
  |-----|------|---------|
  | `ticker` | string | AAPL, TSLA, NVDA, ... |
  | `forecast_time` | datetime | Thời điểm dự báo |
  | `news_id` | string | N001, N002, ... |
  | `news_time` | datetime | Thời điểm đăng tin |
  | `news_title` | string | |
  | `news_text` | string | |
  | `price_5d_return` | float | |
  | `volume_change` | float | |
  | `label` | string | UP / DOWN / HOLD |

- [ ] **S2-P2-02** 🤖 Viết ≥30 dòng tin mô phỏng (3 ticker, 3 nhãn, positive/negative/neutral)
- [ ] **S2-P2-03** Chèn **≥5 dòng leakage**: `news_time >= forecast_time` (để SV3 test retriever)
- [ ] **S2-P2-04** Tạo **≥3 group counterevidence**: cùng `(ticker, forecast_time)`, có tin tốt + tin xấu
- [ ] **S2-P2-05** Đảm bảo `label`, `price_*` nhất quán trong cùng group

#### 2.2 Tiền xử lý & thống kê

- [ ] **S2-P2-06** 🤖 Viết `src/data_utils.py` (hoặc script trong `run_pipeline.py`):
  - `load_csv()` — parse datetime
  - `group_by_forecast(df)` → list group dict
  - validate label ∈ {UP, DOWN, HOLD}
- [ ] **S2-P2-07** 🤖 Tạo bảng thống kê: số dòng, số group, phân bố label, số leakage rows
- [ ] **S2-P2-08** 🔗 Gửi dataset cho SV3 review edge case (P2-07 trong tasks.md)

#### 2.3 (Tùy chọn · C1) Dữ liệu thật

- [ ] **S2-P2-09** Script `scripts/fetch_real_data.py` — Yahoo Finance + news dataset
- [ ] **S2-P2-10** ≥300 mẫu, 3 ticker, label từ `return_next_day`
- [ ] **S2-P2-11** Ghi nguồn dữ liệu + bảng thống kê cho báo cáo

### Deliverables Phase 2

| File | Trạng thái |
|------|-----------|
| `data/sample_news_price.csv` | `[ ]` |
| `src/data_utils.py` (hoặc tương đương) | `[ ]` |
| Bảng thống kê dataset (markdown/csv) | `[ ]` |

### Tiêu chí hoàn thành (A2)

- [ ] ≥30 dòng CSV, ≥3 ticker, đủ UP/DOWN/HOLD
- [ ] ≥5 dòng temporal leakage
- [ ] Group `(ticker, forecast_time)` load được bằng code

---

## PHASE 3 — Temporal Retriever · **A3**

**Mục tiêu:** `src/retriever.py` — không dùng tin tương lai.

### Sub-tasks

- [ ] **S2-P3-01** 🤖 Implement `filter_news_by_time(news_list, forecast_time)`:
  - `valid_news`: `news_time < forecast_time`
  - `invalid_future_news`: `news_time >= forecast_time`
  - return thêm `leakage_count`
- [ ] **S2-P3-02** Log WARNING khi có leakage: `[WARNING] Temporal leakage detected: news_id=..., news_time=... > forecast_time=...`
- [ ] **S2-P3-03** 🤖 Docstring + type hints đầy đủ
- [ ] **S2-P3-04** Chạy retriever trên toàn dataset, xác nhận 5+ tin vào `invalid_future_news`
- [ ] **S2-P3-05** 🔗 Bàn giao interface cho SV3 viết `tests/test_temporal_retriever.py` (6 TC)
- [ ] **S2-P3-06** Chạy `pytest tests/test_temporal_retriever.py -v` — fix nếu fail

### Deliverables Phase 3

| File | Trạng thái |
|------|-----------|
| `src/retriever.py` | `[ ]` |

### Tiêu chí hoàn thành (A3)

- [ ] Hàm filter đúng logic `>=` bị loại
- [ ] Có log cảnh báo + `leakage_count`
- [ ] Test retriever pass (phối hợp SV3)

---

## PHASE 4 — Evidence Extraction · **A4**

**Mục tiêu:** Trích evidence từ text tin tức (rule-based keyword).

### Sub-tasks

- [ ] **S2-P4-01** 🤖 Định nghĩa từ điển keyword:
  - Negative → DOWN: `miss, weak, decline, drop, loss, recall, layoff, ...`
  - Positive → UP: `beat, strong, growth, launch, surge, profit, ...`
  - Neutral → HOLD: `meeting, announce, report, hold, ...`
- [ ] **S2-P4-02** 🤖 Implement `extract_evidence(news_item) -> list[dict]`:

  ```python
  {
    "news_id": "...",
    "news_time": "...",
    "evidence_text": "...",
    "polarity": "negative",
    "expected_direction": "DOWN",
    "confidence": 0.85
  }
  ```

- [ ] **S2-P4-03** Edge cases:
  - Text < 10 từ → neutral + warning log
  - Không có keyword → neutral, HOLD
  - Cả positive và negative → trả về cả hai evidence
- [ ] **S2-P4-04** Chạy trên toàn dataset — **coverage ≥80%** tin có ≥1 evidence
- [ ] **S2-P4-05** 🔗 Cùng SV1: bảng 5 ví dụ đúng + 5 ví dụ sai/biên (cho báo cáo)
- [ ] **S2-P4-06** 🤖 Docstring + type hints

### Deliverables Phase 4

| File | Trạng thái |
|------|-----------|
| `src/evidence_extractor.py` | `[ ]` |
| Bảng 10 ví dụ extractor | `[ ]` |

---

## PHASE 4.5 — Evidence Selector · **A4 / nền B2**

**Mục tiêu:** Tách pro/counter evidence, chọn cited evidence trước khi predict.

### Sub-tasks

- [ ] **S2-P4.5-01** 🤖 Implement `select_evidence(all_evidence, dominant_direction=None)`:
  - `pro_evidence` — align hướng dominant
  - `counter_evidence` — ngược hướng
  - `cited_evidence` — top-k theo `confidence` (≥1 nếu có pro)
- [ ] **S2-P4.5-02** Loại trùng: cùng `news_id` hoặc `evidence_text` giống hệt
- [ ] **S2-P4.5-03** Test thủ công 3 group counterevidence trong dataset — pro và counter không rỗng
- [ ] **S2-P4.5-04** 🤖 Docstring + type hints

### Deliverables Phase 4.5

| File | Trạng thái |
|------|-----------|
| `src/evidence_selector.py` | `[ ]` |

---

## PHASE 5 — Forecast Model · **A5**

**Mục tiêu:** Dự báo UP/DOWN/HOLD + confidence + rationale. **Rule-based, không train.**

### Sub-tasks

- [ ] **S2-P5-01** 🤖 Implement `predict(ticker, forecast_time, valid_news, price_features, cited_evidence=None)`:

  **Rule-based (đủ điểm A5):**
  ```
  positive_count, negative_count từ evidence (bỏ neutral)
  price_signal = sign(price_5d_return)
  score = (positive_count - negative_count) + 0.5 * price_signal

  score > 0  → UP,   confidence = positive / (positive + negative)
  score < 0  → DOWN, confidence = negative / (positive + negative)
  score = 0  → HOLD, confidence = 0.5
  ```

- [ ] **S2-P5-02** Trả về `cited_evidence` + `rationale` (câu tiếng Việt/Anh mô tả lý do)
- [ ] **S2-P5-03** Fallback khi không có tin / tất cả bị leakage → HOLD, confidence thấp, rationale rõ
- [ ] **S2-P5-04** Chạy predict trên mọi group → lưu `outputs/prediction_results.csv`
- [ ] **S2-P5-05** 🤖 Tính accuracy + confusion matrix (`sklearn.metrics`)
- [ ] **S2-P5-06** 🔗 Cùng SV1: viết giải thích chi tiết **1 prediction** (case study cho báo cáo)
- [ ] **S2-P5-07** 🤖 Docstring + type hints

### Deliverables Phase 5

| File | Trạng thái |
|------|-----------|
| `src/forecast_model.py` | `[ ]` |
| `outputs/prediction_results.csv` | `[ ]` |
| Accuracy + confusion matrix (markdown hoặc notebook) | `[ ]` |

### Tiêu chí hoàn thành (A5)

- [ ] Predict được UP/DOWN/HOLD cho mọi group
- [ ] Có confidence + ít nhất 1 cited evidence (khi có tin hợp lệ)
- [ ] Có 1 case giải thích rõ trong báo cáo

---

## PHASE 6 — Faithfulness Metrics · **A6**

**Mục tiêu:** Chứng minh evidence có faithful hay không — **cốt lõi đồ án**.

### Sub-tasks

#### 6.1 Ba metric cơ bản

- [ ] **S2-P6-01** 🤖 `temporal_validity(cited_evidence, forecast_time)` → float [0, 1]
- [ ] **S2-P6-02** 🤖 `evidence_support(cited_evidence, prediction)` → float [0, 1]
- [ ] **S2-P6-03** `confidence_drop(...)`:
  1. Chạy model full input → `confidence_original`
  2. Bỏ cited evidence → chạy lại → `confidence_without`
  3. `confidence_drop = original - without`
  4. Cũng tính `confidence_drop_random` (bỏ 1 tin không cite)
- [ ] **S2-P6-04** Verdict: `likely_faithful` (drop > 0.1), `possibly_decorative` (drop < 0.05)
- [ ] **S2-P6-05** Chạy trên mọi group → `outputs/faithfulness_results.csv`
- [ ] **S2-P6-06** 🔗 Cùng SV1: bảng mean 3 metric trên toàn dataset
- [ ] **S2-P6-07** 🔗 Bàn giao interface cho SV3: `test_metrics.py` (5 TC)
- [ ] **S2-P6-08** 🤖 Docstring + type hints

#### 6.2 Chuẩn bị cho dashboard (SV3 dùng)

- [ ] **S2-P6-09** Export format CSV đủ cột cho dashboard Tab 3
- [ ] **S2-P6-10** Document cách gọi `confidence_drop` từ dashboard (re-run tại runtime)

### Deliverables Phase 6

| File | Trạng thái |
|------|-----------|
| `src/faithfulness_metrics.py` | `[ ]` |
| `outputs/faithfulness_results.csv` | `[ ]` |

### Tiêu chí hoàn thành (A6)

- [ ] 3 metric tính được cho mọi prediction có cited evidence
- [ ] Có so sánh cited vs random confidence drop
- [ ] Test metrics pass (phối hợp SV3)

---

## PHASE 7 — Hỗ trợ Dashboard (SV3 owner)

**Bạn không viết dashboard chính**, nhưng phải hỗ trợ SV3 tích hợp.

### Sub-tasks

- [ ] **S2-P7-01** 🔗 Cung cấp API ổn định: `run_single_forecast(group)` trả đủ fields cho dashboard
- [ ] **S2-P7-02** 🔗 Hỗ trợ SV3 implement "Remove cited evidence" — gọi lại `predict()` + `confidence_drop()`
- [ ] **S2-P7-03** Test dashboard trên máy bạn: `streamlit run src/dashboard.py`
- [ ] **S2-P7-04** Chuẩn bị **2 case demo** (1 faithful, 1 decorative) để thuyết trình

---

## PHASE 8 — Pipeline E2E & QA

**Mục tiêu:** `run_pipeline.py` chạy một lệnh, ra đủ output.

### Sub-tasks

- [ ] **S2-P8-01** 🤖 Viết `src/run_pipeline.py`:

  ```bash
  python src/run_pipeline.py --input data/sample_news_price.csv
  ```

  Luồng: load → group → retriever → extractor → selector → model → metrics → ghi CSV

- [ ] **S2-P8-02** 🔗 Cùng SV3: chạy E2E, không runtime error
- [ ] **S2-P8-03** Xử lý edge cases trong pipeline:
  - Group không có tin → HOLD
  - Tất cả tin leakage → HOLD + cảnh báo
  - Không có cited evidence → confidence_drop = 0
- [ ] **S2-P8-04** Chạy `pytest tests/ -v` — fix bug phía ML modules
- [ ] **S2-P8-05** Ghi `outputs/commit_log.md` hoặc link PR cho code bạn viết (B4)

### Deliverables Phase 8

| File | Trạng thái |
|------|-----------|
| `src/run_pipeline.py` | `[ ]` |
| Pipeline chạy E2E không lỗi | `[ ]` |

---

## PHASE 9 — Báo cáo & Demo

### Sub-tasks (phần bạn viết)

- [ ] **S2-P9-01** Viết báo cáo **phần 4 — Dữ liệu**: schema, thống kê, cách tạo label, group logic
- [ ] **S2-P9-02** Viết báo cáo **phần 5 — Pipeline kỹ thuật**: mô tả 5 module ML (không paste code dài)
- [ ] **S2-P9-03** 🔗 Cùng SV1: **phần 6–7** — metric + kết quả thực nghiệm (bảng, số liệu thật từ `outputs/`)
- [ ] **S2-P9-04** Tham gia demo ~5 phút: giải thích pipeline + thao tác "Remove cited evidence"
- [ ] **S2-P9-05** Review báo cáo lần 1 — góp ý kỹ thuật

### Deliverables Phase 9

| Việc | Trạng thái |
|------|-----------|
| Báo cáo phần 4–5 (draft) | `[ ]` |
| Tham gia demo video | `[ ]` |

---

## PHASE 10 — Agentic SDLC (phối hợp SV1)

Ghi log mỗi lần dùng Cursor/ChatGPT cho task ML:

- [ ] **S2-P10-01** ≥2 entry trong `outputs/run_log.json` với `agent_role: "Coding Agent"`
- [ ] **S2-P10-02** Mỗi entry ghi: task_id (S2-P*), human_review, quality_gate

**Task nên ghi log:** P2-02, P3-01, P4-02, P5-01, P6-03, P8-01

---

## PHASE 11 — Advanced Metrics (tùy chọn · B1–B3)

Chỉ làm sau khi Phase 6 xong và nhóm quyết định nhắm điểm nâng cao.

- [ ] **S2-P11-01** (B1) `sufficiency_test()` — chỉ cited evidence → predict lại
- [ ] **S2-P11-02** (B1) `counterfactual_perturbation()` — thay evidence bằng tin neutral
- [ ] **S2-P11-03** (B2) `counterevidence_coverage()` — dùng output từ selector
- [ ] **S2-P11-04** (B3) `market_consistency()` — so evidence vs label/return thực tế
- [ ] **S2-P11-05** (B3) Phân tích theo regime bull/bear/sideway
- [ ] **S2-P11-06** Bổ sung cột vào `faithfulness_results.csv`

---

## PHASE 12 — Dữ liệu thật & GPU (tùy chọn · C1–C2)

- [ ] **S2-P12-01** (C1) Thu thập ≥300 mẫu, 3 ticker — xem S2-P2-09
- [ ] **S2-P12-02** (C2) FinBERT sentiment hoặc LSTM — **chỉ nếu muốn +1 điểm cộng**
- [ ] **S2-P12-03** (C2) Bảng so sánh rule-based vs model GPU (accuracy, avg confidence drop, thời gian chạy)

---

## Checklist tổng — SV2 trước khi nộp

### Code (bắt buộc)

- [ ] `requirements.txt`
- [ ] `data/sample_news_price.csv` (≥30 dòng)
- [ ] `src/retriever.py`
- [ ] `src/evidence_extractor.py`
- [ ] `src/evidence_selector.py`
- [ ] `src/forecast_model.py`
- [ ] `src/faithfulness_metrics.py`
- [ ] `src/run_pipeline.py`
- [ ] `outputs/prediction_results.csv`
- [ ] `outputs/faithfulness_results.csv`

### Chất lượng

- [ ] `python src/run_pipeline.py` chạy không lỗi
- [ ] `pytest tests/ -v` pass
- [ ] Không có tin tương lai trong input model (chỉ `valid_news`)
- [ ] Hiểu giải thích được mọi module khi bị phản biện

### Phối hợp nhóm

- [ ] SV3 có đủ CSV + API để làm dashboard
- [ ] SV1 có số liệu thật cho báo cáo phần 6–7
- [ ] Đã tham gia demo video

---

## Ghi chú nhanh khi bí

| Câu hỏi | Trả lời |
|---------|---------|
| Có cần train model? | **Không** (7 điểm cơ bản). Rule-based đủ. |
| Làm module nào trước? | Dataset → Retriever → Extractor → Selector → Model → Metrics → Pipeline |
| Metric quan trọng nhất? | **Confidence Drop** — bỏ cited evidence, confidence có giảm không? |
| File nào SV3 cần từ bạn? | `prediction_results.csv`, `faithfulness_results.csv`, hàm re-run predict |

---

*Cập nhật trạng thái `[ ]` → `[~]` → `[x]` sau mỗi buổi làm việc. File này là sub-task cá nhân SV2; task nhóm đầy đủ nằm trong `openspec/changes/faithful-evidence-forecasting/tasks.md`.*
