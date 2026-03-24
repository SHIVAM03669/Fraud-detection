from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, brier_score_loss
import numpy as np


def split_data(df):   # ✅ fixed name
    X = df.drop('Class', axis=1)
    y = df['Class']

    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

def handle_imbalance(X_train, y_train):
    """
    DEPRECATED: This function is no longer used.
    We now handle imbalance using class_weight='balanced' in the models.
    """
    raise DeprecationWarning(
        "SMOTE-based imbalance handling has been replaced with class_weight='balanced'. "
        "Remove this function call from your pipeline."
    )


def train_models(X_train, y_train, X_val, y_val):
    """
    Train models with class balancing and probability calibration.
    Uses class_weight='balanced' instead of SMOTE for better probability estimates.
    """
    models = {
        "logistic": LogisticRegression(
            max_iter=1000, 
            class_weight='balanced',
            random_state=42
        ),
        "random_forest": RandomForestClassifier(
            class_weight='balanced',
            random_state=42,
            n_estimators=100
        )
    }

    trained_models = {}

    for name, model in models.items():
        print(f"Training {name}...")
        
        # Fit the base model
        model.fit(X_train, y_train)
        
        # Apply probability calibration using validation set
        print(f"Calibrating {name} probabilities...")
        calibrated_model = CalibratedClassifierCV(
            model, 
            method='isotonic',  # Better for small datasets
            cv='prefit'  # Use our own validation split
        )
        calibrated_model.fit(X_val, y_val)
        
        trained_models[name] = calibrated_model

    return trained_models


def evaluate(models, X_test, y_test):
    """
    Evaluate models with additional probability calibration metrics.
    """
    for name, model in models.items():
        print(f"\n{name.upper()} EVALUATION")
        print("=" * 50)

        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]

        print("Classification Report:")
        print(classification_report(y_test, preds))

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, preds))

        print(f"ROC-AUC: {roc_auc_score(y_test, probs):.4f}")
        
        # Probability calibration metrics
        brier_score = brier_score_loss(y_test, probs)
        print(f"Brier Score (lower is better): {brier_score:.4f}")
        
        # Probability distribution analysis
        fraud_probs = probs[y_test == 1]
        normal_probs = probs[y_test == 0]
        
        print(f"\nProbability Distribution Analysis:")
        print(f"Fraud cases - Mean prob: {fraud_probs.mean():.3f}, Std: {fraud_probs.std():.3f}")
        print(f"Normal cases - Mean prob: {normal_probs.mean():.3f}, Std: {normal_probs.std():.3f}")
        
        # Check for extreme probabilities
        extreme_high = np.sum(probs > 0.95)
        extreme_low = np.sum(probs < 0.05)
        print(f"Extreme probabilities: {extreme_high} high (>95%), {extreme_low} low (<5%)")


def create_validation_split(X_train, y_train, val_size=0.2):
    """
    Create a validation split from training data for calibration.
    """
    return train_test_split(
        X_train, y_train, 
        test_size=val_size, 
        random_state=42, 
        stratify=y_train
    )