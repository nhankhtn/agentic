# Design — Faithful Evidence-Centric Financial News Forecasting

**Phiên bản:** 1.0  
**Ngày tạo:** [Ngày]  
**Tác giả:** SV1 — Research & Spec Owner  
**Trạng thái:** Draft  
**Tài liệu liên quan:** proposal.md, specs/forecasting/spec.md

---

## 1. Kiến trúc tổng quan

### 1.1 Sơ đồ pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                          INPUT LAYER                            │
│                                                                 │
│  ticker + forecast_time + news_list + price_features            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MODULE 1: TEMPORAL RETRIEVER                 │
│                                                                 │
│  • So sánh news_time vs forecast_time                           │
│  • Phân loại: valid_news / invalid_future_news                  │
│  • Ghi log cảnh báo nếu có tin bị loại                         │
│                                                                 │
│  Input:  news_list, forecast_time                               │
│  Output: valid_news[], invalid_future_news[], leakage_count     │
└────────────────────────────┬────────────────────────────────────┘
                             │ valid_news[]
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MODULE 2: EVIDENCE EXTRACTOR                   │
│                                                                 │
│  • Trích evidence_text từ từng tin hợp lệ                      │
│  • Phân loại polarity: positive / negative / neutral            │
│  • Suy ra expected_direction: UP / DOWN / HOLD                  │
│                                                                 │
│  Input:  valid_news[]                                           │
│  Output: evidence_list[] (mỗi item: text, polarity, direction)  │
└────────────────────────────┬────────────────────────────────────┘
                             │ evidence_list[]
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MODULE 3: EVIDENCE SELECTOR                    │
│                                                                 │
│  • Tách pro_evidence (align với prediction)                     │
│  • Tách counterevidence (ngược chiều prediction)                │
│  • Chọn top-k evidence để cite                                  │
│                                                                 │
│  Input:  evidence_list[], prediction (sơ bộ)                   │
│  Output: cited_evidence[], counter_evidence[]                   │
└────────────────────────────┬────────────────────────────────────┘
                             │ cited_evidence[]
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MODULE 4: FORECAST MODEL                      │
│                                                                 │
│  • Dự báo UP/DOWN/HOLD từ evidence + price_features             │
│  • Tính confidence score                                        │
│  • Tạo rationale bằng ngôn ngữ tự nhiên                        │
│                                                                 │
│  Input:  cited_evidence[], price_features                       │
│  Output: prediction, confidence, rationale                      │
└────────────────────────────┬────────────────────────────────────┘
                             │ prediction + confidence
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               MODULE 5: FAITHFULNESS EVALUATOR                  │
│                                                                 │
│  • Temporal Validity: % evidence trước forecast_time            │
│  • Evidence Support: % evidence align với prediction            │
│  • Confidence Drop: chạy lại model khi bỏ cited evidence        │
│  • (Nâng cao) Counterfactual, Counterevidence Coverage          │
│                                                                 │
│  Input:  prediction, confidence, cited_evidence[], valid_news[] │
│  Output: faithfulness_scores{}                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │ tất cả kết quả
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               MODULE 6: VISUALIZATION DASHBOARD                 │
│                                                                 │
│  Tab 1: Prediction Overview    Tab 2: Evidence Explorer         │
│  Tab 3: Faithfulness Analysis  Tab 4: Temporal Leakage Monitor  │
│                                                                 │
│  Input:  prediction_results.csv, faithfulness_results.csv       │
│  Output: interactive Streamlit app + static figures             │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Luồng dữ liệu end-to-end (ví dụ cụ thể)

