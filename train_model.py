"""Generate data, train disease risk models, and save the best pipelines."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "datasets" / "healthcare_dataset.csv"
MODEL_PATH = ROOT / "models" / "risk_prediction_model.pkl"
RANDOM_STATE = 42

FEATURES = [
    "Age",
    "Gender",
    "Height",
    "Weight",
    "BMI",
    "Systolic BP",
    "Diastolic BP",
    "Blood Sugar",
    "Heart Rate",
    "Sleep Hours",
    "Exercise Frequency",
    "Smoking",
    "Alcohol",
    "Stress Level",
    "Water Intake",
]

TARGETS = {
    "Diabetes": "Diabetes Risk",
    "Heart Disease": "Heart Disease Risk",
    "Hypertension": "Hypertension Risk",
    "Obesity": "Obesity Risk",
    "Cancer": "Cancer Risk",
}


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def generate_synthetic_dataset(rows: int = 5000) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE)
    age = rng.integers(18, 81, rows)
    gender = rng.choice(["Male", "Female", "Other"], rows, p=[0.49, 0.49, 0.02])
    height = np.clip(rng.normal(166, 10, rows), 140, 200).round(1)
    base_bmi = np.clip(rng.normal(25.5, 4.8, rows) + (age - 45) * 0.025, 16, 42)
    weight = (base_bmi * (height / 100) ** 2).round(1)
    bmi = (weight / ((height / 100) ** 2)).round(2)
    exercise = np.clip(rng.poisson(3, rows), 0, 7)
    smoking = rng.choice(["Yes", "No"], rows, p=[0.22, 0.78])
    alcohol = rng.choice(["Never", "Occasional", "Regular", "Heavy"], rows, p=[0.35, 0.42, 0.18, 0.05])
    stress = np.clip(rng.normal(5.3, 2.2, rows).round(), 1, 10).astype(int)
    sleep = np.clip(rng.normal(7.1, 1.25, rows) - stress * 0.08, 4, 10).round(1)
    water = np.clip(rng.normal(2.2, 0.65, rows), 0.7, 4.5).round(1)

    systolic = np.clip(
        104 + age * 0.42 + (bmi - 24) * 1.5 + stress * 1.1 + (smoking == "Yes") * 7 - exercise * 1.4
        + rng.normal(0, 10, rows),
        85,
        195,
    ).round()
    diastolic = np.clip(
        66 + age * 0.18 + (bmi - 24) * 0.8 + stress * 0.6 + (smoking == "Yes") * 4 - exercise * 0.8
        + rng.normal(0, 7, rows),
        50,
        125,
    ).round()
    sugar = np.clip(
        82 + age * 0.28 + (bmi - 24) * 2.1 + stress * 1.2 - exercise * 1.5 + rng.normal(0, 15, rows),
        60,
        280,
    ).round()
    heart_rate = np.clip(72 + stress * 1.9 - exercise * 1.3 + (smoking == "Yes") * 5 + rng.normal(0, 9, rows), 45, 145).round()

    diabetes_prob = sigmoid(-7.0 + age * 0.035 + bmi * 0.105 + sugar * 0.028 + stress * 0.12 - exercise * 0.18)
    heart_prob = sigmoid(
        -8.0 + age * 0.05 + systolic * 0.018 + heart_rate * 0.014 + (smoking == "Yes") * 0.9
        + (alcohol == "Heavy") * 0.5 + stress * 0.11 - exercise * 0.14
    )
    hypertension_prob = sigmoid(-9.0 + age * 0.035 + systolic * 0.045 + diastolic * 0.035 + bmi * 0.05 + stress * 0.08)
    obesity_prob = sigmoid(-10.0 + bmi * 0.38 + age * 0.01 - exercise * 0.22 + (sleep < 6) * 0.55)
    cancer_prob = sigmoid(
        -8.5 + age * 0.045 + (smoking == "Yes") * 1.6 + (alcohol == "Heavy") * 0.9 
        + (alcohol == "Regular") * 0.45 + stress * 0.12 - exercise * 0.15 - water * 0.1
    )

    df = pd.DataFrame(
        {
            "Age": age,
            "Gender": gender,
            "Height": height,
            "Weight": weight,
            "BMI": bmi,
            "Systolic BP": systolic.astype(int),
            "Diastolic BP": diastolic.astype(int),
            "Blood Sugar": sugar.astype(int),
            "Heart Rate": heart_rate.astype(int),
            "Sleep Hours": sleep,
            "Exercise Frequency": exercise,
            "Smoking": smoking,
            "Alcohol": alcohol,
            "Stress Level": stress,
            "Water Intake": water,
            "Diabetes Risk": rng.binomial(1, diabetes_prob),
            "Heart Disease Risk": rng.binomial(1, heart_prob),
            "Hypertension Risk": rng.binomial(1, hypertension_prob),
            "Obesity Risk": rng.binomial(1, obesity_prob),
            "Cancer Risk": rng.binomial(1, cancer_prob),
        }
    )
    return df


def build_preprocessor() -> ColumnTransformer:
    numeric_features = [feature for feature in FEATURES if feature not in {"Gender", "Smoking", "Alcohol"}]
    categorical_features = ["Gender", "Smoking", "Alcohol"]
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )


def evaluate(y_true, y_pred, y_prob=None) -> dict:
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    roc_auc = round(roc_auc_score(y_true, y_prob), 4) if y_prob is not None else 0.0

    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "roc_auc": roc_auc,
        "sensitivity": round(sensitivity, 4),
        "specificity": round(specificity, 4),
        "confusion_matrix": cm.tolist(),
    }


def train() -> dict:
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DATASET_PATH.exists():
        df = pd.read_csv(DATASET_PATH)
    else:
        df = generate_synthetic_dataset()
        df.to_csv(DATASET_PATH, index=False)

    X = df[FEATURES]
    trained_models = {}
    metrics = {}

    for disease, target in TARGETS.items():
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
        )
        candidates = {
            "Random Forest": RandomForestClassifier(
                n_estimators=220,
                max_depth=10,
                class_weight="balanced",
                random_state=RANDOM_STATE,
            ),
            "Logistic Regression": LogisticRegression(max_iter=1500, class_weight="balanced"),
        }
        disease_metrics = {}
        best_name = ""
        best_pipeline = None
        best_f1 = -1.0

        for name, estimator in candidates.items():
            pipeline = Pipeline(
                steps=[
                    ("preprocess", build_preprocessor()),
                    ("model", estimator),
                ]
            )
            pipeline.fit(X_train, y_train)
            predictions = pipeline.predict(X_test)
            probs = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else None
            candidate_metrics = evaluate(y_test, predictions, probs)
            disease_metrics[name] = candidate_metrics
            if candidate_metrics["f1"] > best_f1:
                best_f1 = candidate_metrics["f1"]
                best_name = name
                best_pipeline = pipeline

        trained_models[disease] = best_pipeline
        metrics[disease] = {
            "best_model": best_name,
            "comparison": disease_metrics,
        }

    bundle = {
        "models": trained_models,
        "metrics": metrics,
        "features": FEATURES,
        "targets": TARGETS,
        "dataset_path": str(DATASET_PATH),
    }
    joblib.dump(bundle, MODEL_PATH)
    return bundle


if __name__ == "__main__":
    result = train()
    print(f"Dataset saved to: {DATASET_PATH}")
    print(f"Model bundle saved to: {MODEL_PATH}")
    for disease, metric in result["metrics"].items():
        best = metric["best_model"]
        f1 = metric["comparison"][best]["f1"]
        print(f"{disease}: best={best}, f1={f1}")

