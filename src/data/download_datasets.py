"""Dataset Acquisition Script for Medi-Guard AI."""

from __future__ import annotations

import argparse
from pathlib import Path
import urllib.request
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = ROOT / "data" / "raw"


def download_heart_disease() -> Path:
    """Acquires UCI Heart Disease Dataset (ID 45)."""
    target_dir = RAW_DATA_DIR / "heart_disease"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "heart_disease.csv"

    if target_file.exists():
        print(f"[OK] [Heart Disease] Raw dataset already exists: {target_file}")
        return target_file

    print("[INFO] [Heart Disease] Fetching UCI Heart Disease dataset (ID 45) via ucimlrepo...")
    try:
        from ucimlrepo import fetch_ucirepo
        hd = fetch_ucirepo(id=45)
        X = hd.data.features
        y = hd.data.targets
        df = pd.concat([X, y], axis=1)
        df.to_csv(target_file, index=False)
        print(f"[OK] [Heart Disease] Successfully saved {df.shape[0]} rows to: {target_file}")
        return target_file
    except Exception as e:
        print(f"[ERROR] [Heart Disease] Failed to fetch dataset: {e}")
        return target_file


def download_diabetes() -> Path:
    """Acquires CDC Diabetes Health Indicators Dataset (UCI ID 891)."""
    target_dir = RAW_DATA_DIR / "diabetes"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "cdc_diabetes_health_indicators.csv"

    if target_file.exists():
        print(f"[OK] [Diabetes] Raw dataset already exists: {target_file}")
        return target_file

    # Check if cached in datasets/ directory
    legacy_file = ROOT / "datasets" / "cdc_diabetes_health_indicators.csv"
    if legacy_file.exists():
        df = pd.read_csv(legacy_file)
        df.to_csv(target_file, index=False)
        print(f"[OK] [Diabetes] Copied from cached dataset to: {target_file}")
        return target_file

    print("[INFO] [Diabetes] Fetching CDC Diabetes Health Indicators dataset (UCI ID 891)...")
    try:
        from ucimlrepo import fetch_ucirepo
        cdc = fetch_ucirepo(id=891)
        X = cdc.data.features
        y = cdc.data.targets
        df = pd.concat([X, y], axis=1)
        df.to_csv(target_file, index=False)
        print(f"[OK] [Diabetes] Successfully saved {df.shape[0]} rows to: {target_file}")
        return target_file
    except Exception as e:
        print(f"[ERROR] [Diabetes] Failed to fetch dataset: {e}")
        return target_file


def download_stroke() -> Path:
    """Acquires Stroke Prediction Dataset."""
    target_dir = RAW_DATA_DIR / "stroke"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "healthcare-dataset-stroke-data.csv"

    if target_file.exists():
        print(f"[OK] [Stroke] Raw dataset already exists: {target_file}")
        return target_file

    print("[INFO] [Stroke] Fetching Stroke Prediction Dataset from public mirror...")
    mirror_url = "https://raw.githubusercontent.com/JulioArapa/mypackage/main/healthcare-dataset-stroke-data.csv"
    try:
        urllib.request.urlretrieve(mirror_url, target_file)
        df = pd.read_csv(target_file)
        print(f"[OK] [Stroke] Successfully downloaded {df.shape[0]} rows to: {target_file}")
        return target_file
    except Exception as e:
        print(f"[WARN] [Stroke] Automatic download mirror failed: {e}")
        print("  Manual Download Instructions:")
        print("  1. Download healthcare-dataset-stroke-data.csv from Kaggle: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset")
        print(f"  2. Place the file at: {target_file}")
        return target_file


def download_chronic_kidney_disease() -> Path:
    """Acquires UCI Chronic Kidney Disease Dataset (ID 336)."""
    target_dir = RAW_DATA_DIR / "chronic_kidney_disease"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "chronic_kidney_disease.csv"

    if target_file.exists():
        print(f"[OK] [Chronic Kidney Disease] Raw dataset already exists: {target_file}")
        return target_file

    print("[INFO] [Chronic Kidney Disease] Fetching UCI CKD dataset (ID 336) via ucimlrepo...")
    try:
        from ucimlrepo import fetch_ucirepo
        ckd = fetch_ucirepo(id=336)
        X = ckd.data.features
        y = ckd.data.targets
        df = pd.concat([X, y], axis=1)
        df.to_csv(target_file, index=False)
        print(f"[OK] [Chronic Kidney Disease] Successfully saved {df.shape[0]} rows to: {target_file}")
        return target_file
    except Exception as e:
        print(f"[ERROR] [Chronic Kidney Disease] Failed to fetch dataset: {e}")
        return target_file


def download_all():
    print("=== Medi-Guard AI Healthcare Dataset Acquisition ===")
    download_heart_disease()
    download_diabetes()
    download_stroke()
    download_chronic_kidney_disease()
    print("=== Acquisition Complete ===")


def main():
    parser = argparse.ArgumentParser(description="Download healthcare datasets for Medi-Guard AI.")
    parser.add_argument(
        "--dataset",
        choices=["heart_disease", "diabetes", "stroke", "chronic_kidney_disease", "all"],
        default="all",
        help="Specify which dataset to download.",
    )
    args = parser.parse_args()

    if args.dataset == "heart_disease":
        download_heart_disease()
    elif args.dataset == "diabetes":
        download_diabetes()
    elif args.dataset == "stroke":
        download_stroke()
    elif args.dataset == "chronic_kidney_disease":
        download_chronic_kidney_disease()
    else:
        download_all()


if __name__ == "__main__":
    main()
