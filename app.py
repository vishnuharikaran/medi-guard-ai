"""Medi-Guard AI Streamlit Application — Refactored, Secure, and Medically Framed."""

from __future__ import annotations

import html
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.database import init_db, save_assessment, delete_all_records, delete_record
from utils.health_age import estimate_health_age
from utils.health_score import calculate_health_score
from utils.pdf_generator import generate_health_report_pdf
from utils.pdf_parser import extract_text_from_pdf, parse_patient_details
from utils.preprocessing import HealthProfile
from utils.recommendation_engine import build_insight_summary, generate_recommendations
from utils.risk_predictor import model_available, predict_disease_risks
from utils.styles import inject_styles, apply_plot_theme
from utils.triage import classify_triage
from utils.validation import validate_health_profile

st.set_page_config(page_title="Medi-Guard AI", page_icon="+", layout="wide")
init_db()


def make_profile_from_form() -> tuple[HealthProfile | None, bool]:
    st.subheader("Health Profile Assessment Form")
    
    # Defaults from session state if confirmed from PDF parser
    d_name = st.session_state.get("ext_name", "Sample Patient")
    d_age = st.session_state.get("ext_age", 28)
    
    g_opts = ["Male", "Female", "Other"]
    d_gender = st.session_state.get("ext_gender", "Male")
    d_gender_idx = g_opts.index(d_gender) if d_gender in g_opts else 0
    
    d_height = float(st.session_state.get("ext_height", 170.0))
    d_weight = float(st.session_state.get("ext_weight", 72.0))
    d_heart_rate = int(st.session_state.get("ext_heart_rate", 78))
    
    d_systolic_bp = int(st.session_state.get("ext_systolic_bp", 120))
    d_diastolic_bp = int(st.session_state.get("ext_diastolic_bp", 80))
    d_blood_sugar = float(st.session_state.get("ext_blood_sugar", 98.0))
    
    d_sleep_hours = float(st.session_state.get("ext_sleep_hours", 7.0))
    d_exercise_frequency = int(st.session_state.get("ext_exercise_frequency", 3))
    d_stress_level = int(st.session_state.get("ext_stress_level", 5))
    
    sm_opts = ["No", "Yes"]
    d_smoking = st.session_state.get("ext_smoking", "No")
    d_smoking_idx = sm_opts.index(d_smoking) if d_smoking in sm_opts else 0
    
    alc_opts = ["Never", "Occasional", "Regular", "Heavy"]
    d_alcohol = st.session_state.get("ext_alcohol", "Never")
    d_alcohol_idx = alc_opts.index(d_alcohol) if d_alcohol in alc_opts else 0
    
    d_water_intake = float(st.session_state.get("ext_water_intake", 2.2))

    with st.form("health_profile_form"):
        st.markdown("##### 1. Demographics")
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Patient Name", value=d_name, help="Enter full name for assessment labeling.")
        age = c2.number_input("Age (Years)", min_value=1, max_value=100, value=int(d_age))
        gender = c3.selectbox("Biological Sex / Gender", g_opts, index=d_gender_idx)

        st.markdown("##### 2. Physical Metrics & Vital Signs")
        c1, c2, c3 = st.columns(3)
        height = c1.number_input("Height (cm)", min_value=80.0, max_value=230.0, value=d_height, step=0.5)
        weight = c2.number_input("Weight (kg)", min_value=20.0, max_value=220.0, value=d_weight, step=0.5)
        heart_rate = c3.number_input("Resting Heart Rate (bpm)", min_value=35, max_value=190, value=d_heart_rate)

        c1, c2, c3 = st.columns(3)
        systolic_bp = c1.number_input("Systolic Blood Pressure (mmHg)", min_value=70, max_value=240, value=d_systolic_bp)
        diastolic_bp = c2.number_input("Diastolic Blood Pressure (mmHg)", min_value=40, max_value=150, value=d_diastolic_bp)
        blood_sugar = c3.number_input("Fasting Blood Sugar (mg/dL)", min_value=40, max_value=350, value=int(d_blood_sugar))

        st.markdown("##### 3. Lifestyle & Habits")
        c1, c2, c3 = st.columns(3)
        sleep_hours = c1.number_input("Sleep Duration (Hours/night)", min_value=0.0, max_value=16.0, value=d_sleep_hours, step=0.5)
        exercise_frequency = c2.slider("Exercise Frequency (Days/week)", 0, 7, d_exercise_frequency)
        stress_level = c3.slider("Perceived Stress Level (1-10)", 1, 10, d_stress_level)

        c1, c2, c3 = st.columns(3)
        smoking = c1.selectbox("Smoking Habit", sm_opts, index=d_smoking_idx)
        alcohol = c2.selectbox("Alcohol Consumption", alc_opts, index=d_alcohol_idx)
        water_intake = c3.number_input("Daily Water Intake (Liters)", min_value=0.0, max_value=8.0, value=d_water_intake, step=0.1)

        submitted = st.form_submit_button("Generate Health Assessment", type="primary")

    profile = HealthProfile(
        name=name.strip() or "Unnamed Patient",
        age=int(age),
        gender=gender,
        height=float(height),
        weight=float(weight),
        systolic_bp=float(systolic_bp),
        diastolic_bp=float(diastolic_bp),
        blood_sugar=float(blood_sugar),
        heart_rate=float(heart_rate),
        sleep_hours=float(sleep_hours),
        exercise_frequency=int(exercise_frequency),
        smoking=smoking,
        alcohol=alcohol,
        stress_level=int(stress_level),
        water_intake=float(water_intake),
    )

    if submitted:
        is_valid, validation_errors = validate_health_profile(profile)
        if not is_valid:
            for err in validation_errors:
                st.error(f"Validation Error: {err}")
            return None, False
        return profile, True

    return profile, False


