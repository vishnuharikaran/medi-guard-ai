"""Saved-record dashboard page."""

from __future__ import annotations

import html
import plotly.express as px
import streamlit as st

from utils.database import load_history, load_prediction_history, delete_record
from utils.styles import inject_styles, apply_plot_theme

st.set_page_config(page_title="Medi-Guard AI Dashboard", page_icon="+", layout="wide")
inject_styles()
st.markdown('<h1 class="main-title-gradient">Medi-Guard AI Dashboard</h1>', unsafe_allow_html=True)
st.caption("Educational digital twin summaries and longitudinal statistics")

history = load_history()
predictions = load_prediction_history()

if history.empty:
    st.info("No saved records found. Submit a health profile assessment from the main app.")
    st.stop()

latest = history.iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Latest Patient", html.escape(str(latest["name"])))
c2.metric("Health Score", f"{int(latest['health_score'])}/100", latest["risk_category"])
c3.metric("Lifestyle Age Estimate", int(latest["health_age"]))
c4.metric("Triage Priority", f"{latest['triage_color']} - {latest['triage_level']}")

left, right = st.columns(2)
with left:
    fig = px.line(history.sort_values("recorded_at"), x="recorded_at", y="health_score", color="name", markers=True)
    fig.update_layout(title="Health Score Progression", xaxis_title="Date", yaxis_title="Health Score")
    apply_plot_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
with right:
    if not predictions.empty:
        risk_fig = px.bar(
            predictions.tail(20),
            x="disease",
            y="risk_probability",
            color="label",
            title="Recent Disease Risk Forecasts",
        )
        risk_fig.update_layout(yaxis_tickformat=".0%")
        apply_plot_theme(risk_fig)
        st.plotly_chart(risk_fig, use_container_width=True)

st.subheader("Recent Historical Records")
st.dataframe(history.head(25), use_container_width=True, hide_index=True)

with st.expander("🗑️ Delete Record by ID"):
    del_id = st.number_input("Enter Record ID to delete", min_value=1, step=1)
    if st.button("Delete Record", type="secondary"):
        if delete_record(int(del_id)):
            st.success(f"Record #{del_id} deleted successfully.")
            st.rerun()
        else:
            st.error(f"Record #{del_id} not found.")
