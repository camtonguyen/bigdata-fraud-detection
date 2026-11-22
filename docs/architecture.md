# Kiến trúc hệ thống (T02 – Tố; sơ đồ T03 – Vy)

## Thành phần

| Lớp | Công nghệ | Vai trò |
|---|---|---|
| Nguồn | PaySim CSV + Producer Python | Phát lại giao dịch theo `step`, chỉnh tốc độ |
| Truyền tải | Apache Kafka (`transactions`, `fraud-alerts`) | Hàng đợi bền vững, phân partition theo `nameOrig` |
| Xử lý | Spark Structured Streaming | Parse JSON, watermark, feature online, chấm điểm |
| Mô hình | XGBoost + Deep Autoencoder (hybrid) | Phân loại có giám sát + phát hiện bất thường |
| Lưu trữ | HDFS + Hive (Parquet, partition `dt`) | Lưu raw, predictions, alerts. Hive = Hive support của Spark (metastore Derby nhúng), bảng external trỏ vào Parquet trên HDFS |
| Hiển thị | Streamlit | Cảnh báo real-time, so sánh mô hình, hiệu năng |

## Luồng batch (huấn luyện)
HDFS raw → Spark (features, split theo step) → LR / RF / XGB / AE → models/registry

## Luồng streaming (suy luận)
Producer → Kafka → Spark Streaming → (Hive predictions, Kafka fraud-alerts) → Dashboard

## Nguyên tắc
- Feature dùng chung một module (`src/features`) cho batch và streaming.
- Split theo thời gian; scaler/ngưỡng chỉ fit trên train.
- Checkpoint streaming trên HDFS để phục hồi khi lỗi.

## Sơ đồ luồng

```
PaySim CSV ──► Producer ──► Kafka [transactions] ──► Spark Structured Streaming
                                                        │  parse → build_features → score()
                                          ┌─────────────┴─────────────┐
                                          ▼                           ▼
                        HDFS/Hive Parquet (predictions)     Kafka [fraud-alerts] ──► Streamlit
                        HDFS/Hive Parquet (fraud_alerts)
Batch: HDFS raw ──► Spark (build_features, split theo step) ──► LR/RF/XGB/AE ──► models/registry/<version>/
```

## Ánh xạ mảng ↔ thư mục ↔ contract

| Mảng | Task | Thư mục | Mục data contract |
|---|---|---|---|
| Producer | T18 | `src/producer/` | 1 |
| Streaming + sink | T19, T20 | `src/streaming/` | 1, 2, 3 |
| Hive DDL, nạp dữ liệu | T07, T08 | `sql/hive/`, `src/ingestion/` | 3 |
| Features, mô hình, registry | T11–T17 | `src/features/`, `src/models/`, `models/registry/` | 4 |
| Dashboard | T22, T24 | `src/dashboard/` | 2, 5 |
| Thực nghiệm, benchmark | T25, T26 | `results/` | 5 |

## Quyết định chính
- Hive dùng Hive support của Spark (metastore Derby), không dựng container Hive riêng, vì máy ≥ 8 GB RAM.
- Kafka 3 partition, key = `nameOrig`: cùng khách hàng vào cùng partition, giữ thứ tự theo tài khoản.
- Chỉ chấm điểm `TRANSFER` và `CASH_OUT`: gian lận PaySim chỉ nằm ở hai loại này.
- Ngưỡng cảnh báo lấy từ `threshold.json` của model, không hard-code.
