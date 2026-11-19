"""Cấu hình dùng chung. Ghi đè bằng biến môi trường (xem .env.example)."""
import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC_TX = os.getenv("TOPIC_TX", "transactions")
TOPIC_ALERTS = os.getenv("TOPIC_ALERTS", "fraud-alerts")

HDFS_URI = os.getenv("HDFS_URI", "hdfs://namenode:9000")
RAW_PATH = f"{HDFS_URI}/data/raw/paysim"
CURATED_PATH = f"{HDFS_URI}/data/curated"
CHECKPOINT_PATH = f"{HDFS_URI}/checkpoints"

MODEL_DIR = os.getenv("MODEL_DIR", "models/registry")
FRAUD_THRESHOLD = float(os.getenv("FRAUD_THRESHOLD", "0.5"))
