# Requirement.md — Đồ án Cuối kì
## Faithful Evidence-Centric Financial News Forecasting
### Môn: Công nghệ mới | Nhóm: 3 sinh viên | Tổng điểm: 10 + 2 điểm cộng

---

## Tổng quan các Phase

| Phase | Tên | Mục tiêu chính | Điểm liên quan |
|-------|-----|----------------|----------------|
| 0 | Khởi động & Lập kế hoạch | Hiểu bài toán, phân công, setup môi trường | A1 |
| 1 | OpenSpec & Đặc tả yêu cầu | Viết proposal, spec, design, tasks, metric definition | A1, B4 |
| 2 | Chuẩn bị dữ liệu | Tạo/thu thập dataset, group, tiền xử lý | A2, C1 |
| 3 | Temporal Retriever | Module lọc tin theo thời gian | A3 |
| 4 | Evidence Extraction | Module trích xuất bằng chứng từ tin tức | A4 |
| 4.5 | Evidence Selector | Chọn pro/counter evidence trước khi dự báo | A4, B2 |
| 5 | Forecast Model | Mô hình dự báo UP/DOWN/HOLD | A5 |
| 6 | Faithfulness Metrics | 3 metric cơ bản: Support, Validity, Confidence Drop | A6 |
| 7 | Visualization Dashboard | Dashboard, biểu đồ, cảnh báo, re-run model | A7 |
| 8 | Testing & QA | Test case, pipeline E2E, test report | A3, A6 |
| 9 | Báo cáo & Demo | Viết báo cáo, quay demo, nộp bài | A7, B4 |
| 10 (nâng cao) | Agentic SDLC Maturity | Agent roles, trace log, quality gate, commit log | B4 |
| 11 (nâng cao) | Advanced Metrics | Sufficiency, counterfactual, counterevidence, market consistency | B1, B2, B3 |
| 12 (điểm cộng) | Dữ liệu thật & GPU | Real data, FinBERT/LSTM | C1, C2 |

**Pipeline chuẩn (khớp đề bài):**
```
News + Price → Temporal Retriever → Evidence Extractor → Evidence Selector
  → Forecast Model → Faithfulness Evaluator → Dashboard
```

---

## Phase 0 — Khởi động & Lập kế hoạch

### Mục tiêu
Đảm bảo cả nhóm hiểu rõ bài toán, phân công hợp lý và có môi trường làm việc thống nhất trước khi bắt tay vào code.

### Công việc cần làm

#### 0.1 Đọc hiểu đề bài
- Đọc toàn bộ file đề bài.
- Hiểu rõ khái niệm **faithfulness**: evidence mà mô hình cite ra có thật sự ảnh hưởng đến prediction không.
- Hiểu 4 ví dụ trong đề: evidence faithful, evidence trang trí, temporal leakage, counterevidence.
- Cả 3 thành viên đều phải hiểu luồng dữ liệu end-to-end.

#### 0.2 Phân công nhóm

| Vai trò | Nhiệm vụ chính |
|---------|----------------|
| **SV1 — Research & Spec Owner** | Viết OpenSpec, user stories, metric definition, báo cáo phần 1–3 |
| **SV2 — ML/NLP Engineer** | Tạo dataset, retriever, extractor, selector, forecast model, pipeline, thí nghiệm |
| **SV3 — Visualization & QA** | Dashboard, notebook, biểu đồ, test case, temporal leakage, demo video |

> ⚠️ Lưu ý: Tất cả 3 người đều phải hiểu và giải thích được toàn bộ hệ thống khi bị hỏi phản biện.

#### 0.3 Setup môi trường
- Tạo repository Git chung (GitHub/GitLab).
- Tạo cấu trúc thư mục theo đúng yêu cầu đề bài:
```
agentic/
├── README.md
├── requirements.txt
├── report.pdf
├── demo_video_link.txt
├── openspec/
│   ├── changes/faithful-evidence-forecasting/
│   │   ├── proposal.md
│   │   ├── design.md
│   │   └── tasks.md
│   └── specs/forecasting/spec.md
├── metric_definition.md
├── data/
│   └── sample_news_price.csv
├── src/
│   ├── retriever.py
│   ├── evidence_extractor.py
│   ├── evidence_selector.py
│   ├── forecast_model.py
│   ├── faithfulness_metrics.py
│   ├── run_pipeline.py
│   └── dashboard.py
├── tests/
│   ├── test_temporal_retriever.py
│   └── test_metrics.py
├── notebooks/
│   └── visualization.ipynb
└── outputs/
    ├── prediction_results.csv
    ├── faithfulness_results.csv
    ├── run_log.json
    ├── test_report.md
    └── figures/
```
- Cài đặt Python 3.9+, các thư viện trong `requirements.txt`: `pandas`, `numpy`, `scikit-learn`, `streamlit`, `jupyter`, `pytest`, `plotly`.
- Thống nhất format dữ liệu và convention đặt tên biến.
- Ghi **commit log** (hoặc link PR) làm minh chứng Agentic SDLC — cập nhật liên tục, không để cuối đồ án.

### Output của Phase 0
- [ ] Repository Git đã tạo, có cấu trúc thư mục đầy đủ.
- [ ] `requirements.txt` đã tạo và cài được trên máy mọi thành viên.
- [ ] Phân công rõ ràng, được ghi trong `README.md`.
- [ ] Môi trường Python chạy được trên máy mọi thành viên.

---

## Phase 1 — OpenSpec & Đặc tả yêu cầu

### Mục tiêu
Viết đặc tả hệ thống theo chuẩn OpenSpec, bao gồm proposal, design, tasks và spec. Đây là pha bắt buộc, chiếm **1.0 điểm (A1)**.

