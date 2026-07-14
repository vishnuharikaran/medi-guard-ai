"""Model loading and disease risk inference."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from .preprocessing import HealthProfile, profile_to_model_row, risk_label

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "risk_prediction_model.pkl"


def model_available() -> bool:
    return MODEL_PATH.exists()


def load_model_bundle() -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model file not found. Run `python train_model.py` first.")
    return joblib.load(MODEL_PATH)


def predict_disease_risks(profile: HealthProfile) -> tuple[dict, dict]:
    bundle = load_model_bundle()
    row = pd.DataFrame([profile_to_model_row(profile)])
    results = {}

    for disease, model in bundle["models"].items():
        probability = float(model.predict_proba(row)[0][1])
        confidence = max(probability, 1 - probability)
        results[disease] = {
            "probability": probability,
            "confidence": confidence,
            "label": risk_label(probability),
        }

    return results, bundle.get("metrics", {})

