# Medi-Guard AI — Educational Digital Health Twin & Future Disease Forecaster

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Tests-11%20Passed-success.svg)](tests/)

Medi-Guard AI is an educational health analytics application built with Python, Streamlit, Scikit-Learn, SQLite, Pandas, Plotly, and ReportLab. It simulates a digital health twin, calculates lifestyle age estimates, predicts future disease risks, performs priority triage, and compiles print-ready PDF reports.

---

> ⚠️ **EDUCATIONAL MEDICAL DISCLAIMER**: Medi-Guard AI is an academic demonstration software prototype. It is **not** a certified medical device and must **not** be used for medical diagnosis, treatment decisions, or clinical triage. Consult a licensed healthcare provider for clinical medical advice.

---

## 🔑 Key Features

- **Educational Health Scoring**: Calculates a weighted score from 0 to 100 across physiological vitals and lifestyle habits.
- **Experimental Lifestyle Age Estimate**: Approximates biological lifestyle impact relative to chronological age.
- **Machine Learning Disease Risk Forecasting**: Random Forest and Logistic Regression classifiers predicting Diabetes, Heart Disease, Hypertension, and Obesity risks.
- **2-Step PDF Report Parser**: Upload digital clinical PDFs, review extracted vitals, and apply them to the assessment form with explicit user confirmation.
- **Smart Educational Priority Triage**: Priority alert system (Green, Yellow, Orange, Red) with emergency safety notices.
- **Interactive What-If Lifestyle Simulator**: Dynamic side-by-side comparison of baseline habits versus simulated lifestyle adjustments.
- **Privacy & Record Control**: Session data privacy controls and database record deletion capabilities.
- **Escaped PDF Report Export**: Generates ReportLab PDF reports with XML text escaping and non-clinical disclaimers.

---

## 🛠️ Technology Stack

- **Frontend & Navigation**: Streamlit (Multi-page architecture with custom tabs)
- **Machine Learning**: Scikit-Learn (Random Forest, Logistic Regression, ColumnTransformer, StandardScaler, OneHotEncoder)
- **Data & Visualizations**: Pandas, NumPy, Plotly
- **Database & Persistence**: SQLite3
- **PDF Processing**: ReportLab, PyPDF
- **Testing**: Pytest

---

## 📁 Repository Structure

```text
medi-guard-ai/
├── app.py                      # Main Streamlit application entry point
├── train_model.py              # Machine learning training pipeline & synthetic dataset generator
├── requirements.txt            # Pinned project dependencies
├── README.md                   # Project documentation & overview
├── .env.example                # Environment variable configuration template
├── datasets/
│   └── healthcare_dataset.csv  # 5,000 synthetic patient records
├── models/
│   └── risk_prediction_model.pkl # Trained Scikit-learn model bundle (cached via @st.cache_resource)
├── database/
│   └── database.db             # SQLite storage (patients, health_records, predictions)
├── utils/
│   ├── validation.py           # Centralized health profile input validation
│   ├── database.py             # Parameterized database access layer & record deletion
│   ├── health_score.py         # Weighted educational health score calculator
│   ├── health_age.py           # Lifestyle age estimate rules
│   ├── risk_predictor.py       # Cached model inference module
│   ├── triage.py               # Priority triage heuristics & emergency alerts
│   ├── recommendation_engine.py# Dynamic educational recommendations
│   ├── pdf_generator.py        # ReportLab PDF generator with XML escaping
│   ├── pdf_parser.py           # PyPDF parser for health report auto-fill
│   ├── preprocessing.py        # HealthProfile dataclass & feature engineering
│   └── styles.py               # Modern healthcare UI CSS theme & Plotly template
├── pages/
│   ├── dashboard.py            # Historical metrics dashboard
│   ├── history.py              # Searchable patient history & record deletion
│   └── analytics.py            # Longitudinal health trend analytics
├── tests/                      # Automated Pytest test suite (11 unit tests)
│   ├── test_validation.py
│   ├── test_database.py
│   ├── test_ml_pipeline.py
│   ├── test_pdf_generator.py
│   └── test_security.py
└── docs/                       # Technical documentation specifications
    ├── PROJECT_AUDIT.md        # Codebase audit & refactoring roadmap
    ├── ARCHITECTURE.md         # Architecture & database schema specification
    ├── ML_METHODOLOGY.md       # Machine learning training & evaluation methodology
    ├── PRIVACY_AND_SAFETY.md   # Privacy lifecycle & medical disclaimers
    └── TESTING.md              # Automated test suite specification & execution logs
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

### 2. Train Models (Optional)
Generate the synthetic dataset and train the Scikit-learn model bundle:

```bash
python train_model.py
```

### 3. Run Automated Tests
Execute the pytest suite:

```bash
pytest -v
```

### 4. Launch Application
Start the Streamlit web application:

```bash
streamlit run app.py
```

---

## 📊 Machine Learning Model Performance

Models are evaluated on a 20% holdout test set across accuracy, precision, recall, F1 score, sensitivity, specificity, and ROC-AUC:

| Disease Target | Selected Model | F1 Score | Accuracy | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- |
| **Diabetes** | Logistic Regression | 0.7486 | 0.7420 | 0.8124 |
| **Heart Disease** | Logistic Regression | 0.5145 | 0.6380 | 0.6912 |
| **Hypertension** | Random Forest | 0.9189 | 0.9230 | 0.9745 |
| **Obesity** | Random Forest | 0.7403 | 0.8840 | 0.9102 |

---

## 🛡️ Security & Privacy

- **Input Validation**: Centralized validation in `utils/validation.py` checking numeric boundaries and Systolic > Diastolic blood pressure.
- **XSS & XML Escaping**: User inputs are escaped (`html.escape`) before rendering in HTML containers or ReportLab PDF paragraphs.
- **Data Ownership**: Record deletion tools (`delete_record`, `delete_all_records`) allow users to purge stored records on demand.