```
Input:
  ticker = "AAPL"
  forecast_time = "2025-03-12 09:00"
  news = [
    { id: "N001", time: "2025-03-11 08:30", text: "Apple reports weak iPhone sales in China" },
    { id: "N002", time: "2025-03-12 15:30", text: "Apple announces new MacBook lineup" }  ← future!
  ]
  price_features = { price_5d_return: -0.02, volume_change: 0.15 }

Sau Temporal Retriever:
  valid_news   = [N001]   ← chỉ N001 hợp lệ
  invalid_news = [N002]   ← N002 bị loại vì 15:30 > 09:00

Sau Evidence Extractor:
  evidence = [{ text: "weak iPhone sales in China", polarity: "negative", direction: "DOWN" }]

Sau Forecast Model:
  prediction = "DOWN", confidence = 0.72
  rationale  = "1 negative evidence (weak iPhone sales in China) → DOWN"

Sau Faithfulness Evaluator:
  temporal_validity  = 1.0   (N001 hợp lệ)
  evidence_support   = 1.0   (DOWN aligns với DOWN)
  confidence_drop    = 0.21  (confidence 0.72 → 0.51 khi bỏ N001)
```

---

## 2. Data Schema

### 2.1 Input Schema — `sample_news_price.csv`

| Cột | Kiểu dữ liệu | Bắt buộc | Mô tả | Ví dụ |
|-----|-------------|----------|-------|-------|
| `ticker` | string | ✅ | Mã cổ phiếu | AAPL |
| `forecast_time` | datetime (ISO 8601) | ✅ | Thời điểm dự báo | 2025-03-12 09:00 |
| `news_id` | string | ✅ | ID duy nhất của tin | N001 |
| `news_time` | datetime (ISO 8601) | ✅ | Thời điểm đăng tin | 2025-03-11 08:30 |
| `news_title` | string | ✅ | Tiêu đề tin tức | Apple reports weak iPhone sales |
| `news_text` | string | ✅ | Nội dung đầy đủ | Apple Inc. today reported... |
| `price_5d_return` | float | ✅ | Tỷ suất sinh lời 5 ngày gần nhất | -0.02 |
| `volume_change` | float | ⬜ | Thay đổi khối lượng giao dịch | 0.15 |
| `label` | string (UP/DOWN/HOLD) | ✅ | Nhãn thực tế để đánh giá | DOWN |

### 2.2 Output Schema — Prediction

```json
{
  "ticker": "AAPL",
  "forecast_time": "2025-03-12 09:00",
  "prediction": "DOWN",
  "confidence": 0.72,
  "rationale": "1 negative evidence found: weak iPhone sales in China",
  "cited_evidence": [
    {
      "news_id": "N001",
      "evidence_text": "weak iPhone sales in China",
      "polarity": "negative",
      "expected_direction": "DOWN",
      "support_score": 1.0,
      "news_time": "2025-03-11 08:30"
    }
  ],
  "label": "DOWN",
  "correct": true
}
```

### 2.3 Output Schema — Faithfulness

```json
{
  "ticker": "AAPL",
  "forecast_time": "2025-03-12 09:00",
  "prediction": "DOWN",
  "confidence_original": 0.72,
  "confidence_without_evidence": 0.51,
  "confidence_drop": 0.21,
  "temporal_validity": 1.0,
  "evidence_support": 1.0,
  "leakage_count": 1,
  "faithful_verdict": "likely_faithful"
}
```

### 2.4 Output Schema — Agent Trace Log

```json
{
  "run_id": "R001",
  "timestamp": "2025-03-10 14:30:00",
  "agent_role": "Testing Agent",
  "task": "Generate temporal leakage test cases",
  "input_summary": "forecast_time and news_time examples",
  "output_summary": "5 unit tests for retriever.py",
  "human_review": "accepted with minor edits",
  "quality_gate": "passed"
}
```

---

## 3. Thiết kế chi tiết từng module

### 3.1 Module 1 — Temporal Retriever (`src/retriever.py`)

**Nhiệm vụ:** Lọc tin tức theo thời gian, đảm bảo không dùng thông tin tương lai.

**Interface:**
```python
def filter_news_by_time(
    news_list: list[dict],
    forecast_time: str  # format: "YYYY-MM-DD HH:MM"
) -> tuple[list[dict], list[dict], int]:
    """
    Returns:
        valid_news          : list tin có news_time < forecast_time
        invalid_future_news : list tin có news_time >= forecast_time
        leakage_count       : số tin bị loại
    """
```