### Công việc cần làm

#### 1.1 Viết `proposal.md`
Nội dung cần có:
- **Bài toán**: Dự báo xu hướng cổ phiếu từ tin tức có kiểm chứng evidence.
- **Động lực**: Tại sao accuracy chưa đủ, cần faithful evidence.
- **Phạm vi**: Những gì nhóm làm được và không làm được.
- **Kết quả mong đợi**: Prototype, dashboard, báo cáo, demo.
- **Timeline dự kiến**: Lịch hoàn thành từng phase.

#### 1.2 Viết `design.md`
Nội dung cần có:
- **Sơ đồ kiến trúc tổng quát**: vẽ sơ đồ pipeline từ input đến output.
- **Data schema**: Mô tả cấu trúc JSON/CSV của input và output (xem mẫu trong đề bài).
- **Mô tả từng module**: Retriever, Extractor, **Selector**, Model, Metrics, Dashboard — nhiệm vụ và interface.
- **Luồng group dữ liệu**: CSV phẳng → group theo `(ticker, forecast_time)` → pipeline xử lý per group.
- **Thiết kế dashboard**: Gồm những tab/biểu đồ nào.
- **Quyết định công nghệ**: Chọn thư viện gì, lý do.

#### 1.3 Viết `tasks.md`
- Liệt kê tất cả task cụ thể (tạo dữ liệu, viết từng module, viết test...).
- Mỗi task ghi rõ: người phụ trách, deadline, trạng thái (TODO/IN PROGRESS/DONE).
- Có ghi chú AI agent hỗ trợ task nào (ví dụ: dùng ChatGPT để sinh test case).

#### 1.4 Viết `specs/forecasting/spec.md`
Nội dung bắt buộc:
- **Input specification**: Mô tả chi tiết từng trường dữ liệu đầu vào.
- **Output specification**: Mô tả chi tiết từng trường đầu ra, bao gồm faithfulness fields.
- **Functional requirements**: Liệt kê các chức năng hệ thống phải có.
- **Non-functional requirements**: Độ chính xác tối thiểu, tốc độ xử lý, v.v.
- **Acceptance criteria** theo format Given/When/Then. Ví dụ:

```
User Story: Là nhà phân tích tài chính, tôi muốn xem evidence nào 
khiến mô hình dự báo cổ phiếu giảm, để biết dự báo đó có đáng tin không.

Acceptance Criteria:
  Given một prediction DOWN,
  When người dùng mở dashboard,
  Then hệ thống phải hiển thị ít nhất 1 evidence ủng hộ DOWN,
  And hiển thị thời gian xuất bản của evidence,
  And cảnh báo nếu evidence xuất hiện sau thời điểm dự báo.
```

- **AI Agent Usage**: Ghi rõ AI agent được dùng ở bước nào trong SDLC, ví dụ:
  - Requirement: dùng ChatGPT để generate user stories.
  - Implementation: dùng Cursor/Copilot để gợi ý code.
  - Testing: dùng AI để sinh test case temporal leakage.
- **Quality gate**: Mỗi output từ agent phải có bước human review trước khi merge (ghi trong `tasks.md`).

#### 1.5 Viết `metric_definition.md` (SV1)
Định nghĩa chính thức các metric, công thức và ngưỡng đánh giá:
- Temporal Validity, Evidence Support, Confidence Drop (A6).
- Sufficiency, Counterfactual Drop, Counterevidence Coverage, Market Consistency (B1–B3, nếu làm nâng cao).
- Ngưỡng: `confidence_drop > 0.1` → likely faithful; `< 0.05` → possibly decorative.

#### 1.6 Bắt đầu Agent Trace Log (B4 — xuyên suốt)
- Tạo `outputs/run_log.json` ngay từ Phase 1.
- Mỗi lần dùng AI agent: ghi `run_id`, `agent_role`, `task`, `human_review`, `quality_gate`.
- Lưu **commit log** (hoặc `outputs/commit_log.md` tóm tắt PR/commit có review) làm minh chứng A1.

### Output của Phase 1
- [ ] `openspec/changes/faithful-evidence-forecasting/proposal.md` — đầy đủ.
- [ ] `openspec/changes/faithful-evidence-forecasting/design.md` — có sơ đồ kiến trúc (bao gồm Evidence Selector).
- [ ] `openspec/changes/faithful-evidence-forecasting/tasks.md` — có phân công, timeline và quality gate.
- [ ] `openspec/specs/forecasting/spec.md` — có acceptance criteria rõ ràng.
- [ ] `metric_definition.md` — định nghĩa metric và ngưỡng.
- [ ] `outputs/run_log.json` — ít nhất 1 entry (ví dụ: Research Agent sinh user stories).

---

## Phase 2 — Chuẩn bị dữ liệu

### Mục tiêu
Tạo hoặc thu thập dataset đủ để chạy toàn bộ pipeline. Đây là pha bắt buộc, chiếm **1.0 điểm (A2)**. Nếu dùng dữ liệu thật sẽ có thêm **+1.0 điểm cộng (C1)**.

### Công việc cần làm

#### 2.1 Tạo dataset mô phỏng (tối thiểu — bắt buộc)
Dataset cần ít nhất **30 dòng**, mỗi dòng gồm:

| Cột | Kiểu | Mô tả | Ví dụ |
|-----|------|-------|-------|
| `ticker` | string | Mã cổ phiếu | AAPL |
| `forecast_time` | datetime | Thời điểm dự báo | 2025-03-12 09:00 |
| `news_id` | string | ID tin tức | N001 |
| `news_time` | datetime | Thời điểm đăng tin | 2025-03-11 08:30 |
| `news_title` | string | Tiêu đề tin | Apple reports weak iPhone sales |
| `news_text` | string | Nội dung tin | Full news text... |
| `price_5d_return` | float | Tỷ suất sinh lời 5 ngày | -0.02 |
| `volume_change` | float | Thay đổi khối lượng giao dịch | 0.15 |
| `label` | string | Nhãn thực tế | DOWN |

