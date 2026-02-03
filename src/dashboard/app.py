import streamlit as st
import pandas as pd
import time
import os

LOG = "src/results/logs.csv"

st.set_page_config(layout="wide")
st.title("🔐 Intrusion Detection System Dashboard")

col1, col2 = st.columns(2)
placeholder = st.empty()

while True:

    if os.path.exists(LOG):

        df = pd.read_csv(LOG, header=None, names=["decision"])

        total = len(df)
        attacks = (df["decision"] == "High Risk Attack").sum()

        with placeholder.container():
            col1.metric("Packets Analyzed", total)
            col2.metric("Attacks Detected", attacks)

            st.line_chart(
                df["decision"].map(
                    {"Normal Traffic": 0, "High Risk Attack": 1}
                )
            )

            st.dataframe(df.tail(10), use_container_width=True)

    time.sleep(1)