def risk_chart(risks: dict) -> go.Figure:
    labels = list(risks.keys())
    values = [round(risks[label]["probability"] * 100, 1) for label in labels]
    colors = ["#0284C7" if value < 40 else "#EAB308" if value < 70 else "#EF4444" for value in values]
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors, text=[f"{v}%" for v in values], textposition="auto"))
    fig.update_layout(
        title="Experimental Disease Risk Forecasts",
        yaxis_title="Model Probability %",
        xaxis_title="",
        height=360,
        margin=dict(l=20, r=20, t=55, b=30),
        yaxis=dict(range=[0, 100]),
    )
    apply_plot_theme(fig)
    return fig


def component_chart(components: dict) -> go.Figure:
    fig = go.Figure(
        go.Scatterpolar(
            r=list(components.values()),
            theta=list(components.keys()),
            fill="toself",
            line_color="#0284C7",
        )
    )
    fig.update_layout(
        title="Educational Health Score Breakdown",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        height=360
    )
    apply_plot_theme(fig)
    return fig


def ascvd_gauge(risk_prob: float) -> go.Figure:
    risk_percent = risk_prob * 100
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=risk_percent,
        mode="gauge+number",
        title={'text': "Experimental Cardiovascular Marker Gauge", 'font': {'size': 13, 'color': '#475569'}},
        number={'suffix': "%", 'font': {'size': 22, 'color': "#0F172A"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
            'bar': {'color': "#0284C7"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 1,
            'bordercolor': "#CBD5E1",
            'steps': [
                {'range': [0, 7.5], 'color': 'rgba(16, 185, 129, 0.12)'},
                {'range': [7.5, 20], 'color': 'rgba(245, 158, 11, 0.12)'},
                {'range': [20, 100], 'color': 'rgba(239, 68, 68, 0.12)'}
            ],
            'threshold': {
                'line': {'color': "#EF4444", 'width': 3},
                'thickness': 0.75,
                'value': 20
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#475569", 'family': "Inter, sans-serif"},
        height=240,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def render_overview_tab() -> None:
    st.markdown("### Welcome to Medi-Guard AI")
    st.write(
        "Medi-Guard AI is an educational preventive health analytics application designed to demonstrate "
        "machine learning classification, health scoring, lifestyle modeling, and report generation workflows."
    )
    
    st.markdown(
        """
        <div class="disclaimer-banner">
            <strong>EDUCATIONAL DISCLAIMER:</strong> Medi-Guard AI is an academic demonstration software prototype. 
            It is not a certified medical device and must not be used for diagnosis, treatment decisions, or clinical triage.
            Consult a qualified healthcare professional for medical interpretation.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="med-card">
                <h4 class="blue-title">🎯 Health Scoring</h4>
                <p class="small-muted">Calculates a weighted lifestyle score from 0 to 100 based on BMI, Blood Pressure, Blood Sugar, Heart Rate, Sleep, Exercise, and Stress.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            """
            <div class="med-card">
                <h4 class="blue-title">🤖 Risk Classification</h4>
                <p class="small-muted">Trains Random Forest and Logistic Regression classifiers on synthetic healthcare datasets to estimate condition probabilities.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            """
            <div class="med-card">
                <h4 class="blue-title">📄 Diagnostic Reports</h4>
                <p class="small-muted">Compiles complete patient metrics and experimental model outputs into print-ready PDF reports with XML-escaped data safety.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def main() -> None:
    inject_styles()
    st.markdown('<h1 class="main-title-gradient">Medi-Guard AI</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Educational Health Analytics & Experimental Machine Learning Forecaster</div>', unsafe_allow_html=True)

    tabs = st.tabs([
        "📋 Overview",
        "🩺 Health Profile Form",
        "📊 Results & Insights",
        "💡 What-If Simulator",
        "📄 Reports & Export",
        "🔒 Privacy & Settings"
    ])

    # Tab 1: Overview
    with tabs[0]:
        render_overview_tab()

    # Active profile management
    active_profile = st.session_state.get("active_profile", None)

    # Tab 2: Form & Assessment
    with tabs[1]:
        st.markdown(
            """
            <div class="med-card">
                <h4 class="blue-title">📄 2-Step PDF Report Extraction & Auto-Fill Workflow</h4>
                <p class="small-muted">Upload a digital health report in PDF format to automatically extract patient vitals. Review the extracted metrics before applying them to the form.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_pdf = st.file_uploader("Upload Health Report (PDF)", type=["pdf"])
        
        if uploaded_pdf is not None:
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            if not pdf_text.strip():
                st.error("The uploaded PDF has no detectable text layer (scanned/image PDF). OCR is unsupported; please fill out the form manually.")
            else:
                extracted = parse_patient_details(pdf_text)
                if extracted:
                    with st.expander("🔍 Review Extracted PDF Vitals (Step 1 of 2)", expanded=True):
                        st.json(extracted)
                        if st.button("Apply Extracted Vitals to Form (Step 2 of 2)", type="secondary"):
                            for k, v in extracted.items():
                                st.session_state[f"ext_{k}"] = v
                            st.success("Extracted vitals applied to form fields below!")
                            st.rerun()
                else:
                    st.warning("Could not locate recognizable health parameters in the PDF text layer.")

        profile, submitted = make_profile_from_form()
        if submitted and profile is not None:
            st.session_state["active_profile"] = profile
            st.session_state["assessment_generated"] = True
            
            # Calculate and save
            health_score, category, components = calculate_health_score(profile)
            health_age, age_diff = estimate_health_age(profile, health_score)
            risks, metrics = predict_disease_risks(profile)
            triage = classify_triage(profile, risks)
            rec_list = generate_recommendations(profile, risks, health_score)
            
            record_id = save_assessment(profile, health_score, category, health_age, triage, risks)
            st.session_state["last_record_id"] = record_id
            
            # Store session record IDs
            if "session_records" not in st.session_state:
                st.session_state["session_records"] = []
            st.session_state["session_records"].append(record_id)

            st.success(f"Assessment completed and recorded successfully! Record ID: #{record_id}. Switch to the 'Results & Insights' tab to view results.")

    # Fetch assessment details if profile exists
    if active_profile is not None:
        health_score, category, components = calculate_health_score(active_profile)
        health_age, age_diff = estimate_health_age(active_profile, health_score)
        risks, metrics = predict_disease_risks(active_profile)
        triage = classify_triage(active_profile, risks)
        recommendations = generate_recommendations(active_profile, risks, health_score)
    else:
        health_score, category, components = 0, "N/A", {}
        health_age, age_diff = 0, 0
        risks, metrics = {}, {}
        triage = {"color": "Green", "level": "Normal", "action": "None", "is_emergency": False}
        recommendations = []

    # Tab 3: Results & Insights
    with tabs[2]:
        if active_profile is None:
            st.info("Please fill out and submit the Health Profile Form to view results.")
        else:
            safe_name = html.escape(active_profile.name)
            st.markdown(f"### Assessment Results for: **{safe_name}**")
            
            if triage.get("is_emergency", False):
                st.error("⚠️ **EMERGENCY SAFETY NOTICE**: Measured blood pressure or vitals indicate significant elevation. Please consult a licensed medical professional or emergency service immediately.")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Health Score", f"{health_score}/100", category)
            c2.metric("Chronological Age", active_profile.age)
            c3.metric("Lifestyle Age Estimate", f"{health_age} yrs", f"{age_diff:+d} years")
            c4.metric("Triage Level", f"{triage['color']} - {triage['level']}")

            st.markdown(
                f"""
                <div class="med-card">
                    <h4 class="blue-title">Health Insights Summary</h4>
                    <p class="small-muted">{html.escape(build_insight_summary(active_profile, risks, health_score, health_age))}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            left, middle, right = st.columns([1.2, 0.9, 0.9])
            with left:
                st.plotly_chart(risk_chart(risks), use_container_width=True)
            with middle:
                st.plotly_chart(component_chart(components), use_container_width=True)
            with right:
                # Experimental cardiovascular gauge
                age_factor = (active_profile.age - 20) * 0.25
                bp_factor = max(0, (active_profile.systolic_bp - 110) * 0.15)
                smoke_factor = 4.5 if active_profile.smoking == "Yes" else 0.0
                sugar_factor = 3.5 if active_profile.blood_sugar > 125 else (max(0, (active_profile.blood_sugar - 90)) * 0.04)
                gender_factor = 2.0 if active_profile.gender == "Male" else 0.5
                raw_score = age_factor + bp_factor + smoke_factor + sugar_factor + gender_factor
                prob = float(1 / (1 + np.exp(-(raw_score - 10) / 3)))
                st.plotly_chart(ascvd_gauge(prob), use_container_width=True)

            st.subheader("Experimental Disease Risk Classifications")
            cols = st.columns(len(risks))
            for index, (disease, result) in enumerate(risks.items()):
                with cols[index]:
                    st.metric(disease, f"{result['probability']:.1%}", result["label"])
                    st.caption(f"Model: {result.get('model_name', 'Selected Classifier')}")

            st.subheader("Smart Priority Triage")
            t_level = triage["level"]
            st.markdown(
                f"""
                <div class="triage-alert-{t_level}">
                    <strong>Triage Priority Level:</strong> {triage['color']} - {triage['level']}<br/>
                    <strong>Recommended Action:</strong> {html.escape(triage['action'])}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("Personalized Educational Suggestions")
            for rec in recommendations:
                st.write(f"- {rec}")

    # Tab 4: What-If Simulator
    with tabs[3]:
        if active_profile is None:
            st.info("Please complete the Health Profile Form to enable the What-If Simulator.")
        else:
            st.subheader("💡 Interactive 'What-If' Lifestyle Simulator")
            st.caption("Adjust hypothetical habits below to compare baseline vs simulated experimental model outputs in real time.")

            sc1, sc2, sc3 = st.columns(3)
            sim_exercise = sc1.slider("Simulated Exercise (Days/week)", 0, 7, int(active_profile.exercise_frequency))
            sim_stress = sc2.slider("Simulated Stress (1-10)", 1, 10, int(active_profile.stress_level))
            sim_sleep = sc3.slider("Simulated Sleep (Hours/night)", 4.0, 10.0, float(active_profile.sleep_hours), step=0.5)

            sc1, sc2, sc3 = st.columns(3)
            sim_smoking = sc1.selectbox("Simulated Smoking", ["No", "Yes"], index=["No", "Yes"].index(active_profile.smoking))
            sim_alcohol = sc2.selectbox("Simulated Alcohol", ["Never", "Occasional", "Regular", "Heavy"], index=["Never", "Occasional", "Regular", "Heavy"].index(active_profile.alcohol))
            sim_water = sc3.slider("Simulated Water Intake (L/day)", 0.5, 5.0, float(active_profile.water_intake), step=0.1)

            sim_profile = HealthProfile(
                name=active_profile.name,
                age=active_profile.age,
                gender=active_profile.gender,
                height=active_profile.height,
                weight=active_profile.weight,
                systolic_bp=active_profile.systolic_bp,
                diastolic_bp=active_profile.diastolic_bp,
                blood_sugar=active_profile.blood_sugar,
                heart_rate=active_profile.heart_rate,
                sleep_hours=sim_sleep,
                exercise_frequency=sim_exercise,
                smoking=sim_smoking,
                alcohol=sim_alcohol,
                stress_level=sim_stress,
                water_intake=sim_water
            )

            sim_health_score, sim_category, _ = calculate_health_score(sim_profile)
            sim_health_age, sim_age_diff = estimate_health_age(sim_profile, sim_health_score)
            sim_risks, _ = predict_disease_risks(sim_profile)

            cc1, cc2, cc3 = st.columns(3)
            score_delta = sim_health_score - health_score
            cc1.metric("Simulated Health Score", f"{sim_health_score}/100", f"{score_delta:+d} points vs baseline")
            
            age_delta = sim_health_age - health_age
            cc2.metric("Simulated Lifestyle Age", f"{sim_health_age} yrs", f"{age_delta:+d} years vs baseline")
            
            sim_triage = classify_triage(sim_profile, sim_risks)
            cc3.metric("Simulated Triage Level", f"{sim_triage['level']}", f"Priority: {sim_triage['color']}")

            compare_data = []
            for disease in risks.keys():
                compare_data.append({
                    "Disease Condition": disease,
                    "Experimental Risk %": round(risks[disease]["probability"] * 100, 1),
                    "Profile State": "Baseline Twin"
                })
                compare_data.append({
                    "Disease Condition": disease,
                    "Experimental Risk %": round(sim_risks[disease]["probability"] * 100, 1),
                    "Profile State": "Simulated Habits"
                })
            df_compare = pd.DataFrame(compare_data)
            fig_compare = px.bar(
                df_compare,
                x="Disease Condition",
                y="Experimental Risk %",
                color="Profile State",
                barmode="group",
                color_discrete_map={"Baseline Twin": "#64748B", "Simulated Habits": "#0284C7"}
            )
            apply_plot_theme(fig_compare)
            st.plotly_chart(fig_compare, use_container_width=True)

    # Tab 5: Reports & Export
    with tabs[4]:
        if active_profile is None:
            st.info("Complete an assessment to generate downloadable reports.")
        else:
            st.subheader("📄 Report Export Options")
            pdf_bytes = generate_health_report_pdf(
                active_profile, health_score, category, health_age, age_diff, triage, risks, recommendations
            )
            st.download_button(
                label="📄 Download Educational Health Profile Report (PDF)",
                data=pdf_bytes,
                file_name=f"MediGuard_Report_{active_profile.name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary"
            )
            st.caption("Generates a print-ready educational document with XML-escaped data protection and non-clinical disclaimers.")

    # Tab 6: Privacy & Settings
    with tabs[5]:
        st.subheader("🔒 Data Privacy & Record Management")
        st.write("Manage stored patient assessment records and privacy controls below.")

        if st.button("🗑️ Delete All Stored Database Records", type="secondary"):
            if delete_all_records():
                st.session_state["active_profile"] = None
                st.session_state["assessment_generated"] = False
                st.success("All stored records purged successfully from SQLite database.")
                st.rerun()


if __name__ == "__main__":
    main()
