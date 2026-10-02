# Medi-Guard AI — Healthcare Datasets Specification & Acquisition Guide

This directory contains raw and processed healthcare datasets used to train independent experimental machine learning classifiers in Medi-Guard AI.

---

## 📋 Targeted Healthcare Datasets Overview

### 1. UCI Heart Disease Dataset
- **Official Source**: [UCI Machine Learning Repository — Heart Disease (ID 45)](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **Local Directory**: `data/raw/heart_disease/`
- **Expected File**: `data/raw/heart_disease/heart_disease.csv`
- **Target Column**: `num` (Converted to binary target `num > 0`: 0 = No Disease, 1 = Presence of Disease)
- **Features (13)**: `age`, `sex`, `cp` (chest pain type), `trestbps` (resting BP), `chol` (serum cholesterol), `fbs` (fasting blood sugar > 120), `restecg`, `thalach` (max heart rate), `exang` (exercise angina), `oldpeak`, `slope`, `ca`, `thal`
- **License / Restrictions**: Open public domain for research.

---

### 2. CDC Diabetes Health Indicators Dataset
- **Official Source**: [UCI Machine Learning Repository — CDC Diabetes Health Indicators (ID 891)](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)
- **Local Directory**: `data/raw/diabetes/`
- **Expected File**: `data/raw/diabetes/cdc_diabetes_health_indicators.csv`
- **Target Column**: `Diabetes_binary` (0 = No Diabetes, 1 = Prediabetes / Diabetes)
- **Features (21)**: `HighBP`, `HighChol`, `CholCheck`, `BMI`, `Smoker`, `Stroke`, `HeartDiseaseorAttack`, `PhysActivity`, `Fruits`, `Veggies`, `HvyAlcoholConsump`, `AnyHealthcare`, `NoDocbcCost`, `GenHlth`, `MentHlth`, `PhysHlth`, `DiffWalk`, `Sex`, `Age`, `Education`, `Income`
- **License / Restrictions**: Public domain survey data from CDC BRFSS.

---

### 3. Stroke Prediction Dataset
- **Primary Source**: [Kaggle — Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)
- **Local Directory**: `data/raw/stroke/`
- **Expected File**: `data/raw/stroke/healthcare-dataset-stroke-data.csv`
- **Target Column**: `stroke` (0 = No Stroke, 1 = Stroke)
- **Features (10)**: `gender`, `age`, `hypertension`, `heart_disease`, `ever_married`, `work_type`, `Residence_type`, `avg_glucose_level`, `bmi`, `smoking_status`
- **License / Restrictions**: CC0: Public Domain.
- **Manual Download Instructions**: If automatic download mirror is unavailable, download `healthcare-dataset-stroke-data.csv` directly from Kaggle and place it in `data/raw/stroke/`.

---

### 4. UCI Chronic Kidney Disease Dataset
- **Official Source**: [UCI Machine Learning Repository — Chronic Kidney Disease (ID 336)](https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease)
- **Local Directory**: `data/raw/chronic_kidney_disease/`
- **Expected File**: `data/raw/chronic_kidney_disease/chronic_kidney_disease.csv`
- **Target Column**: `class` (Converted to binary target: 1 if `class == 'ckd'` else 0)
- **Features (24)**: `age`, `bp`, `sg`, `al`, `su`, `rbc`, `pc`, `pcc`, `ba`, `bgr`, `bu`, `sc`, `sod`, `pot`, `hemo`, `pcv`, `wbcc`, `rbcc`, `htn`, `dm`, `cad`, `appet`, `pe`, `ane`
- **License / Restrictions**: Open public domain for research.

---

## 🔮 Optional Future Datasets (Documented)

- **UCI Heart Failure Clinical Records** (ID 519): 299 clinical records for mortality prediction.
- **UCI Obesity Levels** (ID 544): 2,111 records for obesity category classification.
- **CDC BRFSS Microdata**: Large-scale annual behavioral risk survey microdata.
- **WHO NCD Microdata Repository**: Country-specific non-communicable disease survey data.
- **MIMIC-IV** ([PhysioNet](https://physionet.org/content/mimiciv/3.1/)): Requires credentialed access, ethics training, and formal data-use agreements.
