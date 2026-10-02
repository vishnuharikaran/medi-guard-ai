"""Model loading and disease risk inference with caching."""

from __future__ import annotations

from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

from .preprocessing import HealthProfile, profile_to_model_row, risk_label

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "risk_prediction_model.pkl"


def model_available() -> bool:
    return MODEL_PATH.exists()


@st.cache_resource
def load_model_bundle() -> dict:
    """Loads and caches the model bundle from disk using Streamlit resource caching."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model file not found. Run `python train_model.py` first.")
    return joblib.load(MODEL_PATH)


def predict_disease_risks(profile: HealthProfile) -> tuple[dict, dict]:
    """
    Evaluates disease risks for a given HealthProfile.
    Returns (risk_results, model_performance_metrics).
    """
    bundle = load_model_bundle()
    row = pd.DataFrame([profile_to_model_row(profile)])
    results = {}

    for disease, model in bundle["models"].items():
        probability = float(model.predict_proba(row)[0][1])
        # Class probability label
        results[disease] = {
            "probability": probability,
            "label": risk_label(probability),
            "model_name": bundle.get("metrics", {}).get(disease, {}).get("best_model", "Selected Classifier")
        }

    return results, bundle.get("metrics", {})
