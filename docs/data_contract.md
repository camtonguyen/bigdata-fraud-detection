# Data contract (T02 – Tố, review: Hoà)

Thống nhất định dạng giữa các mảng để mỗi người làm song song, dùng dữ liệu giả (các ví dụ bên dưới) cho tới khi phần trước hoàn thành. Muốn đổi contract: mở PR sửa file này và báo người dùng phần đó.

Quy ước chung: thời gian UTC, ISO-8601 (`2026-11-20T08:00:00Z`); điểm số là float trong [0, 1]; cờ nhãn là int 0/1; tên cột giữ nguyên PaySim (camelCase) cho tới tầng Hive.

## 1. Message Kafka `transactions` (Producer T18 → Streaming T19)

Topic `transactions`, 3 partition, key = `nameOrig`, value = JSON (UTF-8).

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `tx_id` | string | UUID, Producer sinh |
| `event_time` | string (ts) | `start_time + step giờ`; `start_time` do Producer truyền vào (`--start-time`, mặc định 2026-01-01T00:00:00Z) |
| `step`, `type`, `amount`, `nameOrig`, `oldbalanceOrg`, `newbalanceOrig`, `nameDest`, `oldbalanceDest`, `newbalanceDest`, `isFraud`, `isFlaggedFraud` | như `PAYSIM_SCHEMA` (`src/common/schema.py`) | giữ nguyên cột gốc |

```json
{"tx_id": "7b0f9f0e-5c1a-4d6e-9a53-1f2b6c1d0a11", "event_time": "2026-01-01T01:00:00Z", "step": 1,
 "type": "TRANSFER", "amount": 181.0, "nameOrig": "C1305486145", "oldbalanceOrg": 181.0,
 "newbalanceOrig": 0.0, "nameDest": "C553264065", "oldbalanceDest": 0.0, "newbalanceDest": 0.0,
 "isFraud": 1, "isFlaggedFraud": 0}
```

Streaming chỉ chấm điểm `TRANSFER` và `CASH_OUT` (xem `FRAUD_TYPES` trong `src/features`); các loại khác bị loại, không ghi vào `predictions`.

## 2. Message Kafka `fraud-alerts` (Streaming T20 → Dashboard T22)

Topic `fraud-alerts`, 3 partition, key = `nameOrig`. Chỉ phát giao dịch có `hybrid_score >= threshold` (từ `threshold.json`). Value = toàn bộ trường của message 1, thêm:

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `xgb_score`, `ae_score`, `hybrid_score` | float | `ae_score` đã chuẩn hóa theo `ae_p99` (xem mục 4) |
| `is_fraud_pred` | int | `hybrid_score >= threshold` |
| `reason` | string | lý do ngắn, vd `high_hybrid_score`, `balance_mismatch` |
| `processed_time` | string (ts) | lúc Spark chấm điểm xong. `event_time` là thời gian mô phỏng nên T26 đo latency = `processed_time` − timestamp Kafka (cột `timestamp` khi đọc từ Kafka), không dùng `event_time` |

```json
{"tx_id": "7b0f9f0e-5c1a-4d6e-9a53-1f2b6c1d0a11", "event_time": "2026-01-01T01:00:00Z", "step": 1,
 "type": "TRANSFER", "amount": 181.0, "nameOrig": "C1305486145", "oldbalanceOrg": 181.0,
 "newbalanceOrig": 0.0, "nameDest": "C553264065", "oldbalanceDest": 0.0, "newbalanceDest": 0.0,
 "isFraud": 1, "isFlaggedFraud": 0, "xgb_score": 0.97, "ae_score": 0.81, "hybrid_score": 0.92,
 "is_fraud_pred": 1, "reason": "high_hybrid_score", "processed_time": "2026-11-20T08:00:01Z"}
```

## 3. Bảng Hive (T07, DDL: `sql/hive/01_create_tables.sql`)

Database `fraud`, external Parquet trên HDFS `/data/curated/<bảng>`. Cách ánh xạ từ message:

| Bảng | Partition | Nguồn | Khác tên so với message |
|---|---|---|---|
| `transactions_raw` | không | CSV PaySim nạp batch (T08) | không có `tx_id`, `event_time` |
| `predictions` | `dt` | mọi giao dịch đã chấm điểm (T20) | `is_fraud_label` = `isFraud`; chỉ giữ `tx_id, step, type, amount`, 3 điểm, `is_fraud_pred`, `event_time`, `processed_time` |
| `fraud_alerts` | `dt` | message 2 (T20) | `alert_time` = `processed_time`; giữ `tx_id, nameOrig, nameDest, amount, hybrid_score, reason` |

`dt` = `date(event_time)` định dạng `yyyy-MM-dd`.

## 4. Model registry (T16 → T17 → T19)

```
models/registry/<version>/
  feature_cols.json     # danh sách cột đặc trưng theo đúng thứ tự FEATURE_COLS (src/features)
  xgb/                  # SparkXGBClassifierModel.save()
  autoencoder.keras
  scaler.json           # {"mean": [...], "std": [...]} theo thứ tự feature_cols
  threshold.json        # {"w": 0.7, "ae_p99": 0.05, "threshold": 0.6}
```

- `<version>` dạng `v1`, `v2`…; biến `MODEL_DIR` trỏ tới thư mục `registry`, `score()` lấy version mới nhất (hoặc `MODEL_VERSION` nếu đặt).
- `hybrid_score = w·xgb_score + (1−w)·min(ae_error / ae_p99, 1)`; `threshold` thay `FRAUD_THRESHOLD` mặc định trong `src/common/config.py`.
- Hàm dùng chung: `src.models.registry.score(df) -> df` nhận df đã qua `build_features`, thêm `xgb_score`, `ae_score`, `hybrid_score`, `is_fraud_pred`. Cho tới khi có model thật, T19 dùng bản giả trả điểm cố định/ngẫu nhiên cùng chữ ký.

## 5. File kết quả cho dashboard

`results/experiments/metrics.json` (T25), `model` ∈ `LR, RF, XGBoost, Autoencoder, Hybrid`:
```json
[{"model": "XGBoost", "pr_auc": 0.85, "roc_auc": 0.99, "precision": 0.9, "recall": 0.8, "f1": 0.85}]
```

`results/benchmark/benchmark.csv` (T26):
```
rate_tx_per_s,partitions,throughput,p50_latency_ms,p95_latency_ms
100,3,98.5,420,910
```
