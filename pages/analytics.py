"""Health trend analytics page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils.database import load_history, load_prediction_history
from utils.styles import inject_styles, apply_plot_theme

st.set_page_config(page_title="Health Trend Analytics", page_icon="+", layout="wide")
inject_styles()
st.markdown('<h1 class="main-title-gradient">Health Trend Analytics</h1>', unsafe_allow_html=True)
st.caption("Longitudinal tracking of physical metrics and disease risk trends")

history = load_history().sort_values("recorded_at")
predictions = load_prediction_history()

if history.empty:
    st.info("No analytics available yet. Submit multiple assessments to build trends.")
    st.stop()

c1, c2 = st.columns(2)
with c1:
    fig1 = px.line(history, x="recorded_at", y="health_score", color="name", markers=True, title="Health Score Trend")
    apply_plot_theme(fig1)
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    fig2 = px.line(history, x="recorded_at", y="bmi", color="name", markers=True, title="BMI Trend")
    apply_plot_theme(fig2)
    st.plotly_chart(fig2, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    bp_fig = px.line(
        history,
        x="recorded_at",
        y=["systolic_bp", "diastolic_bp"],
        title="Blood Pressure Trend",
    )
    apply_plot_theme(bp_fig)
    st.plotly_chart(bp_fig, use_container_width=True)
with c2:
    if not predictions.empty:
        risk_fig = px.line(
            predictions,
            x="recorded_at",
            y="risk_probability",
            color="disease",
            markers=True,
            title="Disease Risk Trend",
        )
        risk_fig.update_layout(yaxis_tickformat=".0%")
        apply_plot_theme(risk_fig)
        st.plotly_chart(risk_fig, use_container_width=True)