**Logic xử lý:**
```
Với mỗi tin trong news_list:
  parse news_time thành datetime object
  parse forecast_time thành datetime object
  
  nếu news_time < forecast_time:
    thêm vào valid_news
  ngược lại:
    thêm vào invalid_future_news
    in WARNING log
    
trả về (valid_news, invalid_future_news, len(invalid_future_news))
```

**Lưu ý triển khai:**
- Parse datetime phải chuẩn xác đến phút, không chỉ đến ngày.
- Tin có `news_time == forecast_time` được coi là không hợp lệ (bằng = tương lai).
- Log format: `[WARNING] Temporal leakage: news_id={id}, news_time={t} >= forecast_time={ft}`.

---

### 3.2 Module 2 — Evidence Extractor (`src/evidence_extractor.py`)

**Nhiệm vụ:** Trích xuất evidence từ nội dung tin tức, phân loại polarity và hướng tác động.

**Interface:**
```python
def extract_evidence(
    news_text: str,
    news_id: str
) -> list[dict]:
    """
    Returns list of evidence:
    [
      {
        "evidence_text": str,
        "polarity": "positive" | "negative" | "neutral",
        "expected_direction": "UP" | "DOWN" | "HOLD",
        "confidence": float
      }
    ]
    """
```

**Từ điển keyword (rule-based baseline):**

| Nhóm | Keywords |
|------|---------|
| **Negative → DOWN** | miss, weak, decline, drop, loss, recall, layoff, fine, lawsuit, shortage, cut, downgrade, slump, concern, risk, warning, disappointing |
| **Positive → UP** | beat, strong, growth, launch, surge, profit, record, partnership, innovation, upgrade, exceed, outperform, rise, rally, boost |
| **Neutral → HOLD** | meeting, announce, maintain, hold, review, explore, consider, discuss, schedule |

**Logic phân loại:**
```
negative_count = số keyword negative trong text
positive_count = số keyword positive trong text

nếu negative_count > positive_count: polarity = "negative", direction = "DOWN"
nếu positive_count > negative_count: polarity = "positive", direction = "UP"
nếu bằng nhau hoặc = 0:             polarity = "neutral",  direction = "HOLD"

confidence = max(negative_count, positive_count) / (negative_count + positive_count + 1)
```

---

### 3.3 Module 3 — Forecast Model (`src/forecast_model.py`)

**Nhiệm vụ:** Dự báo UP/DOWN/HOLD từ evidence đã trích xuất và đặc trưng giá.

**Interface:**
```python
def predict(
    evidence_list: list[dict],
    price_features: dict,
    ticker: str,
    forecast_time: str
) -> dict:
    """
    Returns:
    {
      "prediction": "UP" | "DOWN" | "HOLD",
      "confidence": float,
      "cited_evidence": list[dict],
      "rationale": str
    }
    """
```

**Thuật toán rule-based (baseline):**
```
positive_count = số evidence có expected_direction = "UP"
negative_count = số evidence có expected_direction = "DOWN"
total          = positive_count + negative_count

# Tích hợp price signal
nếu price_5d_return > 0: positive_count += 0.5
nếu price_5d_return < 0: negative_count += 0.5

score = positive_count - negative_count

nếu score > 0:
  prediction  = "UP"
  confidence  = positive_count / (total + 1)
  cited       = tất cả UP evidence
  
nếu score < 0:
  prediction  = "DOWN"
  confidence  = negative_count / (total + 1)
  cited       = tất cả DOWN evidence

nếu score = 0:
  prediction  = "HOLD"
  confidence  = 0.5
  cited       = tất cả evidence (không rõ chiều)
```

**Cách tính Confidence Drop:**
```python
def compute_confidence_drop(evidence_list, price_features, cited_evidence):
    # Chạy predict với full input
    result_full = predict(evidence_list, price_features, ...)
    confidence_original = result_full["confidence"]
    
    # Loại cited evidence ra khỏi evidence_list
    evidence_without = [e for e in evidence_list if e not in cited_evidence]
    
    # Chạy predict lại
    result_without = predict(evidence_without, price_features, ...)
    confidence_without = result_without["confidence"]
    
    return confidence_original - confidence_without
```

---

