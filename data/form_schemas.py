"""
Form Schemas
Defines the input fields for each disease's symptom form.

Field types:
  - text       : TextInput (free text)
  - number     : TextInput (numeric keyboard)
  - spinner    : Dropdown selection
  - slider     : Numeric range slider
  - toggle     : Yes/No toggle
  - checkbox   : Multi-select checkboxes
"""

DISEASE_FORMS = {

    # -----------------------------------------------------------------------
    # DIABETES
    # -----------------------------------------------------------------------
    "Diabetes": {
        "category": "diabetes",
        "description": "AI-powered diabetes risk assessment",
        "model": "diabetes",
        "fields": [
            {
                "name": "pregnancies",
                "label": "Number of Pregnancies",
                "type": "number",
                "hint": "0",
                "required": True,
            },
            {
                "name": "glucose",
                "label": "Plasma Glucose Level (mg/dL)",
                "type": "slider",
                "min": 0, "max": 200, "step": 1, "default": 120,
                "required": True,
            },
            {
                "name": "blood_pressure",
                "label": "Diastolic Blood Pressure (mmHg)",
                "type": "slider",
                "min": 0, "max": 130, "step": 1, "default": 72,
                "required": True,
            },
            {
                "name": "skin_thickness",
                "label": "Skin Fold Thickness (mm)",
                "type": "slider",
                "min": 0, "max": 100, "step": 1, "default": 20,
                "required": True,
            },
            {
                "name": "insulin",
                "label": "2-Hour Serum Insulin (μU/ml)",
                "type": "slider",
                "min": 0, "max": 900, "step": 1, "default": 80,
                "required": True,
            },
            {
                "name": "bmi",
                "label": "Body Mass Index (BMI)",
                "type": "slider",
                "min": 0, "max": 70, "step": 0.1, "default": 25.0,
                "required": True,
            },
            {
                "name": "dpf",
                "label": "Diabetes Pedigree Function",
                "type": "slider",
                "min": 0.0, "max": 2.5, "step": 0.01, "default": 0.47,
                "required": True,
            },
            {
                "name": "age",
                "label": "Age (years)",
                "type": "slider",
                "min": 1, "max": 100, "step": 1, "default": 30,
                "required": True,
            },
        ]
    },

    # -----------------------------------------------------------------------
    # HEART DISEASE
    # -----------------------------------------------------------------------
    "Heart Disease": {
        "category": "heart",
        "description": "AI-powered cardiovascular risk assessment",
        "model": "heart",
        "fields": [
            {
                "name": "age",
                "label": "Age (years)",
                "type": "slider",
                "min": 1, "max": 100, "step": 1, "default": 50,
                "required": True,
            },
            {
                "name": "sex",
                "label": "Biological Sex",
                "type": "spinner",
                "options": ["Male", "Female"],
                "required": True,
            },
            {
                "name": "cp",
                "label": "Chest Pain Type",
                "type": "spinner",
                "options": [
                    "Typical Angina",
                    "Atypical Angina",
                    "Non-anginal Pain",
                    "Asymptomatic",
                ],
                "required": True,
            },
            {
                "name": "trestbps",
                "label": "Resting Blood Pressure (mmHg)",
                "type": "slider",
                "min": 80, "max": 200, "step": 1, "default": 120,
                "required": True,
            },
            {
                "name": "chol",
                "label": "Serum Cholesterol (mg/dL)",
                "type": "slider",
                "min": 100, "max": 600, "step": 1, "default": 240,
                "required": True,
            },
            {
                "name": "fbs",
                "label": "Fasting Blood Sugar > 120 mg/dL?",
                "type": "toggle",
                "required": True,
            },
            {
                "name": "restecg",
                "label": "Resting ECG Results",
                "type": "spinner",
                "options": ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"],
                "required": True,
            },
            {
                "name": "thalach",
                "label": "Maximum Heart Rate Achieved",
                "type": "slider",
                "min": 60, "max": 220, "step": 1, "default": 150,
                "required": True,
            },
            {
                "name": "exang",
                "label": "Exercise Induced Angina?",
                "type": "toggle",
                "required": True,
            },
            {
                "name": "oldpeak",
                "label": "ST Depression (Oldpeak)",
                "type": "slider",
                "min": 0.0, "max": 6.0, "step": 0.1, "default": 1.0,
                "required": True,
            },
            {
                "name": "slope",
                "label": "Slope of Peak Exercise ST Segment",
                "type": "spinner",
                "options": ["Upsloping", "Flat", "Downsloping"],
                "required": True,
            },
            {
                "name": "ca",
                "label": "Major Vessels Colored by Fluoroscopy",
                "type": "spinner",
                "options": ["0", "1", "2", "3"],
                "required": True,
            },
            {
                "name": "thal",
                "label": "Thalassemia",
                "type": "spinner",
                "options": ["Normal", "Fixed Defect", "Reversible Defect"],
                "required": True,
            },
        ]
    },

    # -----------------------------------------------------------------------
    # COMMON DISEASES
    # -----------------------------------------------------------------------
    "Influenza (Flu)": {
        "category": "common",
        "description": "Assess flu severity and symptoms",
        "model": "rule_based",
        "fields": [
            {"name": "fever", "label": "Do you have a fever?", "type": "toggle"},
            {"name": "temp", "label": "Body Temperature (°C)", "type": "slider",
             "min": 35, "max": 42, "step": 0.1, "default": 37.0},
            {"name": "cough", "label": "Do you have a cough?", "type": "toggle"},
            {"name": "sore_throat", "label": "Sore throat?", "type": "toggle"},
            {"name": "body_ache", "label": "Body aches?", "type": "toggle"},
            {"name": "fatigue", "label": "Fatigue level", "type": "spinner",
             "options": ["None", "Mild", "Moderate", "Severe"]},
            {"name": "duration", "label": "How long have you had symptoms? (days)",
             "type": "slider", "min": 1, "max": 30, "step": 1, "default": 3},
        ]
    },

    "Common Cold": {
        "category": "common",
        "description": "Assess cold symptoms",
        "model": "rule_based",
        "fields": [
            {"name": "runny_nose", "label": "Runny nose?", "type": "toggle"},
            {"name": "sneezing", "label": "Sneezing?", "type": "toggle"},
            {"name": "congestion", "label": "Nasal congestion?", "type": "toggle"},
            {"name": "mild_cough", "label": "Mild cough?", "type": "toggle"},
            {"name": "duration", "label": "Duration (days)",
             "type": "slider", "min": 1, "max": 14, "step": 1, "default": 2},
            {"name": "severity", "label": "Severity",
             "type": "spinner", "options": ["Mild", "Moderate", "Severe"]},
        ]
    },

    "Hypertension": {
        "category": "chronic",
        "description": "High blood pressure assessment",
        "model": "rule_based",
        "fields": [
            {"name": "systolic", "label": "Systolic Blood Pressure (mmHg)",
             "type": "slider", "min": 80, "max": 220, "step": 1, "default": 130},
            {"name": "diastolic", "label": "Diastolic Blood Pressure (mmHg)",
             "type": "slider", "min": 40, "max": 140, "step": 1, "default": 85},
            {"name": "headache", "label": "Frequent headaches?", "type": "toggle"},
            {"name": "dizziness", "label": "Dizziness?", "type": "toggle"},
            {"name": "history", "label": "Family history of hypertension?", "type": "toggle"},
            {"name": "smoker", "label": "Smoking status",
             "type": "spinner", "options": ["Non-smoker", "Former smoker", "Current smoker"]},
            {"name": "exercise", "label": "Exercise frequency",
             "type": "spinner",
             "options": ["Never", "1-2x/week", "3-4x/week", "Daily"]},
        ]
    },

    "Asthma": {
        "category": "respiratory",
        "description": "Assess asthma symptoms",
        "model": "rule_based",
        "fields": [
            {"name": "wheezing", "label": "Wheezing?", "type": "toggle"},
            {"name": "shortness", "label": "Shortness of breath?", "type": "toggle"},
            {"name": "night_cough", "label": "Night-time cough?", "type": "toggle"},
            {"name": "triggers", "label": "Common trigger",
             "type": "spinner",
             "options": ["Exercise", "Allergens", "Cold air", "Smoke", "Unknown"]},
            {"name": "frequency", "label": "Symptom frequency",
             "type": "spinner",
             "options": ["Rarely", "Weekly", "Daily", "Constant"]},
            {"name": "inhaler", "label": "Using an inhaler?", "type": "toggle"},
        ]
    },

    "Anxiety": {
        "category": "mental",
        "description": "Mental health anxiety screening",
        "model": "rule_based",
        "fields": [
            {"name": "nervousness", "label": "Feeling nervous or anxious?", "type": "toggle"},
            {"name": "worry", "label": "Unable to control worrying?", "type": "toggle"},
            {"name": "irritable", "label": "Easily irritable?", "type": "toggle"},
            {"name": "sleep", "label": "Sleep quality",
             "type": "spinner",
             "options": ["Good", "Fair", "Poor", "Very Poor"]},
            {"name": "duration_weeks", "label": "Duration (weeks)",
             "type": "slider", "min": 1, "max": 52, "step": 1, "default": 2},
            {"name": "severity", "label": "Symptom severity",
             "type": "spinner", "options": ["Mild", "Moderate", "Severe"]},
        ]
    },
}


# -----------------------------------------------------------------------
# Diseases listed per category (for disease list screen)
# -----------------------------------------------------------------------
CATEGORY_DISEASES = {
    "common":      ["Influenza (Flu)", "Common Cold"],
    "children":    ["Influenza (Flu)", "Common Cold"],
    "chronic":     ["Hypertension", "Diabetes"],
    "women":       ["Anxiety", "Hypertension"],
    "mental":      ["Anxiety"],
    "respiratory": ["Asthma", "Influenza (Flu)"],
    "heart":       ["Heart Disease"],
    "diabetes":    ["Diabetes"],
}
