"""Patient history page."""

from __future__ import annotations

import streamlit as st

from utils.database import load_history, load_prediction_history, delete_record
from utils.styles import inject_styles

st.set_page_config(page_title="Patient History", page_icon="+", layout="wide")
inject_styles()
st.markdown('<h1 class="main-title-gradient">Patient History</h1>', unsafe_allow_html=True)
st.caption("Search and manage historical assessment records")

search = st.text_input("Search records by patient name")
history = load_history(search)

if history.empty:
    st.info("No matching records found in database.")
else:
    st.dataframe(history, use_container_width=True, hide_index=True)

st.subheader("Model Risk Classification History")
predictions = load_prediction_history()
if search and not predictions.empty:
    predictions = predictions[predictions["name"].str.lower().str.contains(search.lower(), na=False)]

if predictions.empty:
    st.info("No prediction records found.")
else:
    st.dataframe(predictions.sort_values("recorded_at", ascending=False), use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("🗑️ Record Deletion Control")
col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
with col1:
    record_to_del = st.number_input("Record ID to remove", min_value=1, step=1)
with col2:
    if st.button("Delete Selected Record", type="secondary"):
        if delete_record(int(record_to_del)):
            st.success(f"Record #{record_to_del} removed.")
            st.rerun()
        else:
            st.error(f"Record #{record_to_del} not found.")