**Yêu cầu về nội dung dataset:**
- Có ít nhất 3 mã cổ phiếu khác nhau (ví dụ: AAPL, TSLA, NVDA).
- Có đủ 3 nhãn: UP, DOWN, HOLD (không quá mất cân bằng).
- Có **ít nhất 5 dòng có news_time > forecast_time** (để test temporal leakage).
- Có tin tức rõ ràng positive, negative và neutral.
- Có ít nhất 2–3 trường hợp counterevidence (cùng ticker, cùng `forecast_time`, có cả tin tốt và tin xấu).

#### 2.2 Group dữ liệu theo `(ticker, forecast_time)`

CSV lưu dạng phẳng (1 dòng = 1 tin), nhưng pipeline xử lý theo **nhóm dự báo**:

```python
# Mỗi group = 1 lần predict
{
  "ticker": "AAPL",
  "forecast_time": "2025-03-12 09:00",
  "news": [
    {"news_id": "N001", "news_time": "...", "news_title": "...", "news_text": "..."},
    {"news_id": "N002", ...}
  ],
  "price_features": {"price_5d_return": -0.02, "volume_change": 0.15},
  "label": "DOWN"
}
```

**Quy tắc group:**
- Group key: `(ticker, forecast_time)`.
- `label`, `price_5d_return`, `volume_change` lặp trên nhiều dòng cùng group → lấy **một giá trị** (phải nhất quán).
- Retriever, Extractor, Selector, Model chạy **per group**, không per row.
- Đếm "30 dòng" theo đề = ít nhất 30 dòng CSV; số **group dự báo** có thể ít hơn (ví dụ 10 group × 3 tin).

#### 2.3 Tiền xử lý dữ liệu
- Chuẩn hóa định dạng datetime (ISO 8601).
- Loại bỏ dòng thiếu dữ liệu quan trọng.
- Kiểm tra label hợp lệ (chỉ chấp nhận UP/DOWN/HOLD).
- Ghi log số dòng hợp lệ/không hợp lệ.

#### 2.4 Thống kê mô tả dataset
Tạo bảng thống kê gồm:
- Số group `(ticker, forecast_time)` và số dòng tin tổng.
- Phân bố nhãn UP/DOWN/HOLD.
- Số tin bị loại do temporal leakage.
- Số lượng tin theo từng ticker.

#### 2.5 (Điểm cộng C1) Dữ liệu thật
Nếu nhóm muốn làm điểm cộng:
- Dùng **Yahoo Finance** (`yfinance`) để lấy dữ liệu giá thật của ít nhất 3 ticker.
- Dùng **Kaggle financial news** hoặc **Financial PhraseBank** cho dữ liệu tin tức.
- Tạo nhãn từ giá thực tế:
  ```
  return_next_day = (close_t+1 - close_t) / close_t
  Nếu return_next_day > 0.005  → UP
  Nếu return_next_day < -0.005 → DOWN
  Ngược lại                    → HOLD
  ```
- Cần ít nhất **300 mẫu** và xử lý temporal leakage trong dữ liệu thật.
- Lưu script tiền xử lý và bảng thống kê mô tả nguồn dữ liệu.

### Output của Phase 2
- [ ] `data/sample_news_price.csv` — ít nhất 30 dòng, đủ cột.
- [ ] Bảng thống kê mô tả dataset (trong notebook hoặc báo cáo).
- [ ] (Điểm cộng) Script lấy dữ liệu thật, nguồn dữ liệu được ghi rõ.

---

## Phase 3 — Temporal Retriever

### Mục tiêu
Xây dựng module lọc tin tức theo thời gian, đảm bảo hệ thống **không dùng thông tin tương lai**. Chiếm **1.0 điểm (A3)**.

### Công việc cần làm

#### 3.1 Viết `src/retriever.py`
Module phải có các hàm:

```python
def filter_news_by_time(news_list, forecast_time):
    """
    Input:
      - news_list: list of dict, mỗi dict gồm news_id, news_time, news_title, news_text
      - forecast_time: datetime — thời điểm dự báo
    Output:
      - valid_news: list tin có news_time < forecast_time
      - invalid_future_news: list tin có news_time >= forecast_time
    """
```

**Logic kiểm tra:**
- So sánh `news_time` với `forecast_time` theo timestamp chính xác đến phút.
- Tin có `news_time >= forecast_time` → loại vào `invalid_future_news`.
- Log cảnh báo nếu có tin bị loại.

#### 3.2 Viết `tests/test_temporal_retriever.py`
Viết ít nhất **6 test case**, bao gồm:

| Test | Mô tả |
|------|-------|
| TC01 | Tin hợp lệ: news_time 1 ngày trước forecast_time → nằm trong valid_news |
| TC02 | Tin tương lai: news_time 6 giờ sau forecast_time → nằm trong invalid_future_news |
| TC03 | Tin đúng thời điểm: news_time = forecast_time → bị loại (không hợp lệ) |
| TC04 | Nhiều tin hỗn hợp: 3 hợp lệ + 2 không hợp lệ → kiểm tra split đúng |
| TC05 | Không có tin nào: `valid_news=[]`, `invalid_future_news=[]` |
| TC06 | Tất cả tin đều leakage: `valid_news=[]`, `invalid_future_news` chứa toàn bộ |

