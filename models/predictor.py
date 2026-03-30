"""
ML Model Predictor
Loads pre-trained .pkl models and provides a unified predict() interface.
"""

import os
import numpy as np

# Try to import joblib/sklearn; graceful fallback for environments without it.
try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False

# Resolve models directory relative to this file
MODELS_DIR = os.path.join(os.path.dirname(__file__))


class Predictor:
    """Unified prediction interface for all disease models."""

    _loaded_models = {}   # cache

    @classmethod
    def _load(cls, model_name: str):
        if model_name in cls._loaded_models:
            return cls._loaded_models[model_name]

        path = os.path.join(MODELS_DIR, f"{model_name}_model.pkl")
        if not JOBLIB_AVAILABLE:
            return None
        if not os.path.exists(path):
            return None

        try:
            model = joblib.load(path)
            cls._loaded_models[model_name] = model
            return model
        except Exception:
            return None

    @classmethod
    def predict_diabetes(cls, inputs: dict) -> dict:
        """
        Expected keys: pregnancies, glucose, blood_pressure, skin_thickness,
                       insulin, bmi, dpf, age
        Returns: {risk_label, confidence, recommendation}
        """
        model = cls._load("diabetes")
        if model is None:
            return cls._rule_based_diabetes(inputs)

        features = np.array([[
            float(inputs.get("pregnancies", 0)),
            float(inputs.get("glucose", 0)),
            float(inputs.get("blood_pressure", 0)),
            float(inputs.get("skin_thickness", 0)),
            float(inputs.get("insulin", 0)),
            float(inputs.get("bmi", 0)),
            float(inputs.get("dpf", 0)),
            float(inputs.get("age", 0)),
        ]])

        try:
            pred = model.predict(features)[0]
            proba = model.predict_proba(features)[0]
            confidence = float(max(proba))
            risk = "High" if pred == 1 else "Low"
        except Exception:
            return cls._rule_based_diabetes(inputs)

        return cls._format_result(risk, confidence, "diabetes")

    @classmethod
    def predict_heart(cls, inputs: dict) -> dict:
        """
        Expected keys: age, sex, cp, trestbps, chol, fbs, restecg,
                       thalach, exang, oldpeak, slope, ca, thal
        """
        model = cls._load("heart")
        if model is None:
            return cls._rule_based_heart(inputs)

        sex_map   = {"Male": 1, "Female": 0}
        cp_map    = {"Typical Angina": 0, "Atypical Angina": 1,
                     "Non-anginal Pain": 2, "Asymptomatic": 3}
        ecg_map   = {"Normal": 0, "ST-T Wave Abnormality": 1,
                     "Left Ventricular Hypertrophy": 2}
        slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}
        thal_map  = {"Normal": 1, "Fixed Defect": 2, "Reversible Defect": 3}

        features = np.array([[
            float(inputs.get("age", 50)),
            sex_map.get(inputs.get("sex", "Male"), 1),
            cp_map.get(inputs.get("cp", "Asymptomatic"), 3),
            float(inputs.get("trestbps", 120)),
            float(inputs.get("chol", 240)),
            1 if inputs.get("fbs", False) else 0,
            ecg_map.get(inputs.get("restecg", "Normal"), 0),
            float(inputs.get("thalach", 150)),
            1 if inputs.get("exang", False) else 0,
            float(inputs.get("oldpeak", 1.0)),
            slope_map.get(inputs.get("slope", "Flat"), 1),
            int(inputs.get("ca", 0)),
            thal_map.get(inputs.get("thal", "Normal"), 1),
        ]])

        try:
            pred = model.predict(features)[0]
            proba = model.predict_proba(features)[0]
            confidence = float(max(proba))
            risk = "High" if pred == 1 else "Low"
        except Exception:
            return cls._rule_based_heart(inputs)

        return cls._format_result(risk, confidence, "heart")

    @classmethod
    def predict_rule_based(cls, disease: str, inputs: dict) -> dict:
        """Simple rule-based predictions for diseases without ML models."""
        positive_count = sum(
            1 for v in inputs.values()
            if v is True or v in ["Severe", "Daily", "Constant", "Poor", "Very Poor"]
        )
        total = max(len(inputs), 1)
        ratio = positive_count / total

        if ratio >= 0.6:
            risk, confidence = "High", 0.80
        elif ratio >= 0.3:
            risk, confidence = "Medium", 0.65
        else:
            risk, confidence = "Low", 0.85

        return cls._format_result(risk, confidence, "general")

    # -----------------------------------------------------------------------
    # Fallback rule-based
    # -----------------------------------------------------------------------
    @classmethod
    def _rule_based_diabetes(cls, inputs: dict) -> dict:
        glucose = float(inputs.get("glucose", 0))
        bmi     = float(inputs.get("bmi", 0))
        age     = float(inputs.get("age", 0))

        score = 0
        if glucose >= 140:  score += 3
        elif glucose >= 100: score += 1
        if bmi >= 30:        score += 2
        elif bmi >= 25:      score += 1
        if age >= 45:        score += 1

        if score >= 4:   risk, conf = "High",   0.82
        elif score >= 2: risk, conf = "Medium",  0.68
        else:            risk, conf = "Low",     0.88

        return cls._format_result(risk, conf, "diabetes")

    @classmethod
    def _rule_based_heart(cls, inputs: dict) -> dict:
        age    = float(inputs.get("age", 50))
        chol   = float(inputs.get("chol", 200))
        thal   = inputs.get("thalach", 150)
        exang  = inputs.get("exang", False)
        oldpk  = float(inputs.get("oldpeak", 0))

        score = 0
        if age >= 55:     score += 2
        if chol >= 240:   score += 2
        if exang:         score += 2
        if oldpk >= 2.0:  score += 2
        if float(thal) < 120: score += 1

        if score >= 5:   risk, conf = "High",   0.80
        elif score >= 3: risk, conf = "Medium",  0.65
        else:            risk, conf = "Low",     0.88

        return cls._format_result(risk, conf, "heart")

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------
    @staticmethod
    def _format_result(risk: str, confidence: float, disease_type: str) -> dict:
        recommendations = {
            "High": {
                "diabetes": "Your results indicate a high risk of diabetes. Please consult an endocrinologist immediately for proper testing and treatment.",
                "heart":    "Your results indicate a significant cardiovascular risk. Seek cardiology consultation as soon as possible.",
                "general":  "Your symptom profile suggests significant concern. Please see a healthcare professional promptly.",
            },
            "Medium": {
                "diabetes": "Moderate diabetes risk detected. Monitor your blood sugar regularly and consider lifestyle changes. Consult your doctor.",
                "heart":    "Moderate cardiovascular risk. Lifestyle modification and medical evaluation are recommended.",
                "general":  "Symptoms suggest moderate concern. Monitor closely and consult a doctor if symptoms worsen.",
            },
            "Low": {
                "diabetes": "Low diabetes risk based on your input. Maintain a healthy lifestyle with regular check-ups.",
                "heart":    "Low cardiovascular risk. Keep up your healthy habits and get periodic check-ups.",
                "general":  "Your symptoms appear mild. Rest, hydrate, and monitor. See a doctor if condition worsens.",
            },
        }

        rec = recommendations.get(risk, {}).get(disease_type,
              recommendations.get(risk, {}).get("general", "Consult a healthcare professional."))

        return {
            "risk_label":     risk,
            "confidence":     confidence,
            "recommendation": rec,
        }
