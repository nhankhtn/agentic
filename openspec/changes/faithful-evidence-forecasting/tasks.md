# Tasks — Faithful Evidence-Centric Financial News Forecasting

**Phiên bản:** 1.0  
**Ngày tạo:** [Ngày]  
**Cập nhật lần cuối:** [Ngày]  
**Tài liệu liên quan:** proposal.md, design.md

---

## Quy ước trạng thái

| Ký hiệu | Ý nghĩa |
|---------|---------|
| `⬜ TODO` | Chưa bắt đầu |
| `🔄 IN PROGRESS` | Đang làm |
| `👀 REVIEW` | Đã làm, chờ review |
| `✅ DONE` | Hoàn thành và được approve |
| `❌ BLOCKED` | Bị chặn, cần unblock |

---

## Quy ước AI Agent

| Ký hiệu | Ý nghĩa |
|---------|---------|
| `🤖 AI-assisted` | Task có dùng AI agent hỗ trợ |
| `👤 Human-only` | Task do con người làm hoàn toàn |
| `✔️ QG-passed` | Đã qua quality gate (human review) |

---

## PHASE 0 — Khởi động & Lập kế hoạch

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P0-01 | Đọc và hiểu toàn bộ đề bài | Cả nhóm | 👤 | ⬜ TODO | [Ngày] | Mỗi người tóm tắt 1 trang hiểu biết của mình |
| P0-02 | Họp nhóm, thống nhất phân công vai trò | Cả nhóm | 👤 | ⬜ TODO | [Ngày] | Ghi biên bản họp |
| P0-03 | Tạo repository GitHub và cấu trúc thư mục | SV3 | 👤 | ⬜ TODO | [Ngày] | Dùng cấu trúc trong design.md |
| P0-04 | Cài đặt môi trường Python, requirements.txt | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI gợi ý thư viện, human kiểm tra |
| P0-05 | Thống nhất naming convention và git workflow | SV1 | 👤 | ⬜ TODO | [Ngày] | Ghi vào README.md |
| P0-06 | Tạo file README.md bộ khung ban đầu | SV1 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI sinh template, human điền thông tin thật |

**Agent trace cần ghi:** P0-04, P0-06

---

## PHASE 1 — OpenSpec & Đặc tả yêu cầu

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P1-01 | Viết proposal.md (bài toán, động lực, mục tiêu, timeline) | SV1 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI gợi ý cấu trúc, human viết nội dung thật |
| P1-02 | Viết design.md (kiến trúc, schema, wireframe dashboard) | SV1 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI gợi ý diagram, human xác nhận logic |
| P1-03 | Viết tasks.md (file này) | SV1 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |
| P1-04 | Viết specs/forecasting/spec.md (user stories, acceptance criteria) | SV1 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Ít nhất 5 user story + AC đầy đủ |
| P1-05 | Review OpenSpec: SV2 và SV3 đọc, góp ý | SV2, SV3 | 👤 | ⬜ TODO | [Ngày] | Đảm bảo cả nhóm hiểu spec |
| P1-06 | Revise và approve OpenSpec sau review | SV1 | 👤 | ⬜ TODO | [Ngày] | Merge vào main branch |
| P1-07 | Viết metric_definition.md: định nghĩa 3 metric faithfulness | SV1 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Dùng cho báo cáo phần 6 |

**Agent trace cần ghi:** P1-01, P1-02, P1-03, P1-04, P1-07

---

## PHASE 2 — Chuẩn bị dữ liệu

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P2-01 | Thiết kế cấu trúc CSV dataset (cột, kiểu dữ liệu) | SV1, SV2 | 👤 | ⬜ TODO | [Ngày] | Theo schema trong design.md |
| P2-02 | Tạo 30+ dòng dữ liệu mô phỏng (tối thiểu) | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI gợi ý tin mẫu, human kiểm tra tính hợp lý |
| P2-03 | Đảm bảo dataset có đủ: 3 ticker, 3 nhãn, 5+ temporal leakage rows | SV2 | 👤 | ⬜ TODO | [Ngày] | Kiểm tra bằng script thống kê |
| P2-04 | Thêm ít nhất 3 cặp tin counterevidence vào dataset | SV2 | 👤 | ⬜ TODO | [Ngày] | Cùng ticker + ngày, có cả tin tốt và xấu |
| P2-05 | Viết script tiền xử lý: chuẩn hóa datetime, kiểm tra null | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI sinh code mẫu, human test và chỉnh |
| P2-06 | Tạo bảng thống kê mô tả dataset | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Đưa vào báo cáo phần 4 |
| P2-07 | Review dataset: SV3 kiểm tra có đủ edge case không | SV3 | 👤 | ⬜ TODO | [Ngày] | Dùng checklist trong requirement.md |