#### 3.3 Tạo cảnh báo temporal leakage
- Nếu có tin bị loại, hệ thống phải ghi log rõ: `[WARNING] Temporal leakage detected: news_id=N005, news_time=2025-03-12 15:30 > forecast_time=2025-03-12 09:00`.
- Đầu ra cần bao gồm `leakage_count` (số tin bị loại) để hiển thị trên dashboard.

### Output của Phase 3
- [ ] `src/retriever.py` — chạy được, có docstring rõ ràng.
- [ ] `tests/test_temporal_retriever.py` — ít nhất 6 test case, tất cả pass.
- [ ] Log cảnh báo temporal leakage hoạt động đúng.

---

## Phase 4 — Evidence Extraction

### Mục tiêu
Xây dựng module trích xuất bằng chứng (evidence) từ tin tức và phân loại hướng tác động của chúng. Chiếm **1.0 điểm (A4)**.

### Công việc cần làm

#### 4.1 Viết `src/evidence_extractor.py`
Module phải:
- Nhận đầu vào là nội dung tin tức (text).
- Trả về danh sách evidence, mỗi evidence gồm:

```python
{
  "evidence_text": "weak iPhone sales in China",  # đoạn text trích ra
  "polarity": "negative",                          # positive / negative / neutral
  "expected_direction": "DOWN",                    # UP / DOWN / HOLD
  "confidence": 0.85                               # độ tự tin của extraction
}
```

**Phương pháp tối thiểu (rule-based):**
- Định nghĩa từ điển keyword:
  - Negative keywords: `miss, weak, decline, drop, loss, recall, layoff, fine, lawsuit, shortage`
  - Positive keywords: `beat, strong, growth, launch, surge, profit, record, partnership, innovation`
  - Neutral keywords: `meeting, announce, report, hold, maintain`
- Tìm các keyword trong text, phân loại polarity, suy ra expected_direction.

**Phương pháp nâng cao (tùy chọn):**
- Dùng FinBERT để phân loại sentiment từng câu.
- Dùng LLM (GPT/Claude) để extract evidence có nghĩa hơn.

#### 4.2 Kiểm thử evidence extractor
Chuẩn bị ít nhất **5 ví dụ đúng và 5 ví dụ sai/biên** để minh họa:

| Input text | Expected polarity | Expected direction |
|-----------|-------------------|-------------------|
| "Tesla misses delivery expectations" | negative | DOWN |
| "Apple beats earnings forecast" | positive | UP |
| "CEO holds annual investor meeting" | neutral | HOLD |
| "Samsung launches new Galaxy series" | positive | UP |
| "Revenue declines 15% year-over-year" | negative | DOWN |

#### 4.3 Xử lý trường hợp đặc biệt
- Tin tức mơ hồ hoặc không có keyword rõ → trả về neutral, expected_direction = HOLD.
- Tin tức có cả positive và negative keyword → ghi nhận cả hai, để Evidence Selector quyết định.
- Văn bản quá ngắn (< 10 từ) → log cảnh báo, gán neutral.

### Output của Phase 4
- [ ] `src/evidence_extractor.py` — chạy được với ít nhất 30 tin trong dataset.
- [ ] Bảng 5 ví dụ đúng và 5 ví dụ sai trong báo cáo.
- [ ] Coverage: bao nhiêu % tin trong dataset extract được ít nhất 1 evidence.

---

## Phase 4.5 — Evidence Selector

### Mục tiêu
Chọn và phân loại evidence trước khi đưa vào Forecast Model — khớp pipeline đề bài: `Extractor → **Selector** → Model`. Hỗ trợ phân tách pro/counter evidence (nền tảng cho B2).

### Công việc cần làm

#### 4.5.1 Viết `src/evidence_selector.py`

```python
def select_evidence(all_evidence, prediction_direction=None):
    """
    Input:
      - all_evidence: list evidence từ extractor (đã gắn news_id, news_time)
      - prediction_direction: optional — dùng khi phân loại counterevidence (B2)
    Output:
      - pro_evidence: list evidence ủng hộ hướng dự báo (hoặc hướng dominant)
      - counter_evidence: list evidence ngược chiều
      - cited_evidence: list evidence được chọn để cite (subset của pro_evidence)
    """
```

**Logic tối thiểu:**
- Loại evidence trùng `evidence_text` hoặc cùng `news_id`.
- `pro_evidence`: evidence có `expected_direction` khớp hướng dominant (UP/DOWN) hoặc polarity rõ.
- `counter_evidence`: evidence có `expected_direction` ngược hướng dominant.
- `cited_evidence`: top-k evidence (theo `confidence` extraction), ít nhất 1 nếu có.
- Neutral evidence (`HOLD`) không vào pro/counter trừ khi không còn evidence khác.

#### 4.5.2 Test selector
- Case có cả tin tích cực và tiêu cực cùng group → pro và counter đều không rỗng.
- Case chỉ có neutral → `cited_evidence` rỗng hoặc fallback HOLD.

### Output của Phase 4.5
- [ ] `src/evidence_selector.py` — chạy được per group.
- [ ] `design.md` cập nhật interface Selector.

---

## Phase 5 — Forecast Model

### Mục tiêu
Xây dựng mô hình dự báo UP/DOWN/HOLD và giải thích dự báo cụ thể. Chiếm **1.0 điểm (A5)**.

### Công việc cần làm

#### 5.1 Viết `src/forecast_model.py`
Hàm dự báo chính:

