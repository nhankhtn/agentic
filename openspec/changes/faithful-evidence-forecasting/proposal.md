# Proposal — Faithful Evidence-Centric Financial News Forecasting

**Môn học:** Công nghệ mới  
**Nhóm:** [Điền tên nhóm]  
**Thành viên:**
- SV1 — [Họ tên] — [MSSV] — Research & Spec Owner  
- SV2 — [Họ tên] — [MSSV] — ML/NLP Engineer  
- SV3 — [Họ tên] — [MSSV] — Visualization & QA Engineer  

**Ngày tạo:** [Ngày]  
**Trạng thái:** Draft

---

## 1. Bối cảnh & Động lực

### 1.1 Vấn đề thực tế

Hiện nay có nhiều hệ thống AI có khả năng đọc tin tức tài chính và đưa ra dự báo xu hướng cổ phiếu (tăng/giảm/đi ngang). Tuy nhiên, một vấn đề nghiêm trọng thường bị bỏ qua: **mô hình có thể đưa ra lời giải thích nghe rất hợp lý nhưng lời giải thích đó chưa chắc phản ánh đúng nguyên nhân khiến mô hình ra quyết định.**

Ví dụ minh họa:
- Mô hình dự báo **NVDA tăng**, giải thích rằng vì có tin "NVIDIA công bố chip AI thế hệ mới".
- Nhưng khi bỏ tin đó ra khỏi input, mô hình vẫn dự báo tăng với confidence gần như không đổi (0.88 → 0.86).
- Điều này cho thấy evidence được đưa ra chỉ là **lời giải thích hậu nghiệm**, không thật sự quyết định prediction.

Ngược lại, khi mô hình dự báo **TSLA giảm** do tin "Tesla phải thu hồi xe do lỗi phần mềm", và khi bỏ tin này đi confidence giảm từ 0.81 xuống 0.55 — đây là dấu hiệu evidence thật sự quan trọng (faithful).

### 1.2 Câu hỏi nghiên cứu trung tâm

> **Khi một mô hình dự báo stock movement từ news, liệu evidence mà nó đưa ra có thật sự quyết định prediction không?**

### 1.3 Tại sao vấn đề này quan trọng?

| Vấn đề | Hệ quả |
|--------|--------|
| Evidence không faithful | Người dùng tin vào lý do sai, quyết định đầu tư sai |
| Temporal leakage | Kết quả thí nghiệm ảo, không áp dụng được thực tế |
| Bỏ qua counterevidence | Mô hình thiên lệch, chỉ cite tin thuận chiều |
| Accuracy cao ≠ đáng tin | Mô hình đúng nhưng vì lý do sai |

---

## 2. Mục tiêu đồ án

### 2.1 Mục tiêu chính
Xây dựng một **prototype nhỏ** để:
1. Dự báo xu hướng cổ phiếu (UP/DOWN/HOLD) từ tin tức tài chính.
2. Trích xuất evidence mà mô hình dùng để ra quyết định.
3. **Kiểm chứng tính faithful** của evidence đó bằng các metric định lượng.
4. Trực quan hóa kết quả trên dashboard có thể tương tác.

### 2.2 Mục tiêu học thuật
- Hiểu sự khác biệt giữa **prediction accuracy** và **explanation faithfulness**.
- Biết áp dụng **Agentic AI vào SDLC** có kiểm soát (có quality gate, human review).
- Biết đặc tả hệ thống ML/NLP theo hướng kiểm chứng bằng **OpenSpec**.
- Biết phát hiện và xử lý lỗi **temporal leakage** trong bài toán tài chính.

### 2.3 Ngoài phạm vi đồ án
- **Không** xây dựng hệ thống giao dịch thật.
- **Không** khuyến nghị mua/bán chứng khoán thật.
- **Không** đảm bảo kết quả thí nghiệm đại diện cho thị trường thực.
- Dataset nhỏ/mô phỏng chưa đủ để áp dụng thực tế.

---

## 3. Bài toán kỹ thuật

### 3.1 Input

```
ticker:        Mã cổ phiếu (vd: AAPL, TSLA, NVDA)
forecast_time: Thời điểm hệ thống ra dự báo (vd: 2025-03-12 09:00)
news:          Danh sách tin tức, mỗi tin gồm:
                 - news_id, news_time, title, text
price_features: Dữ liệu giá lịch sử:
                 - price_5d_return, volume_change
```

### 3.2 Output

```
prediction:    UP | DOWN | HOLD
confidence:    float [0.0 - 1.0]
evidence:      Danh sách evidence được cite:
                 - evidence_text, polarity, expected_direction, support_score
faithfulness:  Các metric kiểm chứng:
                 - temporal_validity, evidence_support, confidence_drop
```

### 3.3 Pipeline tổng quát

```
News + Price Data
      │
      ▼
Temporal Retriever   ──→  loại tin có news_time >= forecast_time
      │
      ▼
Evidence Extractor   ──→  trích evidence_text, polarity, expected_direction
      │
      ▼
Evidence Selector    ──→  chọn pro evidence & counterevidence
      │
      ▼
Forecast Model       ──→  prediction + confidence + cited_evidence
      │
      ▼
Faithfulness Evaluator ─→  temporal_validity, evidence_support, confidence_drop
      │
      ▼
Visualization Dashboard ─→ bảng, biểu đồ, cảnh báo leakage
```

