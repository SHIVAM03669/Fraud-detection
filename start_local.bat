@echo off
echo 🚀 Starting Fraud Detection System Locally...

REM Check if model exists
if not exist "models\fraud_model.pkl" (
    echo ❌ Model file not found. 
    echo Please ensure you have the trained model file at: models\fraud_model.pkl
    echo.
    echo If you need to train the model, you'll need the fraud dataset.
    echo You can download it from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
    echo Place it at: data\raw\fraud.csv
    echo Then run: python main.py
    echo.
    pause
    exit /b 1
)

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🏃 Starting API server on port 8001...
start "Fraud Detection API" cmd /k "uvicorn api.app:app --host 127.0.0.1 --port 8001 --reload"

echo ⏳ Waiting for API to start...
timeout /t 5 /nobreak >nul

echo 🎨 Starting Dashboard...
start "Fraud Detection Dashboard" cmd /k "streamlit run dashboard/app.py --server.port 8501"

echo ✅ Services started!
echo.
echo 🌐 Access your services:
echo   API: http://localhost:8001
echo   API Docs: http://localhost:8001/docs
echo   Dashboard: http://localhost:8501
echo   Health Check: http://localhost:8001/health
echo.
echo ⚠️  Note: Update the API_URL in dashboard if needed
echo Press any key to continue...
pause >nul