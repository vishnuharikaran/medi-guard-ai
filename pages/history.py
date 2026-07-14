"""Patient history page."""

from __future__ import annotations

import streamlit as st

from utils.database import load_history, load_prediction_history
from utils.styles import inject_styles

st.set_page_config(page_title="Patient History", page_icon="+", layout="wide")
inject_styles()
st.markdown('<h1 class="main-title-gradient">Patient History</h1>', unsafe_allow_html=True)
st.caption("Browse and search complete historical scan records")

search = st.text_input("Search by patient name")
history = load_history(search)

if history.empty:
    st.info("No matching records found.")
else:
    st.dataframe(history, use_container_width=True, hide_index=True)

st.subheader("Prediction Details")
predictions = load_prediction_history()
if search and not predictions.empty:
    predictions = predictions[predictions["name"].str.lower().str.contains(search.lower(), na=False)]

if predictions.empty:
    st.info("No prediction records found.")
else:
    st.dataframe(predictions.sort_values("recorded_at", ascending=False), use_container_width=True, hide_index=True)

