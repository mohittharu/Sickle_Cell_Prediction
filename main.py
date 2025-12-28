import joblib
import numpy as np

# Load model & scaler
MODEL_PATH = "Classifier/Random_forest1.joblib"
SCALER_PATH = "Classifier/Scaler1.joblib"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def encode_gender(value):
    """Encode gender as numeric (Male=0, Female=1)."""
    if isinstance(value, str):
        value = value.strip().lower()
        if value == "male":
            return 0
        elif value == "female":
            return 1
    return value

def predict_sickle_cell(gender, hemoglobin, mch, mchc, mcv):
    # Encode gender
    gender_encoded = encode_gender(gender)

    # Convert to numpy array
    features = np.array([[gender_encoded, hemoglobin, mch, mchc, mcv]])

    # Scale data
    features_scaled = scaler.transform(features)

    # Predict
    prediction = model.predict(features_scaled)[0]

    return "Positive" if prediction == 1 else "Negative"
