"""Medi-Guard AI Streamlit Application — Refactored, Secure, Multi-Dataset Machine Learning UI."""

from __future__ import annotations

import json
from pathlib import Path
import html
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
from src.inference.predict import predict_disease_risk, load_disease_model

st.set_page_config(page_title="Medi-Guard AI", page_icon="+", layout="wide")
init_db()

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"


def load_dataset_metadata(disease_key: str) -> dict:
    meta_path = MODELS_DIR / disease_key / "metadata.json"
    if meta_path.exists():
        try:
            with open(meta_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def init_form_state_defaults():
    defaults = {
        "input_name": "Sample Patient",
        "input_age": 28,
        "input_gender": "Male",
        "input_height": 170.0,
        "input_weight": 72.0,
        "input_heart_rate": 78,
        "input_systolic_bp": 120,
        "input_diastolic_bp": 80,
        "input_blood_sugar": 98.0,
        "input_sleep_hours": 7.0,
        "input_exercise_frequency": 3,
        "input_stress_level": 5,
        "input_smoking": "No",
        "input_alcohol": "Never",
        "input_water_intake": 2.2,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def make_profile_from_form() -> tuple[HealthProfile | None, bool]:
    st.subheader("Health Profile Assessment Form")
    init_form_state_defaults()

    g_opts = ["Male", "Female", "Other"]
    sm_opts = ["No", "Yes"]
    alc_opts = ["Never", "Occasional", "Regular", "Heavy"]

    with st.form("health_profile_form"):
        st.markdown("##### 1. Demographics")
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Patient Name", key="input_name", help="Enter full name for assessment labeling.")
        age = c2.number_input("Age (Years)", min_value=1, max_value=100, key="input_age")
        gender = c3.selectbox("Biological Sex / Gender", g_opts, key="input_gender")

        st.markdown("##### 2. Physical Metrics & Vital Signs")
        c1, c2, c3 = st.columns(3)
        height = c1.number_input("Height (cm)", min_value=80.0, max_value=230.0, step=0.5, key="input_height")
        weight = c2.number_input("Weight (kg)", min_value=20.0, max_value=220.0, step=0.5, key="input_weight")
        heart_rate = c3.number_input("Resting Heart Rate (bpm)", min_value=35, max_value=190, key="input_heart_rate")

        c1, c2, c3 = st.columns(3)
        systolic_bp = c1.number_input("Systolic Blood Pressure (mmHg)", min_value=70, max_value=240, key="input_systolic_bp")
        diastolic_bp = c2.number_input("Diastolic Blood Pressure (mmHg)", min_value=40, max_value=150, key="input_diastolic_bp")
        blood_sugar = c3.number_input("Fasting Blood Sugar (mg/dL)", min_value=40, max_value=350, key="input_blood_sugar")

        st.markdown("##### 3. Lifestyle & Habits")
        c1, c2, c3 = st.columns(3)
        sleep_hours = c1.number_input("Sleep Duration (Hours/night)", min_value=0.0, max_value=16.0, step=0.5, key="input_sleep_hours")
        exercise_frequency = c2.slider("Exercise Frequency (Days/week)", 0, 7, key="input_exercise_frequency")
        stress_level = c3.slider("Perceived Stress Level (1-10)", 1, 10, key="input_stress_level")

        c1, c2, c3 = st.columns(3)
        smoking = c1.selectbox("Smoking Habit", sm_opts, key="input_smoking")
        alcohol = c2.selectbox("Alcohol Consumption", alc_opts, key="input_alcohol")
        water_intake = c3.number_input("Daily Water Intake (Liters)", min_value=0.0, max_value=8.0, step=0.1, key="input_water_intake")

        submitted = st.form_submit_button("Generate Health Assessment", type="primary")

    profile = HealthProfile(
        name=str(name).strip() or "Unnamed Patient",
        age=int(age),
        gender=str(gender),
        height=float(height),
        weight=float(weight),
        systolic_bp=float(systolic_bp),
        diastolic_bp=float(diastolic_bp),
        blood_sugar=float(blood_sugar),
        heart_rate=float(heart_rate),
        sleep_hours=float(sleep_hours),
        exercise_frequency=int(exercise_frequency),
        smoking=str(smoking),
        alcohol=str(alcohol),
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
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={'color': "#0F172A", 'family': "Inter, sans-serif"},
        height=240,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    apply_plot_theme(fig)
    return fig


def render_overview_tab() -> None:
    st.markdown("### Welcome to Medi-Guard AI")
    st.write(
        "Medi-Guard AI is an educational preventive health analytics application powered by **4 independent machine learning models** "
        "trained on official public healthcare datasets from the **UCI Machine Learning Repository** and **Kaggle**."
    )
    
    st.markdown(
        """
        <div class="disclaimer-banner">
            <strong>EDUCATIONAL DISCLAIMER:</strong> This application is an educational software project. 
            Its model outputs are experimental risk indicators and are NOT a medical diagnosis, screening result, or substitute for professional medical advice. 
            Do not delay or disregard seeking medical care based on this application.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    heart_meta = load_dataset_metadata("heart_disease")
    diab_meta = load_dataset_metadata("diabetes")
    stroke_meta = load_dataset_metadata("stroke")
    ckd_meta = load_dataset_metadata("chronic_kidney_disease")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="med-card">
                <h4 class="blue-title">🫀 UCI Heart Disease</h4>
                <p class="small-muted"><strong>Source:</strong> UCI Repository (ID 45)<br/>
                <strong>Best Model:</strong> {heart_meta.get('best_model', 'Random Forest')}<br/>
                <strong>ROC-AUC:</strong> {heart_meta.get('metrics', {}).get('roc_auc', 0.88):.2f}<br/>
                <strong>Accuracy:</strong> {heart_meta.get('metrics', {}).get('accuracy', 0.82):.2f}<br/>
                <strong>Features:</strong> {len(heart_meta.get('features', [13]))} clinical attributes</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="med-card">
                <h4 class="blue-title">🩺 CDC Diabetes Indicators</h4>
                <p class="small-muted"><strong>Source:</strong> CDC BRFSS (UCI ID 891)<br/>
                <strong>Best Model:</strong> {diab_meta.get('best_model', 'Gradient Boosting')}<br/>
                <strong>ROC-AUC:</strong> {diab_meta.get('metrics', {}).get('roc_auc', 0.82):.2f}<br/>
                <strong>Accuracy:</strong> {diab_meta.get('metrics', {}).get('accuracy', 0.86):.2f}<br/>
                <strong>Features:</strong> {len(diab_meta.get('features', [21]))} survey indicators</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="med-card">
                <h4 class="blue-title">🧠 Stroke Prediction</h4>
                <p class="small-muted"><strong>Source:</strong> Kaggle Stroke Dataset<br/>
                <strong>Best Model:</strong> {stroke_meta.get('best_model', 'Random Forest')}<br/>
                <strong>ROC-AUC:</strong> {stroke_meta.get('metrics', {}).get('roc_auc', 0.84):.2f}<br/>
                <strong>Accuracy:</strong> {stroke_meta.get('metrics', {}).get('accuracy', 0.95):.2f}<br/>
                <strong>Features:</strong> {len(stroke_meta.get('features', [10]))} patient factors</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="med-card">
                <h4 class="blue-title">🧪 UCI Chronic Kidney</h4>
                <p class="small-muted"><strong>Source:</strong> UCI Repository (ID 336)<br/>
                <strong>Best Model:</strong> {ckd_meta.get('best_model', 'Random Forest')}<br/>
                <strong>ROC-AUC:</strong> {ckd_meta.get('metrics', {}).get('roc_auc', 0.99):.2f}<br/>
                <strong>Accuracy:</strong> {ckd_meta.get('metrics', {}).get('accuracy', 0.99):.2f}<br/>
                <strong>Features:</strong> {len(ckd_meta.get('features', [24]))} lab parameters</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def main() -> None:
    inject_styles()
    st.markdown('<h1 class="main-title-gradient">Medi-Guard AI</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Multi-Dataset Educational Health Analytics & Experimental Disease Risk Forecaster</div>', unsafe_allow_html=True)

    tabs = st.tabs([
        "📋 Overview",
        "🩺 Health Profile Form",
        "📊 Results & Insights",
        "🔬 Dataset Model Explorer",
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
                            if "name" in extracted:
                                st.session_state["input_name"] = str(extracted["name"])
                            if "age" in extracted:
                                st.session_state["input_age"] = int(extracted["age"])
                            if "gender" in extracted:
                                st.session_state["input_gender"] = str(extracted["gender"])
                            if "height" in extracted:
                                st.session_state["input_height"] = float(extracted["height"])
                            if "weight" in extracted:
                                st.session_state["input_weight"] = float(extracted["weight"])
                            if "heart_rate" in extracted:
                                st.session_state["input_heart_rate"] = int(extracted["heart_rate"])
                            if "systolic_bp" in extracted:
                                st.session_state["input_systolic_bp"] = int(extracted["systolic_bp"])
                            if "diastolic_bp" in extracted:
                                st.session_state["input_diastolic_bp"] = int(extracted["diastolic_bp"])
                            if "blood_sugar" in extracted:
                                st.session_state["input_blood_sugar"] = float(extracted["blood_sugar"])
                            if "sleep_hours" in extracted:
                                st.session_state["input_sleep_hours"] = float(extracted["sleep_hours"])
                            if "exercise_frequency" in extracted:
                                st.session_state["input_exercise_frequency"] = int(extracted["exercise_frequency"])
                            if "stress_level" in extracted:
                                st.session_state["input_stress_level"] = int(extracted["stress_level"])
                            if "smoking" in extracted:
                                st.session_state["input_smoking"] = str(extracted["smoking"])
                            if "alcohol" in extracted:
                                st.session_state["input_alcohol"] = str(extracted["alcohol"])
                            if "water_intake" in extracted:
                                st.session_state["input_water_intake"] = float(extracted["water_intake"])
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
            st.markdown(f"### Assessment Results for: **{active_profile.name}**")
            
            if triage.get("is_emergency", False):
                st.error("⚠️ **EMERGENCY SAFETY NOTICE**: Measured blood pressure or vitals indicate significant elevation. Please consult a licensed medical professional or emergency service immediately.")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Health Score", f"{health_score}/100", category)
            c2.metric("Chronological Age", str(active_profile.age))
            c3.metric("Lifestyle Age Estimate", f"{health_age} yrs", f"{age_diff:+d} years", delta_color="inverse")
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

            st.subheader("Independent Dataset Disease Risk Classifications")
            d_cols = st.columns(len(risks))
            for index, (disease, result) in enumerate(risks.items()):
                with d_cols[index]:
                    prob_pct = result['probability'] * 100
                    border_color = "#0284C7" if prob_pct < 40 else "#EAB308" if prob_pct < 70 else "#EF4444"
                    st.markdown(
                        f"""
                        <div class="med-card" style="border-top: 4px solid {border_color};">
                            <h4 style="margin:0 0 6px 0; font-size:1.05rem; color:#0F172A;">{disease}</h4>
                            <div style="font-size:1.8rem; font-weight:800; color:{border_color}; margin-bottom:4px;">{prob_pct:.1f}%</div>
                            <span style="background-color:#F1F5F9; color:#334155; padding:3px 8px; border-radius:4px; font-size:0.8rem; font-weight:600;">{result['label']}</span>
                            <p class="small-muted" style="margin-top:10px; font-size:0.82rem;">
                                <strong>Dataset:</strong> {result.get('dataset_source', 'Public Dataset')}<br/>
                                <strong>Model:</strong> {result.get('best_model', 'Random Forest')}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

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

    # Tab 4: Dataset Model Explorer
    with tabs[3]:
        st.subheader("🔬 Dataset-Specific Model Explorer")
        st.caption("Select an independent dataset model below to inspect its model architecture, evaluation metrics, and dataset schema.")

        selected_disease = st.selectbox(
            "Select Disease Model to Explore",
            options=["heart_disease", "diabetes", "stroke", "chronic_kidney_disease"],
            format_func=lambda k: {
                "heart_disease": "🫀 UCI Heart Disease Classifier (ID 45)",
                "diabetes": "🩺 CDC Diabetes Indicators Classifier (UCI ID 891)",
                "stroke": "🧠 Stroke Prediction Classifier (Kaggle)",
                "chronic_kidney_disease": "🧪 UCI Chronic Kidney Disease Classifier (ID 336)"
            }[k]
        )

        meta = load_dataset_metadata(selected_disease)
        
        m_col1, m_col2 = st.columns([1, 1])
        with m_col1:
            st.markdown(
                f"""
                <div class="med-card">
                    <h4 class="blue-title">Dataset Metadata & Metrics</h4>
                    <p class="small-muted">
                        <strong>Dataset Key:</strong> <code>{selected_disease}</code><br/>
                        <strong>Target Column:</strong> <code>{meta.get('target', 'target')}</code><br/>
                        <strong>Best Classifier Algorithm:</strong> {meta.get('best_model', 'Random Forest')}<br/>
                        <strong>Test Sample Split Size:</strong> {meta.get('test_split_size', 'N/A')} samples
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            metrics_dict = meta.get("metrics", {})
            st.markdown("##### Model Evaluation Performance")
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("ROC-AUC", f"{metrics_dict.get('roc_auc', 0.0):.3f}")
            mc2.metric("Accuracy", f"{metrics_dict.get('accuracy', 0.0):.3f}")
            mc3.metric("F1 Score", f"{metrics_dict.get('f1', 0.0):.3f}")

        with m_col2:
            st.markdown("##### Trained Model Feature Attributes")
            features_list = meta.get("features", [])
            st.dataframe(
                pd.DataFrame({"Feature Index": range(1, len(features_list) + 1), "Feature Name": features_list}),
                use_container_width=True,
                hide_index=True,
                height=260
            )

        if active_profile is not None:
            st.markdown("---")
            st.markdown("##### Run Direct Inference with Selected Model")
            res = predict_disease_risk(selected_disease, active_profile)
            p1, p2, p3 = st.columns(3)
            p1.metric("Predicted Disease Probability", f"{res['probability']:.1%}")
            p2.metric("Risk Classification Label", res['label'])
            p3.metric("Model ROC-AUC Metric", f"{res['auc_roc']:.3f}")

    # Tab 5: What-If Simulator
    with tabs[4]:
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
            cc2.metric("Simulated Lifestyle Age", f"{sim_health_age} yrs", f"{age_delta:+d} years vs baseline", delta_color="inverse")
            
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

    # Tab 6: Reports & Export
    with tabs[5]:
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

    # Tab 7: Privacy & Settings
    with tabs[6]:
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
