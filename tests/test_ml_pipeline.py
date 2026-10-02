"""Unit tests for ML model prediction and pipeline integrity across dataset models."""

from utils.preprocessing import HealthProfile
from utils.risk_predictor import model_available, predict_disease_risks
from src.inference.predict import load_disease_model


def test_model_availability():
    assert model_available() is True


def test_individual_disease_model_loading():
    for disease in ["diabetes", "heart_disease", "stroke", "chronic_kidney_disease"]:
        model, schema, meta = load_disease_model(disease)
        assert model is not None
        assert "features" in schema
        assert "best_model" in meta


def test_predict_disease_risks():
    profile = HealthProfile(
        name="ML Test Patient",
        age=50,
        gender="Male",
        height=175.0,
        weight=85.0,
        systolic_bp=145,
        diastolic_bp=92,
        blood_sugar=135.0,
        heart_rate=82,
        sleep_hours=6.0,
        exercise_frequency=1,
        smoking="Yes",
        alcohol="Regular",
        stress_level=8,
        water_intake=1.5,
    )
    risks, metrics = predict_disease_risks(profile)
    assert isinstance(risks, dict)
    assert "Diabetes" in risks
    assert "Heart Disease" in risks
    assert "Stroke" in risks
    assert "Chronic Kidney Disease" in risks

    for disease, details in risks.items():
        prob = details["probability"]
        assert 0.0 <= prob <= 1.0
        assert details["label"] in ["Low Risk", "Moderate Risk", "High Risk"]
