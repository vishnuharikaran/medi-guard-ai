# Medi-Guard AI — Multi-Model Evaluation Report

This report details the quantitative test-set evaluation results for the 4 independent experimental disease-risk models trained in Medi-Guard AI.

---

## Summary Performance Table

| Dataset / Disease Model | Selected Model | Accuracy | Precision | Recall | Specificity | F1 Score | ROC-AUC | Test Split Size |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Heart Disease** | Random Forest | 0.9016 | 0.8438 | 0.9643 | 0.8485 | 0.9000 | 0.9589 | 61 |
| **Diabetes** | Random Forest | 0.7272 | 0.3091 | 0.7755 | 0.7194 | 0.4420 | 0.8226 | 50736 |
| **Stroke** | Random Forest | 0.8728 | 0.1774 | 0.4400 | 0.8951 | 0.2529 | 0.8004 | 1022 |
| **Chronic Kidney Disease** | Random Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 80 |

---

## Detailed Classification Metrics & Confusion Matrices

### Heart Disease (heart_disease)
- **Selected Classifier**: `Random Forest`
- **Features Evaluated**: 13 parameters
- **Accuracy**: `0.9016`
- **Precision**: `0.8438`
- **Recall (Sensitivity)**: `0.9643`
- **Specificity**: `0.8485`
- **F1 Score**: `0.9000`
- **ROC-AUC**: `0.9589`
- **Confusion Matrix**: 
  ```text
  True Negatives (TN): 28 | False Positives (FP): 5
  False Negatives (FN): 1 | True Positives (TP): 27
  ```

### Diabetes (diabetes)
- **Selected Classifier**: `Random Forest`
- **Features Evaluated**: 21 parameters
- **Accuracy**: `0.7272`
- **Precision**: `0.3091`
- **Recall (Sensitivity)**: `0.7755`
- **Specificity**: `0.7194`
- **F1 Score**: `0.4420`
- **ROC-AUC**: `0.8226`
- **Confusion Matrix**: 
  ```text
  True Negatives (TN): 31414 | False Positives (FP): 12253
  False Negatives (FN): 1587 | True Positives (TP): 5482
  ```

### Stroke (stroke)
- **Selected Classifier**: `Random Forest`
- **Features Evaluated**: 10 parameters
- **Accuracy**: `0.8728`
- **Precision**: `0.1774`
- **Recall (Sensitivity)**: `0.4400`
- **Specificity**: `0.8951`
- **F1 Score**: `0.2529`
- **ROC-AUC**: `0.8004`
- **Confusion Matrix**: 
  ```text
  True Negatives (TN): 870 | False Positives (FP): 102
  False Negatives (FN): 28 | True Positives (TP): 22
  ```

### Chronic Kidney Disease (chronic_kidney_disease)
- **Selected Classifier**: `Random Forest`
- **Features Evaluated**: 24 parameters
- **Accuracy**: `1.0000`
- **Precision**: `1.0000`
- **Recall (Sensitivity)**: `1.0000`
- **Specificity**: `1.0000`
- **F1 Score**: `1.0000`
- **ROC-AUC**: `1.0000`
- **Confusion Matrix**: 
  ```text
  True Negatives (TN): 30 | False Positives (FP): 0
  False Negatives (FN): 0 | True Positives (TP): 50
  ```
