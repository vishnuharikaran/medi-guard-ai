"""Dynamic recommendation generation."""

from __future__ import annotations

from .preprocessing import HealthProfile


def generate_recommendations(profile: HealthProfile, risks: dict, health_score: int) -> list[str]:
    recs: list[str] = []

    if profile.bmi >= 25:
        recs.append("Adopt a calorie-aware diet with vegetables, lean protein, whole grains, and weekly weight tracking.")
    elif profile.bmi < 18.5:
        recs.append("Increase nutrient-dense calories and discuss healthy weight gain with a clinician or dietitian.")

    if profile.systolic_bp >= 130 or profile.diastolic_bp >= 85:
        recs.append("Reduce sodium intake, add potassium-rich foods if medically suitable, and recheck blood pressure regularly.")

    if profile.blood_sugar >= 125 or risks.get("Diabetes", {}).get("probability", 0) >= 0.4:
        recs.append("Prioritize low-glycemic meals, reduce sugary drinks, and consider HbA1c testing.")

    if risks.get("Heart Disease", {}).get("probability", 0) >= 0.4:
        recs.append("Add moderate cardio, review lipid profile, and avoid tobacco exposure.")

    if profile.exercise_frequency < 3:
        recs.append("Build toward at least 150 minutes of moderate activity per week plus two strength sessions.")

    if profile.sleep_hours < 7:
        recs.append("Target 7-9 hours of sleep with a fixed wake time and reduced late-night screen exposure.")

    if profile.stress_level >= 7:
        recs.append("Use daily stress reduction: breathing drills, journaling, meditation, or brief walks.")

    if profile.water_intake < 2:
        recs.append("Increase water intake gradually toward 2-3 liters daily unless medically restricted.")

    if profile.smoking == "Yes":
        recs.append("Create a smoking reduction plan and ask a healthcare professional about cessation support.")

    if profile.alcohol in {"Regular", "Heavy"}:
        recs.append("Limit alcohol intake and keep several alcohol-free days each week.")

    if health_score >= 85 and not recs:
        recs.append("Maintain current habits and continue routine preventive screening.")

    return recs[:8]


def build_insight_summary(profile: HealthProfile, risks: dict, health_score: int, health_age: int) -> str:
    highest = max(risks.items(), key=lambda item: item[1]["probability"], default=("No major", {"probability": 0}))
    return (
        f"{profile.name}'s health score is {health_score}/100 and estimated health age is {health_age}. "
        f"The highest modeled risk is {highest[0]} at {highest[1]['probability']:.0%}. "
        "Use this as a preventive screening aid, not as a medical diagnosis."
    )

