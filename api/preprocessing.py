"""
Preprocessing utilities to ensure API input matches training data format.
"""
import numpy as np
import pandas as pd

# These values should be extracted from training data
# For now, using reasonable defaults based on the credit card dataset
TIME_MAX = 172792.0  # Approximate max time from credit card dataset
AMOUNT_LOG_TRANSFORM = True

def preprocess_transaction(input_data: dict) -> pd.DataFrame:
    """
    Apply the same preprocessing as training pipeline.
    
    Args:
        input_data: Dictionary with transaction features
        
    Returns:
        DataFrame with preprocessed features
    """
    # Make a copy to avoid modifying original
    processed_data = input_data.copy()
    
    # 1. Log transform Amount (same as cleaning.py)
    if 'Amount' in processed_data and AMOUNT_LOG_TRANSFORM:
        processed_data['Amount'] = np.log1p(processed_data['Amount'])
    
    # 2. Normalize Time (same as feature_engineering.py)
    if 'Time' in processed_data:
        # If Time is already normalized (0-1), keep it
        # If Time is raw seconds, normalize it
        if processed_data['Time'] > 1.0:
            processed_data['Time'] = processed_data['Time'] / TIME_MAX
    
    return processed_data

def get_training_stats():
    """
    Get preprocessing statistics from training data.
    This should be run once to extract the correct normalization values.
    """
    try:
        df = pd.read_csv("data/raw/fraud.csv")
        
        stats = {
            'time_max': df['Time'].max(),
            'time_min': df['Time'].min(),
            'amount_max': df['Amount'].max(),
            'amount_min': df['Amount'].min(),
            'amount_mean': df['Amount'].mean(),
            'amount_std': df['Amount'].std()
        }
        
        print("Training data statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")
            
        return stats
        
    except Exception as e:
        print(f"Error getting training stats: {e}")
        return None

if __name__ == "__main__":
    get_training_stats()