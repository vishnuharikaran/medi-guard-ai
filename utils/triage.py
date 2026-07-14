"""Smart triage classification."""

from __future__ import annotations

from .preprocessing import HealthProfile


def classify_triage(profile: HealthProfile, risks: dict) -> dict:
    max_risk = max((item["probability"] for item in risks.values()), default=0)
    red = (
        profile.systolic_bp >= 180
        or profile.diastolic_bp >= 120
        or profile.blood_sugar >= 250
        or profile.heart_rate >= 140
        or max_risk >= 0.85
    )
    orange = (
        profile.systolic_bp >= 160
        or profile.diastolic_bp >= 100
        or profile.blood_sugar >= 200
        or profile.heart_rate >= 120
        or max_risk >= 0.7
    )
    yellow = (
        profile.systolic_bp >= 140
        or profile.diastolic_bp >= 90
        or profile.blood_sugar >= 140
        or profile.heart_rate >= 105
        or max_risk >= 0.4
    )

    if red:
        return {
            "color": "Red",
            "level": "Critical",
            "action": "Seek emergency medical care immediately.",
        }
    if orange:
        return {
            "color": "Orange",
            "level": "Urgent",
            "action": "Book urgent clinical review within 24 hours.",
        }
    if yellow:
        return {
            "color": "Yellow",
            "level": "Moderate",
            "action": "Schedule a non-emergency consultation and monitor symptoms.",
        }
    return {
        "color": "Green",
        "level": "Normal",
        "action": "Continue preventive care and routine health monitoring.",
    }

