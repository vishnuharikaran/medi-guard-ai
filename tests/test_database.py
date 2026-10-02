"""Unit tests for SQLite database persistence layer."""

import pytest
from utils.database import init_db, save_assessment, load_history, delete_record, delete_all_records
from utils.preprocessing import HealthProfile


@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    yield


def test_save_and_load_assessment():
    profile = HealthProfile(
        name="DB Test Patient",
        age=35,
        gender="Male",
        height=180.0,
        weight=75.0,
        systolic_bp=122,
        diastolic_bp=78,
        blood_sugar=95.0,
        heart_rate=70,
        sleep_hours=7.5,
        exercise_frequency=3,
        smoking="No",
        alcohol="Never",
        stress_level=4,
        water_intake=2.5,
    )
    triage = {"color": "Green", "level": "Normal", "action": "Routine checkup"}
    risks = {"Diabetes": {"probability": 0.15, "confidence": 0.85, "label": "Low Risk"}}

    record_id = save_assessment(profile, 88, "Excellent", 33, triage, risks)
    assert isinstance(record_id, int)
    assert record_id > 0

    history = load_history("DB Test Patient")
    assert not history.empty
    assert history.iloc[0]["name"] == "DB Test Patient"


def test_delete_record():
    profile = HealthProfile(
        name="Delete Candidate",
        age=45,
        gender="Female",
        height=160.0,
        weight=65.0,
        systolic_bp=130,
        diastolic_bp=85,
        blood_sugar=105.0,
        heart_rate=76,
        sleep_hours=6.5,
        exercise_frequency=2,
        smoking="No",
        alcohol="Occasional",
        stress_level=6,
        water_intake=2.0,
    )
    triage = {"color": "Yellow", "level": "Moderate", "action": "Monitor BP"}
    risks = {"Hypertension": {"probability": 0.45, "confidence": 0.55, "label": "Moderate Risk"}}

    record_id = save_assessment(profile, 65, "Average", 47, triage, risks)
    success = delete_record(record_id)
    assert success is True

    # Confirm record is gone
    history = load_history("Delete Candidate")
    assert history.empty