**Agent trace cần ghi:** P2-02, P2-05, P2-06

---

## PHASE 3 — Temporal Retriever

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P3-01 | Viết hàm `filter_news_by_time()` trong `retriever.py` | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI sinh code mẫu, human review logic |
| P3-02 | Thêm WARNING log khi phát hiện temporal leakage | SV2 | 👤 | ⬜ TODO | [Ngày] | Format log theo design.md |
| P3-03 | Viết docstring và type hint đầy đủ cho retriever.py | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |
| P3-04 | Viết 5 unit test trong `test_temporal_retriever.py` | SV3 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI gợi ý test case, human thêm edge case |
| P3-05 | Chạy pytest, đảm bảo tất cả test pass | SV3 | 👤 | ⬜ TODO | [Ngày] | Ghi kết quả vào test report |
| P3-06 | Tích hợp retriever vào pipeline chính | SV2 | 👤 | ⬜ TODO | [Ngày] | Kiểm tra output đúng format |

**Agent trace cần ghi:** P3-01, P3-03, P3-04

---

## PHASE 4 — Evidence Extraction

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P4-01 | Xây dựng từ điển keyword negative/positive/neutral | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI gợi ý keyword, human bổ sung theo domain |
| P4-02 | Viết hàm `extract_evidence()` trong `evidence_extractor.py` | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI sinh code, human kiểm tra logic phân loại |
| P4-03 | Xử lý trường hợp biên: tin quá ngắn, không có keyword | SV2 | 👤 | ⬜ TODO | [Ngày] | Gán neutral, log warning |
| P4-04 | Chạy extractor trên toàn bộ dataset, kiểm tra coverage | SV2 | 👤 | ⬜ TODO | [Ngày] | Cần ≥80% tin extract được ≥1 evidence |
| P4-05 | Chuẩn bị bảng 5 ví dụ đúng + 5 ví dụ sai/biên | SV2, SV1 | 👤 | ⬜ TODO | [Ngày] | Đưa vào báo cáo phần 5 |
| P4-06 | Review extractor: SV3 kiểm tra 10 tin mẫu thủ công | SV3 | 👤 | ⬜ TODO | [Ngày] | So sánh output của code vs phán đoán của người |
| P4-07 | Viết docstring và type hint cho evidence_extractor.py | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |

**Agent trace cần ghi:** P4-01, P4-02, P4-07

---

## PHASE 5 — Forecast Model

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P5-01 | Viết hàm `predict()` trong `forecast_model.py` | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Rule-based baseline, AI hỗ trợ code |
| P5-02 | Viết hàm `compute_confidence_drop()` | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Quan trọng nhất — cần test kỹ |
| P5-03 | Tích hợp price_features vào score tính prediction | SV2 | 👤 | ⬜ TODO | [Ngày] | Theo thiết kế trong design.md |
| P5-04 | Chạy predict trên toàn dataset, lưu ra `prediction_results.csv` | SV2 | 👤 | ⬜ TODO | [Ngày] | Kiểm tra output đúng format |
| P5-05 | Tính accuracy và confusion matrix | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Dùng sklearn.metrics |
| P5-06 | Viết giải thích chi tiết cho 1 prediction cụ thể | SV1, SV2 | 👤 | ⬜ TODO | [Ngày] | Đưa vào báo cáo phần 5 |
| P5-07 | Viết docstring và type hint cho forecast_model.py | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |

**Agent trace cần ghi:** P5-01, P5-02, P5-05, P5-07

---

