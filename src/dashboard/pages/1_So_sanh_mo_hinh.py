"""T24 (Phúc) — dữ liệu từ T25 (Tố). — So sánh LR / RF / XGBoost / Autoencoder / Hybrid."""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.title("So sánh mô hình")
p = Path("reports/experiments/metrics.json")
if p.exists():
    st.dataframe(pd.DataFrame(json.loads(p.read_text())))
else:
    st.info("Chưa có reports/experiments/metrics.json — chạy `make train` trước.")