```python
def predict(ticker, forecast_time, valid_news, price_features, cited_evidence=None):
    """
    Input:
      - ticker: str
      - forecast_time: datetime
      - valid_news: list of news đã qua Temporal Retriever
      - price_features: dict gồm price_5d_return, volume_change
      - cited_evidence: list evidence từ Selector (nếu None → tự chọn từ valid_news)
    Output:
      - prediction: "UP" | "DOWN" | "HOLD"
      - confidence: float (0.0 - 1.0)
      - cited_evidence: list evidence dùng để ra quyết định
      - rationale: str mô tả lý do dự báo
    """
```

**Mô hình tối thiểu (rule-based):**
```
# Chỉ đếm evidence không neutral
positive_count = số evidence có expected_direction = UP
negative_count = số evidence có expected_direction = DOWN
price_signal = sign(price_5d_return)  # +1 / 0 / -1

score = (positive_count - negative_count) + 0.5 * price_signal
# price_features: baseline dùng nhẹ; mô hình nâng cao/C2 có thể weight mạnh hơn

Nếu score > 0  → UP,   confidence = positive_count / max(positive_count + negative_count, 1)
Nếu score < 0  → DOWN, confidence = negative_count / max(positive_count + negative_count, 1)
Nếu score = 0  → HOLD, confidence = 0.5
```

**Mô hình nâng cao (tùy chọn, cần cho điểm cộng C2):**
- Logistic Regression với TF-IDF features.
- LSTM hoặc FinBERT fine-tuned.
- Fusion model kết hợp text và price features.

#### 5.2 Đánh giá mô hình
Tính các chỉ số:
- **Accuracy**: Tỷ lệ dự báo đúng.
- **Confusion matrix**: Bảng 3x3 cho UP/DOWN/HOLD.
- **Per-class precision, recall, F1**.

#### 5.3 Giải thích một prediction cụ thể
Chọn 1 prediction trong dataset, giải thích rõ:
- Prediction là gì, confidence bao nhiêu.
- Evidence nào được cite, polarity của chúng.
- Rationale (câu giải thích bằng ngôn ngữ tự nhiên).

**Ví dụ rationale:**
```
"Dự báo AAPL DOWN (confidence=0.72) dựa trên 2 evidence tiêu cực: 
(1) 'weak iPhone sales in China' và (2) 'supply chain disruption'. 
Không có evidence tích cực đáng kể."
```

#### 5.4 Lưu kết quả
Lưu tất cả prediction ra `outputs/prediction_results.csv`:

| ticker | forecast_time | prediction | confidence | label | correct |
|--------|--------------|------------|------------|-------|---------|
| AAPL | 2025-03-12 09:00 | DOWN | 0.72 | DOWN | True |

### Output của Phase 5
- [ ] `src/forecast_model.py` — dự báo được toàn bộ dataset.
- [ ] `outputs/prediction_results.csv` — có đủ cột.
- [ ] Bảng accuracy và confusion matrix.
- [ ] Ít nhất 1 case giải thích rõ prediction trong báo cáo.

---

## Phase 6 — Faithfulness Metrics

### Mục tiêu
Tính **3 metric faithfulness cơ bản**. Đây là phần **cốt lõi nhất** của đồ án. Chiếm **1.0 điểm (A6)**. Metric nâng cao (B1–B3) triển khai ở **Phase 11**.

### Công việc cần làm

#### 6.1 Viết `src/faithfulness_metrics.py`

**Metric 1 — Temporal Validity**
```
temporal_validity = (số evidence có news_time < forecast_time) / (tổng số evidence cited)
Kết quả lý tưởng: 1.0 (không dùng tin tương lai)
```

**Metric 2 — Evidence Support**
```
Với mỗi evidence được cite:
  support_score = 1.0 nếu expected_direction == prediction
                = 0.0 nếu ngược lại
evidence_support = trung bình support_score của tất cả cited evidence
```

**Metric 3 — Confidence Drop (quan trọng nhất)**
```
1. Chạy model với full input → confidence_original
2. Bỏ cited evidence khỏi input → chạy lại model → confidence_without
3. confidence_drop = confidence_original - confidence_without

Nếu confidence_drop > 0.1 → evidence có khả năng quan trọng (faithful)
Nếu confidence_drop < 0.05 → evidence chỉ là lời giải thích trang trí
```

So sánh với baseline: cũng bỏ 1 tin **ngẫu nhiên không được cite** và đo confidence drop của tin ngẫu nhiên đó → nếu confidence drop của cited evidence > random evidence thì evidence có dấu hiệu faithful hơn.

#### 6.2 Lưu kết quả faithfulness
Lưu ra `outputs/faithfulness_results.csv`:

| ticker | forecast_time | prediction | confidence_original | confidence_without | confidence_drop | confidence_drop_random | temporal_validity | evidence_support |
|--------|--------------|------------|--------------------|--------------------|-----------------|------------------------|-------------------|-----------------|

(`confidence_drop_random`: drop khi bỏ 1 tin ngẫu nhiên **không** được cite — baseline so sánh faithful.)

#### 6.3 Tạo bảng tổng hợp
Tính giá trị trung bình của từng metric trên toàn bộ dataset → hiển thị trong dashboard.

> Các metric nâng cao (Sufficiency, Counterfactual, Counterevidence Coverage, Market Consistency) — xem **Phase 11**.

### Output của Phase 6
- [ ] `src/faithfulness_metrics.py` — tính được 3 metric cơ bản + confidence_drop_random.
- [ ] `outputs/faithfulness_results.csv` — có đủ cột.
- [ ] Bảng tổng hợp metric trung bình của toàn dataset.

---

## Phase 7 — Visualization Dashboard

### Mục tiêu
Xây dựng dashboard hoặc notebook trực quan hóa toàn bộ kết quả. Chiếm **1.0 điểm (A7)**.

### Công việc cần làm

