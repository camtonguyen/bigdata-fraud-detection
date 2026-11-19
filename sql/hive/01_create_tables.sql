-- T07 (Hoà): bảng Hive (external, Parquet) trỏ vào dữ liệu trên HDFS. Chạy: make tables
CREATE DATABASE IF NOT EXISTS fraud;

CREATE EXTERNAL TABLE IF NOT EXISTS fraud.transactions_raw (
  step INT, type STRING, amount DOUBLE,
  nameOrig STRING, oldbalanceOrg DOUBLE, newbalanceOrig DOUBLE,
  nameDest STRING, oldbalanceDest DOUBLE, newbalanceDest DOUBLE,
  isFraud INT, isFlaggedFraud INT
)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/data/curated/transactions_raw';

CREATE EXTERNAL TABLE IF NOT EXISTS fraud.predictions (
  tx_id STRING, step INT, type STRING, amount DOUBLE,
  xgb_score DOUBLE, ae_score DOUBLE, hybrid_score DOUBLE,
  is_fraud_pred INT, is_fraud_label INT,
  event_time TIMESTAMP, processed_time TIMESTAMP
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/data/curated/predictions';

CREATE EXTERNAL TABLE IF NOT EXISTS fraud.fraud_alerts (
  tx_id STRING, nameOrig STRING, nameDest STRING, amount DOUBLE,
  hybrid_score DOUBLE, reason STRING, alert_time TIMESTAMP
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/data/curated/fraud_alerts';

-- Đăng ký các partition dt mà streaming đã ghi (chạy lại `make tables` sau khi stream chạy)
MSCK REPAIR TABLE fraud.predictions;
MSCK REPAIR TABLE fraud.fraud_alerts;