## PHASE 6 — Faithfulness Metrics

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P6-01 | Viết hàm `temporal_validity()` trong `faithfulness_metrics.py` | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |
| P6-02 | Viết hàm `evidence_support()` | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |
| P6-03 | Viết hàm `confidence_drop()` và verdict classifier | SV2 | 👤 | ⬜ TODO | [Ngày] | Drop >0.1 = likely_faithful, <0.05 = decorative |
| P6-04 | Chạy metrics trên toàn dataset, lưu ra `faithfulness_results.csv` | SV2 | 👤 | ⬜ TODO | [Ngày] | Kiểm tra output đúng format |
| P6-05 | Tạo bảng tổng hợp: mean của 3 metric trên toàn dataset | SV2, SV1 | 👤 | ⬜ TODO | [Ngày] | Đưa vào báo cáo phần 6 |
| P6-06 | Viết 5 unit test trong `test_metrics.py` | SV3 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI gợi ý test, human thêm edge case |
| P6-07 | (Nâng cao B1) Viết hàm sufficiency test | SV2 | 👤 | ⬜ TODO | [Ngày] | Chỉ dùng cited evidence để dự báo lại |
| P6-08 | (Nâng cao B1) Viết hàm counterfactual perturbation | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Thay evidence = neutral news |
| P6-09 | (Nâng cao B2) Viết hàm counterevidence_coverage() | SV2 | 👤 | ⬜ TODO | [Ngày] | Tìm tin ngược chiều, tính coverage |
| P6-10 | (Nâng cao B3) Viết hàm market_consistency() | SV2 | 👤 | ⬜ TODO | [Ngày] | So evidence với next-day return thực tế |

**Agent trace cần ghi:** P6-01, P6-02, P6-06, P6-08

---

## PHASE 7 — Visualization Dashboard

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P7-01 | Setup Streamlit app skeleton (4 tab) | SV3 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI sinh code khung, human thêm logic |
| P7-02 | Viết Tab 1 — Prediction Overview (bảng + bar chart + metrics) | SV3 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |
| P7-03 | Viết Tab 2 — Evidence Explorer (dropdown + bảng + cảnh báo) | SV3 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Banner đỏ nếu có temporal leakage |
| P7-04 | Viết Tab 3 — Faithfulness Analysis (bar + radar chart + bảng) | SV3 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | Radar chart cần 4 trục |
| P7-05 | Viết Tab 4 — Temporal Leakage Monitor (bảng + cảnh báo) | SV3 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |
| P7-06 | Export 4 hình tĩnh vào `outputs/figures/` | SV3 | 👤 | ⬜ TODO | [Ngày] | PNG, độ phân giải ≥800px |
| P7-07 | Test dashboard chạy được trên máy SV1 và SV2 | SV3 | 👤 | ⬜ TODO | [Ngày] | Cross-machine compatibility |
| P7-08 | Chuẩn bị kịch bản demo 5 phút, tập thuyết trình | Cả nhóm | 👤 | ⬜ TODO | [Ngày] | Theo kịch bản trong requirement.md |

**Agent trace cần ghi:** P7-01, P7-02, P7-03, P7-04, P7-05

---

## PHASE 8 — Testing & QA

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P8-01 | Finalize `test_temporal_retriever.py` (≥5 test, pass hết) | SV3 | 👤 | ⬜ TODO | [Ngày] | Chạy `pytest tests/ -v` |
| P8-02 | Finalize `test_metrics.py` (≥5 test, pass hết) | SV3 | 👤 | ⬜ TODO | [Ngày] | — |
| P8-03 | Test pipeline end-to-end trên toàn dataset | SV2, SV3 | 👤 | ⬜ TODO | [Ngày] | Không có runtime error |
| P8-04 | Kiểm tra edge case: ticker không có tin nào | SV3 | 👤 | ⬜ TODO | [Ngày] | Hệ thống không crash |
| P8-05 | Kiểm tra edge case: tất cả tin bị loại do leakage | SV3 | 👤 | ⬜ TODO | [Ngày] | Prediction fallback hợp lý |
| P8-06 | Kiểm tra output files được tạo đúng format | SV3 | 👤 | ⬜ TODO | [Ngày] | Dùng checklist schema trong design.md |
| P8-07 | (Nâng cao B4) Tạo `run_log.json` với ≥6 agent trace entries | SV1 | 👤 | ⬜ TODO | [Ngày] | 2 entry mỗi agent role |

**Agent trace cần ghi:** P8-07

---

## PHASE 9 — Báo cáo & Demo

