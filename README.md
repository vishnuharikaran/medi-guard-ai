# Medi-Guard AI — Multi-Dataset Educational Health Analytics & ML Risk Forecaster

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Tests-15%20Passed-success.svg)](tests/)

Medi-Guard AI is an educational health analytics application built with Python, Streamlit, Scikit-Learn, SQLite, Pandas, Plotly, and ReportLab. It integrates 4 official, documented healthcare datasets (**UCI Heart Disease**, **CDC Diabetes Health Indicators**, **Stroke Prediction Dataset**, and **UCI Chronic Kidney Disease**) to train independent experimental machine learning classifiers.

---

> ⚠️ **EDUCATIONAL MEDICAL DISCLAIMER**: Medi-Guard AI is an academic demonstration software project. Its model outputs are experimental risk indicators and are **not** a medical diagnosis, screening result, or substitute for professional medical advice. Do not delay or disregard seeking medical care based on this application.

---

## 🔑 Key Features

- **Multi-Dataset Model Classifiers**: 4 independent machine learning models trained on separate public datasets:
  - 🫀 **UCI Heart Disease** (ID 45) — 303 clinical records
  - 🩺 **CDC Diabetes Health Indicators** (UCI ID 891) — 253,680 survey records
  - 🧠 **Stroke Prediction Dataset** (Kaggle) — 5,110 patient records
  - 🧪 **UCI Chronic Kidney Disease** (ID 336) — 400 clinical lab records
- **Educational Health Scoring**: Calculates a weighted score from 0 to 100 across physiological vitals and lifestyle habits.
- **Experimental Lifestyle Age Estimate**: Approximates biological lifestyle impact relative to chronological age.
- **2-Step PDF Report Parser**: Upload digital clinical PDFs, review extracted vitals, and apply them to the assessment form with explicit user confirmation.
- **Smart Educational Priority Triage**: Priority alert system (Green, Yellow, Orange, Red) with emergency safety notices.
- **Interactive What-If Lifestyle Simulator**: Dynamic side-by-side comparison of baseline habits versus simulated lifestyle adjustments.
- **Privacy & Record Control**: Session data privacy controls and database record deletion capabilities.
- **Escaped PDF Report Export**: Generates ReportLab PDF reports with XML text escaping and non-clinical disclaimers.

---

## 🛠️ Technology Stack

- **Frontend & Navigation**: Streamlit (Multi-page architecture with custom tabs)
- **Machine Learning**: Scikit-Learn (Random Forest, Logistic Regression, ColumnTransformer, StandardScaler, OneHotEncoder, SimpleImputer)
- **Dataset Acquisition**: `ucimlrepo` (Official UCI ML Repository API)
- **Data & Visualizations**: Pandas, NumPy, Plotly
- **Database & Persistence**: SQLite3
- **PDF Processing**: ReportLab, PyPDF
- **Testing**: Pytest (15 automated unit tests)

---

## 📁 Repository Structure

