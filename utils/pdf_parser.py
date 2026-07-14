"""Clinical PDF Report Parser for extracting patient vitals and health profile."""

from __future__ import annotations

import re
import pypdf
from typing import Dict, Any, Optional

def extract_text_from_pdf(pdf_file) -> str:
    """Extracts all text content from an uploaded PDF file stream."""
    try:
        reader = pypdf.PdfReader(pdf_file)
        text_list = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_list.append(page_text)
        return "\n".join(text_list)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def parse_patient_details(text: str) -> Dict[str, Any]:
    """
    Parses clinical text and extracts patient metrics using regular expressions.
    Returns a dictionary of matched fields.
    """
    results = {}
    
    # Pre-clean text (lower case and normalize whitespace for numeric/vitals matching)
    clean_text = re.sub(r'\s+', ' ', text).lower()
    
    # 1. Patient Name (Scan raw text to preserve double-space boundary and avoid matching "Report ID")
    name_match = re.search(
        r'\b(?:patient name|patient|name)\b\s*[:\-\s]*\s*([a-zA-Z\s]{2,30}?)(?:\s{2,}|\n|\t|report|date|age|$)',
        text,
        re.IGNORECASE
    )
    if name_match:
        results["name"] = name_match.group(1).strip()
        
    # 2. Age
    # Handle composite Age / Gender layout first (e.g., age / gender : 28 / male)
    age_match = re.search(r'\bage\b\s*(?:\/\s*gender)?\s*[:\-\s]*\s*(\d{1,3})', clean_text)
    if not age_match:
        age_match = re.search(r'(\d{1,3})\s*(?:years old|years|yrs)', clean_text)
    if age_match:
        results["age"] = int(age_match.group(1))
        
    # 3. Gender
    # Handle composite Age / Gender layout first (e.g., age / gender : 28 / male)
    gender_match = re.search(r'\bgender\b\s*[:\-\s\d\/]*\s*(male|female|other)', clean_text)
    if not gender_match:
        gender_match = re.search(r'\b(?:sex|biological sex)\b\s*[:\-\s]*\s*(male|female|other)', clean_text)
    if gender_match:
        gender_str = gender_match.group(1).strip()
        results["gender"] = gender_str.title()
        
    # 4. Height (cm or m)
    # Heuristics: Skip non-digits to find the first decimal/integer number
    height_match = re.search(r'\b(?:height|ht)\b[^0-9]*?(\d{2,3}(?:\.\d+)?)', clean_text)
    if height_match:
        val = float(height_match.group(1))
        # If height is parsed in meters (e.g., 1.70), convert to cm
        if val < 2.5:
            val = val * 100.0
        results["height"] = round(val, 2)
            
    # 5. Weight (kg)
    weight_match = re.search(r'\b(?:weight|wt)\b[^0-9]*?(\d{2,3}(?:\.\d+)?)', clean_text)
    if weight_match:
        results["weight"] = float(weight_match.group(1))
        
    # 6. Heart Rate (bpm)
    hr_match = re.search(r'\b(?:heart rate|pulse|hr|pulse rate)\b[^0-9]*?(\d{2,3})', clean_text)
    if hr_match:
        results["heart_rate"] = int(hr_match.group(1))
        
    # 7. Blood Pressure (systolic/diastolic)
    # Check for separate lines first (e.g. systolic bp 120 and diastolic bp 80)
    sys_match = re.search(r'\b(?:systolic bp|systolic|sys bp)\b[^0-9]*?(\d{2,3})', clean_text)
    dia_match = re.search(r'\b(?:diastolic bp|diastolic|dia bp)\b[^0-9]*?(\d{2,3})', clean_text)
    
    if sys_match and dia_match:
        results["systolic_bp"] = int(sys_match.group(1))
        results["diastolic_bp"] = int(dia_match.group(1))
    else:
        # Fallback to combined BP formats (e.g., bp: 120/80)
        bp_match = re.search(r'\b(?:bp|blood pressure)\b\s*[:\-\s]*\s*(\d{2,3})\s*[\/\s-]\s*(\d{2,3})', clean_text)
        if bp_match:
            results["systolic_bp"] = int(bp_match.group(1))
            results["diastolic_bp"] = int(bp_match.group(2))
        
    # 8. Blood Sugar / Glucose
    sugar_match = re.search(r'\b(?:blood sugar|glucose|fbs|fasting glucose|sugar)\b[^0-9]*?(\d{2,3}(?:\.\d+)?)', clean_text)
    if sugar_match:
        results["blood_sugar"] = float(sugar_match.group(1))
        
    # 9. Sleep Hours
    sleep_match = re.search(r'\b(?:sleep hours|sleep duration|sleep)\b[^0-9]*?(\d{1,2}(?:\.\d+)?)', clean_text)
    if sleep_match:
        results["sleep_hours"] = float(sleep_match.group(1))
        
    # 10. Exercise Frequency
    exercise_match = re.search(r'\b(?:exercise frequency|exercise|activity)\b[^0-9]*?(\d)', clean_text)
    if exercise_match:
        results["exercise_frequency"] = int(exercise_match.group(1))
        
    # 11. Stress Level
    stress_match = re.search(r'\b(?:stress level|stress)\b(?:\s*\(\s*\d+\s*-\s*\d+\s*\))?[^0-9]*?(\d{1,2})', clean_text)
    if stress_match:
        results["stress_level"] = int(stress_match.group(1))
        
    # 12. Smoking
    smoking_match = re.search(r'\b(?:smoking habit|smoking|smoker)\b[a-z\s]*?\s*(yes|no|never|active)', clean_text)
    if smoking_match:
        smk = smoking_match.group(1).strip()
        results["smoking"] = "Yes" if smk in ["yes", "active"] else "No"
        
    # 13. Alcohol
    alcohol_match = re.search(r'\b(?:alcohol consumption|alcohol|drinking)\b[a-z\s]*?\s*(never|occasional|regular|heavy)', clean_text)
    if alcohol_match:
        results["alcohol"] = alcohol_match.group(1).title().strip()
        
    # 14. Water Intake
    water_match = re.search(r'\b(?:water intake|water)\b[^0-9]*?(\d{1,2}(?:\.\d+)?)', clean_text)
    if water_match:
        results["water_intake"] = float(water_match.group(1))
        
    return results
