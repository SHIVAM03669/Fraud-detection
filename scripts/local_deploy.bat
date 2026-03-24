@echo off
REM Windows batch script for local deployment

echo 🚀 Starting Fraud Detection System Locally...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found. Please install Docker Desktop first.
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if model exists
if not exist "models\fraud_model.pkl" (
    echo ❌ Model file not found. Please train the model first:
    echo Run: python main.py
    pause
    exit /b 1
)

echo 📦 Building Docker containers...
docker-compose down --remove-orphans
docker-compose build --no-cache

echo 🏃 Starting services...
docker-compose up -d

echo ✅ Deployment complete!
echo.
echo 🌐 Access your services:
echo   API: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Dashboard: http://localhost:8501
echo   Health Check: http://localhost:8000/health
echo.
echo 📊 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
echo.
pause