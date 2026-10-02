"""Model loading and disease risk inference with caching across independent dataset models."""

from __future__ import annotations

from pathlib import Path
from utils.preprocessing import HealthProfile
from src.inference.predict import predict_all_diseases, load_disease_model

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


def model_available() -> bool:
    """Checks if trained models exist in models/."""
    return (MODELS_DIR / "diabetes" / "model.pkl").exists() or (MODELS_DIR / "heart_disease" / "model.pkl").exists()


def load_model_bundle() -> dict:
    """Legacy helper function returning primary disease models for testing compatibility."""
    model, schema, meta = load_disease_model("diabetes")
    return {"models": {"Diabetes": model}, "metrics": {"Diabetes": meta}, "features": schema.get("features", [])}


def predict_disease_risks(profile: HealthProfile) -> tuple[dict, dict]:
    """
    Evaluates disease risks for a given HealthProfile using independent disease models.
    Returns (risk_results, model_performance_metrics).
    """
    return predict_all_diseases(profile)
