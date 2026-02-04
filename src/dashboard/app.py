import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

LOG = "src/results/logs.csv"

st.set_page_config(layout="wide")
st_autorefresh(interval=3000, key="refresh")

st.title("🔐 Hybrid IDS Monitor")


# =================================================
# LOAD LOGS
# =================================================
if not os.path.exists(LOG):
    st.warning("Run detector first")
    st.stop()

df = pd.read_csv(LOG)


# =================================================
# METRICS
# =================================================
counts = df["risk"].value_counts()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Packets", len(df))
c2.metric("High", counts.get("HIGH", 0))
c3.metric("Critical", counts.get("CRITICAL", 0))
c4.metric("Medium", counts.get("MEDIUM", 0))


# =================================================
# CHARTS
# =================================================
left, mid, right = st.columns([2, 1, 2])

with left:
    st.bar_chart(counts)

with mid:
    fig, ax = plt.subplots(figsize=(2, 2))
    counts.plot.pie(ax=ax, autopct="%1.0f%%")
    ax.set_ylabel("")
    st.pyplot(fig)

with right:
    mapping = {"LOW":0, "MEDIUM":1, "HIGH":2, "CRITICAL":3}
    st.line_chart(df["risk"].map(mapping))


# =================================================
# PROBABILITY TREND
# =================================================
st.subheader("Attack Probability")
st.line_chart(df["probability"])


# =================================================
# LIVE TABLE ⭐ FULL DETAILS
# =================================================
st.subheader("Live Logs")

st.dataframe(
    df.tail(25),
    use_container_width=True
)


st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    "ids_logs.csv"
)
