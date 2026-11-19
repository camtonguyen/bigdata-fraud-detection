"""T16 (Tố) — Kết hợp điểm XGBoost và Autoencoder."""
import numpy as np


def normalize_ae(err: np.ndarray, p99: float) -> np.ndarray:
    """Đưa reconstruction error về [0, 1] theo phân vị 99 của tập validation."""
    return np.clip(err / p99, 0.0, 1.0)


def hybrid_score(xgb_proba: np.ndarray, ae_norm: np.ndarray, w: float = 0.7) -> np.ndarray:
    """w chọn trên validation theo PR-AUC."""
    return w * xgb_proba + (1 - w) * ae_norm
