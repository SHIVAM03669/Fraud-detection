"""
AWS Lambda handler for fraud detection API
"""
import json
import joblib
import numpy as np
import pandas as pd
from api.preprocessing import preprocess_transaction

# Load model once during cold start
model = None

def load_model():
    global model
    if model is None:
        try:
            model = joblib.load("models/fraud_model.pkl")
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None
    return model

def lambda_handler(event, context):
    """
    AWS Lambda handler for fraud detection
    """
    try:
        # Load model
        fraud_model = load_model()
        if fraud_model is None:
            return {
                'statusCode': 503,
                'body': json.dumps({'error': 'Model not available'})
            }
        
        # Parse request body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        # Expected features
        EXPECTED_FEATURES = [
            'Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
            'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
            'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount'
        ]
        
        # Preprocess input
        processed_data = preprocess_transaction(body)
        
        # Create feature array
        features_array = []
        missing_features = []
        
        for feature in EXPECTED_FEATURES:
            if feature in processed_data:
                features_array.append(processed_data[feature])
            else:
                missing_features.append(feature)
        
        if missing_features:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Missing required features: {missing_features}'
                })
            }
        
        # Create DataFrame for prediction
        feature_df = pd.DataFrame([features_array], columns=EXPECTED_FEATURES)
        
        # Make prediction
        prediction = fraud_model.predict(feature_df)[0]
        probability = fraud_model.predict_proba(feature_df)[0][1]
        
        # Determine risk level
        if probability < 0.1:
            risk_level = "very_low"
        elif probability < 0.3:
            risk_level = "low"
        elif probability < 0.7:
            risk_level = "medium"
        elif probability < 0.9:
            risk_level = "high"
        else:
            risk_level = "very_high"
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'fraud': int(prediction),
                'probability': round(float(probability), 4),
                'risk_level': risk_level,
                'features_processed': len(features_array)
            })
        }
        
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }