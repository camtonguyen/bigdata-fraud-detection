"""Điểm vào huấn luyện offline.

T12 split/imbalance · T14 XGBoost · T15 Autoencoder · T16 hybrid (Tố) · T13 baseline LR/RF (Phúc)
"""
from src.common.config import CURATED_PATH
from src.common.spark import get_spark
from src.features.build_features import build_features


def time_split(df, train_ratio: float = 0.8):
    """Chia theo thời gian (step) để tránh rò rỉ tương lai vào train."""
    cutoff = df.approxQuantile("step", [train_ratio], 0.001)[0]
    return df.filter(df.step <= cutoff), df.filter(df.step > cutoff)


def main() -> None:
    spark = get_spark("fraud-train")
    df = build_features(spark.read.parquet(f"{CURATED_PATH}/transactions_raw"))
    train, test = time_split(df)
    # TODO: from src.models import baseline, xgb_model, autoencoder, hybrid
    print("train:", train.count(), "test:", test.count())


if __name__ == "__main__":
    main()
