# Medi-Guard AI — Dataset Integration & ML Pipeline Audit

## Executive Summary

This document presents a comprehensive audit of the dataset architecture, machine learning pipelines, feature mapping schemas, and integration roadmap for upgrading Medi-Guard AI to utilize four official, publicly available healthcare datasets from UCI Machine Learning Repository and Kaggle.

---

## 1. Existing ML Pipeline & Data Audit

### 1.1 Current Dataset Files & Paths
- **Synthetic Healthcare Dataset**: `datasets/healthcare_dataset.csv` (5,000 records).
- **CDC Diabetes Health Indicators Dataset**: `datasets/cdc_diabetes_health_indicators.csv` (253,680 records, UCI ID 891).

### 1.2 Current Model Training & Pipeline Architecture
- **Training Script**: `train_model.py` trains separate classifiers for Diabetes, Heart Disease, Hypertension, Obesity, and Cancer.
- **Model Bundle Artifact**: `models/risk_prediction_model.pkl` (cached via `@st.cache_resource` in `utils/risk_predictor.py`).
- **Feature Engineering**: `HealthProfile` dataclass in `utils/preprocessing.py` encapsulates input attributes and converts user vitals into standard or CDC model input rows.

---

## 2. Targeted Healthcare Datasets Audit

| Dataset Name | Official Source / ID | Primary Target | Rows / Features | Data Type & Notes |
| :--- | :--- | :--- | :--- | :--- |
| **UCI Heart Disease** | [UCI Repo ID 45](https://archive.ics.uci.edu/dataset/45/heart+disease) | `num` (binary `num > 0`) | 303 rows / 13 features | Clinical parameters (chest pain, resting BP, cholesterol, max HR, st depression). |
| **CDC Diabetes Health Indicators** | [UCI Repo ID 891](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators) | `Diabetes_binary` | 253,680 rows / 21 features | Survey-derived health indicators from CDC BRFSS. |
| **Stroke Prediction Dataset** | [Kaggle / Public Mirror](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset) | `stroke` (0/1) | 5,110 rows / 10 features | Demographics, glucose level, BMI, hypertension, heart disease. |
| **UCI Chronic Kidney Disease** | [UCI Repo ID 336](https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease) | `class` (`ckd`/`notckd`) | 400 rows / 24 features | Clinical lab values (blood urea, serum creatinine, hemoglobin, PCV, etc.). |

---

## 3. Potential Feature & Target Mismatches

1. **Target Definitions**:
   - UCI Heart Disease target `num` ranges from 0 to 4; must be binarized to `num > 0`.
   - UCI CKD target `class` contains string tags `ckd` / `notckd` (and occasional trailing spaces `ckd\t`); must be sanitized to binary 1/0.
   - CDC Diabetes target is binary `Diabetes_binary` (0/1).
   - Stroke target is binary `stroke` (0/1).
2. **Feature Mismatches & Input Form Mapping**:
   - Each model requires a distinct feature schema. User inputs from `HealthProfile` must be mapped into dataset-specific feature rows without mixing feature names or forcing artificial values.
3. **Missing Value Conventions**:
   - UCI CKD and Stroke datasets contain missing values (`?` or `NaN` in `bmi`, `hemo`, etc.). Preprocessing pipelines must apply training-fitted imputers (`SimpleImputer`).

---

## 4. Proposed Directory & Architecture Roadmap

### 4.1 Modular Directory Layout
```text
data/
  raw/
    heart_disease/
    diabetes/
    stroke/
    chronic_kidney_disease/
  processed/
    heart_disease/
    diabetes/
    stroke/
    chronic_kidney_disease/
  README.md

models/
  heart_disease/
  diabetes/
  stroke/
  chronic_kidney_disease/

src/
  data/
    download_datasets.py
    preprocess.py
  training/
    train_all_models.py
  inference/
    predict.py
  evaluation/
    evaluate_models.py
```

---

## 5. Optional Future Datasets (Documented)

- **UCI Heart Failure Clinical Records** ([UCI ID 519](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)): 299 clinical records for mortality prediction.
- **UCI Obesity Levels** ([UCI ID 544](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)): 2,111 records for obesity category classification.
- **CDC BRFSS Annual Data**: Large-scale annual behavioral risk survey microdata.
- **WHO NCD Microdata Repository**: Country-specific non-communicable disease survey data.
- **MIMIC-IV** ([PhysioNet](https://physionet.org/content/mimiciv/3.1/)): Requires credentialed access, ethics training, and formal data-use agreements; not suitable for uncredentialed automated downloading.