---

## 4. Agentic AI trong SDLC

### 4.1 Vai trò của AI Agent

Đồ án áp dụng Agentic AI không chỉ để viết code, mà như một tác nhân hỗ trợ có kiểm soát trong từng pha của SDLC.

| Pha SDLC | AI Agent hỗ trợ | Human kiểm soát |
|----------|----------------|-----------------|
| Requirement | Tạo user stories, acceptance criteria | Kiểm tra yêu cầu có rõ và test được không |
| Design | Đề xuất kiến trúc, data schema, dashboard layout | Chọn thiết kế vừa sức nhóm |
| Implementation | Sinh code mẫu, gợi ý hàm, giải thích thuật toán | Đọc hiểu, chỉnh sửa, không dùng mù quáng |
| Testing | Sinh test case, dữ liệu lỗi, edge case | Tự chạy test, phân tích kết quả |
| Evaluation | Gợi ý metric, phân tích kết quả | Không overclaim, ghi rõ limitation |

### 4.2 Nguyên tắc sử dụng AI Agent
- Mọi output của AI agent đều phải qua **human review** trước khi merge.
- Ghi lại **trace log** cho mỗi lần dùng agent (task, input, output, review, quality gate).
- Không để agent tự quyết định những gì ảnh hưởng đến kết quả thí nghiệm.

---

## 5. Kết quả mong đợi

| Sản phẩm | Mô tả |
|----------|-------|
| **Prototype** | Pipeline Python end-to-end chạy được |
| **OpenSpec** | proposal, design, tasks, spec đầy đủ |
| **Dashboard** | Streamlit app với 4 tab: prediction, evidence, faithfulness, leakage |
| **Báo cáo** | PDF 5–8 trang, phân tích case đúng/sai, limitations |
| **Demo video** | ~5 phút, theo kịch bản remove cited evidence |
| **Test suite** | pytest với ít nhất 10 test cases |

---

## 6. Phân công nhóm

| Vai trò | Thành viên | Sản phẩm chính |
|---------|-----------|----------------|
| **Research & Spec Owner** | SV1 | proposal.md, spec.md, metric_definition.md, phần 1–3 báo cáo |
| **ML/NLP Engineer** | SV2 | data.csv, retriever.py, evidence_extractor.py, forecast_model.py, faithfulness_metrics.py, results.csv |
| **Visualization & QA** | SV3 | dashboard.py, figures/, tests/, demo video |

> ⚠️ Lưu ý quan trọng: Ba sinh viên đều phải hiểu toàn bộ hệ thống. Trong buổi phản biện, bất kỳ thành viên nào cũng có thể bị hỏi về bất kỳ phần nào.

---

## 7. Timeline dự kiến

| Tuần | Phase | Công việc chính | Người phụ trách |
|------|-------|----------------|-----------------|
| 1 | Phase 0–1 | Setup môi trường, viết OpenSpec | Cả nhóm (SV1 lead) |
| 2 | Phase 2–3 | Tạo dataset, viết Temporal Retriever | SV2 lead |
| 3 | Phase 4–5 | Evidence Extractor, Forecast Model | SV2 lead |
| 4 | Phase 6–8 | Faithfulness Metrics, Testing | SV2 + SV3 |
| 5 | Phase 7 | Dashboard, figures | SV3 lead |
| 6 | Phase 9–11 | Báo cáo, demo, phần nâng cao | Cả nhóm (SV1 lead) |
| 7 | Buffer | Sửa lỗi, review, nộp bài | Cả nhóm |

---

## 8. Rủi ro & Biện pháp

| Rủi ro | Khả năng xảy ra | Biện pháp |
|--------|----------------|-----------|
| Dataset mô phỏng không đủ đa dạng | Cao | Chuẩn bị sẵn thêm 20 dòng dữ liệu backup |
| Mô hình rule-based accuracy quá thấp | Trung bình | Chấp nhận — trọng tâm là faithfulness, không phải accuracy |
| Dashboard bị lỗi khi demo | Thấp | Test kỹ trên nhiều máy, có notebook backup |
| Thành viên không hiểu phần của người khác | Trung bình | Họp review nội bộ trước ngày nộp |
| AI agent sinh code sai logic | Cao | Luôn đọc hiểu và chạy test sau mỗi lần dùng agent |

---

## 9. Tài liệu tham khảo

- OpenSpec workflow: https://github.com/Fission-AI/OpenSpec/
- FinBERT: https://huggingface.co/ProsusAI/finbert
- Financial PhraseBank dataset: Malo et al., 2014
- Yahoo Finance API: https://pypi.org/project/yfinance/
- Streamlit documentation: https://docs.streamlit.io/
- Faithful Explanations of Black-box NLP Models: Jacovi & Goldberg, 2020

---

*Tài liệu này thuộc OpenSpec workflow — pha Proposal. Sau khi được nhóm review và approve, sẽ chuyển sang pha Design.*