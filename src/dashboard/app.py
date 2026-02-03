import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

LOG = "src/results/logs.csv"

# =================================
# Config
# =================================
st.set_page_config(page_title="Hybrid IDS", layout="wide")

st_autorefresh(interval=3000, key="refresh")

st.markdown(
    "<h1 style='text-align:center;color:#ff4b4b;'>🔐 Hybrid IDS Dashboard</h1>",
    unsafe_allow_html=True
)


# =================================
# Load logs
# =================================
if not os.path.exists(LOG):
    st.warning("Start realtime detector first.")
    st.stop()

df = pd.read_csv(LOG, header=None, names=["risk"])

total = len(df)
counts = df["risk"].value_counts()

low = counts.get("LOW", 0)
med = counts.get("MEDIUM", 0)
high = counts.get("HIGH", 0)
crit = counts.get("CRITICAL", 0)


# =================================
# METRICS
# =================================
c1, c2, c3, c4 = st.columns(4)

c1.metric("🟢 LOW", low)
c2.metric("🟡 MEDIUM", med)
c3.metric("🟠 HIGH", high)
c4.metric("🔴 CRITICAL", crit)


# =================================
# ALERT
# =================================
if crit > 0:
    st.error("🚨 CRITICAL THREAT DETECTED!")
elif high > 0:
    st.warning("⚠ High Risk Traffic Detected")
else:
    st.success("✅ Network Stable")


st.divider()


# =================================
# Charts
# =================================
left, right = st.columns(2)

with left:
    st.subheader("Risk Distribution (Bar)")
    st.bar_chart(counts)

with right:
    st.subheader("Risk Share (Pie)")
    fig, ax = plt.subplots(figsize=(3, 3))
    counts.plot.pie(autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)


st.divider()


# =================================
# Timeline
# =================================
st.subheader("Live Risk Timeline")

timeline = df["risk"].apply(
    lambda x: {"LOW":0,"MEDIUM":1,"HIGH":2,"CRITICAL":3}[x]
)

st.line_chart(timeline)


st.divider()


# =================================
# Logs + Export
# =================================
st.subheader("Recent Events")
st.dataframe(df.tail(30), use_container_width=True)

st.download_button(
    "⬇ Download Logs",
    df.to_csv(index=False),
    "ids_logs.csv",
    key="download"
)
