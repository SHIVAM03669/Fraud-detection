from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List
import logging
from api.preprocessing import preprocess_transaction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fraud Detection API", version="1.0.0")

# Load model at startup
try:
    model = joblib.load("models/fraud_model.pkl")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

# Expected feature order (should match training data)
EXPECTED_FEATURES = [
    'Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
    'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
    'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount'
]

class TransactionData(BaseModel):
    """Pydantic model for transaction data validation"""
    # Support both direct format and wrapped format
    Time: float = None
    V1: float = None
    V2: float = None
    V3: float = None
    V4: float = None
    V5: float = None
    V6: float = None
    V7: float = None
    V8: float = None
    V9: float = None
    V10: float = None
    V11: float = None
    V12: float = None
    V13: float = None
    V14: float = None
    V15: float = None
    V16: float = None
    V17: float = None
    V18: float = None
    V19: float = None
    V20: float = None
    V21: float = None
    V22: float = None
    V23: float = None
    V24: float = None
    V25: float = None
    V26: float = None
    V27: float = None
    V28: float = None
    Amount: float = None
    
    # Alternative: wrapped format
    data: Dict[str, float] = None
    
    class Config:
        schema_extra = {
            "example": {
                "Time": 0.5,
                "V1": -1.359807,
                "V2": -0.072781,
                "Amount": 149.62
            }
        }

@app.get("/")
def root():
    return {"message": "Fraud Detection API", "status": "running"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None
    }

@app.post("/predict")
def predict_fraud(transaction: TransactionData):
    """
    Predict fraud probability for a transaction.
    Returns both binary prediction and calibrated probability.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Handle both direct format and wrapped format
        if transaction.data is not None:
            # Wrapped format: {"data": {"Time": 0.5, "V1": -1.0, ...}}
            input_data = transaction.data.copy()
        else:
            # Direct format: {"Time": 0.5, "V1": -1.0, ...}
            input_data = transaction.dict(exclude_none=True, exclude={'data'})
        
        # CRITICAL: Apply the same preprocessing as training
        processed_data = preprocess_transaction(input_data)
        
        # Ensure feature ordering consistency
        features_array = []
        missing_features = []
        
        for feature in EXPECTED_FEATURES:
            if feature in processed_data:
                features_array.append(processed_data[feature])
            else:
                missing_features.append(feature)
        
        if missing_features:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required features: {missing_features}"
            )
        
        # Convert to pandas DataFrame to match training format
        feature_df = pd.DataFrame([features_array], columns=EXPECTED_FEATURES)
        
        # Debug logging
        logger.info(f"Input features shape: {feature_df.shape}")
        logger.info(f"Amount after preprocessing: {feature_df['Amount'].iloc[0]:.4f}")
        logger.info(f"Time after preprocessing: {feature_df['Time'].iloc[0]:.4f}")
        
        # Make predictions using DataFrame (matches training format)
        prediction = model.predict(feature_df)[0]
        probability = model.predict_proba(feature_df)[0][1]
        
        # Log prediction for monitoring
        logger.info(f"Prediction made: fraud={prediction}, probability={probability:.4f}")
        
        return {
            "fraud": int(prediction),
            "probability": round(float(probability), 4),
            "risk_level": get_risk_level(probability),
            "features_processed": len(features_array),
            "debug_info": {
                "amount_transformed": round(float(feature_df['Amount'].iloc[0]), 4),
                "time_normalized": round(float(feature_df['Time'].iloc[0]), 4),
                "feature_count": len(features_array)
            }
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

def get_risk_level(probability: float) -> str:
    """Convert probability to risk level for better interpretability"""
    if probability < 0.1:
        return "very_low"
    elif probability < 0.3:
        return "low"
    elif probability < 0.7:
        return "medium"
    elif probability < 0.9:
        return "high"
    else:
        return "very_high"

@app.get("/features")
def get_expected_features():
    """Return the expected feature names and order"""
    return {
        "features": EXPECTED_FEATURES,
        "count": len(EXPECTED_FEATURES)
    }