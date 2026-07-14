# MediGuard AI Project Report

## Title

MediGuard AI: Digital Health Twin and Future Disease Risk Forecaster

## Objective

The objective of MediGuard AI is to build a complete machine learning web application that helps users understand preventive health risk. The system accepts a health profile, creates a digital health twin, estimates health score and health age, predicts disease risks, assigns a triage priority, generates recommendations, and stores all outcomes for trend analysis.

## Technology Stack

- Frontend: Streamlit
- Backend: Python
- Machine Learning: Scikit-Learn
- Data Processing: Pandas, NumPy
- Database: SQLite
- Visualization: Plotly
- Model Storage: Joblib
- Deployment Target: Streamlit Cloud

## Modules

### User Health Profile

The Streamlit form collects demographic, physical, clinical, and lifestyle data:

- Name, age, gender
- Height, weight, BMI
- Systolic and diastolic blood pressure
- Blood sugar and heart rate
- Sleep, exercise, smoking, alcohol, stress, and water intake

### Health Score

The health score uses weighted rules across BMI, blood pressure, blood sugar, heart rate, sleep, exercise, smoking, and stress. The score is normalized from 0 to 100 and assigned to a category:

- Excellent
- Good
- Average
- Poor
- Critical

### Health Age

Health age is estimated from actual age and lifestyle or clinical modifiers. Risk factors such as high BMI, high blood pressure, high blood sugar, smoking, poor sleep, low exercise, and high stress increase health age. Healthy habits reduce it.

### Disease Risk Prediction

The system predicts four disease risks:

- Diabetes
- Heart Disease
- Hypertension
- Obesity

Each disease uses a binary classifier. Random Forest and Logistic Regression are compared independently, and the best model for each target is selected using F1 Score.

### Smart Triage

The triage engine classifies priority as:

- Green: Normal
- Yellow: Moderate
- Orange: Urgent
- Red: Critical

The classification uses blood pressure, blood sugar, heart rate, and predicted risk scores.

### Recommendation Engine

Recommendations are generated dynamically from the user's profile and risk levels. The engine provides suggestions for diet, exercise, sleep, stress management, hydration, smoking reduction, alcohol reduction, and preventive screening.

## Dataset

If no dataset exists, `train_model.py` creates a synthetic healthcare dataset with 5000 records. The data uses realistic distributions for age, gender, height, weight, BMI, blood pressure, blood sugar, heart rate, sleep, exercise, smoking, alcohol, stress, and water intake.

Disease labels are generated from probabilistic formulas that increase risk based on clinically plausible factors such as age, BMI, high blood sugar, high blood pressure, smoking, stress, sleep, and low exercise.

## Model Training

The training pipeline performs:

1. Dataset loading or generation.
2. Feature selection.
3. Train/test split.
4. Numeric scaling.
5. Categorical one-hot encoding.
6. Random Forest training.
7. Logistic Regression training.
8. Evaluation with Accuracy, Precision, Recall, and F1 Score.
9. Best-model selection by disease.
10. Joblib model export.

## Database Schema

### patients

Stores patient identity metadata.

### health_records

Stores submitted health profile values, health score, health age, and triage outcome.

### predictions

Stores each disease prediction, probability, confidence score, and risk label.

## User Interface

The application uses a professional light healthcare dashboard with white background, blue accents, clean metrics, Plotly charts, tables, and responsive Streamlit columns. Pages include:

- Main assessment form
- Dashboard
- Patient History
- Health Trend Analytics

## Limitations

This project uses synthetic data and rule-based clinical approximations. It is intended for academic demonstration and preventive awareness only. It is not a certified medical device and must not be used for diagnosis.

## Future Enhancements

- Integrate real de-identified clinical datasets.
- Add model explainability with SHAP.
- Add user authentication.
- Add PDF report export.
- Add clinician dashboard mode.
- Add wearable data import.

