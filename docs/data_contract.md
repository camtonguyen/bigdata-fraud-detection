# Data contract (T02 – Tố, review: Hoà)

Thống nhất định dạng giữa các mảng để mỗi người làm song song, dùng dữ liệu giả cho tới khi phần trước hoàn thành.

## 1. Message Kafka `transactions` (Producer T18 → Streaming T19)

JSON, key = `nameOrig`:

```json
{"tx_id": "uuid", "event_time": "2026-11-20T08:00:00Z", "step": 1, "type": "TRANSFER",
 "amount": 181.0, "nameOrig": "C123", "oldbalanceOrg": 181.0, "newbalanceOrig": 0.0,
 "nameDest": "C456", "oldbalanceDest": 0.0, "newbalanceDest": 0.0,
 "isFraud": 1, "isFlaggedFraud": 0}
```

## 2. Message Kafka `fraud-alerts` (Streaming T20 → Dashboard T22)

Các trường của message 1, thêm: `xgb_score`, `ae_score`, `hybrid_score` (float 0–1), `is_fraud_pred` (0/1), `processed_time`.

## 3. Bảng Hive (T07)

`fraud.transactions_raw`, `fraud.predictions`, `fraud.fraud_alerts`, xem `sql/hive/01_create_tables.sql`.

## 4. Model registry (T16 → T17 → T19)

```
models/registry/<version>/
  feature_cols.json     # thứ tự cột đặc trưng (src/features)
  xgb/                  # SparkXGBClassifierModel.save()
  autoencoder.keras
  scaler.json           # mean/std dùng cho autoencoder
  threshold.json        # {"w": 0.7, "ae_p99": ..., "threshold": ...}
```

Hàm dùng chung: `src.models.registry.score(df) -> df` thêm 3 cột điểm và `is_fraud_pred`.

## 5. File kết quả cho dashboard

- `results/experiments/metrics.json` (T25): danh sách `{model, pr_auc, roc_auc, precision, recall, f1}`
- `results/benchmark/benchmark.csv` (T26): `rate_tx_per_s, partitions, throughput, p50_latency_ms, p95_latency_ms`
