import joblib

def save_model(model, path="models/fraud_model.pkl"):
    joblib.dump(model, path)
    print("Model saved at", path)