#### 7.1 Viết `src/dashboard.py`
Dùng **Streamlit** (khuyến nghị). Bổ sung `notebooks/visualization.ipynb` cho SV3 (biểu đồ tĩnh, khám phá dữ liệu).

**Thiết kế kỹ thuật — re-run model tại runtime:**
- Dashboard **import** `forecast_model`, `faithfulness_metrics`, `evidence_selector`, `retriever`.
- Khi user chọn `(ticker, forecast_time)`: load group từ CSV → chạy pipeline in-memory (hoặc đọc cache từ `outputs/`).
- Nút **"Remove cited evidence"**: gọi lại `predict(..., cited_evidence=[])` hoặc bỏ cited khỏi input → tính `confidence_drop` live.
- Nút **"Remove random evidence"**: bỏ 1 tin không được cite → so sánh `confidence_drop` vs cited (theo kịch bản demo đề bài).

**Tab 1 — Prediction Overview**
- Bảng tất cả prediction: ticker, forecast_time, prediction, confidence, label, correct.
- Bộ lọc theo ticker và nhãn.
- Biểu đồ phân bố prediction (bar chart: UP vs DOWN vs HOLD).
- Accuracy tổng quát.

**Tab 2 — Evidence Explorer**
- Chọn 1 prediction cụ thể → hiển thị chi tiết:
  - Ticker, forecast_time, prediction, confidence.
  - Danh sách pro evidence, counterevidence (nếu Selector có), và cited evidence.
  - Cảnh báo đỏ nếu có evidence có news_time > forecast_time.
  - Rationale của mô hình.

**Tab 3 — Faithfulness Analysis**
- Biểu đồ confidence_drop cho từng prediction (bar chart).
- Bảng so sánh confidence gốc vs confidence sau khi bỏ cited evidence vs bỏ random evidence.
- **Radar chart (cơ bản — A7):** 3 metric — Temporal Validity, Evidence Support, Confidence Drop.
- **Radar chart (nâng cao — B2):** thêm Counterevidence Coverage khi đã triển khai Phase 11.
- Phân loại prediction thành "Likely Faithful" (drop > 0.1) và "Possibly Decorative" (drop < 0.05).

**Tab 4 — Temporal Leakage Monitor**
- Bảng tất cả tin bị loại do temporal leakage.
- Thống kê: bao nhiêu % tin bị loại trên toàn dataset.
- Cảnh báo nếu không có tin nào bị loại (có thể dataset không có test case leakage).

#### 7.2 Tạo các file hình ảnh tĩnh
Lưu vào `outputs/figures/`:
- `prediction_distribution.png` — phân bố UP/DOWN/HOLD.
- `confidence_drop.png` — biểu đồ confidence drop cho từng prediction.
- `temporal_leakage_warning.png` — bảng/hình cảnh báo temporal leakage.
- `faithfulness_radar.png` — radar 3 metric (4 nếu có B2).

#### 7.3 Kịch bản demo dashboard (5 phút)
Chuẩn bị sẵn kịch bản demo theo đúng trình tự:
1. Mở dashboard.
2. Chọn ticker (ví dụ AAPL).
3. Chọn forecast date.
4. Hiển thị tin hợp lệ trước thời điểm dự báo.
5. Xem prediction và confidence.
6. Xem evidence và rationale.
7. Bấm "Remove cited evidence" → xem confidence thay đổi.
8. (Khuyến nghị) Bấm "Remove random evidence" → so sánh drop cited vs random.
9. Kết luận evidence faithful hay không.
10. Trình bày 1 limitation quan trọng.

### Output của Phase 7
- [ ] `src/dashboard.py` — chạy được bằng `streamlit run src/dashboard.py`.
- [ ] `notebooks/visualization.ipynb` — biểu đồ khám phá / export figures.
- [ ] `outputs/figures/` — có đủ 4 hình.
- [ ] Dashboard re-run được `predict()` và tính confidence drop tại runtime.
- [ ] Kịch bản demo được ghi sẵn trong `README.md`.

---

## Phase 8 — Testing & QA

### Mục tiêu
Kiểm tra toàn bộ pipeline bằng test case tự động, đảm bảo không có lỗi nghiêm trọng trước khi nộp.

### Công việc cần làm

#### 8.1 Hoàn thiện `tests/test_temporal_retriever.py`
(Đã mô tả ở Phase 3 — kiểm tra lại và bổ sung nếu cần.)

#### 8.2 Viết `tests/test_metrics.py`
Viết ít nhất **5 test case** cho faithfulness metrics:

| Test | Mô tả |
|------|-------|
| TM01 | Confidence drop = 0 khi không có cited evidence |
| TM02 | Temporal validity = 1.0 khi tất cả evidence trước forecast_time |
| TM03 | Temporal validity < 1.0 khi có evidence sau forecast_time |
| TM04 | Evidence support = 1.0 khi tất cả evidence align với prediction |
| TM05 | Evidence support = 0.0 khi tất cả evidence ngược chiều prediction |

#### 8.3 Viết `src/run_pipeline.py`
Script orchestrator chạy end-to-end:

```bash
python src/run_pipeline.py --input data/sample_news_price.csv
```

Luồng: **group CSV** → Retriever → Extractor → Selector → Model → Faithfulness Metrics → ghi `outputs/*.csv`.

#### 8.4 Kiểm tra end-to-end
Chạy toàn bộ pipeline trên dataset:
- Input: `data/sample_news_price.csv`
- Chạy qua Retriever → Extractor → **Selector** → Model → Metrics
- Kiểm tra không có lỗi runtime.
- Kiểm tra output files được tạo đúng.

