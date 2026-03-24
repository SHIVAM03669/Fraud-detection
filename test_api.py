"""
Test script for the fraud detection API
"""
import requests
import json

API_URL = "http://127.0.0.1:8000/predict"

def test_api():
    # Test case 1: Normal transaction
    normal_transaction = {
        "Time": 100.0,  # Raw time value
        "V1": -1.359807, "V2": -0.072781, "V3": 2.536347, "V4": 1.378155,
        "V5": -0.338321, "V6": 0.462388, "V7": 0.239599, "V8": 0.098698,
        "V9": 0.363787, "V10": 0.090794, "V11": -0.551600, "V12": -0.617801,
        "V13": -0.991390, "V14": -0.311169, "V15": 1.468177, "V16": -0.470401,
        "V17": 0.207971, "V18": 0.025791, "V19": 0.403993, "V20": 0.251412,
        "V21": -0.018307, "V22": 0.277838, "V23": -0.110474, "V24": 0.066928,
        "V25": 0.128539, "V26": -0.189115, "V27": 0.133558, "V28": -0.021053,
        "Amount": 149.62  # Raw amount
    }
    
    # Test case 2: Potentially fraudulent transaction
    fraud_transaction = {
        "Time": 50000.0,  # Raw time value
        "V1": -2.312227, "V2": 1.951992, "V3": -1.609851, "V4": 3.997906,
        "V5": -0.522188, "V6": -1.426545, "V7": -2.537387, "V8": 1.391657,
        "V9": -2.770089, "V10": -2.772272, "V11": 3.202033, "V12": -2.899907,
        "V13": -0.595221, "V14": -4.289254, "V15": 0.389724, "V16": -1.140651,
        "V17": -2.830075, "V18": -0.016858, "V19": 0.416648, "V20": 0.126910,
        "V21": 0.517232, "V22": -0.035049, "V23": -0.465211, "V24": 0.320198,
        "V25": 0.044519, "V26": 0.177840, "V27": 0.261145, "V28": -0.143276,
        "Amount": 0.77  # Small amount (common in fraud)
    }
    
    print("Testing Fraud Detection API")
    print("=" * 50)
    
    # Test normal transaction
    print("\n1. Testing Normal Transaction:")
    try:
        response = requests.post(API_URL, json=normal_transaction)
        if response.status_code == 200:
            result = response.json()
            print(f"   Fraud: {result['fraud']}")
            print(f"   Probability: {result['probability']:.4f}")
            print(f"   Risk Level: {result['risk_level']}")
            if 'debug_info' in result:
                print(f"   Debug: {result['debug_info']}")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Connection error: {e}")
    
    # Test fraud transaction
    print("\n2. Testing Potentially Fraudulent Transaction:")
    try:
        response = requests.post(API_URL, json=fraud_transaction)
        if response.status_code == 200:
            result = response.json()
            print(f"   Fraud: {result['fraud']}")
            print(f"   Probability: {result['probability']:.4f}")
            print(f"   Risk Level: {result['risk_level']}")
            if 'debug_info' in result:
                print(f"   Debug: {result['debug_info']}")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Connection error: {e}")

if __name__ == "__main__":
    test_api()