| ID | Task | Người phụ trách | AI? | Trạng thái | Deadline | Ghi chú |
|----|------|----------------|-----|-----------|----------|---------|
| P9-01 | Viết báo cáo phần 1–3 (giới thiệu, research gap, thiết kế SDLC) | SV1 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | AI hỗ trợ outline, human viết nội dung |
| P9-02 | Viết báo cáo phần 4–5 (dữ liệu, pipeline kỹ thuật) | SV2 | 🤖 AI-assisted | ⬜ TODO | [Ngày] | — |
| P9-03 | Viết báo cáo phần 6–7 (metric, kết quả thực nghiệm) | SV1, SV2 | 👤 | ⬜ TODO | [Ngày] | Đính kèm bảng và biểu đồ thật |
| P9-04 | Viết báo cáo phần 8–9 (case analysis, limitations) | SV1 | 👤 | ⬜ TODO | [Ngày] | Ít nhất 3 limitation cụ thể |
| P9-05 | Viết phụ lục: agent trace, prompt mẫu, test cases | SV1, SV3 | 👤 | ⬜ TODO | [Ngày] | — |
| P9-06 | Review báo cáo lần 1 — SV2 và SV3 đọc và góp ý | SV2, SV3 | 👤 | ⬜ TODO | [Ngày] | — |
| P9-07 | Revise và finalize báo cáo, export PDF | SV1 | 👤 | ⬜ TODO | [Ngày] | ≤8 trang, không tính phụ lục |
| P9-08 | Cập nhật README.md hoàn chỉnh | SV3 | 👤 | ⬜ TODO | [Ngày] | Lệnh cài đặt + chạy đầy đủ |
| P9-09 | Quay video demo (~5 phút) | SV3 (quay), SV2 (demo) | 👤 | ⬜ TODO | [Ngày] | Upload Google Drive / YouTube |
| P9-10 | Tạo file `demo_video_link.txt` | SV3 | 👤 | ⬜ TODO | [Ngày] | — |
| P9-11 | Final checklist trước khi nộp | Cả nhóm | 👤 | ⬜ TODO | [Ngày] | Dùng checklist trong requirement.md |
| P9-12 | Nộp bài | Cả nhóm | 👤 | ⬜ TODO | [Ngày] | ⚠️ Deadline cứng |

**Agent trace cần ghi:** P9-01, P9-02

---

## Tổng hợp theo người phụ trách

### SV1 — Research & Spec Owner

| ID | Task | Deadline | Trạng thái |
|----|------|----------|-----------|
| P0-05 | Naming convention và git workflow | | ⬜ |
| P0-06 | README.md bộ khung | | ⬜ |
| P1-01 | proposal.md | | ⬜ |
| P1-02 | design.md | | ⬜ |
| P1-03 | tasks.md | | ⬜ |
| P1-04 | spec.md | | ⬜ |
| P1-07 | metric_definition.md | | ⬜ |
| P2-01 | Thiết kế schema CSV (cùng SV2) | | ⬜ |
| P5-06 | Giải thích chi tiết 1 prediction (cùng SV2) | | ⬜ |
| P6-05 | Bảng tổng hợp metric (cùng SV2) | | ⬜ |
| P8-07 | run_log.json | | ⬜ |
| P9-01 | Báo cáo phần 1–3 | | ⬜ |
| P9-03 | Báo cáo phần 6–7 (cùng SV2) | | ⬜ |
| P9-04 | Báo cáo phần 8–9 | | ⬜ |
| P9-05 | Phụ lục (cùng SV3) | | ⬜ |
| P9-07 | Finalize báo cáo, export PDF | | ⬜ |

### SV2 — ML/NLP Engineer

