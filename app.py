"""MediGuard AI Streamlit application."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.database import init_db, save_assessment
from utils.health_age import estimate_health_age
from utils.health_score import calculate_health_score
from utils.preprocessing import HealthProfile
from utils.recommendation_engine import build_insight_summary, generate_recommendations
from utils.risk_predictor import model_available, predict_disease_risks
from utils.triage import classify_triage
from utils.styles import inject_styles, apply_plot_theme

st.set_page_config(page_title="MediGuard AI", page_icon="+", layout="wide")
init_db()


def make_profile_from_form() -> HealthProfile:
    st.subheader("User Health Profile")
    
    # Load defaults from session state if extracted from PDF
    d_name = st.session_state.get("ext_name", "Sample Patient")
    d_age = st.session_state.get("ext_age", 28)
    
    g_opts = ["Male", "Female", "Other"]
    d_gender = st.session_state.get("ext_gender", "Male")
    d_gender_idx = g_opts.index(d_gender) if d_gender in g_opts else 0
    
    d_height = st.session_state.get("ext_height", 170.0)
    d_weight = st.session_state.get("ext_weight", 72.0)
    d_heart_rate = st.session_state.get("ext_heart_rate", 78)
    
    d_systolic_bp = st.session_state.get("ext_systolic_bp", 120)
    d_diastolic_bp = st.session_state.get("ext_diastolic_bp", 80)
    d_blood_sugar = st.session_state.get("ext_blood_sugar", 98.0)
    
    d_sleep_hours = st.session_state.get("ext_sleep_hours", 7.0)
    d_exercise_frequency = st.session_state.get("ext_exercise_frequency", 3)
    d_stress_level = st.session_state.get("ext_stress_level", 5)
    
    sm_opts = ["No", "Yes"]
    d_smoking = st.session_state.get("ext_smoking", "No")
    d_smoking_idx = sm_opts.index(d_smoking) if d_smoking in sm_opts else 0
    
    alc_opts = ["Never", "Occasional", "Regular", "Heavy"]
    d_alcohol = st.session_state.get("ext_alcohol", "Never")
    d_alcohol_idx = alc_opts.index(d_alcohol) if d_alcohol in alc_opts else 0
    
    d_water_intake = st.session_state.get("ext_water_intake", 2.2)

    with st.form("health_profile_form"):
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Name", value=d_name)
        age = c2.number_input("Age", min_value=1, max_value=100, value=int(d_age))
        gender = c3.selectbox("Gender", g_opts, index=d_gender_idx)

        c1, c2, c3 = st.columns(3)
        height = c1.number_input("Height (cm)", min_value=80.0, max_value=230.0, value=d_height)
        weight = c2.number_input("Weight (kg)", min_value=20.0, max_value=220.0, value=d_weight)
        heart_rate = c3.number_input("Heart Rate", min_value=35, max_value=190, value=int(d_heart_rate))

        c1, c2, c3 = st.columns(3)
        systolic_bp = c1.number_input("Systolic Blood Pressure", min_value=70, max_value=240, value=int(d_systolic_bp))
        diastolic_bp = c2.number_input("Diastolic Blood Pressure", min_value=40, max_value=150, value=int(d_diastolic_bp))
        blood_sugar = c3.number_input("Blood Sugar Level", min_value=40, max_value=350, value=int(d_blood_sugar))

        c1, c2, c3 = st.columns(3)
        sleep_hours = c1.number_input("Sleep Hours", min_value=0.0, max_value=16.0, value=d_sleep_hours, step=0.5)
        exercise_frequency = c2.slider("Exercise Frequency per Week", 0, 7, int(d_exercise_frequency))
        stress_level = c3.slider("Stress Level (1-10)", 1, 10, int(d_stress_level))

        c1, c2, c3 = st.columns(3)
        smoking = c1.selectbox("Smoking Habit", sm_opts, index=d_smoking_idx)
        alcohol = c2.selectbox("Alcohol Consumption", alc_opts, index=d_alcohol_idx)
        water_intake = c3.number_input("Water Intake (Liters)", min_value=0.0, max_value=8.0, value=d_water_intake, step=0.1)

        submitted = st.form_submit_button("Generate Health Twin Assessment", type="primary")

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
    return profile, submitted


def risk_chart(risks: dict) -> go.Figure:
    labels = list(risks.keys())
    values = [round(risks[label]["probability"] * 100, 1) for label in labels]
    colors = ["#38BDF8" if value < 40 else "#FBBF24" if value < 70 else "#F87171" for value in values]
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors, text=[f"{v}%" for v in values], textposition="auto"))
    fig.update_layout(
        title="Disease Risk Forecast",
        yaxis_title="Risk %",
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
            line_color="#38BDF8",
        )
    )
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=380)
    apply_plot_theme(fig)
    return fig


def ascvd_gauge(risk_prob: float) -> go.Figure:
    risk_percent = risk_prob * 100
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=risk_percent,
        mode="gauge+number",
        title={'text': "10-Year ASCVD Cardiovascular Risk", 'font': {'size': 14, 'color': '#94A3B8'}},
        number={'suffix': "%", 'font': {'size': 24, 'color': "#FFFFFF"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
            'bar': {'color': "#38BDF8"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 1,
            'bordercolor': "#202D62",
            'steps': [
                {'range': [0, 7.5], 'color': 'rgba(16, 185, 129, 0.15)'},
                {'range': [7.5, 20], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [20, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
            ],
            'threshold': {
                'line': {'color': "#EF4444", 'width': 4},
                'thickness': 0.75,
                'value': 20
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#94A3B8", 'family': "Inter, sans-serif"},
        height=240,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def display_results(profile: HealthProfile, save: bool = True) -> None:
    if not model_available():
        st.error("Model file is missing. Run `python train_model.py` before launching the app.")
        st.stop()

    health_score, category, components = calculate_health_score(profile)
    health_age, age_difference = estimate_health_age(profile, health_score)
    risks, metrics = predict_disease_risks(profile)
    triage = classify_triage(profile, risks)
    recommendations = generate_recommendations(profile, risks, health_score)
    if save:
        record_id = save_assessment(profile, health_score, category, health_age, triage, risks)
        st.success(f"Assessment saved successfully. Record ID: {record_id}")

    st.subheader("Digital Health Twin Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Health Score", f"{health_score}/100", category)
    c2.metric("Actual Age", profile.age)
    c3.metric("Health Age", health_age, f"{age_difference:+d} years")
    c4.metric("Triage", f"{triage['color']} - {triage['level']}")

    # Export PDF Report Button
    from utils.pdf_generator import generate_health_report_pdf
    pdf_bytes = generate_health_report_pdf(
        profile, health_score, category, health_age, age_difference, triage, risks, recommendations
    )
    
    st.download_button(
        label="📄 Download Diagnostic Clinical Report (PDF)",
        data=pdf_bytes,
        file_name=f"MediGuard_Report_{profile.name.replace(' ', '_')}.pdf",
        mime="application/pdf",
        type="primary"
    )
        
    st.caption("Generates print-ready clinical diagnostic documents.")

    st.markdown(
        f"""
        <div class="med-card">
          <h4 class="blue-title">Health Insights Summary</h4>
          <div class="small-muted">{build_insight_summary(profile, risks, health_score, health_age)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([1.2, 0.9, 0.9])
    with left:
        st.plotly_chart(risk_chart(risks), use_container_width=True)
    with middle:
        st.plotly_chart(component_chart(components), use_container_width=True)
    with right:
        import numpy as np
        # Clinical ASCVD 10-year risk assessment calculations
        age_factor = (profile.age - 20) * 0.25
        bp_factor = max(0, (profile.systolic_bp - 110) * 0.15)
        smoke_factor = 4.5 if profile.smoking == "Yes" else 0.0
        sugar_factor = 3.5 if profile.blood_sugar > 125 else (max(0, (profile.blood_sugar - 90)) * 0.04)
        gender_factor = 2.0 if profile.gender == "Male" else 0.5
        raw_score = age_factor + bp_factor + smoke_factor + sugar_factor + gender_factor
        prob = 1 / (1 + np.exp(-(raw_score - 10) / 3))
        st.plotly_chart(ascvd_gauge(prob), use_container_width=True)

    st.subheader("Disease Risk Cards")
    cols = st.columns(len(risks))
    for index, (disease, result) in enumerate(risks.items()):
        with cols[index]:
            st.metric(disease, f"{result['probability']:.1%}", result["label"])
            st.caption(f"Confidence: {result['confidence']:.1%}")

    st.subheader("Smart Triage")
    t_level = triage["level"]
    st.markdown(
        f"""
        <div class="triage-alert-{t_level}">
            <strong>Triage Priority:</strong> {triage['color']} - {triage['level']}<br/>
            <strong>Recommended Action:</strong> {triage['action']}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Personalized Recommendations")
    for rec in recommendations:
        st.write(f"- {rec}")

    # Interactive What-If Health Twin Simulator
    st.markdown("---")
    st.subheader("💡 Interactive 'What-If' Health Twin Simulator")
    st.info("What if you changed your lifestyle habits? Use the sliders below to simulate adjustments to your daily routines and see the dynamic impact on your biological age, health score, and future disease risk factors in real-time.")
    
    sc1, sc2, sc3 = st.columns(3)
    sim_exercise = sc1.slider("Simulated Exercise (days/week)", 0, 7, int(profile.exercise_frequency))
    sim_stress = sc2.slider("Simulated Stress Level (1-10)", 1, 10, int(profile.stress_level))
    sim_sleep = sc3.slider("Simulated Sleep (hours/night)", 4.0, 10.0, float(profile.sleep_hours), step=0.5)
    
    sc1, sc2, sc3 = st.columns(3)
    sim_smoking = sc1.selectbox("Simulated Smoking", ["No", "Yes"], index=["No", "Yes"].index(profile.smoking))
    sim_alcohol = sc2.selectbox("Simulated Alcohol", ["Never", "Occasional", "Regular", "Heavy"], index=["Never", "Occasional", "Regular", "Heavy"].index(profile.alcohol))
    sim_water = sc3.slider("Simulated Water Intake (Liters/day)", 0.5, 5.0, float(profile.water_intake), step=0.1)
    
    sim_profile = HealthProfile(
        name=profile.name,
        age=profile.age,
        gender=profile.gender,
        height=profile.height,
        weight=profile.weight,
        systolic_bp=profile.systolic_bp,
        diastolic_bp=profile.diastolic_bp,
        blood_sugar=profile.blood_sugar,
        heart_rate=profile.heart_rate,
        sleep_hours=sim_sleep,
        exercise_frequency=sim_exercise,
        smoking=sim_smoking,
        alcohol=sim_alcohol,
        stress_level=sim_stress,
        water_intake=sim_water
    )
    
    sim_health_score, sim_category, _ = calculate_health_score(sim_profile)
    sim_health_age, sim_age_difference = estimate_health_age(sim_profile, sim_health_score)
    sim_risks, _ = predict_disease_risks(sim_profile)
    
    # Side-by-side comparison metrics
    cc1, cc2, cc3 = st.columns(3)
    
    score_delta = sim_health_score - health_score
    cc1.metric("Simulated Health Score", f"{sim_health_score}/100", f"{score_delta:+d} points")
    
    age_delta = sim_health_age - health_age
    cc2.metric("Simulated Biological Age", f"{sim_health_age} yrs", f"{age_delta:+d} years vs current")
    
    # Triage check for simulated
    sim_triage = classify_triage(sim_profile, sim_risks)
    cc3.metric("Simulated Triage Priority", f"{sim_triage['level']}", f"Status: {sim_triage['color']}")
    
    # Dual bar chart comparing current vs simulated risks
    import plotly.express as px
    compare_data = []
    for disease in risks.keys():
        compare_data.append({
            "Disease": disease,
            "Risk %": round(risks[disease]["probability"] * 100, 1),
            "Profile": "Current Twin"
        })
        compare_data.append({
            "Disease": disease,
            "Risk %": round(sim_risks[disease]["probability"] * 100, 1),
            "Profile": "Simulated Twin"
        })
    df_compare = pd.DataFrame(compare_data)
    fig_compare = px.bar(
        df_compare,
        x="Disease",
        y="Risk %",
        color="Profile",
        barmode="group",
        color_discrete_map={"Current Twin": "#64748B", "Simulated Twin": "#38BDF8"}
    )
    apply_plot_theme(fig_compare)
    st.plotly_chart(fig_compare, use_container_width=True)

    with st.expander("Model Performance Metrics"):
        rows = []
        for disease, details in metrics.items():
            for model_name, values in details["comparison"].items():
                rows.append({"Disease": disease, "Model": model_name, "Selected": model_name == details["best_model"], **values})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def main() -> None:
    inject_styles()
    st.markdown('<h1 class="main-title-gradient">MediGuard AI</h1>', unsafe_allow_html=True)
    st.caption("Digital Health Twin and Future Disease Risk Forecaster")
    st.warning("This project is for educational preventive screening only and does not replace professional medical advice.")

    # PDF Report Parser Widget
    st.markdown(
        """
        <div class="med-card">
            <h4 class="blue-title">📄 Auto-Fill Profile from Clinical PDF Report</h4>
            <p class="small-muted">Upload a digital clinical report or lab summary in PDF format. The system will scan the report and automatically pre-fill the form fields below.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    uploaded_pdf = st.file_uploader("Upload Health Report (PDF)", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_pdf is not None:
        from utils.pdf_parser import extract_text_from_pdf, parse_patient_details
        with st.spinner("Analyzing PDF and extracting patient vitals..."):
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            
            if not pdf_text.strip():
                st.error("The uploaded PDF appears to be a scanned image or screenshot (no text layer detected). To auto-fill, please upload a digital PDF report containing selectable text.")
            else:
                extracted_data = parse_patient_details(pdf_text)
                if extracted_data:
                    st.success(f"Successfully extracted details for: {extracted_data.get('name', 'Patient')}! Vitals loaded into the form below.")
                    # Store in session state using our ext_ prefix
                    for key, val in extracted_data.items():
                        st.session_state[f"ext_{key}"] = val
                else:
                    st.warning("Could not find recognizable patient vitals in the text layer of this PDF. Please fill out the form manually.")

    profile, submitted = make_profile_from_form()
    
    if submitted:
        st.session_state["assessment_generated"] = True
        st.session_state["active_profile"] = profile
        st.session_state["save_this_run"] = True

    if st.session_state.get("assessment_generated", False):
        active_prof = st.session_state["active_profile"]
        should_save = st.session_state.pop("save_this_run", False)
        display_results(active_prof, save=should_save)
    else:
        st.info("Fill the form and submit to create a digital health twin assessment.")


if __name__ == "__main__":
    main()

