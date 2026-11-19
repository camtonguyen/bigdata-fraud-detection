# Phát hiện gian lận giao dịch thanh toán di động thời gian thực

**Môn:** Công nghệ dữ liệu lớn (Big Data) · **Nhóm 9**

Hệ thống Kafka – Spark Structured Streaming – HDFS/Hive kết hợp mô hình XGBoost + Deep Autoencoder,
chấm điểm gian lận cho từng giao dịch và cảnh báo trên dashboard Streamlit. Dữ liệu: PaySim (6.362.620 giao dịch, ~0,13% gian lận).

## Thành viên

| MSSV | Họ và tên | Vai trò | Mảng phụ trách |
|---|---|---|---|
| 26410134 | Nguyễn Thị Cẩm Tố | Nhóm trưởng | Dữ liệu & mô hình: kiến trúc, data contract, EDA, features, XGBoost, Autoencoder, hybrid, thực nghiệm |
| 26410092 | Huỳnh Duy Phúc | Nhóm phó | Producer, baseline LR/RF, dashboard Streamlit, kiểm thử end-to-end, video, đóng gói nộp |
| 26410042 | Nguyễn Quang Hoà | Thành viên | Hạ tầng & streaming: Docker, Hive, nạp dữ liệu, CI, Spark Streaming, sink, model registry, benchmark |
| 26410158 | Nguyễn Thị Tường Vy | Thành viên | Thiết kế & trình bày: sơ đồ, mockup, trực quan EDA, theme dashboard, slide, dàn trang, dựng video |

Kế hoạch 4 tuần (20/11 – 17/12/2026), chi tiết từng task: [docs/phan_cong.md](docs/phan_cong.md).

## Kiến trúc

```
PaySim CSV ──► Producer (Python) ──► Kafka [transactions]
                                          │
                                          ▼
                         Spark Structured Streaming
                   (parse → features → XGBoost + Autoencoder)
                     │                    │
                     ▼                    ▼
           HDFS/Hive (Parquet)    Kafka [fraud-alerts]
                     │                    │
                     └──────► Streamlit Dashboard
```

Chi tiết: [docs/architecture.md](docs/architecture.md)

## Cấu trúc thư mục

```
.
├── .github/                 # CI (lint + pytest), PR/issue template, CODEOWNERS
├── infra/                   # docker-compose: Kafka, HDFS, Spark (+ Dockerfile Spark)
├── scripts/                 # tải dữ liệu, khởi tạo HDFS/topic Kafka
├── sql/hive/                # DDL bảng Hive (external, Parquet trên HDFS) — chạy bằng make tables
├── data/                    # raw/processed (không commit), sample nhỏ để test
├── src/
│   ├── common/              # config, schema, spark session
│   ├── ingestion/           # đưa PaySim lên HDFS/Hive
│   ├── features/            # feature engineering (dùng chung batch & streaming)
│   ├── models/              # LR, RF, XGBoost, Autoencoder, hybrid, registry
│   ├── producer/            # Kafka producer phát lại PaySim
│   ├── streaming/           # Spark Structured Streaming job + sinks
│   └── dashboard/           # Streamlit app
├── notebooks/               # EDA, thử nghiệm
├── models/registry/         # model đã huấn luyện (không commit file lớn)
├── tests/                   # pytest
├── reports/                 # hình, kết quả thực nghiệm, benchmark
├── docs/                    # kiến trúc, data contract, phân công, cài đặt, biên bản họp, sơ đồ
├── design/                  # mockup dashboard (Figma export)
├── report/                  # quyển báo cáo (Word/LaTeX + PDF)
├── slides/                  # slide 25–30 trang
└── video/                   # kịch bản + link video demo
```

## Chạy nhanh

```bash
make up              # khởi động Kafka, HDFS, Spark (lần đầu build image Spark)
make data            # tải PaySim (cần Kaggle API) và đưa lên HDFS
make tables          # tạo bảng Hive fraud.* (external, Parquet trên HDFS)
make train           # huấn luyện offline
make stream          # chạy Spark Structured Streaming
make produce         # phát giao dịch vào Kafka
make dashboard       # mở dashboard tại http://localhost:8501
```

Xem [docs/setup.md](docs/setup.md).

## Quy ước Git

- Nhánh `main` được bảo vệ; mọi thay đổi qua Pull Request, ít nhất 1 người review.
- Đặt tên nhánh: `feat/<mảng>-<mô-tả>`, `fix/...`, `docs/...` (vd: `feat/streaming-watermark`).
- Commit theo Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- Mỗi PR gắn mã task trong file phân công (T01…T43, xem [docs/phan_cong.md](docs/phan_cong.md)).
- Không commit dữ liệu thô, model lớn, file `.env`.