### 3.4 Module 4 — Faithfulness Evaluator (`src/faithfulness_metrics.py`)

**Nhiệm vụ:** Tính các metric định lượng để kiểm chứng tính faithful của evidence.

**Metric 1 — Temporal Validity:**
```python
def temporal_validity(cited_evidence: list, forecast_time: str) -> float:
    valid = [e for e in cited_evidence if e["news_time"] < forecast_time]
    return len(valid) / len(cited_evidence) if cited_evidence else 0.0
```

**Metric 2 — Evidence Support:**
```python
def evidence_support(cited_evidence: list, prediction: str) -> float:
    scores = [1.0 if e["expected_direction"] == prediction else 0.0
              for e in cited_evidence]
    return sum(scores) / len(scores) if scores else 0.0
```

**Metric 3 — Confidence Drop:**
```python
def confidence_drop(original: float, without: float) -> float:
    return round(original - without, 4)

# Phân loại:
# drop > 0.10  → "likely_faithful"
# drop 0.05-0.10 → "uncertain"
# drop < 0.05  → "possibly_decorative"
```

---

### 3.5 Module 5 — Dashboard (`src/dashboard.py`)

**Công nghệ:** Streamlit + Plotly

**Cấu trúc 4 tab:**

#### Tab 1 — Prediction Overview
- Bảng tất cả prediction (ticker, time, prediction, confidence, label, correct).
- Dropdown lọc theo ticker.
- Bar chart phân bố UP/DOWN/HOLD.
- Metric cards: Accuracy, Avg Confidence, Avg Confidence Drop.

#### Tab 2 — Evidence Explorer
- Dropdown chọn 1 prediction cụ thể.
- Hiển thị: ticker, forecast_time, prediction (với màu: xanh=UP, đỏ=DOWN, vàng=HOLD), confidence.
- Bảng evidence được cite: text, polarity, support_score, news_time.
- ⚠️ Banner đỏ nếu có evidence có news_time > forecast_time.
- Text box hiển thị rationale.

#### Tab 3 — Faithfulness Analysis
- Bar chart confidence drop cho từng prediction.
- Bảng so sánh confidence gốc vs confidence sau khi bỏ evidence, có cột verdict.
- Radar chart: Temporal Validity, Evidence Support, Confidence Drop (normalized), Counterevidence Coverage.
- Bảng phân loại: Likely Faithful vs Possibly Decorative.

#### Tab 4 — Temporal Leakage Monitor
- Bảng tất cả tin bị loại: news_id, ticker, news_time, forecast_time, delta (giờ).
- Metric: tổng số tin bị loại / tổng số tin.
- ⚠️ Cảnh báo nếu `leakage_rate > 0`.
- ✅ Xác nhận nếu `leakage_rate = 0`.

---

## 4. Quyết định công nghệ

| Hạng mục | Lựa chọn | Lý do |
|----------|---------|-------|
| **Ngôn ngữ** | Python 3.10+ | Phổ biến, nhiều thư viện ML/NLP |
| **Data format** | CSV + JSON | Đơn giản, dễ đọc, không cần database |
| **Evidence Extraction** | Rule-based keyword (baseline) | Đủ để demo, dễ kiểm tra, không cần GPU |
| **Forecast Model** | Rule-based sentiment aggregation | Dễ giải thích, phù hợp với bài toán faithfulness |
| **Dashboard** | Streamlit | Nhanh, không cần frontend riêng, dễ deploy |
| **Visualization** | Plotly | Interactive, đẹp, tích hợp tốt với Streamlit |
| **Testing** | pytest | Standard, dễ CI/CD |
| **Version Control** | Git + GitHub | Theo dõi lịch sử, phân công rõ ràng |

**Thư viện Python cần cài:**
```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.1.0
streamlit>=1.20.0
plotly>=5.13.0
pytest>=7.2.0
python-dateutil>=2.8.0
```

---

## 5. Thiết kế Dashboard — Wireframe

