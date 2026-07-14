# MediGuard AI: Digital Health Twin and Future Disease Risk Forecaster

MediGuard AI is a final-year-level AI and Data Science machine learning project built with Streamlit, Python, SQLite, Scikit-Learn, Pandas, NumPy, Plotly, and Joblib.

It creates a digital health twin from a user health profile, predicts future disease risk, calculates a health score and health age, performs smart triage classification, stores results in SQLite, and visualizes trends across historical records.

## Features

- User health profile form with BMI, blood pressure, blood sugar, heart rate, sleep, exercise, smoking, alcohol, stress, and water intake.
- Weighted Health Score from 0 to 100 with categories: Excellent, Good, Average, Poor, Critical.
- Rule-based Health Age estimation.
- Disease risk prediction for Diabetes, Heart Disease, Hypertension, and Obesity.
- Random Forest and Logistic Regression model comparison with Accuracy, Precision, Recall, and F1 Score.
- Smart triage classification: Green, Yellow, Orange, Red.
- Dynamic recommendations for exercise, diet, sleep, stress, hydration, alcohol, and smoking.
- SQLite database with patient records, health records, and predictions.
- Interactive dashboard, analytics page, and searchable patient history.
- Synthetic healthcare dataset generator with 5000 realistic records.

## Project Structure

```text
medi_guard_ai/
  app.py
  train_model.py
  requirements.txt
  README.md
  PROJECT_REPORT.md
  database/
    database.db
  datasets/
    healthcare_dataset.csv
  models/
    risk_prediction_model.pkl
  utils/
    preprocessing.py
    health_score.py
    health_age.py
    risk_predictor.py
    triage.py
    recommendation_engine.py
    database.py
  pages/
    dashboard.py
    history.py
    analytics.py
  assets/
```

## Installation

Open a terminal inside the `medi_guard_ai` folder.

```bash
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

The first command installs dependencies. The second command creates `datasets/healthcare_dataset.csv`, trains machine learning models, compares Random Forest and Logistic Regression, and saves the selected disease models to `models/risk_prediction_model.pkl`. The third command starts the local Streamlit app.

## Database

The app uses SQLite at `database/database.db`. It creates the following tables automatically:

- `patients`
- `health_records`
- `predictions`

Every submitted assessment is stored for later dashboard, history, and analytics views.

## Machine Learning Pipeline

1. Generate or load a 5000-row synthetic healthcare dataset.
2. Engineer BMI and lifestyle-health features.
3. Train/test split with stratification for each disease target.
4. Train Random Forest and Logistic Regression pipelines.
5. Preprocess numeric features with `StandardScaler`.
6. Encode categorical features with `OneHotEncoder`.
7. Evaluate with Accuracy, Precision, Recall, and F1 Score.
8. Select the best model per disease using F1 Score.
9. Save the model bundle with Joblib.

## Important Note

MediGuard AI is an educational preventive screening project. It is not a medical device and must not be used as a replacement for professional medical advice, diagnosis, or treatment.

