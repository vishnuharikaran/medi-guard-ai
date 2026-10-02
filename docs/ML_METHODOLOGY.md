# Medi-Guard AI — Machine Learning Methodology & Evaluation Specification

## 1. Overview & Dataset Generation

Medi-Guard AI implements machine learning classification pipelines to predict five preventive disease risk indicators:
1. **Diabetes Risk**
2. **Heart Disease Risk**
3. **Hypertension Risk**
4. **Obesity Risk**
5. **Cancer Risk**

### 1.1 Synthetic Dataset Characteristics
- **Size**: 5,000 synthetic patient records generated via `train_model.py`.
- **Feature Set**: Age, Gender, Height, Weight, BMI, Systolic BP, Diastolic BP, Blood Sugar, Heart Rate, Sleep Hours, Exercise Frequency, Smoking, Alcohol, Stress Level, Water Intake.
- **Probabilistic Risk Formulas**: Clinical risk labels are generated using logistic sigmoid probabilistic equations combining established physiological interactions (e.g., BMI, BP, Blood Sugar, Smoking).

> **Disclaimer**: Synthetic data is used strictly for academic and educational demonstration. Models trained on synthetic data do not demonstrate real-world clinical performance.

---

## 2. Preprocessing & Feature Pipeline

All numerical and categorical features are encapsulated inside Scikit-learn `Pipeline` objects using a unified `ColumnTransformer`:
- **Numeric Pipeline**: Scaled using `StandardScaler()`.
- **Categorical Pipeline**: One-hot encoded using `OneHotEncoder(handle_unknown="ignore")`.

Feature ordering is strictly enforced between training time and real-time inference (`profile_to_model_row`).

---

## 3. Model Training & Selection Strategy

For each target disease condition, two distinct classifiers are trained independently:
1. **Random Forest Classifier** (`n_estimators=220`, `max_depth=10`, `class_weight="balanced"`)
2. **Logistic Regression** (`max_iter=1500`, `class_weight="balanced"`)

A 80/20 train/test split with target stratification is performed (`test_size=0.2`, `stratify=y`).
The model achieving the highest **F1 Score** on the holdout test set is automatically selected for inference export in `models/risk_prediction_model.pkl`.

---

## 4. Extended Evaluation Metrics

Model performance is evaluated across eight quantitative metrics on the test split:
- **Accuracy**: Overall prediction correctness.
- **Precision**: Ratio of true positive predictions to total positive predictions.
- **Recall (Sensitivity)**: Ratio of true positive predictions to total actual positive cases.
- **Specificity**: Ratio of true negative predictions to total actual negative cases.
- **F1 Score**: Harmonic mean of Precision and Recall.
- **ROC-AUC**: Area under the Receiver Operating Characteristic curve.
- **Confusion Matrix**: Full `[[TN, FP], [FN, TP]]` classification layout.

---

## 5. Model Deployment & Resource Caching

The 17.6MB Scikit-learn model bundle is loaded using Streamlit's `@st.cache_resource` decorator in `utils/risk_predictor.py`, preventing redundant disk I/O on application reruns.
