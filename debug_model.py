"""
Debug script to test the model and identify probability issues.
"""
import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV

def test_model():
    print("=== MODEL DEBUGGING ===")
    
    try:
        # Load the model
        model = joblib.load("models/fraud_model.pkl")
        print(f"✅ Model loaded successfully")
        print(f"Model type: {type(model)}")
        
        # Check if it's calibrated
        is_calibrated = isinstance(model, CalibratedClassifierCV)
        print(f"Is calibrated: {is_calibrated}")
        
        if is_calibrated:
            # In newer sklearn versions, it's estimators_ instead of base_estimator
            if hasattr(model, 'estimators_'):
                print(f"Base estimator: {type(model.estimators_[0])}")
            elif hasattr(model, 'base_estimator'):
                print(f"Base estimator: {type(model.base_estimator)}")
            print(f"Calibration method: {model.method}")
        
        # Create test data (normal transaction) with proper preprocessing
        normal_features_raw = {
            'Time': 0.1,
            'V1': 0.1, 'V2': 0.1, 'V3': 0.1, 'V4': 0.1, 'V5': 0.1, 'V6': 0.1, 'V7': 0.1, 'V8': 0.1, 'V9': 0.1, 'V10': 0.1,
            'V11': 0.1, 'V12': 0.1, 'V13': 0.1, 'V14': 0.1, 'V15': 0.1, 'V16': 0.1, 'V17': 0.1, 'V18': 0.1, 'V19': 0.1, 'V20': 0.1,
            'V21': 0.1, 'V22': 0.1, 'V23': 0.1, 'V24': 0.1, 'V25': 0.1, 'V26': 0.1, 'V27': 0.1, 'V28': 0.1,
            'Amount': 100.0  # Raw amount
        }
        
        # Apply preprocessing (log transform Amount)
        normal_features_raw['Amount'] = np.log1p(normal_features_raw['Amount'])
        normal_features_df = pd.DataFrame([normal_features_raw])
        
        # Create test data (suspicious transaction) with proper preprocessing
        suspicious_features_raw = {
            'Time': 0.9,
            'V1': -2.5, 'V2': 3.0, 'V3': -1.8, 'V4': 2.2, 'V5': -3.1, 'V6': 1.9, 'V7': -2.7, 'V8': 2.8, 'V9': -1.5, 'V10': 3.2,
            'V11': -2.1, 'V12': 2.9, 'V13': -1.7, 'V14': 2.4, 'V15': -2.8, 'V16': 1.6, 'V17': -3.0, 'V18': 2.1, 'V19': -1.9, 'V20': 2.7,
            'V21': -2.3, 'V22': 3.1, 'V23': -1.4, 'V24': 2.6, 'V25': -2.9, 'V26': 1.8, 'V27': -2.4, 'V28': 2.5,
            'Amount': 5000.0  # Raw amount
        }
        
        # Apply preprocessing (log transform Amount)
        suspicious_features_raw['Amount'] = np.log1p(suspicious_features_raw['Amount'])
        suspicious_features_df = pd.DataFrame([suspicious_features_raw])
        
        print(f"\n=== TESTING NORMAL TRANSACTION ===")
        print(f"Features shape: {normal_features_df.shape}")
        print(f"Amount after log transform: {normal_features_df['Amount'].iloc[0]:.4f}")
        
        normal_pred = model.predict(normal_features_df)[0]
        normal_prob = model.predict_proba(normal_features_df)[0]
        
        print(f"Prediction: {normal_pred}")
        print(f"Probabilities: [Normal: {normal_prob[0]:.4f}, Fraud: {normal_prob[1]:.4f}]")
        
        print(f"\n=== TESTING SUSPICIOUS TRANSACTION ===")
        print(f"Features shape: {suspicious_features_df.shape}")
        print(f"Amount after log transform: {suspicious_features_df['Amount'].iloc[0]:.4f}")
        
        suspicious_pred = model.predict(suspicious_features_df)[0]
        suspicious_prob = model.predict_proba(suspicious_features_df)[0]
        
        print(f"Prediction: {suspicious_pred}")
        print(f"Probabilities: [Normal: {suspicious_prob[0]:.4f}, Fraud: {suspicious_prob[1]:.4f}]")
        
        # Test with original data format if available
        try:
            from pipeline.cleaning import run_cleaning_pipeline
            from pipeline.feature_engineering import add_features
            
            print(f"\n=== TESTING WITH PROPERLY PROCESSED DATA ===")
            
            # Load and process data the same way as training
            df = pd.read_csv("data/raw/fraud.csv")
            df = run_cleaning_pipeline("data/raw/fraud.csv")  # This applies log transform
            df = add_features(df)  # This normalizes Time
            
            print(f"Dataset shape after processing: {df.shape}")
            
            # Get a few samples
            normal_sample = df[df['Class'] == 0].iloc[0:1].drop('Class', axis=1)
            fraud_sample = df[df['Class'] == 1].iloc[0:1].drop('Class', axis=1)
            
            print(f"Normal sample prediction:")
            print(f"  Amount (processed): {normal_sample['Amount'].iloc[0]:.4f}")
            normal_real_pred = model.predict(normal_sample)[0]
            normal_real_prob = model.predict_proba(normal_sample)[0]
            print(f"  Prediction: {normal_real_pred}, Prob: {normal_real_prob[1]:.4f}")
            
            print(f"Fraud sample prediction:")
            print(f"  Amount (processed): {fraud_sample['Amount'].iloc[0]:.4f}")
            fraud_real_pred = model.predict(fraud_sample)[0]
            fraud_real_prob = model.predict_proba(fraud_sample)[0]
            print(f"  Prediction: {fraud_real_pred}, Prob: {fraud_real_prob[1]:.4f}")
            
        except Exception as e:
            print(f"Could not test with real data: {e}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("The model might not exist or was not retrained with the new approach.")
        print("Please run: python main.py")

if __name__ == "__main__":
    test_model()