import streamlit as st
import requests
import random
import pandas as pd

st.set_page_config(page_title="Fraud Detection", layout="centered")

st.title("💳 Fraud Detection System")
st.write("Click below to generate or test a transaction")

API_URL = "http://127.0.0.1:8000/predict"

# -------------------------------
# SESSION STATE
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = {
        "Time": 0.0,
        "Amount": 0.0,
        **{f"V{i}": 0.0 for i in range(1, 29)}
    }

# -------------------------------
# BUTTONS
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📦 Load Sample Data"):
        st.session_state.data = {
            "Time": 100.0,  # Raw time value
            "Amount": 149.62,  # Raw amount
            **{f"V{i}": random.uniform(-1, 1) for i in range(1, 29)}
        }

with col2:
    if st.button("🎲 Generate Random Transaction"):
        # Generate more realistic transaction patterns
        transaction_type = random.choice(['normal', 'suspicious'])
        
        if transaction_type == 'normal':
            # Normal transaction pattern
            st.session_state.data = {
                "Time": random.uniform(0, 172792),  # Raw time
                "Amount": round(random.uniform(1, 500), 2),  # Normal amounts
                **{f"V{i}": random.uniform(-2, 2) for i in range(1, 29)}  # Normal V values
            }
        else:
            # Suspicious transaction pattern (based on fraud characteristics)
            st.session_state.data = {
                "Time": random.uniform(0, 172792),  # Raw time
                "Amount": round(random.uniform(0.1, 10), 2),  # Small amounts common in fraud
                **{f"V{i}": random.uniform(-4, 4) for i in range(1, 29)}  # More extreme V values
            }

with col3:
    if st.button("🚨 Load Fraud Example"):
        # Load a transaction pattern that's more likely to be flagged as fraud
        st.session_state.data = {
            "Time": 50000.0,
            "Amount": 1.0,  # Small amount
            "V1": -2.312227, "V2": 1.951992, "V3": -1.609851, "V4": 3.997906,
            "V5": -0.522188, "V6": -1.426545, "V7": -2.537387, "V8": 1.391657,
            "V9": -2.770089, "V10": -2.772272, "V11": 3.202033, "V12": -2.899907,
            "V13": -0.595221, "V14": -4.289254, "V15": 0.389724, "V16": -1.140651,
            "V17": -2.830075, "V18": -0.016858, "V19": 0.416648, "V20": 0.126910,
            "V21": 0.517232, "V22": -0.035049, "V23": -0.465211, "V24": 0.320198,
            "V25": 0.044519, "V26": 0.177840, "V27": 0.261145, "V28": -0.143276
        }

# -------------------------------
# INPUTS
# -------------------------------
st.subheader("Transaction Details")

Time = st.number_input("Time", value=st.session_state.data["Time"])
Amount = st.number_input("Amount", value=st.session_state.data["Amount"])

features = {f"V{i}": st.session_state.data[f"V{i}"] for i in range(1, 29)}

# -------------------------------
# SINGLE PREDICTION
# -------------------------------
if st.button("🚀 Check Fraud"):

    data = {
        "Time": Time,
        **features,
        "Amount": Amount
    }

    try:
        response = requests.post(API_URL, json=data)
        result = response.json()

        fraud = result.get("fraud")
        prob = result.get("probability", 0)

        st.subheader("Result")

        if fraud == 1:
            st.error("🚨 Fraud Detected!")
        else:
            st.success("✅ Legit Transaction")

        st.metric("Fraud Probability", f"{prob * 100:.2f}%")
        
        # Show risk interpretation
        if prob < 0.01:
            st.info("🟢 Very Low Risk - Typical legitimate transaction")
        elif prob < 0.1:
            st.info("🟡 Low Risk - Monitor if needed")
        elif prob < 0.5:
            st.warning("🟠 Medium Risk - Review recommended")
        else:
            st.error("🔴 High Risk - Investigation required")

    except Exception as e:
        st.error(f"Error: {e}")

# =========================================================
# 🚀 FILE UPLOAD (BATCH FRAUD DETECTION)
# =========================================================

st.divider()
st.subheader("📂 Upload CSV for Batch Fraud Detection")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview:", df.head())

    if st.button("🔍 Run Batch Prediction"):
        results = []

        feature_order = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

        for _, row in df.iterrows():
            data = {col: row[col] for col in feature_order}

            try:
                response = requests.post(API_URL, json=data)
                result = response.json()

                results.append({
                    "fraud": result.get("fraud"),
                    "probability": result.get("probability")
                })

            except:
                results.append({"fraud": None, "probability": None})

        result_df = pd.concat([df, pd.DataFrame(results)], axis=1)

        st.success("Batch Prediction Completed ✅")
        st.write(result_df.head())

        # Download result
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Results",
            csv,
            "fraud_results.csv",
            "text/csv"
        )

# =========================================================
# 📄 SAMPLE FILE DOWNLOAD
# =========================================================

st.divider()
st.subheader("📄 Download Sample Files")

col1, col2 = st.columns(2)

