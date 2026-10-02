"""Independent Model Training Pipeline for Medi-Guard AI Healthcare Datasets."""

from __future__ import annotations

import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"
RANDOM_STATE = 42


def evaluate(y_true, y_pred, y_prob=None) -> dict:
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    try:
        roc_auc = round(roc_auc_score(y_true, y_prob), 4) if y_prob is not None and len(set(y_true)) > 1 else 0.0
    except Exception:
        roc_auc = 0.0

    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "roc_auc": roc_auc,
        "sensitivity": round(sensitivity, 4),
        "specificity": round(specificity, 4),
        "confusion_matrix": cm.tolist(),
        "tp": int(tp),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
    }


def train_single_dataset(dataset_name: str, processed_file: str, id_col: str | None = None) -> dict:
    """Trains independent classifiers for a specific dataset."""
    data_dir = PROCESSED_DATA_DIR / dataset_name
    filepath = data_dir / processed_file
    if not filepath.exists():
        raise FileNotFoundError(f"Processed dataset not found at {filepath}")

    df = pd.read_csv(filepath)
    if id_col and id_col in df.columns:
        df = df.drop(columns=[id_col])

    y = df["target"].astype(int)
    X = df.drop(columns=["target"])

    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]), num_cols),
            ("cat", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore"))
            ]), cat_cols)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y if len(y.unique()) > 1 else None
    )

    candidates = {
        "Random Forest": RandomForestClassifier(
            n_estimators=150, max_depth=10, class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1
        ),
        "Logistic Regression": LogisticRegression(max_iter=1500, class_weight="balanced"),
    }

    best_name = ""
    best_pipeline = None
    best_f1 = -1.0
    comparison_metrics = {}

    for name, clf in candidates.items():
        pipeline = Pipeline(steps=[
            ("preprocess", preprocessor),
            ("classifier", clf)
        ])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        if hasattr(pipeline, "predict_proba"):
            probs_matrix = pipeline.predict_proba(X_test)
            y_prob = probs_matrix[:, 1] if probs_matrix.shape[1] > 1 else probs_matrix[:, 0]
        else:
            y_prob = None
        
        metrics = evaluate(y_test, y_pred, y_prob)
        comparison_metrics[name] = metrics

        if metrics["f1"] >= best_f1:
            best_f1 = metrics["f1"]
            best_name = name
            best_pipeline = pipeline

    out_dir = MODELS_DIR / dataset_name
    out_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_pipeline, out_dir / "model.pkl")

    metadata = {
        "dataset_name": dataset_name,
        "features": list(X.columns),
        "target": "target",
        "best_model": best_name,
        "test_split_size": len(X_test),
        "metrics": comparison_metrics[best_name],
        "all_metrics": comparison_metrics
    }

    with open(out_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    with open(out_dir / "feature_schema.json", "w") as f:
        json.dump({"features": list(X.columns), "num_features": num_cols, "cat_features": cat_cols}, f, indent=2)

    print(f"[OK] Trained [{dataset_name}] Best: {best_name} | F1: {best_f1:.4f} | ROC-AUC: {comparison_metrics[best_name]['roc_auc']:.4f}")
    return metadata


def train_all() -> dict:
    print("=== Medi-Guard AI Model Training Pipeline ===")
    results = {}
    datasets = [
        ("heart_disease", "heart_disease_processed.csv", None),
        ("diabetes", "diabetes_processed.csv", None),
        ("stroke", "stroke_processed.csv", None),
        ("chronic_kidney_disease", "chronic_kidney_disease_processed.csv", None),
    ]

    for name, file_name, id_col in datasets:
        results[name] = train_single_dataset(name, file_name, id_col)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORTS_DIR / "model_evaluation_summary.json", "w") as f:
        json.dump(results, f, indent=2)

    print("=== Training Complete ===")
    return results


if __name__ == "__main__":
    train_all()
