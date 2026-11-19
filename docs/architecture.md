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
