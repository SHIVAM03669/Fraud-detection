@echo off
echo 🚀 Starting Fraud Detection System Locally...

REM Check if model exists
if not exist "models\fraud_model.pkl" (
    echo ❌ Model file not found. Training model first...
    python main.py
    if %errorlevel% neq 0 (
        echo ❌ Model training failed. Please check the error above.
        pause
        exit /b 1
    )
)

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🏃 Starting API server...
start "Fraud Detection API" cmd /k "uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload"

echo ⏳ Waiting for API to start...
timeout /t 5 /nobreak >nul

echo 🎨 Starting Dashboard...
start "Fraud Detection Dashboard" cmd /k "streamlit run dashboard/app.py --server.port 8501"

echo ✅ Services started!
echo.
echo 🌐 Access your services:
echo   API: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Dashboard: http://localhost:8501
echo   Health Check: http://localhost:8000/health
echo.
echo Press any key to continue...
pause >nul