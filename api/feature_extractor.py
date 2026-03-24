"""
Feature extraction utilities for consistent API input processing.
"""
import pandas as pd
import numpy as np
from typing import Dict, List

def get_feature_names_from_training_data(csv_path: str = "data/raw/fraud.csv") -> List[str]:
    """
    Extract feature names from the original training data to ensure consistency.
    This should be run once to generate the feature list for the API.
    """
    try:
        # Load a small sample to get column names
        df = pd.read_csv(csv_path, nrows=1)
        
        # Apply the same feature engineering as in training
        from pipeline.feature_engineering import add_features
        df = add_features(df)
        
        # Remove target column
        features = [col for col in df.columns if col != 'Class']
        
        print("Feature names extracted:")
        for i, feature in enumerate(features):
            print(f"{i+1:2d}. {feature}")
        
        return features
        
    except Exception as e:
        print(f"Error extracting features: {e}")
        return []

def validate_input_features(input_data: Dict[str, float], expected_features: List[str]) -> Dict[str, any]:
    """
    Validate and reorder input features to match training data.
    """
    validation_result = {
        "valid": True,
        "missing_features": [],
        "extra_features": [],
        "ordered_values": []
    }
    
    # Check for missing features
    for feature in expected_features:
        if feature not in input_data:
            validation_result["missing_features"].append(feature)
            validation_result["valid"] = False
        else:
            validation_result["ordered_values"].append(input_data[feature])
    
    # Check for extra features
    for feature in input_data:
        if feature not in expected_features:
            validation_result["extra_features"].append(feature)
    
    return validation_result

if __name__ == "__main__":
    # Run this to get the correct feature order for your API
    features = get_feature_names_from_training_data()
    
    # Generate Python list format for copying to API
    print("\nCopy this to your API code:")
    print("EXPECTED_FEATURES = [")
    for feature in features:
        print(f"    '{feature}',")
    print("]")