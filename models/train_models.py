"""
Train and save ML models for the HealthAI app.

Run this script once (on desktop) to generate:
  - models/diabetes_model.pkl
  - models/heart_model.pkl

Usage:
  python models/train_models.py
"""

import os
import sys

try:
    import numpy as np
    import joblib
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.datasets import make_classification
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install scikit-learn numpy joblib")
    import numpy as np
    import joblib
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.datasets import make_classification

MODELS_DIR = os.path.dirname(os.path.abspath(__file__))


def train_diabetes_model():
    """
    Train on synthetic data mirroring Pima Indians Diabetes dataset structure.
    In production, replace with real dataset loading.
    """
    print("Training diabetes model...")

    np.random.seed(42)
    n = 768

    # Feature distributions mimicking real dataset
    pregnancies     = np.random.randint(0, 17, n)
    glucose         = np.random.normal(121, 32, n).clip(0, 200)
    blood_pressure  = np.random.normal(72, 12, n).clip(0, 130)
    skin_thickness  = np.random.normal(29, 15, n).clip(0, 100)
    insulin         = np.random.exponential(80, n).clip(0, 900)
    bmi             = np.random.normal(32, 7, n).clip(10, 70)
    dpf             = np.random.exponential(0.47, n).clip(0, 2.5)
    age             = np.random.normal(33, 12, n).clip(18, 80)

    X = np.column_stack([pregnancies, glucose, blood_pressure, skin_thickness,
                         insulin, bmi, dpf, age])

    # Synthetic labels (higher glucose/BMI → more likely positive)
    risk = (glucose / 200 * 0.4 + bmi / 70 * 0.3 + age / 80 * 0.2
            + dpf / 2.5 * 0.1)
    y = (risk > 0.35).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                         random_state=42)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42,
                                       max_depth=6)),
    ])
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)
    print(f"  Diabetes model accuracy: {score:.3f}")

    out_path = os.path.join(MODELS_DIR, "diabetes_model.pkl")
    joblib.dump(pipeline, out_path)
    print(f"  Saved: {out_path}")


def train_heart_model():
    """
    Train on synthetic data mirroring Cleveland Heart Disease dataset structure.
    """
    print("Training heart disease model...")

    np.random.seed(0)
    n = 303

    age        = np.random.normal(54, 9, n).clip(29, 77)
    sex        = np.random.randint(0, 2, n)
    cp         = np.random.randint(0, 4, n)
    trestbps   = np.random.normal(131, 18, n).clip(94, 200)
    chol       = np.random.normal(247, 52, n).clip(126, 564)
    fbs        = (np.random.rand(n) > 0.85).astype(int)
    restecg    = np.random.randint(0, 3, n)
    thalach    = np.random.normal(149, 23, n).clip(71, 202)
    exang      = np.random.randint(0, 2, n)
    oldpeak    = np.random.exponential(1.1, n).clip(0, 6.2)
    slope      = np.random.randint(0, 3, n)
    ca         = np.random.randint(0, 4, n)
    thal       = np.random.choice([1, 2, 3], n)

    X = np.column_stack([age, sex, cp, trestbps, chol, fbs, restecg,
                         thalach, exang, oldpeak, slope, ca, thal])

    # Synthetic labels
    risk = (age / 77 * 0.2 + chol / 564 * 0.2 + exang * 0.2
            + oldpeak / 6.2 * 0.2 + ca / 3 * 0.2)
    y = (risk > 0.3).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                         random_state=0)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=0,
                                       max_depth=6)),
    ])
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)
    print(f"  Heart model accuracy: {score:.3f}")

    out_path = os.path.join(MODELS_DIR, "heart_model.pkl")
    joblib.dump(pipeline, out_path)
    print(f"  Saved: {out_path}")


if __name__ == "__main__":
    train_diabetes_model()
    train_heart_model()
    print("\nAll models trained and saved successfully!")
