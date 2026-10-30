import numpy as np
from sklearn.ensemble import RandomForestClassifier

FEATURE_NAMES = ["pH", "assay percentage", "dissolution percentage", "moisture percentage"]

def train_model():
    """
    Creates a demonstration classifier from synthetic values.
    This is NOT a validated pharmaceutical model and must not be used
    to decide whether a real medicine is genuine, safe, or fit to use.
    """
    rng = np.random.default_rng(42)
    rows, labels = [], []

    for _ in range(2500):
        ph = rng.uniform(2.0, 9.0)
        assay = rng.uniform(60, 120)
        dissolution = rng.uniform(40, 100)
        moisture = rng.uniform(0, 12)

        # Illustrative teaching rule only; not a real pharmacopoeial standard.
        in_demo_range = (
            4.5 <= ph <= 7.5 and
            90 <= assay <= 110 and
            dissolution >= 75 and
            moisture <= 5
        )
        rows.append([ph, assay, dissolution, moisture])
        labels.append(0 if in_demo_range else 1)

    model = RandomForestClassifier(n_estimators=120, random_state=42)
    model.fit(np.array(rows), np.array(labels))
    return model

def screen_sample(model, values):
    prediction = int(model.predict([values])[0])
    return "Within illustrative screening range" if prediction == 0 else "Flag for laboratory review"