| ID | Task | Deadline | Trạng thái |
|----|------|----------|-----------|
| P0-04 | requirements.txt | | ⬜ |
| P2-01 | Thiết kế schema CSV (cùng SV1) | | ⬜ |
| P2-02 | Tạo dataset 30+ dòng | | ⬜ |
| P2-03 | Kiểm tra đủ ticker/nhãn/leakage | | ⬜ |
| P2-04 | Thêm counterevidence pairs | | ⬜ |
| P2-05 | Script tiền xử lý | | ⬜ |
| P2-06 | Bảng thống kê mô tả dataset | | ⬜ |
| P3-01 | `filter_news_by_time()` | | ⬜ |
| P3-02 | WARNING log | | ⬜ |
| P3-03 | Docstring retriever.py | | ⬜ |
| P3-06 | Tích hợp retriever vào pipeline | | ⬜ |
| P4-01 | Từ điển keyword | | ⬜ |
| P4-02 | `extract_evidence()` | | ⬜ |
| P4-03 | Edge case extractor | | ⬜ |
| P4-04 | Chạy trên toàn dataset | | ⬜ |
| P4-05 | Bảng ví dụ đúng/sai (cùng SV1) | | ⬜ |
| P4-07 | Docstring evidence_extractor.py | | ⬜ |
| P5-01 | `predict()` | | ⬜ |
| P5-02 | `compute_confidence_drop()` | | ⬜ |
| P5-03 | Tích hợp price_features | | ⬜ |
| P5-04 | Chạy predict trên dataset | | ⬜ |
| P5-05 | Accuracy + confusion matrix | | ⬜ |
| P5-07 | Docstring forecast_model.py | | ⬜ |
| P6-01 → P6-05 | Faithfulness metrics (3 metric cơ bản) | | ⬜ |
| P6-07 → P6-10 | (Nâng cao) Advanced metrics | | ⬜ |
| P9-02 | Báo cáo phần 4–5 | | ⬜ |
| P9-03 | Báo cáo phần 6–7 (cùng SV1) | | ⬜ |

### SV3 — Visualization & QA Engineer

| ID | Task | Deadline | Trạng thái |
|----|------|----------|-----------|
| P0-03 | Tạo repository, cấu trúc thư mục | | ⬜ |
| P2-07 | Review dataset | | ⬜ |
| P3-04 | `test_temporal_retriever.py` | | ⬜ |
| P3-05 | Chạy pytest retriever | | ⬜ |
| P4-06 | Review extractor thủ công | | ⬜ |
| P6-06 | `test_metrics.py` | | ⬜ |
| P7-01 → P7-08 | Dashboard (toàn bộ) | | ⬜ |
| P8-01 → P8-06 | Testing & QA | | ⬜ |
| P9-05 | Phụ lục (cùng SV1) | | ⬜ |
| P9-08 | README.md hoàn chỉnh | | ⬜ |
| P9-09 | Quay video demo | | ⬜ |
| P9-10 | demo_video_link.txt | | ⬜ |
| P9-11 | Final checklist | | ⬜ |

---

## Agent Trace Log Template

Mỗi khi dùng AI agent (ChatGPT, Cursor, Copilot, Claude...), ghi vào `outputs/run_log.json`:

```json
{
  "run_id": "R001",
  "task_id": "P3-01",
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "agent_role": "Coding Agent",
  "tool_used": "ChatGPT / Cursor / GitHub Copilot",
  "task": "Mô tả task ngắn gọn",
  "input_summary": "Input đưa cho agent (prompt tóm tắt)",
  "output_summary": "Output agent trả về (tóm tắt)",
  "human_review": "accepted / accepted with edits / rejected",
  "quality_gate": "passed / failed",
  "notes": "Ghi chú thêm nếu có"
}
```

**Danh sách agent role:**
- `Research Agent` — Tìm kiếm thông tin, tổng hợp tài liệu, gợi ý metric
- `Coding Agent` — Sinh code, gợi ý refactor, giải thích thuật toán
- `Testing Agent` — Sinh test case, gợi ý edge case, review test coverage

---

## Checklist nộp bài

- [ ] README.md có hướng dẫn chạy đầy đủ
- [ ] OpenSpec proposal/design/tasks/spec đầy đủ
- [ ] Dataset ≥30 dòng, đúng format
- [ ] `retriever.py` chạy được, có log cảnh báo leakage
- [ ] `evidence_extractor.py` chạy được, có coverage ≥80%
- [ ] `forecast_model.py` dự báo được UP/DOWN/HOLD
- [ ] `faithfulness_metrics.py` tính được 3 metric cơ bản
- [ ] `dashboard.py` chạy được bằng `streamlit run`
- [ ] 4 hình PNG trong `outputs/figures/`
- [ ] `pytest tests/ -v` không có lỗi
- [ ] Báo cáo PDF 5–8 trang
- [ ] Video demo ~5 phút, link trong demo_video_link.txt
- [ ] `run_log.json` có ≥6 agent trace entries
- [ ] **Không có tin tương lai nào được dùng trong thí nghiệm**

---

*Tài liệu này thuộc OpenSpec workflow — pha Tasks. Cập nhật trạng thái sau mỗi buổi làm việc nhóm.*