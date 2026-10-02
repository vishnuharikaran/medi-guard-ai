# Medi-Guard AI — Automated Testing & Verification Specification

## 1. Overview

Medi-Guard AI includes a comprehensive automated test suite built with `pytest`. The test suite verifies input validation, database operations, machine learning inference, PDF generation, security escaping, and code cleanliness.

---

## 2. Test Cases Overview

| Test Module | Test Name | Purpose | Result |
| :--- | :--- | :--- | :--- |
| `test_validation.py` | `test_valid_profile` | Verifies a compliant HealthProfile passes validation | **PASSED** |
| `test_validation.py` | `test_invalid_blood_pressure_systolic_less_than_diastolic` | Verifies validation fails when Systolic <= Diastolic BP | **PASSED** |
| `test_validation.py` | `test_out_of_range_values` | Verifies validation catches out-of-range numeric values | **PASSED** |
| `test_database.py` | `test_save_and_load_assessment` | Verifies SQLite insertion and querying via parameterized SQL | **PASSED** |
| `test_database.py` | `test_delete_record` | Verifies single record deletion from database tables | **PASSED** |
| `test_ml_pipeline.py` | `test_model_availability` | Verifies model file exists at `models/risk_prediction_model.pkl` | **PASSED** |
| `test_ml_pipeline.py` | `test_model_bundle_loading` | Verifies cached model bundle structure | **PASSED** |
| `test_ml_pipeline.py` | `test_predict_disease_risks` | Verifies probability output range (0-1) across all conditions | **PASSED** |
| `test_pdf_generator.py` | `test_pdf_generation_with_special_characters` | Verifies XML escaping for special characters (`<`, `>`, `&`) in PDF generation | **PASSED** |
| `test_security.py` | `test_html_escaping` | Verifies `html.escape` prevents script injection | **PASSED** |
| `test_security.py` | `test_no_speech_references_in_codebase` | Verifies application loads without speech dependencies | **PASSED** |

---

## 3. Actual Execution Log

```text
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
collected 11 items

tests/test_database.py::test_save_and_load_assessment PASSED             [  9%]
tests/test_database.py::test_delete_record PASSED                        [ 18%]
tests/test_ml_pipeline.py::test_model_availability PASSED                [ 27%]
tests/test_ml_pipeline.py::test_model_bundle_loading PASSED              [ 36%]
tests/test_ml_pipeline.py::test_predict_disease_risks PASSED             [ 45%]
tests/test_pdf_generator.py::test_pdf_generation_with_special_characters PASSED [ 54%]
tests/test_security.py::test_html_escaping PASSED                        [ 63%]
tests/test_security.py::test_no_speech_references_in_codebase PASSED     [ 72%]
tests/test_validation.py::test_valid_profile PASSED                      [ 81%]
tests/test_validation.py::test_invalid_blood_pressure_systolic_less_than_diastolic PASSED [ 90%]
tests/test_validation.py::test_out_of_range_values PASSED                [100%]

============================= 11 passed in 12.71s =============================
```

---

## 4. Running Tests Locally

To run the automated test suite locally:

```bash
pytest -v
```
