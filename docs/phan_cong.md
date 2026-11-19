# Phân công công việc – Nhóm 9

Kế hoạch 4 tuần: **20/11/2026 – 17/12/2026**. Bản gốc có công thức và theo dõi trạng thái: file Excel `PhanCong_Nhom9_BigData.xlsx`.

| Tuần | Từ – đến |
|---|---|
| 1 | 20/11 – 26/11 |
| 2 | 27/11 – 03/12 |
| 3 | 04/12 – 10/12 |
| 4 | 11/12 – 17/12 |

| Thành viên | Vai trò | Giờ chính | Giờ hỗ trợ | Tổng | % |
|---|---|---|---|---|---|
| Nguyễn Thị Cẩm Tố | Nhóm trưởng | 62 | 8 | 70 | 25.8% |
| Huỳnh Duy Phúc | Nhóm phó | 58 | 9 | 67 | 24.7% |
| Nguyễn Quang Hoà | Thành viên | 60 | 7 | 67 | 24.7% |
| Nguyễn Thị Tường Vy | Thành viên | 63 | 4 | 67 | 24.7% |

## Danh sách task

| ID | Công việc | Phụ trách | Hỗ trợ (việc) | Phụ thuộc | Tuần | Hạn | Thư mục |
|---|---|---|---|---|---|---|---|
| T01 | Khởi tạo GitHub repo, branch protection, PR/issue template | Tố | Phúc: Tạo issue trên GitHub cho các task trong file phân công | — | 1 | 26/11 | `/ , .github/` |
| T02 | Thiết kế kiến trúc & data contract (schema message Kafka, bảng Hive, định dạng model) | Tố | Hoà: Review tính khả thi phía hạ tầng | — | 1 | 26/11 | `docs/` |
| T03 | Vẽ sơ đồ kiến trúc, luồng dữ liệu; style guide (màu, font) cho báo cáo & slide | Vy | — | T02 | 1 | 26/11 | `docs/diagrams/` |
| T04 | Docker Compose: Kafka, HDFS, Hive Metastore/HiveServer2, Spark | Hoà | Phúc: Chạy thử trên máy cá nhân, ghi lại lỗi cài đặt | — | 1 | 26/11 | `infra/` |
| T05 | Makefile, scripts khởi động & tạo topic; hướng dẫn cài đặt | Phúc | Hoà: Review script hạ tầng | T04 | 1 | 26/11 | `scripts/, docs/` |
| T06 | CI GitHub Actions (lint + pytest) | Hoà | — | T01 | 2 | 03/12 | `.github/` |
| T07 | Hive DDL: transactions_raw, predictions, fraud_alerts (Parquet, partition dt) | Hoà | Tố: Đối chiếu cột với data contract | T02 | 2 | 03/12 | `sql/hive/` |
| T08 | Tải PaySim, đưa dữ liệu raw lên HDFS, nạp bảng Hive transactions_raw | Hoà | — | T04, T07 | 2 | 03/12 | `src/ingestion/` |
| T09 | EDA trên CSV local: phân bố nhãn (~0,13%), loại giao dịch, amount, sai lệch số dư | Tố | Vy: Chốt danh sách biểu đồ cần cho báo cáo/slide | — | 1 | 26/11 | `notebooks/` |
| T10 | Trực quan hóa EDA theo style guide | Vy | Tố: Kiểm tra lại số liệu trên biểu đồ | T09, T03 | 2 | 03/12 | `reports/figures/` |
| T11 | Module feature engineering dùng chung batch & streaming | Tố | Phúc: Viết unit test cho module features | T02 | 1–2 | 03/12 | `src/features/` |
| T12 | Chia train/test theo step; so sánh class weight / undersampling / SMOTE | Tố | — | T11 | 2 | 03/12 | `src/models/` |
| T13 | Baseline Logistic Regression & Random Forest (Spark MLlib) | Phúc | Tố: Review pipeline & cách đánh giá | T12 | 3 | 10/12 | `src/models/` |
| T14 | XGBoost + tuning (scale_pos_weight, early stopping) | Tố | — | T12 | 3 | 10/12 | `src/models/` |
| T15 | Deep Autoencoder: train trên giao dịch bình thường, ngưỡng reconstruction error | Tố | — | T12 | 2–3 | 10/12 | `src/models/` |
| T16 | Kết hợp XGBoost + Autoencoder (hybrid score), chọn ngưỡng theo PR-AUC | Tố | — | T14, T15 | 4 | 17/12 | `src/models/` |
| T17 | Model registry & hàm score() dùng trong streaming | Hoà | Tố: Export model đúng định dạng đã thống nhất | T16 | 4 | 17/12 | `src/models/` |
| T18 | Kafka Producer: phát lại PaySim theo step, chỉnh tốc độ (tx/s) | Phúc | Hoà: Tạo topic, kiểm tra số partition | T02, T04 | 1–2 | 03/12 | `src/producer/` |
| T19 | Spark Structured Streaming: đọc Kafka, parse, feature, chấm điểm (dùng model giả cho tới khi có model registry) | Hoà | Tố: Hướng dẫn tích hợp module features | T11, T18 | 3 | 10/12 | `src/streaming/` |
| T20 | Sink kết quả ra HDFS/Hive (Parquet) + topic fraud-alerts, checkpoint | Hoà | — | T07, T19 | 3–4 | 17/12 | `src/streaming/` |
| T21 | Thiết kế UI/UX dashboard: wireframe → mockup (Figma) | Vy | Phúc: Góp ý khả năng hiện thực bằng Streamlit | T02 | 1–2 | 03/12 | `design/` |
| T22 | Dashboard Streamlit: luồng real-time, bảng cảnh báo, KPI (dùng dữ liệu giả theo data contract) | Phúc | Vy: Review giao diện so với mockup | T21 | 1–3 | 10/12 | `src/dashboard/` |
| T23 | Theme/branding Streamlit, kiểm tra usability | Vy | — | T22 | 3 | 10/12 | `src/dashboard/` |
| T24 | Trang so sánh mô hình & giám sát hiệu năng (đọc metrics.json, benchmark.csv theo data contract) | Phúc | — | T22 | 2–3 | 10/12 | `src/dashboard/pages/` |
| T25 | Thực nghiệm so sánh LR / RF / XGB / AE / Hybrid: PR-AUC, ROC-AUC, Precision, Recall, F1 | Tố | Phúc: Chạy lại baseline trên cùng tập test | T13, T16 | 4 | 17/12 | `reports/experiments/` |
| T26 | Đo hiệu năng: throughput, latency end-to-end theo tốc độ producer & số partition | Hoà | Phúc: Chạy producer ở nhiều tốc độ | T20 | 4 | 17/12 | `reports/benchmark/` |
| T27 | Kiểm thử tích hợp end-to-end & sửa lỗi | Phúc | Hoà: Sửa lỗi phía hạ tầng/streaming | T20, T22, T17 | 4 | 17/12 | `tests/` |
| T28 | Review chéo Pull Request mảng model & streaming | Hoà | — | — | 2–4 | 17/12 | `—` |
| T29 | Viết Mở đầu (3–5 trang) | Vy | Phúc: Góp ý nội dung động lực, phạm vi | — | 1–2 | 03/12 | `report/` |
| T30 | Chương 1 – phần công nghệ: Big Data 5V; HDFS, Hive, Kafka, Spark | Hoà | — | — | 1–2 | 03/12 | `report/` |
| T31 | Chương 1 – phần các phương pháp phát hiện gian lận, lý do lựa chọn | Vy | Tố: Góp ý phần thuật toán | — | 2–3 | 10/12 | `report/` |
| T32 | Chương 2 – phân tích hệ thống & công nghệ (kiến trúc, luồng dữ liệu) | Hoà | — | — | 3–4 | 17/12 | `report/` |
| T33 | Chương 2 – tiền xử lý, xử lý mất cân bằng, mô hình & độ đo | Tố | — | — | 1–4 | 17/12 | `report/` |
| T34 | Chương 3 – mô tả dữ liệu & xây dựng hệ thống (kèm screenshot) | Phúc | Vy: Chụp, chỉnh screenshot dashboard | T27 | 3–4 | 17/12 | `report/` |
| T35 | Chương 3 – thực nghiệm so sánh mô hình & bình luận | Tố | — | T25 | 4 | 17/12 | `report/` |
| T36 | Chương 3 – kết quả hiệu năng hệ thống & bình luận | Hoà | — | T26 | 4 | 17/12 | `report/` |
| T37 | Kết luận, tài liệu tham khảo, phụ lục | Vy | — | T34, T35, T36 | 4 | 17/12 | `report/` |
| T38 | Dàn trang, mục lục, đánh số hình/bảng, xuất PDF (> 40 trang) | Vy | Phúc: Soát lỗi chính tả, định dạng | T29, T30, T31, T32, T33, T34, T35, T36, T37 | 4 | 17/12 | `report/` |
| T39 | Thiết kế & soạn slide 25–30 trang | Vy | Tố: Cung cấp nội dung phần mô hình & kết quả | T03 | 3–4 | 17/12 | `slides/` |
| T40 | Kịch bản & quay video demo giải thích code | Phúc | Hoà: Thuyết minh phần hạ tầng & streaming | T27 | 4 | 17/12 | `video/` |
| T41 | Dựng video, phụ đề, intro/outro | Vy | — | T40 | 4 | 17/12 | `video/` |
| T42 | Rà soát cuối & đóng gói nộp (release repo, PDF, slide, video) | Phúc | Hoà: Kiểm tra repo chạy được từ đầu (clone → make up) | T38, T39, T41 | 4 | 17/12 | `—` |
| T43 | Họp tiến độ hàng tuần, cập nhật tracker, nhắc deadline | Phúc | — | — | 1–4 | 17/12 | `docs/meetings/` |

Nguyên tắc làm việc song song: mọi mảng bám theo [data_contract.md](data_contract.md); phần nào chưa có đầu vào thật thì dùng dữ liệu/model giả (vd. `score(df, dummy=True)`).
