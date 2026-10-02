# Medi-Guard AI — Technical Architecture & Database Schema Specification

## 1. System Architecture Overview

Medi-Guard AI follows a modular, decoupled Python architecture layered into five functional subsystems:

```text
               +-------------------------------------------------------+
               |                  Streamlit UI Layer                   |
               | (app.py, pages/dashboard.py, history.py, analytics.py) |
               +---------------------------+---------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |               Input Validation Layer                  |
               |                 (utils/validation.py)                 |
               +---------------------------+---------------------------+
                                           |
             +-----------------------------+-----------------------------+
             |                                                           |
             v                                                           v
+--------------------------+                               +--------------------------+
|  ML Inference Engine     |                               | SQLite Persistence Layer |
| (utils/risk_predictor.py)|                               |   (utils/database.py)    |
| (Cached @st.cache_res)   |                               |  (database/database.db)  |
+--------------------------+                               +--------------------------+
             |                                                           |
             +-----------------------------+-----------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |               PDF Generator & Report Engine           |
               |               (utils/pdf_generator.py)                |
               +-------------------------------------------------------+
```

---

## 2. Database Schema Specification

The application uses SQLite3 at `database/database.db` with foreign key relationships between patient metadata, assessment records, and disease predictions.

### 2.1 Table: `patients`
Stores patient demographic identifiers.
```sql
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

### 2.2 Table: `health_records`
Stores submitted physical metrics, vital parameters, lifestyle factors, score metrics, and triage outcomes.
```sql
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    recorded_at TEXT NOT NULL,
    height REAL,
    weight REAL,
    bmi REAL,
    systolic_bp REAL,
    diastolic_bp REAL,
    blood_sugar REAL,
    heart_rate REAL,
    sleep_hours REAL,
    exercise_frequency INTEGER,
    smoking TEXT,
    alcohol TEXT,
    stress_level INTEGER,
    water_intake REAL,
    health_score INTEGER,
    risk_category TEXT,
    health_age INTEGER,
    triage_color TEXT,
    triage_level TEXT,
    triage_action TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);
```

### 2.3 Table: `predictions`
Stores target disease risk probabilities and classification labels.
```sql
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    disease TEXT NOT NULL,
    risk_probability REAL NOT NULL,
    confidence REAL NOT NULL,
    label TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(record_id) REFERENCES health_records(id)
);
```

---

## 3. Data Flow & Security Mechanisms

1. **User Input / PDF Upload**: User enters profile details or uploads a PDF. Extracted PDF details require explicit user review and confirmation before form auto-fill.
2. **Input Validation**: `validate_health_profile()` checks all numeric boundaries and enforces `Systolic BP > Diastolic BP`.
3. **Model Inference**: `predict_disease_risks()` loads the model bundle (cached in memory via `@st.cache_resource`) and calculates model probabilities.
4. **HTML & XML Escaping**: All text rendered in HTML components or generated PDF ReportLab paragraphs is XML-escaped (`html.escape`).
5. **Persistence**: `save_assessment()` executes parameterized SQL queries. Records can be removed individually (`delete_record`) or in bulk (`delete_all_records`).
