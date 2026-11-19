"""T17 (Hoà, export model: Tố) — Nạp model theo docs/data_contract.md và chấm điểm DataFrame."""
import json
from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.common.config import MODEL_DIR


def latest_version(model_dir: str = MODEL_DIR) -> Path:
    versions = sorted(p for p in Path(model_dir).iterdir() if p.is_dir())
    if not versions:
        raise FileNotFoundError(f"Chưa có model trong {model_dir}")
    return versions[-1]


def load_threshold(version: Path) -> dict:
    return json.loads((version / "threshold.json").read_text())


def score(df: DataFrame, dummy: bool = False) -> DataFrame:
    """Thêm xgb_score, ae_score, hybrid_score, is_fraud_pred.

    dummy=True: điểm giả để phát triển streaming/dashboard trước khi có model thật.
    """
    if dummy:
        s = F.rand(seed=42)
        return (df.withColumn("xgb_score", s).withColumn("ae_score", s)
                  .withColumn("hybrid_score", s)
                  .withColumn("is_fraud_pred", (s > 0.99).cast("int")))
    raise NotImplementedError("TODO T17: nạp xgb/ + autoencoder.keras và tính hybrid_score")
