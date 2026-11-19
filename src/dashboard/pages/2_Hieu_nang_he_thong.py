"""T24 (Phúc) — dữ liệu từ T26 (Hoà): Throughput, latency end-to-end theo tốc độ producer và số partition."""
from pathlib import Path

import pandas as pd
import streamlit as st

st.title("Hiệu năng hệ thống")
p = Path("results/benchmark/benchmark.csv")
if p.exists():
    df = pd.read_csv(p)
    st.line_chart(df, x="rate_tx_per_s", y=["throughput", "p95_latency_ms"])
    st.dataframe(df)
else:
    st.info("Chưa có results/benchmark/benchmark.csv.")
