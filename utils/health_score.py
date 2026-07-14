"""Weighted health score calculator."""

from __future__ import annotations

from .preprocessing import HealthProfile


def _range_score(value: float, ideal_low: float, ideal_high: float, hard_low: float, hard_high: float) -> float:
    if ideal_low <= value <= ideal_high:
        return 100.0
    if value < ideal_low:
        return max(0.0, 100 * (value - hard_low) / (ideal_low - hard_low))
    return max(0.0, 100 * (hard_high - value) / (hard_high - ideal_high))


def calculate_health_score(profile: HealthProfile) -> tuple[int, str, dict]:
    bmi_score = _range_score(profile.bmi, 18.5, 24.9, 13, 40)
    systolic_score = _range_score(profile.systolic_bp, 90, 120, 70, 190)
    diastolic_score = _range_score(profile.diastolic_bp, 60, 80, 45, 120)
    bp_score = (systolic_score + diastolic_score) / 2
    sugar_score = _range_score(profile.blood_sugar, 70, 110, 45, 260)
    heart_score = _range_score(profile.heart_rate, 60, 100, 40, 150)
    sleep_score = _range_score(profile.sleep_hours, 7, 9, 3, 13)
    exercise_score = min(100, profile.exercise_frequency / 5 * 100)
    smoking_score = 100 if profile.smoking == "No" else 35
    stress_score = max(0, 100 - (profile.stress_level - 1) * 11.11)

    components = {
        "BMI": bmi_score,
        "Blood Pressure": bp_score,
        "Blood Sugar": sugar_score,
        "Heart Rate": heart_score,
        "Sleep": sleep_score,
        "Exercise": exercise_score,
        "Smoking": smoking_score,
        "Stress": stress_score,
    }
    weights = {
        "BMI": 0.15,
        "Blood Pressure": 0.2,
        "Blood Sugar": 0.15,
        "Heart Rate": 0.1,
        "Sleep": 0.1,
        "Exercise": 0.1,
        "Smoking": 0.1,
        "Stress": 0.1,
    }
    score = int(round(sum(components[name] * weights[name] for name in components)))

    if score >= 85:
        category = "Excellent"
    elif score >= 70:
        category = "Good"
    elif score >= 55:
        category = "Average"
    elif score >= 40:
        category = "Poor"
    else:
        category = "Critical"

    return score, category, {k: round(v, 1) for k, v in components.items()}

