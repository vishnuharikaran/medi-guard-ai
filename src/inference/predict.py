"""Inference module for dataset-specific disease risk prediction models with caching."""

from __future__ import annotations

import json
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

from utils.preprocessing import HealthProfile

ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT / "models"


@st.cache_resource
def load_disease_model(disease_key: str) -> tuple[object, dict, dict]:
    """
    Loads and caches a disease-specific model, feature schema, and metadata.
    Returns (model_pipeline, feature_schema, metadata).
    """
    model_dir = MODELS_DIR / disease_key
    model_file = model_dir / "model.pkl"
    schema_file = model_dir / "feature_schema.json"
    meta_file = model_dir / "metadata.json"

    if not model_file.exists():
        raise FileNotFoundError(f"Model file not found for [{disease_key}] at {model_file}")

    model = joblib.load(model_file)
    schema = {}
    if schema_file.exists():
        with open(schema_file, "r") as f:
            schema = json.load(f)

    meta = {}
    if meta_file.exists():
        with open(meta_file, "r") as f:
            meta = json.load(f)

    return model, schema, meta


def profile_to_heart_disease_row(profile: HealthProfile) -> dict:
    """Map HealthProfile to UCI Heart Disease (ID 45) features."""
    return {
        "age": profile.age,
        "sex": 1 if profile.gender == "Male" else 0,
        "cp": 1 if profile.stress_level > 7 else (2 if profile.stress_level > 4 else 4),
        "trestbps": profile.systolic_bp,
        "chol": 210.0 if profile.blood_sugar > 100 else 180.0,
        "fbs": 1 if profile.blood_sugar > 120 else 0,
        "restecg": 0,
        "thalach": profile.heart_rate,
        "exang": 1 if profile.exercise_frequency < 2 else 0,
        "oldpeak": 1.2 if profile.smoking == "Yes" else 0.0,
        "slope": 2,
        "ca": 0,
        "thal": 3
    }


def profile_to_diabetes_row(profile: HealthProfile) -> dict:
    """Map HealthProfile to CDC Diabetes Health Indicators (UCI ID 891) features."""
    if profile.age < 25:
        age_cat = 1
    elif profile.age < 30:
        age_cat = 2
    elif profile.age < 35:
        age_cat = 3
    elif profile.age < 40:
        age_cat = 4
    elif profile.age < 45:
        age_cat = 5
    elif profile.age < 50:
        age_cat = 6
    elif profile.age < 55:
        age_cat = 7
    elif profile.age < 60:
        age_cat = 8
    elif profile.age < 65:
        age_cat = 9
    elif profile.age < 70:
        age_cat = 10
    elif profile.age < 75:
        age_cat = 11
    elif profile.age < 80:
        age_cat = 12
    else:
        age_cat = 13

    return {
        "HighBP": 1 if (profile.systolic_bp >= 130 or profile.diastolic_bp >= 80) else 0,
        "HighChol": 1 if profile.blood_sugar > 100 else 0,
        "CholCheck": 1,
        "BMI": profile.bmi,
        "Smoker": 1 if profile.smoking == "Yes" else 0,
        "Stroke": 0,
        "HeartDiseaseorAttack": 0,
        "PhysActivity": 1 if profile.exercise_frequency >= 3 else 0,
        "Fruits": 1,
        "Veggies": 1,
        "HvyAlcoholConsump": 1 if profile.alcohol in ["Regular", "Heavy"] else 0,
        "AnyHealthcare": 1,
        "NoDocbcCost": 0,
        "GenHlth": 2 if profile.stress_level <= 4 else (3 if profile.stress_level <= 7 else 4),
        "MentHlth": min(30, int(profile.stress_level * 2)),
        "PhysHlth": 0,
        "DiffWalk": 0,
        "Sex": 1 if profile.gender == "Male" else 0,
        "Age": age_cat,
        "Education": 4,
        "Income": 6,
    }


