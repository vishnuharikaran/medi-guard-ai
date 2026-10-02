"""Educational triage priority heuristic classification."""

from __future__ import annotations

from .preprocessing import HealthProfile


def classify_triage(profile: HealthProfile, risks: dict) -> dict:
    """
    Classifies educational priority based on physiological measurements and experimental ML outputs.
    NOTE: This is an educational demonstration rule-set, not a clinical triage engine.
    """
    max_risk = max((item["probability"] for item in risks.values()), default=0)
    
    # Measured vital threshold flags
    vital_red = (
        profile.systolic_bp >= 180
        or profile.diastolic_bp >= 120
        or profile.blood_sugar >= 250
        or profile.heart_rate >= 140
    )
    vital_orange = (
        profile.systolic_bp >= 160
        or profile.diastolic_bp >= 100
        or profile.blood_sugar >= 200
        or profile.heart_rate >= 120
    )
    vital_yellow = (
        profile.systolic_bp >= 140
        or profile.diastolic_bp >= 90
        or profile.blood_sugar >= 140
        or profile.heart_rate >= 105
    )

    if vital_red or max_risk >= 0.85:
        return {
            "color": "Red",
            "level": "Critical",
            "action": "Elevated vitals or experimental risk detected. Seek professional medical evaluation promptly.",
            "is_emergency": vital_red,
            "vital_alert": vital_red,
            "model_alert": max_risk >= 0.85
        }
    if vital_orange or max_risk >= 0.7:
        return {
            "color": "Orange",
            "level": "Urgent",
            "action": "Consider scheduling a clinical review with a healthcare provider.",
            "is_emergency": False,
            "vital_alert": vital_orange,
            "model_alert": max_risk >= 0.7
        }
    if vital_yellow or max_risk >= 0.4:
        return {
            "color": "Yellow",
            "level": "Moderate",
            "action": "Monitor lifestyle habits and routine health indicators.",
            "is_emergency": False,
            "vital_alert": vital_yellow,
            "model_alert": max_risk >= 0.4
        }
    return {
        "color": "Green",
        "level": "Normal",
        "action": "Maintain current healthy routines and preventive screening.",
        "is_emergency": False,
        "vital_alert": False,
        "model_alert": False
    }
