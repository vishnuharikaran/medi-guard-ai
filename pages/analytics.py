"""Health trend analytics page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils.database import load_history, load_prediction_history
from utils.styles import inject_styles, apply_plot_theme

st.set_page_config(page_title="Health Trend Analytics", page_icon="+", layout="wide")
inject_styles()
st.markdown('<h1 class="main-title-gradient">Health Trend Analytics</h1>', unsafe_allow_html=True)
st.caption("Longitudinal tracking of physical metrics and experimental disease risk trends")

history = load_history().sort_values("recorded_at")
predictions = load_prediction_history()

if history.empty:
    st.info("No analytics available yet. Submit multiple health profile assessments to build trends.")
    st.stop()

c1, c2 = st.columns(2)
with c1:
    fig1 = px.line(history, x="recorded_at", y="health_score", color="name", markers=True, title="Health Score Progression Trend")
    fig1.update_layout(xaxis_title="Recorded Date", yaxis_title="Health Score (0-100)")
    apply_plot_theme(fig1)
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    fig2 = px.line(history, x="recorded_at", y="bmi", color="name", markers=True, title="Body Mass Index (BMI) Trend")
    fig2.update_layout(xaxis_title="Recorded Date", yaxis_title="BMI (kg/m²)")
    apply_plot_theme(fig2)
    st.plotly_chart(fig2, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    bp_fig = px.line(
        history,
        x="recorded_at",
        y=["systolic_bp", "diastolic_bp"],
        title="Blood Pressure Progression (mmHg)",
    )
    bp_fig.update_layout(xaxis_title="Recorded Date", yaxis_title="Blood Pressure (mmHg)")
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
            title="Experimental Disease Risk Probability Trends",
        )
        risk_fig.update_layout(xaxis_title="Recorded Date", yaxis_title="Model Probability %", yaxis_tickformat=".0%")
        apply_plot_theme(risk_fig)
        st.plotly_chart(risk_fig, use_container_width=True)
