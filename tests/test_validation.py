"""Unit tests for centralized input validation module."""

from utils.preprocessing import HealthProfile
from utils.validation import validate_health_profile


def test_valid_profile():
    profile = HealthProfile(
        name="Valid Patient",
        age=30,
        gender="Female",
        height=165.0,
        weight=60.0,
        systolic_bp=120,
        diastolic_bp=80,
        blood_sugar=90.0,
        heart_rate=72,
        sleep_hours=8.0,
        exercise_frequency=4,
        smoking="No",
        alcohol="Never",
        stress_level=3,
        water_intake=2.5,
    )
    is_valid, errors = validate_health_profile(profile)
    assert is_valid is True
    assert len(errors) == 0


def test_invalid_blood_pressure_systolic_less_than_diastolic():
    profile = HealthProfile(
        name="Invalid BP Patient",
        age=40,
        gender="Male",
        height=175.0,
        weight=80.0,
        systolic_bp=80,    # Invalid: Systolic < Diastolic
        diastolic_bp=120,
        blood_sugar=100.0,
        heart_rate=75,
        sleep_hours=7.0,
        exercise_frequency=3,
        smoking="No",
        alcohol="Occasional",
        stress_level=5,
        water_intake=2.0,
    )
    is_valid, errors = validate_health_profile(profile)
    assert is_valid is False
    assert any("strictly greater than" in err for err in errors)


def test_out_of_range_values():
    profile = HealthProfile(
        name="",
        age=150,           # Invalid age
        gender="Unknown",  # Invalid gender
        height=50.0,       # Invalid height
        weight=300.0,      # Invalid weight
        systolic_bp=300,   # Invalid systolic
        diastolic_bp=30,   # Invalid diastolic
        blood_sugar=500.0, # Invalid sugar
        heart_rate=20,     # Invalid HR
        sleep_hours=24.0,  # Invalid sleep
        exercise_frequency=10, # Invalid exercise
        smoking="Maybe",   # Invalid smoking
        alcohol="Daily",   # Invalid alcohol
        stress_level=15,   # Invalid stress
        water_intake=12.0, # Invalid water
    )
    is_valid, errors = validate_health_profile(profile)
    assert is_valid is False
    assert len(errors) >= 10
