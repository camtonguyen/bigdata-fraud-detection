"""T14 (Tố) — XGBoost. Dùng xgboost.spark.SparkXGBClassifier để huấn luyện phân tán."""
from xgboost.spark import SparkXGBClassifier

from src.features.build_features import FEATURE_COLS


def make_xgb(scale_pos_weight: float) -> SparkXGBClassifier:
    return SparkXGBClassifier(
        features_col=FEATURE_COLS,
        label_col="isFraud",
        scale_pos_weight=scale_pos_weight,
        max_depth=6,
        n_estimators=300,
        learning_rate=0.1,
        eval_metric="aucpr",
    )