def profile_to_stroke_row(profile: HealthProfile) -> dict:
    """Map HealthProfile to Stroke Prediction Dataset features."""
    return {
        "gender": profile.gender,
        "age": profile.age,
        "hypertension": 1 if (profile.systolic_bp >= 140 or profile.diastolic_bp >= 90) else 0,
        "heart_disease": 0,
        "ever_married": "Yes" if profile.age > 25 else "No",
        "work_type": "Private",
        "Residence_type": "Urban",
        "avg_glucose_level": profile.blood_sugar,
        "bmi": profile.bmi,
        "smoking_status": "smokes" if profile.smoking == "Yes" else "never smoked"
    }


def profile_to_ckd_row(profile: HealthProfile) -> dict:
    """Map HealthProfile to UCI Chronic Kidney Disease (ID 336) features."""
    return {
        "age": profile.age,
        "bp": profile.diastolic_bp,
        "sg": 1.020,
        "al": 1.0 if profile.systolic_bp > 140 else 0.0,
        "su": 1.0 if profile.blood_sugar > 140 else 0.0,
        "rbc": "normal",
        "pc": "normal",
        "pcc": "notpresent",
        "ba": "notpresent",
        "bgr": profile.blood_sugar,
        "bu": 36.0,
        "sc": 1.2,
        "sod": 137.0,
        "pot": 4.4,
        "hemo": 13.5,
        "pcv": 42.0,
        "wbcc": 7800.0,
        "rbcc": 5.2,
        "htn": "yes" if profile.systolic_bp >= 140 else "no",
        "dm": "yes" if profile.blood_sugar >= 126 else "no",
        "cad": "no",
        "appet": "good",
        "pe": "no",
        "ane": "no"
    }


def predict_disease_risk(disease_key: str, profile: HealthProfile) -> dict:
    """
    Predicts probability for a specific disease condition using its independent trained model.
    Returns result dictionary containing probability, risk label, model name, and dataset source.
    """
    model, schema, meta = load_disease_model(disease_key)
    
    if disease_key == "heart_disease":
        row_dict = profile_to_heart_disease_row(profile)
        display_name = "Heart Disease"
        source_name = "UCI Heart Disease Dataset (ID 45)"
    elif disease_key == "diabetes":
        row_dict = profile_to_diabetes_row(profile)
        display_name = "Diabetes"
        source_name = "CDC Diabetes Health Indicators (UCI ID 891)"
    elif disease_key == "stroke":
        row_dict = profile_to_stroke_row(profile)
        display_name = "Stroke"
        source_name = "Stroke Prediction Dataset (Kaggle)"
    elif disease_key == "chronic_kidney_disease":
        row_dict = profile_to_ckd_row(profile)
        display_name = "Chronic Kidney Disease"
        source_name = "UCI Chronic Kidney Disease Dataset (ID 336)"
    else:
        raise ValueError(f"Unknown disease key: {disease_key}")

    df_row = pd.DataFrame([row_dict])
    probs = model.predict_proba(df_row)[0]
    probability = float(probs[1]) if len(probs) > 1 else float(probs[0])
    
    if probability >= 0.7:
        label = "High Risk"
    elif probability >= 0.4:
        label = "Moderate Risk"
    else:
        label = "Low Risk"

    return {
        "disease_key": disease_key,
        "display_name": display_name,
        "probability": probability,
        "label": label,
        "best_model": meta.get("best_model", "Classifier"),
        "dataset_source": source_name,
        "auc_roc": meta.get("metrics", {}).get("roc_auc", 0.0)
    }


def predict_all_diseases(profile: HealthProfile) -> tuple[dict, dict]:
    """Predicts risks across all 4 independent disease models."""
    diseases = ["diabetes", "heart_disease", "stroke", "chronic_kidney_disease"]
    results = {}
    metrics = {}

    for d in diseases:
        try:
            res = predict_disease_risk(d, profile)
            results[res["display_name"]] = res
            metrics[d] = res
        except Exception as e:
            print(f"Error predicting [{d}]: {e}")

    return results, metrics
