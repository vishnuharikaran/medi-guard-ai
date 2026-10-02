# Medi-Guard AI — Comprehensive Project Audit & Refactoring Roadmap

## Executive Summary

Medi-Guard AI is an educational preventive health analytics application built with Python, Streamlit, Scikit-learn, SQLite, Pandas, Plotly, and ReportLab. This document presents a comprehensive technical, security, machine learning, medical safety, and UI/UX audit of the codebase, followed by a phase-by-phase refactoring plan.

---

## 1. Architectural & Entry Point Analysis

- **Entry Point**: `app.py` serves as the primary Streamlit entry point.
- **Pages Directory**: `pages/dashboard.py`, `pages/history.py`, `pages/analytics.py`.
- **Utils Package**: `database.py`, `health_age.py`, `health_score.py`, `pdf_generator.py`, `pdf_parser.py`, `preprocessing.py`, `recommendation_engine.py`, `risk_predictor.py`, `styles.py`, `triage.py`.
- **Models & Datasets**: `models/risk_prediction_model.pkl` (17.6 MB Scikit-learn model bundle), `datasets/healthcare_dataset.csv` (5,000 synthetic rows).
- **Database**: SQLite database at `database/database.db` storing `patients`, `health_records`, and `predictions`.

---

## 2. Comprehensive Findings & Identified Vulnerabilities

### 2.1 Security & Privacy
1. **Unauthenticated Public Patient Data Exposure**:
   - `utils/database.py` allows any application visitor to search and view all stored patient records and disease predictions without authentication or session isolation.
   - *Remediation*: Implement session-isolated local demonstration records and a privacy mode that prevents cross-user record exposure. Add explicit record deletion controls.
2. **XSS / Unsafe HTML Injection**:
   - `app.py` passes unescaped patient names into `st.markdown(..., unsafe_allow_html=True)`.
   - *Remediation*: Sanitize and escape all user-provided strings (using `html.escape`) before rendering in HTML cards, or replace with native Streamlit components.
3. **ReportLab Markup Injection in PDF Generation**:
   - `utils/pdf_generator.py` inserts raw strings like `profile.name` into ReportLab `Paragraph` objects without XML escaping (`<`, `>`, `&`).
   - *Remediation*: Use `xml.sax.saxutils.escape()` on all patient text inputs.
4. **Missing Environment Configuration**:
   - No `.env.example` file exists to document environment variable templates.

### 2.2 Medical Safety & Terminology
1. **Misleading Clinical Claims**:
   - PDF report headers, gauge labels, and UI captions used clinical terms like `"Diagnostic Clinical Report"`, `"Confidential - Medical Twin Diagnostic Screening Report"`, and `"10-Year ASCVD Cardiovascular Risk"`.
   - *Remediation*: Rename report titles to `"Medi-Guard — Educational Health Profile & Model Output Report"`. Rename formulas to `"Experimental Lifestyle-Based Age Estimate"` and `"Experimental Risk Score"`. Add prominent non-clinical educational disclaimers.
2. **Unvalidated Custom Formulas**:
   - The ASCVD gauge formula and Health Age adjustments use arbitrary point additions.
   - *Remediation*: Frame as experimental educational visualizations with documented assumptions and limitations.
3. **Triage Safety**:
   - Smart triage returns levels like `"Critical"`, `"Urgent"`, `"Moderate"`, `"Normal"`.
   - *Remediation*: Clearly label model outputs as experimental heuristics, separate raw vital measurements from ML predictions, and add emergency safety disclaimers.

### 2.3 Machine Learning Pipeline & Performance
1. **Uncached Model Loading**:
   - `risk_predictor.py` calls `joblib.load(MODEL_PATH)` on every single prediction call, loading a 17.6MB file repeatedly.
   - *Remediation*: Implement `@st.cache_resource` on `load_model_bundle()`.
2. **Misleading Confidence Metric**:
   - `confidence = max(probability, 1 - probability)` misrepresents class probability as prediction confidence.
   - *Remediation*: Display raw experimental model probability scores with clear model metrics and calibration context.
3. **Training & Pipeline Evaluation Gaps**:
   - Model training evaluates F1 score, precision, and recall, but lacks confusion matrices, ROC-AUC, PR-AUC, sensitivity, specificity, and calibration analysis.
   - *Remediation*: Expand `train_model.py` to calculate comprehensive evaluation metrics and save detailed model metadata.

### 2.4 Input Validation & PDF Parsing
1. **Lack of Centralized Validation**:
   - Profile inputs lack strict schema-level validation for logical combinations (e.g., Systolic BP <= Diastolic BP, extreme height/weight).
   - *Remediation*: Create `utils/validation.py` for centralized profile validation with clear user-facing error messages.
2. **PDF Parser Auto-fill Workflow**:
   - Currently auto-fills form fields directly without an explicit review and confirmation step.
   - *Remediation*: Implement a 2-step PDF confirmation workflow (Upload -> Review Extracted Fields -> Explicit User Confirmation -> Apply).

### 2.5 UI/UX & Navigation
1. **Visual Styling**:
   - Current dark mode style in `styles.py` contains heavy gradients and saturated metric cards.
   - *Remediation*: Redesign UI into a clean, modern, professional healthcare aesthetic with light background option, soft blue/teal accents, high accessibility contrast, responsive cards, and clean multi-page navigation.

---

## 3. Comprehensive Refactoring Roadmap

- **Phase 0**: Repository audit & baseline test setup (`tests/`).
- **Phase 1**: Verify complete removal of speech/audio features (completed in baseline, audited for zero remaining references).
- **Phase 2**: Application bug fixes (input handling, model loading, Streamlit reruns).
- **Phase 3**: Security & privacy hardening (escaping HTML/PDF markup, privacy-scoped data access, `.env.example`, data lifecycle docs).
- **Phase 4**: ML pipeline enhancements (Scikit-learn pipeline consistency, model caching, ROC-AUC / confusion matrix evaluation).
- **Phase 5**: Medical safety & terminology overhaul (renaming reports, disclaimer banners, experimental age label).
- **Phase 6**: Centralized input validation module (`utils/validation.py`).
- **Phase 7**: PDF extraction & user confirmation workflow.
- **Phase 8**: Complete UI/UX redesign (professional design system, responsive tabs/navigation, clean color palette).
- **Phase 9**: Interactive What-If Simulator improvements (baseline vs simulated comparison with disclaimer).
- **Phase 10**: Centralized database & session-scoped privacy layer (record deletion, search, session privacy).
- **Phase 11**: Performance & deployment optimization (caching, dependency pin check, Streamlit Cloud compatibility).
- **Phase 12**: Automated testing suite (`pytest` for validation, ML, DB, PDF, security).
- **Phase 13**: Complete technical documentation (`README.md`, `ARCHITECTURE.md`, `ML_METHODOLOGY.md`, `PRIVACY_AND_SAFETY.md`, `TESTING.md`).
- **Phase 14**: Final end-to-end validation.
