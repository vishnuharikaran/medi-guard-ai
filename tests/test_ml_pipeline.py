"""Unit tests for ML model prediction and pipeline integrity."""

from utils.preprocessing import HealthProfile
from utils.risk_predictor import model_available, load_model_bundle, predict_disease_risks


def test_model_availability():
    assert model_available() is True


def test_model_bundle_loading():
    bundle = load_model_bundle()
    assert "models" in bundle
    assert "metrics" in bundle
    assert "features" in bundle
    assert len(bundle["models"]) >= 4


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
    assert "Hypertension" in risks
    assert "Obesity" in risks

    for disease, details in risks.items():
        prob = details["probability"]
        assert 0.0 <= prob <= 1.0
        assert details["label"] in ["Low Risk", "Moderate Risk", "High Risk"]