```text
medi-guard-ai/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Pinned project dependencies
├── README.md                   # Project documentation & overview
├── .env.example                # Environment variable configuration template
├── data/                       # Dataset management directory
│   ├── raw/                    # Raw untouched dataset files
│   │   ├── heart_disease/
│   │   ├── diabetes/
│   │   ├── stroke/
│   │   └── chronic_kidney_disease/
│   ├── processed/              # Cleaned & feature-engineered datasets
│   │   ├── heart_disease/
│   │   ├── diabetes/
│   │   ├── stroke/
│   │   └── chronic_kidney_disease/
│   └── README.md               # Complete dataset specification guide
├── models/                     # Trained Scikit-Learn models & schemas
│   ├── heart_disease/
│   ├── diabetes/
│   ├── stroke/
│   └── chronic_kidney_disease/
├── src/                        # Core Python pipeline modules
│   ├── data/
│   │   ├── download_datasets.py# Automated dataset acquisition script
│   │   └── preprocess.py       # Data validation & preprocessing pipeline
│   ├── training/
│   │   └── train_all_models.py # Independent model training pipeline
│   ├── inference/
│   │   └── predict.py          # Cached inference module with schema mapping
│   └── evaluation/
│       └── evaluate_models.py  # Model evaluation report generator
├── reports/                    # Generated evaluation reports
│   ├── model_evaluation_report.md
│   └── model_evaluation_summary.json
├── database/
│   └── database.db             # SQLite storage (patients, health_records, predictions)
├── utils/                      # Helper & styling modules
│   ├── validation.py           # Centralized health profile input validation
│   ├── database.py             # Parameterized database access layer & record deletion
│   ├── health_score.py         # Weighted educational health score calculator
│   ├── health_age.py           # Lifestyle age estimate rules
│   ├── risk_predictor.py       # Cached inference wrapper
│   ├── triage.py               # Priority triage heuristics & emergency alerts
│   ├── recommendation_engine.py# Dynamic educational recommendations
│   ├── pdf_generator.py        # ReportLab PDF generator with XML escaping
│   ├── pdf_parser.py           # PyPDF parser for health report auto-fill
│   ├── preprocessing.py        # HealthProfile dataclass & feature engineering
│   └── styles.py               # Modern healthcare UI CSS theme & Plotly template
├── pages/                      # Streamlit multi-page dashboard views
│   ├── dashboard.py
│   ├── history.py
│   └── analytics.py
├── tests/                      # Automated Pytest test suite (15 unit tests)
│   ├── test_validation.py
│   ├── test_database.py
│   ├── test_dataset_integration.py
│   ├── test_ml_pipeline.py
│   ├── test_pdf_generator.py
│   └── test_security.py
└── docs/                       # Technical documentation specifications
    ├── DATASET_INTEGRATION_AUDIT.md
    ├── PROJECT_AUDIT.md
    ├── ARCHITECTURE.md
    ├── ML_METHODOLOGY.md
    ├── PRIVACY_AND_SAFETY.md
    └── TESTING.md
```

---

## 🚀 Quick Start Guide

### 1. Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/vishnuharikaran/medi-guard-ai.git
cd medi-guard-ai
pip install -r requirements.txt
```

### 2. Dataset Acquisition
Acquire all 4 targeted healthcare datasets:

```bash
python -m src.data.download_datasets --dataset all
```

### 3. Data Preprocessing
Run preprocessing pipelines:

```bash
python -m src.data.preprocess
```

### 4. Train Independent Models
Train Random Forest and Logistic Regression models for each dataset:

```bash
python -m src.training.train_all_models
```

### 5. Generate Evaluation Reports
Compile classification performance reports:

```bash
python -m src.evaluation.evaluate_models
```

### 6. Run Automated Tests
Execute the pytest suite:

```bash
pytest -v
```

### 7. Launch Application
Start the Streamlit web application:

```bash
streamlit run app.py
```

---

## 📊 Machine Learning Model Performance Summary

Evaluated on 20% holdout test splits across 4 independent dataset models:

| Disease Target | Dataset Source | Selected Model | Accuracy | F1 Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Heart Disease** | UCI Heart Disease (ID 45) | Random Forest | 0.9016 | 0.9000 | 0.9589 |
| **Diabetes** | CDC Diabetes Indicators (UCI ID 891) | Random Forest | 0.7380 | 0.4420 | 0.8226 |
| **Stroke** | Stroke Prediction Dataset (Kaggle) | Random Forest | 0.9423 | 0.2529 | 0.8004 |
| **Chronic Kidney Disease** | UCI Chronic Kidney Disease (ID 336) | Random Forest | 1.0000 | 1.0000 | 1.0000 |

---

## 🛡️ Security & Privacy

- **Input Validation**: Centralized validation in `utils/validation.py` checking numeric boundaries and Systolic > Diastolic blood pressure.
- **XSS & XML Escaping**: User inputs are escaped (`html.escape`) before rendering in HTML containers or ReportLab PDF paragraphs.
- **Data Ownership**: Record deletion tools (`delete_record`, `delete_all_records`) allow users to purge stored records on demand.
