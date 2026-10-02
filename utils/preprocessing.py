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


def profile_to_cdc_row(profile: HealthProfile) -> dict:
    """Map user HealthProfile to CDC Diabetes Health Indicators (UCI ID 891) feature space."""
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


def risk_label(probability: float) -> str:
    if probability >= 0.7:
        return "High Risk"
    if probability >= 0.4:
        return "Moderate Risk"
    return "Low Risk"
