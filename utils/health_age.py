"""Experimental Lifestyle-Based Age Estimate calculator."""

from __future__ import annotations

from .preprocessing import HealthProfile


def estimate_health_age(profile: HealthProfile, health_score: int) -> tuple[int, int]:
    """
    Calculates an Experimental Lifestyle-Based Age Estimate based on physiological
    and lifestyle modifiers relative to chronological age.
    
    NOTE: This is an educational heuristic calculation and does not represent a
    validated biological age or clinical measurement.
    """
    delta = 0
    delta += max(-5, min(8, round((70 - health_score) / 5)))
    if profile.bmi >= 30:
        delta += 5
    elif profile.bmi >= 25:
        delta += 2
    elif 18.5 <= profile.bmi <= 24.9:
        delta -= 2
    if profile.systolic_bp >= 140 or profile.diastolic_bp >= 90:
        delta += 5
    if profile.blood_sugar >= 140:
        delta += 5
    if profile.smoking == "Yes":
        delta += 6
    if profile.exercise_frequency >= 5:
        delta -= 3
    if 7 <= profile.sleep_hours <= 9:
        delta -= 2
    if profile.stress_level >= 8:
        delta += 3
    if profile.water_intake >= 2.5:
        delta -= 1

    health_age = max(1, profile.age + delta)
    return int(health_age), int(health_age - profile.age)