with col1:
    st.write("**Legitimate Transactions Sample**")
    
    # Create sample legitimate transactions
    legit_data = pd.DataFrame([
        {
            "Time": 100.0,
            "V1": -1.359807, "V2": -0.072781, "V3": 2.536347, "V4": 1.378155,
            "V5": -0.338321, "V6": 0.462388, "V7": 0.239599, "V8": 0.098698,
            "V9": 0.363787, "V10": 0.090794, "V11": -0.551600, "V12": -0.617801,
            "V13": -0.991390, "V14": -0.311169, "V15": 1.468177, "V16": -0.470401,
            "V17": 0.207971, "V18": 0.025791, "V19": 0.403993, "V20": 0.251412,
            "V21": -0.018307, "V22": 0.277838, "V23": -0.110474, "V24": 0.066928,
            "V25": 0.128539, "V26": -0.189115, "V27": 0.133558, "V28": -0.021053,
            "Amount": 149.62
        },
        {
            "Time": 500.0,
            "V1": 1.191857, "V2": 0.266151, "V3": 0.166480, "V4": 0.448154,
            "V5": 0.060018, "V6": -0.082361, "V7": -0.078803, "V8": 0.085102,
            "V9": -0.255425, "V10": -0.166974, "V11": 1.612727, "V12": 1.065235,
            "V13": 0.489095, "V14": -0.143772, "V15": 0.635558, "V16": 0.463917,
            "V17": -0.114805, "V18": -0.183361, "V19": -0.145783, "V20": -0.069083,
            "V21": -0.225775, "V22": -0.638672, "V23": 0.101288, "V24": -0.339846,
            "V25": 0.167170, "V26": 0.125895, "V27": -0.008983, "V28": 0.014724,
            "Amount": 59.99
        },
        {
            "Time": 1200.0,
            "V1": -0.966272, "V2": -0.185226, "V3": 1.792993, "V4": -0.863291,
            "V5": -0.010309, "V6": 1.247203, "V7": 0.237609, "V8": 0.377436,
            "V9": -1.387024, "V10": -0.054952, "V11": -0.226487, "V12": 0.178228,
            "V13": 0.507757, "V14": -0.287924, "V15": -0.631418, "V16": -1.059647,
            "V17": -0.684093, "V18": 1.965775, "V19": -1.232622, "V20": -0.208038,
            "V21": -0.108300, "V22": 0.005274, "V23": -0.190321, "V24": -1.175575,
            "V25": 0.647376, "V26": -0.221929, "V27": 0.062723, "V28": 0.061458,
            "Amount": 89.00
        }
    ])
    
    csv_legit = legit_data.to_csv(index=False).encode("utf-8")
    
    st.download_button(
        "⬇️ Download Legitimate Sample",
        csv_legit,
        "legitimate_transactions.csv",
        "text/csv",
        help="Sample of normal/legitimate transactions with low fraud probability"
    )

with col2:
    st.write("**Fraudulent Transactions Sample**")
    
    # Create sample fraudulent transactions (based on known fraud patterns)
    fraud_data = pd.DataFrame([
        {
            "Time": 50000.0,
            "V1": -2.312227, "V2": 1.951992, "V3": -1.609851, "V4": 3.997906,
            "V5": -0.522188, "V6": -1.426545, "V7": -2.537387, "V8": 1.391657,
            "V9": -2.770089, "V10": -2.772272, "V11": 3.202033, "V12": -2.899907,
            "V13": -0.595221, "V14": -4.289254, "V15": 0.389724, "V16": -1.140651,
            "V17": -2.830075, "V18": -0.016858, "V19": 0.416648, "V20": 0.126910,
            "V21": 0.517232, "V22": -0.035049, "V23": -0.465211, "V24": 0.320198,
            "V25": 0.044519, "V26": 0.177840, "V27": 0.261145, "V28": -0.143276,
            "Amount": 0.77
        },
        {
            "Time": 75000.0,
            "V1": -3.043541, "V2": -3.157307, "V3": 1.088463, "V4": 2.288644,
            "V5": 1.359805, "V6": -1.064823, "V7": 0.325574, "V8": -2.067441,
            "V9": -2.296914, "V10": 1.643865, "V11": -1.492513, "V12": -0.482748,
            "V13": 0.771679, "V14": -2.808455, "V15": -0.447061, "V16": 0.881946,
            "V17": -2.996123, "V18": -5.086672, "V19": 1.252967, "V20": 0.237609,
            "V21": 0.377436, "V22": -0.503198, "V23": 1.800499, "V24": -0.246761,
            "V25": 1.151816, "V26": 0.246219, "V27": 0.151156, "V28": 0.061216,
            "Amount": 1.00
        },
        {
            "Time": 120000.0,
            "V1": -1.158233, "V2": 2.040747, "V3": -2.420165, "V4": 0.275735,
            "V5": -1.401834, "V6": -1.506637, "V7": -0.681673, "V8": -1.462320,
            "V9": -0.470034, "V10": 0.570328, "V11": -3.581652, "V12": 2.781648,
            "V13": -2.770089, "V14": -2.772272, "V15": 0.731762, "V16": -0.558097,
            "V17": 0.389724, "V18": -0.070972, "V19": 0.570328, "V20": -0.399486,
            "V21": -0.665637, "V22": -0.418608, "V23": -0.126910, "V24": 0.517232,
            "V25": -0.035049, "V26": -0.465211, "V27": 0.320198, "V28": 0.044519,
            "Amount": 2.69
        }
    ])
    
    csv_fraud = fraud_data.to_csv(index=False).encode("utf-8")
    
    st.download_button(
        "⬇️ Download Fraudulent Sample",
        csv_fraud,
        "fraudulent_transactions.csv",
        "text/csv",
        help="Sample of suspicious/fraudulent transactions with high fraud probability"
    )

st.info("💡 **Tip**: The legitimate transactions should show low fraud probabilities (<5%), while fraudulent transactions should show higher probabilities (>50%). Use these samples to test your fraud detection system.")

# =========================================================
# 📄 SAMPLE FILE DOWNLOAD
# =========================================================

st.divider()
st.subheader("📄 Download Sample File")

sample_data = pd.DataFrame([{
    "Time": 0.1,
    **{f"V{i}": 0.1 for i in range(1, 29)},
    "Amount": 100.0
}])

csv_sample = sample_data.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Sample CSV",
    csv_sample,
    "sample_input.csv",
    "text/csv"
)