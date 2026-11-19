"""T22 (Phúc; mockup T21 & review UI: Vy) — Dashboard cảnh báo gian lận thời gian thực."""
import json

import pandas as pd
import streamlit as st
from kafka import KafkaConsumer

from src.common.config import KAFKA_BOOTSTRAP, TOPIC_ALERTS

st.set_page_config(page_title="Fraud Monitor – Nhóm 9", layout="wide")
st.title("Giám sát gian lận giao dịch thời gian thực")


@st.cache_resource
def consumer() -> KafkaConsumer:
    return KafkaConsumer(TOPIC_ALERTS, bootstrap_servers=KAFKA_BOOTSTRAP,
                         value_deserializer=lambda v: json.loads(v.decode()),
                         auto_offset_reset="latest", consumer_timeout_ms=1000)


if "alerts" not in st.session_state:
    st.session_state.alerts = []

for msg in consumer():
    st.session_state.alerts.append(msg.value)
st.session_state.alerts = st.session_state.alerts[-500:]

df = pd.DataFrame(st.session_state.alerts)
c1, c2, c3 = st.columns(3)
c1.metric("Cảnh báo (phiên)", len(df))
c2.metric("Tổng tiền nghi gian lận", f"{df['amount'].astype(float).sum():,.0f}" if len(df) else "0")
c3.metric("Điểm TB", f"{df['hybrid_score'].astype(float).mean():.2f}" if len(df) else "-")
st.dataframe(df.tail(50), use_container_width=True)
st.button("Làm mới")
