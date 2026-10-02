"""Automated unit tests for multi-dataset acquisition, preprocessing, and inference."""

import json
from pathlib import Path
import pandas as pd
import pytest

from utils.preprocessing import HealthProfile
from src.data.download_datasets import RAW_DATA_DIR
from src.data.preprocess import PROCESSED_DATA_DIR
from src.inference.predict import predict_disease_risk, predict_all_diseases, load_disease_model

ROOT = Path(__file__).resolve().parents[1]


def test_raw_datasets_exist():
    assert (RAW_DATA_DIR / "heart_disease" / "heart_disease.csv").exists()
    assert (RAW_DATA_DIR / "diabetes" / "cdc_diabetes_health_indicators.csv").exists()
    assert (RAW_DATA_DIR / "stroke" / "healthcare-dataset-stroke-data.csv").exists()
    assert (RAW_DATA_DIR / "chronic_kidney_disease" / "chronic_kidney_disease.csv").exists()


def test_processed_datasets_and_schemas_exist():
    for ds in ["heart_disease", "diabetes", "stroke", "chronic_kidney_disease"]:
        proc_dir = PROCESSED_DATA_DIR / ds
        assert (proc_dir / f"{ds}_processed.csv").exists()
        assert (proc_dir / "feature_schema.json").exists()

        with open(proc_dir / "feature_schema.json") as f:
            schema = json.load(f)
            assert "features" in schema
            assert "target" in schema


def test_independent_disease_model_inference():
    profile = HealthProfile(
        name="Multi-Dataset Test Patient",
        age=45,
        gender="Male",
        height=175.0,
        weight=80.0,
        systolic_bp=135,
        diastolic_bp=88,
        blood_sugar=115.0,
        heart_rate=78,
        sleep_hours=7.0,
        exercise_frequency=3,
        smoking="No",
        alcohol="Occasional",
        stress_level=5,
        water_intake=2.2,
    )

    results, metrics = predict_all_diseases(profile)
    assert len(results) >= 4
    assert "Diabetes" in results
    assert "Heart Disease" in results
    assert "Stroke" in results
    assert "Chronic Kidney Disease" in results

    for name, res in results.items():
        assert 0.0 <= res["probability"] <= 1.0
        assert res["label"] in ["Low Risk", "Moderate Risk", "High Risk"]
        assert "dataset_source" in res


def test_missing_model_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_disease_model("non_existent_disease")
