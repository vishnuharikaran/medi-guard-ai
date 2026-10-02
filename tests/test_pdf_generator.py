"""Unit tests for ReportLab PDF report compilation and XML character escaping."""

from utils.pdf_generator import generate_health_report_pdf
from utils.preprocessing import HealthProfile


def test_pdf_generation_with_special_characters():
    # Test special characters (<, >, &) in patient name that break unescaped ReportLab Paragraphs
    profile = HealthProfile(
        name="Jane & John <Escaped> Doe",
        age=29,
        gender="Female",
        height=168.0,
        weight=58.0,
        systolic_bp=118,
        diastolic_bp=76,
        blood_sugar=92.0,
        heart_rate=68,
        sleep_hours=8.0,
        exercise_frequency=4,
        smoking="No",
        alcohol="Never",
        stress_level=2,
        water_intake=2.8,
    )
    triage = {"color": "Green", "level": "Normal", "action": "Routine screening"}
    risks = {
        "Diabetes": {"probability": 0.08, "label": "Low Risk"},
        "Heart Disease": {"probability": 0.05, "label": "Low Risk"},
    }
    recs = ["Maintain regular exercise & healthy diet <test>"]

    pdf_bytes = generate_health_report_pdf(
        profile, 92, "Excellent", 27, -2, triage, risks, recs
    )
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")