#### 8.5 Kiểm tra edge cases
- Ticker không có tin nào → hệ thống xử lý thế nào?
- Tất cả tin bị loại do leakage → prediction fallback là gì?
- Confidence = 0.5 (HOLD) → confidence drop tính thế nào?

#### 8.6 Viết `outputs/test_report.md`
Tóm tắt kết quả `pytest`: số test pass/fail, edge cases đã kiểm tra, lỗi đã sửa.

### Output của Phase 8
- [ ] `src/run_pipeline.py` — chạy end-to-end không lỗi.
- [ ] `tests/test_temporal_retriever.py` — ít nhất 6 test, tất cả pass.
- [ ] `tests/test_metrics.py` — ít nhất 5 test, tất cả pass.
- [ ] Chạy `pytest tests/` không có lỗi.
- [ ] `outputs/test_report.md` — báo cáo test.

---

## Phase 9 — Báo cáo & Demo

### Mục tiêu
Viết báo cáo 5–8 trang và quay video demo 5 phút để nộp.

### Công việc cần làm

#### 9.1 Viết `report.pdf` (5–8 trang)
Cấu trúc gợi ý:

| Phần | Nội dung | Trang |
|------|---------|-------|
| 1. Giới thiệu | Bài toán, động lực, tại sao cần faithful evidence | 0.5 |
| 2. Research gap | Accuracy chưa đủ, vấn đề hallucination trong explanation | 0.5 |
| 3. Thiết kế hệ thống | Kiến trúc pipeline, Agentic SDLC, OpenSpec | 1.0 |
| 4. Dữ liệu | Mô tả dataset, thống kê, cách tạo label | 0.5 |
| 5. Pipeline kỹ thuật | Retriever → Extractor → Selector → Model → Metrics, ví dụ I/O | 1.5 |
| 6. Metric & đánh giá | Định nghĩa 3 metric faithfulness, cách tính | 1.0 |
| 7. Kết quả | Bảng, biểu đồ, so sánh prediction vs faithfulness | 1.0 |
| 8. Case analysis | 1 case faithful, 1 case không faithful, 1 case leakage | 0.5 |
| 9. Limitations | Ít nhất 3 hạn chế cụ thể của hệ thống | 0.5 |
| 10. Phụ lục | Prompt AI agent, trace log, test case | (không tính trang) |

**Lưu ý:**
- Viết bằng tiếng Việt hoặc tiếng Anh (thống nhất).
- Không copy-paste code vào báo cáo — chỉ mô tả thuật toán bằng ngôn ngữ tự nhiên hoặc pseudocode.
- Mỗi biểu đồ phải có chú thích và phân tích ý nghĩa.

#### 9.2 Viết `README.md`
- Hướng dẫn cài đặt: `pip install -r requirements.txt`
- Lệnh chạy pipeline: `python src/run_pipeline.py`
- Lệnh chạy dashboard: `streamlit run src/dashboard.py`
- Lệnh chạy test: `pytest tests/`
- Mô tả cấu trúc thư mục.
- Phân công nhóm (tên, MSSV, vai trò).

#### 9.3 Quay video demo (~5 phút)
Theo kịch bản đã chuẩn bị ở Phase 7, quay màn hình kết hợp thuyết minh:
- Giới thiệu bài toán (30 giây).
- Demo dashboard từng tab (3 phút).
- Thực hiện thao tác "Remove cited evidence" và giải thích kết quả (1 phút).
- Nêu 1 limitation (30 giây).

Upload video lên Google Drive / YouTube và lưu link vào `demo_video_link.txt`.

#### 9.4 Checklist trước khi nộp

- [ ] README.md có hướng dẫn chạy đầy đủ.
- [ ] OpenSpec proposal/design/tasks/spec + `metric_definition.md` đầy đủ.
- [ ] `requirements.txt` và `src/run_pipeline.py` hoạt động.
- [ ] Dataset có ít nhất 30 dòng, đúng format, group `(ticker, forecast_time)` rõ ràng.
- [ ] Module lọc tin theo thời gian chạy được.
- [ ] Module trích xuất evidence và **evidence selector** chạy được.
- [ ] Mô hình dự báo UP/DOWN/HOLD chạy được.
- [ ] Ít nhất 3 metric faithfulness cơ bản được tính.
- [ ] Dashboard hoặc notebook chạy được.
- [ ] Ít nhất 4 biểu đồ/hình trong `outputs/figures/`.
- [ ] Test case cho temporal leakage pass; `outputs/test_report.md` có.
- [ ] `outputs/run_log.json` và reflection về AI agent trong SDLC (B4).
- [ ] **Không có tin tương lai nào được dùng trong thí nghiệm.**
- [ ] Báo cáo PDF 5–8 trang.
- [ ] Demo video link trong `demo_video_link.txt`.

### Output của Phase 9
- [ ] `report.pdf` — 5–8 trang.
- [ ] `README.md` — hướng dẫn đầy đủ.
- [ ] `demo_video_link.txt` — link video ~5 phút.

---

## Phase 10 (Nâng cao) — Agentic SDLC Maturity

### Mục tiêu
Triển khai ít nhất 3 agent role với trace log, quality gate, commit log và reflection. Chiếm **0.75 điểm (B4)**. **Không làm cuối đồ án** — ghi log xuyên suốt từ Phase 1.

### Công việc cần làm

#### 10.1 Định nghĩa 3 agent role
- **Research Agent**: Tìm kiếm thông tin, tổng hợp dataset, gợi ý metric, sinh user stories.
- **Coding Agent**: Sinh code cho từng module, gợi ý refactor.
- **Testing/Reviewer Agent**: Sinh test case, review output, phát hiện lỗi.

#### 10.2 Trace log (`outputs/run_log.json`)
Mỗi entry gồm: `run_id`, `agent_role`, `task`, `input`, `output`, `human_review`, `quality_gate`.

