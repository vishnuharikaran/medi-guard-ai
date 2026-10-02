"""Model Evaluation & Summary Report Generator for Medi-Guard AI."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"


def generate_evaluation_report() -> str:
    """Reads metadata from models/ and generates a comprehensive Markdown report."""
    datasets = ["heart_disease", "diabetes", "stroke", "chronic_kidney_disease"]
    summary_data = {}
    
    report_lines = [
        "# Medi-Guard AI — Multi-Model Evaluation Report",
        "",
        "This report details the quantitative test-set evaluation results for the 4 independent experimental disease-risk models trained in Medi-Guard AI.",
        "",
        "---",
        "",
        "## Summary Performance Table",
        "",
        "| Dataset / Disease Model | Selected Model | Accuracy | Precision | Recall | Specificity | F1 Score | ROC-AUC | Test Split Size |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for ds in datasets:
        meta_file = MODELS_DIR / ds / "metadata.json"
        if meta_file.exists():
            with open(meta_file, "r") as f:
                data = json.load(f)
            summary_data[ds] = data
            m = data["metrics"]
            model_name = data["best_model"]
            test_sz = data.get("test_split_size", "N/A")

            report_lines.append(
                f"| **{ds.replace('_', ' ').title()}** | {model_name} | {m['accuracy']:.4f} | {m['precision']:.4f} | {m['recall']:.4f} | {m['specificity']:.4f} | {m['f1']:.4f} | {m['roc_auc']:.4f} | {test_sz} |"
            )

    report_lines.extend([
        "",
        "---",
        "",
        "## Detailed Classification Metrics & Confusion Matrices",
        ""
    ])

    for ds, data in summary_data.items():
        m = data["metrics"]
        cm = m.get("confusion_matrix", [[0, 0], [0, 0]])
        report_lines.extend([
            f"### {ds.replace('_', ' ').title()} ({data.get('dataset_name', ds)})",
            f"- **Selected Classifier**: `{data['best_model']}`",
            f"- **Features Evaluated**: {len(data.get('features', []))} parameters",
            f"- **Accuracy**: `{m['accuracy']:.4f}`",
            f"- **Precision**: `{m['precision']:.4f}`",
            f"- **Recall (Sensitivity)**: `{m['recall']:.4f}`",
            f"- **Specificity**: `{m['specificity']:.4f}`",
            f"- **F1 Score**: `{m['f1']:.4f}`",
            f"- **ROC-AUC**: `{m['roc_auc']:.4f}`",
            "- **Confusion Matrix**: ",
            "  ```text",
            f"  True Negatives (TN): {m.get('tn', cm[0][0])} | False Positives (FP): {m.get('fp', cm[0][1])}",
            f"  False Negatives (FN): {m.get('fn', cm[1][0])} | True Positives (TP): {m.get('tp', cm[1][1])}",
            "  ```",
            ""
        ])

    report_content = "\n".join(report_lines)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(REPORTS_DIR / "model_evaluation_report.md", "w") as f:
        f.write(report_content)

    with open(REPORTS_DIR / "model_evaluation_summary.json", "w") as f:
        json.dump(summary_data, f, indent=2)

    print(f"[OK] Evaluation report generated successfully at: {REPORTS_DIR / 'model_evaluation_report.md'}")
    return report_content


if __name__ == "__main__":
    generate_evaluation_report()