```
┌─────────────────────────────────────────────────────────────────┐
│  🏦 Faithful Evidence Forecasting Dashboard                     │
│  ─────────────────────────────────────────────────────────────  │
│  [ Prediction Overview ] [ Evidence Explorer ] [ Faithfulness ] │
│  [ Temporal Leakage ]                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TAB 1: PREDICTION OVERVIEW                                     │
│                                                                 │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │ Accuracy  │  │Avg Conf.  │  │Avg Conf.  │  │ Leakage   │   │
│  │  62.5%    │  │  0.71     │  │Drop: 0.18 │  │ 2 items   │   │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘   │
│                                                                 │
│  Filter: [All tickers ▼]  [All labels ▼]                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Ticker │ Forecast Time      │ Pred  │ Conf │ Label │ OK? │  │
│  │ AAPL   │ 2025-03-12 09:00  │ ▼DOWN │ 0.72 │ DOWN  │ ✅  │  │
│  │ TSLA   │ 2025-03-13 09:00  │ ▼DOWN │ 0.81 │ DOWN  │ ✅  │  │
│  │ NVDA   │ 2025-03-14 09:00  │ ▲UP   │ 0.88 │ UP    │ ✅  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  [Bar chart: UP=3, DOWN=5, HOLD=2]                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Cấu trúc thư mục dự án

```
group_id_project/
├── README.md                          ← Hướng dẫn chạy dự án
├── report.pdf                         ← Báo cáo 5-8 trang
├── demo_video_link.txt                ← Link video demo
├── requirements.txt                   ← Thư viện Python cần cài
│
├── openspec/
│   ├── changes/
│   │   └── faithful-evidence-forecasting/
│   │       ├── proposal.md            ← Đề xuất dự án
│   │       ├── design.md              ← Tài liệu này
│   │       └── tasks.md               ← Phân công task
│   └── specs/
│       └── forecasting/
│           └── spec.md                ← Đặc tả kỹ thuật chi tiết
│
├── data/
│   └── sample_news_price.csv          ← Dataset (>=30 dòng)
│
├── src/
│   ├── retriever.py                   ← Module 1: Temporal Retriever
│   ├── evidence_extractor.py          ← Module 2: Evidence Extractor
│   ├── forecast_model.py              ← Module 3: Forecast Model
│   ├── faithfulness_metrics.py        ← Module 4: Faithfulness Evaluator
│   └── dashboard.py                   ← Module 5: Streamlit Dashboard
│
├── tests/
│   ├── test_temporal_retriever.py     ← Test cho Module 1
│   └── test_metrics.py                ← Test cho Module 4
│
└── outputs/
    ├── prediction_results.csv         ← Kết quả dự báo
    ├── faithfulness_results.csv       ← Kết quả faithfulness
    ├── run_log.json                   ← Agent trace log
    └── figures/
        ├── prediction_distribution.png
        ├── confidence_drop.png
        ├── temporal_leakage_warning.png
        └── faithfulness_radar.png
```

---

## 7. Chiến lược kiểm thử

| Loại test | File | Số test tối thiểu | Mô tả |
|-----------|------|------------------|-------|
| Unit test — Retriever | `tests/test_temporal_retriever.py` | 5 | Kiểm tra filter đúng/sai theo thời gian |
| Unit test — Metrics | `tests/test_metrics.py` | 5 | Kiểm tra tính đúng của 3 metric |
| Integration test | Chạy thủ công | 1 | Chạy toàn bộ pipeline trên dataset |
| Edge case test | Trong 2 file trên | ≥3 | Không có tin, tất cả tin bị loại, v.v. |

**Lệnh chạy test:**
```bash
pytest tests/ -v
```

---

## 8. Lưu ý đạo đức & Giới hạn hệ thống

- Hệ thống chỉ dùng cho **mục đích học tập**.
- Kết quả **không được dùng** để khuyến nghị mua/bán chứng khoán thật.
- Mô hình rule-based đơn giản, accuracy thấp là bình thường — không overclaim.
- Evidence extraction có thể sai với tin mơ hồ, đa nghĩa.
- Kết quả trên dataset nhỏ không đại diện cho thị trường thực.

---

*Tài liệu này thuộc OpenSpec workflow — pha Design. Sau khi được nhóm review và approve, sẽ chuyển sang pha Implementation.*