```json
{
  "run_id": "R001",
  "agent_role": "Testing Agent",
  "task": "Generate temporal leakage test cases",
  "input": "forecast_time and news_time examples",
  "output": "6 unit tests",
  "human_review": "accepted with minor edits",
  "quality_gate": "passed"
}
```

#### 10.3 Quality gate & commit log
- Output của agent chỉ merge sau khi con người review (ghi trong `tasks.md` và `run_log.json`).
- Lưu **commit log** hoặc `outputs/commit_log.md`: commit nào do agent gợi ý, human sửa gì.

#### 10.4 Reflection (báo cáo Phase 9)
- AI agent đã giúp được gì, sai ở đâu, con người đã sửa gì — ít nhất 200 từ.

### Output của Phase 10
- [ ] `outputs/run_log.json` — ít nhất 6 entries (2 entry / agent role).
- [ ] Commit log hoặc `outputs/commit_log.md` — minh chứng review.
- [ ] Phần reflection trong báo cáo (ít nhất 200 từ).

---

## Phase 11 (Nâng cao) — Advanced Metrics

### Mục tiêu
Triển khai metric nâng cao trong `faithfulness_metrics.py` (mở rộng Phase 6). Chiếm **2.25 điểm (B1+B2+B3)**.

### Công việc cần làm

#### 11.1 (B1 — 0.75đ) Sufficiency + Counterfactual Perturbation
- **Sufficiency test**: Chỉ dùng cited evidence (bỏ news/price còn lại) → dự báo lại → nếu prediction giữ nguyên thì evidence sufficient.
- **Counterfactual**: Thay cited evidence bằng tin neutral cùng topic → dự báo lại.

```
Gốc: "Tesla misses delivery" → DOWN, confidence=0.78
Counterfactual: "Tesla holds investor meeting" → DOWN, confidence=0.52
Counterfactual drop = 0.26 → evidence gốc có ảnh hưởng lớn
```

#### 11.2 (B2 — 0.75đ) Counterevidence Coverage
- Dùng output từ `evidence_selector.py`: `counter_evidence` vs `cited_evidence`.
- `counterevidence_coverage = số prediction có ≥1 counterevidence được nhận diện / tổng prediction`
- Dashboard cảnh báo nếu prediction UP nhưng có counterevidence mạnh không được hiển thị.
- Cập nhật radar chart lên 4 metric (thêm Counterevidence Coverage).

#### 11.3 (B3 — 0.75đ) Market Consistency + Regime Analysis
- So sánh evidence với biến động giá sau dự báo (`return_next_day` hoặc label thực tế).
- `market_consistency`: evidence tiêu cực + return âm → 1.0; ngược chiều → 0.0.
- Phân loại regime: bull / bear / sideway (theo `price_5d_return` hoặc rolling market return).
- Phân tích faithfulness metrics theo từng regime.

#### 11.4 Cập nhật output
Bổ sung cột vào `outputs/faithfulness_results.csv`:
`sufficiency_match`, `counterfactual_drop`, `counterevidence_coverage`, `market_consistency`, `regime`.

### Output của Phase 11
- [ ] B1: sufficiency + counterfactual perturbation chạy được trên ≥5 case.
- [ ] B2: counterevidence coverage tính được; dashboard hiển thị counterevidence.
- [ ] B3: market consistency + phân tích regime trong báo cáo.

---

## Phase 12 (Điểm cộng) — Dữ liệu thật & GPU

### Mục tiêu
Tăng thêm tối đa 2 điểm bằng cách dùng dữ liệu thật và/hoặc mô hình GPU.

### Công việc cần làm

**C1 — Dữ liệu thật (+1.0đ)**
(Chi tiết đã mô tả ở Phase 2, mục 2.4)
- Ít nhất 3 ticker, 300 mẫu.
- Xử lý temporal leakage trong dữ liệu thật.
- Ghi rõ nguồn dữ liệu và script tiền xử lý.

**C2 — GPU/Mô hình nâng cao (+1.0đ)**
- Dùng FinBERT, LSTM, PatchTST, TimesNet hoặc fusion model.
- Ghi rõ môi trường GPU (Google Colab T4, Kaggle GPU, v.v.).
- So sánh với baseline rule-based trong bảng như ví dụ đề bài:

| Mô hình | Thiết bị | Số mẫu | Thời gian | Accuracy | Avg Confidence Drop |
|---------|---------|--------|-----------|----------|-------------------|
| Rule-based | CPU | 500 | 5 giây | 48% | 0.08 |
| FinBERT + LR | GPU T4 | 500 | 3 phút | 55% | 0.14 |

---

## Tóm tắt Timeline gợi ý

| Tuần | Phase | Công việc chính |
|------|-------|----------------|
| 1 | 0, 1 | Setup, `requirements.txt`, OpenSpec, `metric_definition.md`, bắt đầu `run_log.json` |
| 2 | 2, 3 | Dataset + group logic, Temporal Retriever + test |
| 3 | 4, 4.5, 5 | Evidence Extractor, **Selector**, Forecast Model |
| 4 | 6, 7 | Faithfulness Metrics (A6), Dashboard + figures (sớm để bắt lỗi integration) |
| 5 | 8 | `run_pipeline.py`, pytest, `test_report.md` |
| 6 | 9, 10, 11 | Báo cáo, demo, B4 reflection, metric nâng cao (nếu làm) |
| 7 | 12, Buffer | Dữ liệu thật/GPU (nếu làm), sửa lỗi, review, nộp bài |

---

*Tài liệu này được tạo dựa trên đề bài đồ án cuối kì môn Công nghệ mới.*