"""Input cleaning and feature engineering helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HealthProfile:
    name: str
    age: int
    gender: str
    height: float
    weight: float
    systolic_bp: float
    diastolic_bp: float
    blood_sugar: float
    heart_rate: float
    sleep_hours: float
    exercise_frequency: int
    smoking: str
    alcohol: str
    stress_level: int
    water_intake: float

    @property
    def bmi(self) -> float:
        height_m = max(self.height / 100, 0.5)
        return round(self.weight / (height_m**2), 2)


def profile_to_model_row(profile: HealthProfile) -> dict:
    """Convert a form profile into the feature names used at training time."""
    return {
        "Age": profile.age,
        "Gender": profile.gender,
        "Height": profile.height,
        "Weight": profile.weight,
        "BMI": profile.bmi,
        "Systolic BP": profile.systolic_bp,
        "Diastolic BP": profile.diastolic_bp,
        "Blood Sugar": profile.blood_sugar,
        "Heart Rate": profile.heart_rate,
        "Sleep Hours": profile.sleep_hours,
        "Exercise Frequency": profile.exercise_frequency,
        "Smoking": profile.smoking,
        "Alcohol": profile.alcohol,
        "Stress Level": profile.stress_level,
        "Water Intake": profile.water_intake,
    }


def risk_label(probability: float) -> str:
    if probability >= 0.7:
        return "High Risk"
    if probability >= 0.4:
        return "Moderate Risk"
    return "Low Risk"

