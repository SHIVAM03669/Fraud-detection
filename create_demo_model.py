"""
Create a demo fraud detection model for testing without the full dataset.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
import joblib
import os

def create_demo_data():
    """Create synthetic fraud detection data for demo purposes."""
    np.random.seed(42)
    
    # Create 1000 samples with 30 features (Time + V1-V28 + Amount)
    n_samples = 1000
    n_features = 30
    
    # Generate normal transactions (95% of data)
    normal_samples = int(n_samples * 0.95)
    normal_data = np.random.normal(0, 1, (normal_samples, n_features))
    normal_labels = np.zeros(normal_samples)
    
    # Generate fraud transactions (5% of data)
    fraud_samples = n_samples - normal_samples
    fraud_data = np.random.normal(0, 2, (fraud_samples, n_features))  # More extreme values
    fraud_labels = np.ones(fraud_samples)
    
    # Combine data
    X = np.vstack([normal_data, fraud_data])
    y = np.hstack([normal_labels, fraud_labels])
    
    # Create feature names
    feature_names = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df['Class'] = y
    
    return df

def train_demo_model():
    """Train a demo fraud detection model."""
    print("🎯 Creating demo fraud detection model...")
    
    # Create demo data
    df = create_demo_data()
    print(f"Created demo dataset with {len(df)} samples")
    print(f"Fraud rate: {df['Class'].mean():.2%}")
    
    # Split features and target
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Further split training data for calibration
    X_train_fit, X_val, y_train_fit, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    print("Training logistic regression model...")
    
    # Train base model
    base_model = LogisticRegression(
        max_iter=1000, 
        class_weight='balanced',
        random_state=42
    )
    base_model.fit(X_train_fit, y_train_fit)
    
    # Calibrate probabilities
    print("Calibrating probabilities...")
    calibrated_model = CalibratedClassifierCV(
        base_model, 
        method='isotonic',
        cv='prefit'
    )
    calibrated_model.fit(X_val, y_val)
    
    # Test the model
    test_pred = calibrated_model.predict(X_test)
    test_prob = calibrated_model.predict_proba(X_test)[:, 1]
    
    print(f"Test accuracy: {(test_pred == y_test).mean():.3f}")
    print(f"Average fraud probability: {test_prob[y_test == 1].mean():.3f}")
    print(f"Average normal probability: {test_prob[y_test == 0].mean():.3f}")
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    joblib.dump(calibrated_model, 'models/fraud_model.pkl')
    print("✅ Demo model saved to models/fraud_model.pkl")
    
    return calibrated_model

if __name__ == "__main__":
    train_demo_model()
    print("\n🎉 Demo model created successfully!")
    print("You can now run the fraud detection system:")
    print("1. API: python -m uvicorn api.app:app --host 127.0.0.1 --port 8001")
    print("2. Dashboard: streamlit run dashboard/app.py")
    print("3. Or use: start_local.bat")