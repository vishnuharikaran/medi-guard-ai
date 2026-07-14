import os
import numpy as np
import pandas as pd
from models.config import RAW_DATA_PATH, RANDOM_STATE

def generate_medical_data(num_samples=10000):
    """
    Generates a high-fidelity synthetic clinical dataset with realistic correlations
    between physiological parameters, lifestyle choices, and chronic diseases.
    """
    np.random.seed(RANDOM_STATE)
    
    # 1. Demographic & Basic Physical Metrics
    age = np.random.randint(18, 85, size=num_samples)
    gender = np.random.binomial(1, 0.5, size=num_samples)  # 0: Female, 1: Male
    
    # BMI: Normal distribution with mean centered at overweight (realistic for general population)
    bmi = np.random.normal(loc=26.8, scale=5.8, size=num_samples)
    bmi = np.clip(bmi, 15.0, 52.0)
    
    # 2. Lifestyle Parameters
    family_history = np.random.binomial(1, 0.35, size=num_samples)  # 35% have family history of chronic diseases
    exercise_hours = np.random.gamma(shape=3.0, scale=1.5, size=num_samples)  # Peak around 4.5 hours
    exercise_hours = np.clip(exercise_hours, 0.0, 20.0)
    
    smoking = np.zeros(num_samples, dtype=int)
    # Higher rate of smoking in males and middle-aged adults
    for i in range(num_samples):
        prob_smoke = 0.12 + (0.05 if gender[i] == 1 else 0) + (0.05 if 30 <= age[i] <= 60 else 0)
        smoking[i] = np.random.binomial(1, prob_smoke)
        
    alcohol = np.random.binomial(1, 0.28, size=num_samples)  # 28% regular drinkers
    sleep_hours = np.random.normal(loc=7.1, scale=1.1, size=num_samples)
    sleep_hours = np.clip(sleep_hours, 4.0, 10.0)
    
    # 3. Vitals & Blood Chemistry (correlated with age, bmi, and lifestyle)
    systolic_bp = np.zeros(num_samples)
    diastolic_bp = np.zeros(num_samples)
    blood_sugar = np.zeros(num_samples)
    
    for i in range(num_samples):
        # Blood Pressure base levels that increase with age and BMI
        bp_age_factor = (age[i] - 18) * 0.45
        bp_bmi_factor = max(0, bmi[i] - 22.0) * 1.1
        bp_lifestyle_factor = (8.0 if smoking[i] == 1 else 0) + (4.0 if alcohol[i] == 1 else 0) - (exercise_hours[i] * 0.5)
        
        sys_mean = 110.0 + bp_age_factor + bp_bmi_factor + bp_lifestyle_factor
        sys_val = np.random.normal(loc=sys_mean, scale=8.0)
        systolic_bp[i] = np.clip(sys_val, 90.0, 195.0)
        
        dia_mean = 70.0 + (bp_age_factor * 0.25) + (bp_bmi_factor * 0.7) + (bp_lifestyle_factor * 0.5)
        dia_val = np.random.normal(loc=dia_mean, scale=6.0)
        diastolic_bp[i] = np.clip(dia_val, 55.0, 115.0)
        
        # Blood Sugar base (Fasting Blood Glucose)
        sugar_age_factor = (age[i] - 18) * 0.35
        sugar_bmi_factor = max(0, bmi[i] - 22.0) * 1.2
        sugar_lifestyle_factor = (10.0 if family_history[i] == 1 else 0) - (exercise_hours[i] * 0.8) + ((8.0 - sleep_hours[i]) * 2.0)
        
        sugar_mean = 85.0 + sugar_age_factor + sugar_bmi_factor + sugar_lifestyle_factor
        sugar_val = np.random.normal(loc=sugar_mean, scale=12.0)
        blood_sugar[i] = np.clip(sugar_val, 60.0, 260.0)
        
    # 4. Generate Target Risk Variables using Logit Models to ensure clinical validity
    
    # A. Diabetes Risk Target
    # Driven primarily by BloodSugar, BMI, Family History, and Age
    log_odds_diabetes = (
        -3.8
        + 0.055 * (blood_sugar - 95.0) * (blood_sugar > 95.0)
        + 0.12 * (blood_sugar - 125.0) * (blood_sugar > 125.0)
        + 0.08 * (bmi - 25.0)
        + 0.015 * age
        + 0.85 * family_history
        - 0.08 * exercise_hours
    )
    prob_diabetes = 1 / (1 + np.exp(-log_odds_diabetes))
    diabetes_risk = np.random.binomial(1, prob_diabetes)
    
    # B. Heart Disease Risk Target
    # Driven by Age, BP, BMI, Smoking, Alcohol, Family History, and low Sleep
    log_odds_heart = (
        -4.2
        + 0.045 * age
        + 0.04 * (systolic_bp - 120.0)
        + 0.03 * (diastolic_bp - 80.0)
        + 0.06 * (bmi - 25.0)
        + 0.95 * smoking
        + 0.45 * alcohol
        + 0.65 * family_history
        - 0.12 * exercise_hours
        + 0.20 * (7.0 - sleep_hours)
    )
    prob_heart = 1 / (1 + np.exp(-log_odds_heart))
    heart_disease_risk = np.random.binomial(1, prob_heart)
    
    # C. Hypertension Risk Target
    # Driven heavily by BP itself, Age, BMI, Smoking, and Alcohol
    log_odds_hyper = (
        -4.0
        + 0.08 * (systolic_bp - 110.0)
        + 0.06 * (diastolic_bp - 70.0)
        + 0.02 * age
        + 0.07 * (bmi - 25.0)
        + 0.55 * smoking
        + 0.35 * alcohol
        - 0.08 * exercise_hours
    )
    prob_hyper = 1 / (1 + np.exp(-log_odds_hyper))
    hypertension_risk = np.random.binomial(1, prob_hyper)
    
    # Assemble DataFrame
    df = pd.DataFrame({
        "Age": age,
        "Gender": gender,
        "BMI": np.round(bmi, 2),
        "SystolicBP": np.round(systolic_bp).astype(int),
        "DiastolicBP": np.round(diastolic_bp).astype(int),
        "BloodSugar": np.round(blood_sugar, 1),
        "ExerciseHoursPerWeek": np.round(exercise_hours, 1),
        "Smoking": smoking,
        "AlcoholConsumption": alcohol,
        "SleepHoursPerNight": np.round(sleep_hours, 1),
        "FamilyHistory": family_history,
        "DiabetesRisk": diabetes_risk,
        "HeartDiseaseRisk": heart_disease_risk,
        "HypertensionRisk": hypertension_risk
    })
    
    return df

if __name__ == "__main__":
    print("Generating simulated medical dataset...")
    df = generate_medical_data()
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Dataset generated successfully and saved to {RAW_DATA_PATH}.")
    print(f"Shape: {df.shape}")
    print("\nTarget Prevalence Rates:")
    print(f"Diabetes Risk: {df['DiabetesRisk'].mean()*100:.2f}%")
    print(f"Heart Disease Risk: {df['HeartDiseaseRisk'].mean()*100:.2f}%")
    print(f"Hypertension Risk: {df['HypertensionRisk'].mean()*100:.2f}%")
