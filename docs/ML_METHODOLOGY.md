# Medi-Guard AI — Machine Learning Methodology & Evaluation Specification

## 1. Overview & Datasets

Medi-Guard AI implements machine learning classification pipelines to predict five preventive disease risk indicators:
1. **Diabetes Risk** (Trained on real CDC Diabetes Health Indicators data via `ucimlrepo`)
2. **Heart Disease Risk** (Synthetic healthcare dataset)
3. **Hypertension Risk** (Synthetic healthcare dataset)
4. **Obesity Risk** (Synthetic healthcare dataset)
5. **Cancer Risk** (Synthetic healthcare dataset)

### 1.1 CDC Diabetes Health Indicators Dataset (UCI Repo ID 891)
- **Source**: UCI ML Repository (`from ucimlrepo import fetch_ucirepo; fetch_ucirepo(id=891)`)
- **Size**: **253,680 real health survey records**
- **Target**: `Diabetes_binary` (0 = No Diabetes, 1 = Prediabetes/Diabetes)
- **Features (21 parameters)**: `HighBP`, `HighChol`, `CholCheck`, `BMI`, `Smoker`, `Stroke`, `HeartDiseaseorAttack`, `PhysActivity`, `Fruits`, `Veggies`, `HvyAlcoholConsump`, `AnyHealthcare`, `NoDocbcCost`, `GenHlth`, `MentHlth`, `PhysHlth`, `DiffWalk`, `Sex`, `Age`, `Education`, `Income`
- **Cached Dataset Path**: `datasets/cdc_diabetes_health_indicators.csv`

### 1.2 Multi-Condition Demonstration Dataset
- **Size**: 5,000 synthetic patient records generated via `train_model.py`.
- **Feature Set**: Age, Gender, Height, Weight, BMI, Systolic BP, Diastolic BP, Blood Sugar, Heart Rate, Sleep Hours, Exercise Frequency, Smoking, Alcohol, Stress Level, Water Intake.

> **Disclaimer**: Synthetic data is used for academic demonstration. Real CDC survey data powers the Diabetes classifier. Models do not replace clinical diagnosis.

---

## 2. Preprocessing & Feature Pipeline

- **UCI CDC Features Mapping**: Real-time feature mapping converts user `HealthProfile` entries into 21 CDC health survey indicators (`profile_to_cdc_row`).
- **Standard Preprocessing**: Numerical features are scaled using `StandardScaler()`. Categorical variables (`Gender`, `Smoking`, `Alcohol`) are encoded via `OneHotEncoder(handle_unknown="ignore")`.

---

## 3. Model Training & Performance Metrics

For each target disease condition, two distinct classifiers are trained independently:
1. **Random Forest Classifier** (`n_estimators=100`, `max_depth=12`, `class_weight="balanced"`)
2. **Logistic Regression** (`max_iter=1500`, `class_weight="balanced"`)

A 80/20 train/test split with target stratification is performed (`test_size=0.2`, `stratify=y`).
The model achieving the highest **F1 Score** on the holdout test set is selected for inference export in `models/risk_prediction_model.pkl`.

### Performance Results (Holdout Test Split):

| Disease Target | Dataset Source | Selected Model | F1 Score | Accuracy | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Diabetes** | **UCI CDC Repo #891** (253,680 records) | **Random Forest** | **0.4456** | **0.7380** | **0.8232** |
| **Heart Disease** | Synthetic Dataset | Logistic Regression | 0.5145 | 0.6380 | 0.7826 |
| **Hypertension** | Synthetic Dataset | Random Forest | 0.9189 | 0.9230 | 0.7772 |
| **Obesity** | Synthetic Dataset | Random Forest | 0.7403 | 0.8840 | 0.8424 |

---

## 4. Model Deployment & Resource Caching

The Scikit-learn model bundle is loaded using Streamlit's `@st.cache_resource` decorator in `utils/risk_predictor.py`, preventing redundant disk I/O on application reruns.
