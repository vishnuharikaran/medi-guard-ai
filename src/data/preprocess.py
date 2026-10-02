"""Data Validation and Preprocessing Pipelines for Medi-Guard AI."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = ROOT / "data" / "raw"
PROCESSED_DATA_DIR = ROOT / "data" / "processed"


def preprocess_heart_disease() -> dict:
    """Preprocesses UCI Heart Disease Dataset (ID 45)."""
    raw_path = RAW_DATA_DIR / "heart_disease" / "heart_disease.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw Heart Disease dataset not found at {raw_path}")

    df = pd.read_csv(raw_path)
    # Target binarization: num > 0 indicates presence of heart disease
    y = (df["num"] > 0).astype(int)
    feature_cols = [c for c in df.columns if c != "num"]
    X = df[feature_cols]

    out_dir = PROCESSED_DATA_DIR / "heart_disease"
    out_dir.mkdir(parents=True, exist_ok=True)

    proc_df = pd.concat([X, y.rename("target")], axis=1)
    proc_df.to_csv(out_dir / "heart_disease_processed.csv", index=False)

    schema = {
        "dataset_name": "UCI Heart Disease (ID 45)",
        "features": feature_cols,
        "target": "target",
        "rows": int(df.shape[0]),
        "pos_count": int(y.sum()),
        "neg_count": int((y == 0).sum())
    }
    with open(out_dir / "feature_schema.json", "w") as f:
        json.dump(schema, f, indent=2)

    print(f"[OK] [Preprocess Heart Disease] Saved {df.shape[0]} rows to {out_dir}")
    return schema


def preprocess_diabetes() -> dict:
    """Preprocesses CDC Diabetes Health Indicators Dataset (UCI ID 891)."""
    raw_path = RAW_DATA_DIR / "diabetes" / "cdc_diabetes_health_indicators.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw Diabetes dataset not found at {raw_path}")

    df = pd.read_csv(raw_path)
    y = df["Diabetes_binary"].astype(int)
    feature_cols = [c for c in df.columns if c != "Diabetes_binary"]
    X = df[feature_cols]

    out_dir = PROCESSED_DATA_DIR / "diabetes"
    out_dir.mkdir(parents=True, exist_ok=True)

    proc_df = pd.concat([X, y.rename("target")], axis=1)
    proc_df.to_csv(out_dir / "diabetes_processed.csv", index=False)

    schema = {
        "dataset_name": "CDC Diabetes Health Indicators (UCI ID 891)",
        "features": feature_cols,
        "target": "target",
        "rows": int(df.shape[0]),
        "pos_count": int(y.sum()),
        "neg_count": int((y == 0).sum())
    }
    with open(out_dir / "feature_schema.json", "w") as f:
        json.dump(schema, f, indent=2)

    print(f"[OK] [Preprocess Diabetes] Saved {df.shape[0]} rows to {out_dir}")
    return schema


def preprocess_stroke() -> dict:
    """Preprocesses Stroke Prediction Dataset."""
    raw_path = RAW_DATA_DIR / "stroke" / "healthcare-dataset-stroke-data.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw Stroke dataset not found at {raw_path}")

    df = pd.read_csv(raw_path)
    if "id" in df.columns:
        df = df.drop(columns=["id"])

    y = df["stroke"].astype(int)
    feature_cols = [c for c in df.columns if c != "stroke"]
    X = df[feature_cols]

    out_dir = PROCESSED_DATA_DIR / "stroke"
    out_dir.mkdir(parents=True, exist_ok=True)

    proc_df = pd.concat([X, y.rename("target")], axis=1)
    proc_df.to_csv(out_dir / "stroke_processed.csv", index=False)

    schema = {
        "dataset_name": "Stroke Prediction Dataset (Kaggle)",
        "features": feature_cols,
        "target": "target",
        "rows": int(df.shape[0]),
        "pos_count": int(y.sum()),
        "neg_count": int((y == 0).sum())
    }
    with open(out_dir / "feature_schema.json", "w") as f:
        json.dump(schema, f, indent=2)

    print(f"[OK] [Preprocess Stroke] Saved {df.shape[0]} rows to {out_dir}")
    return schema


def preprocess_chronic_kidney_disease() -> dict:
    """Preprocesses UCI Chronic Kidney Disease Dataset (ID 336)."""
    raw_path = RAW_DATA_DIR / "chronic_kidney_disease" / "chronic_kidney_disease.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw CKD dataset not found at {raw_path}")

    df = pd.read_csv(raw_path)
    # Clean whitespace and question marks
    df = df.apply(lambda col: col.astype(str).str.strip().replace("?", np.nan).replace("\t?", np.nan))

    # Binarize target: 1 if ckd and NOT notckd, else 0
    y = df["class"].astype(str).str.strip().str.lower().apply(
        lambda val: 1 if ("ckd" in val and "not" not in val) else 0
    )

    feature_cols = [c for c in df.columns if c != "class"]
    X = df[feature_cols]

    # Convert numeric fields
    numeric_cols = ["age", "bp", "bgr", "bu", "sc", "sod", "pot", "hemo", "pcv", "wbcc", "rbcc"]
    for col in numeric_cols:
        if col in X.columns:
            X[col] = pd.to_numeric(X[col], errors="coerce")

    out_dir = PROCESSED_DATA_DIR / "chronic_kidney_disease"
    out_dir.mkdir(parents=True, exist_ok=True)

    proc_df = pd.concat([X, y.rename("target")], axis=1)
    proc_df.to_csv(out_dir / "chronic_kidney_disease_processed.csv", index=False)

    schema = {
        "dataset_name": "UCI Chronic Kidney Disease (ID 336)",
        "features": feature_cols,
        "target": "target",
        "rows": int(df.shape[0]),
        "pos_count": int(y.sum()),
        "neg_count": int((y == 0).sum())
    }
    with open(out_dir / "feature_schema.json", "w") as f:
        json.dump(schema, f, indent=2)

    print(f"[OK] [Preprocess CKD] Saved {df.shape[0]} rows to {out_dir}")
    return schema


def preprocess_all():
    print("=== Medi-Guard AI Data Validation & Preprocessing ===")
    preprocess_heart_disease()
    preprocess_diabetes()
    preprocess_stroke()
    preprocess_chronic_kidney_disease()
    print("=== Preprocessing Complete ===")


if __name__ == "__main__":
    preprocess_all()
