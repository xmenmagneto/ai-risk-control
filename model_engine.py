import joblib

model = joblib.load("model.pkl")

def model_decision(features):
    ua = features.user_agent or ""
    prediction = model.predict([ua])[0]
    return "BLOCK" if prediction == 1 else "ALLOW"