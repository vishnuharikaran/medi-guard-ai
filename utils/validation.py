"""Centralized input validation module for Medi-Guard AI health profiles."""

from __future__ import annotations

from typing import List, Tuple
from .preprocessing import HealthProfile

VALID_GENDERS = {"Male", "Female", "Other"}
VALID_SMOKING = {"Yes", "No"}
VALID_ALCOHOL = {"Never", "Occasional", "Regular", "Heavy"}


def validate_health_profile(profile: HealthProfile) -> Tuple[bool, List[str]]:
    """
    Validates a HealthProfile object against clinical boundaries and logical rules.
    Returns (is_valid, list_of_error_messages).
    """
    errors: List[str] = []

    # Patient Name
    if not profile.name or not profile.name.strip():
        errors.append("Patient name cannot be empty.")
    elif len(profile.name.strip()) > 100:
        errors.append("Patient name must be 100 characters or less.")

    # Age
    if not (1 <= profile.age <= 100):
        errors.append(f"Age must be between 1 and 100 years. Received: {profile.age}")

    # Gender
    if profile.gender not in VALID_GENDERS:
        errors.append(f"Gender must be one of {sorted(list(VALID_GENDERS))}. Received: {profile.gender}")

    # Height & Weight
    if not (80.0 <= profile.height <= 230.0):
        errors.append(f"Height must be between 80.0 cm and 230.0 cm. Received: {profile.height}")

    if not (20.0 <= profile.weight <= 220.0):
        errors.append(f"Weight must be between 20.0 kg and 220.0 kg. Received: {profile.weight}")

    # Blood Pressure validation
    if not (70 <= profile.systolic_bp <= 240):
        errors.append(f"Systolic Blood Pressure must be between 70 and 240 mmHg. Received: {profile.systolic_bp}")

    if not (40 <= profile.diastolic_bp <= 150):
        errors.append(f"Diastolic Blood Pressure must be between 40 and 150 mmHg. Received: {profile.diastolic_bp}")

    if profile.systolic_bp <= profile.diastolic_bp:
        errors.append(
            f"Systolic Blood Pressure ({int(profile.systolic_bp)} mmHg) must be strictly greater than "
            f"Diastolic Blood Pressure ({int(profile.diastolic_bp)} mmHg)."
        )

    # Blood Sugar
    if not (40.0 <= profile.blood_sugar <= 350.0):
        errors.append(f"Fasting Blood Sugar must be between 40 and 350 mg/dL. Received: {profile.blood_sugar}")

    # Heart Rate
    if not (35 <= profile.heart_rate <= 190):
        errors.append(f"Heart Rate must be between 35 and 190 bpm. Received: {profile.heart_rate}")

    # Lifestyle factors
    if not (0.0 <= profile.sleep_hours <= 16.0):
        errors.append(f"Sleep Hours must be between 0.0 and 16.0 hours/night. Received: {profile.sleep_hours}")

    if not (0 <= profile.exercise_frequency <= 7):
        errors.append(f"Exercise Frequency must be between 0 and 7 days/week. Received: {profile.exercise_frequency}")

    if profile.smoking not in VALID_SMOKING:
        errors.append(f"Smoking habit must be 'Yes' or 'No'. Received: {profile.smoking}")

    if profile.alcohol not in VALID_ALCOHOL:
        errors.append(f"Alcohol consumption must be one of {sorted(list(VALID_ALCOHOL))}. Received: {profile.alcohol}")

    if not (1 <= profile.stress_level <= 10):
        errors.append(f"Stress Level must be an integer between 1 and 10. Received: {profile.stress_level}")

    if not (0.0 <= profile.water_intake <= 8.0):
        errors.append(f"Water Intake must be between 0.0 and 8.0 Liters/day. Received: {profile.water_intake}")

    return len(errors) == 0, errors
