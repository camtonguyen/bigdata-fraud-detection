"""T15 (Tố) — Deep Autoencoder phát hiện bất thường.

Huấn luyện chỉ trên giao dịch bình thường; điểm bất thường = reconstruction error (MSE).
"""
import numpy as np
from tensorflow import keras


def build_autoencoder(n_features: int) -> keras.Model:
    inp = keras.Input(shape=(n_features,))
    x = keras.layers.Dense(32, activation="relu")(inp)
    x = keras.layers.Dense(16, activation="relu")(x)
    z = keras.layers.Dense(8, activation="relu")(x)
    x = keras.layers.Dense(16, activation="relu")(z)
    x = keras.layers.Dense(32, activation="relu")(x)
    out = keras.layers.Dense(n_features, activation="linear")(x)
    model = keras.Model(inp, out)
    model.compile(optimizer="adam", loss="mse")
    return model


def reconstruction_error(model: keras.Model, X: np.ndarray) -> np.ndarray:
    return np.mean(np.square(X - model.predict(X, verbose=0)), axis=1)
