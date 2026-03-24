@echo off
echo 🛑 Stopping Fraud Detection System...

REM Kill processes by port
echo Stopping API server (port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo Stopping Dashboard (port 8501)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do (
    taskkill /f /pid %%a >nul 2>&1
)

REM Alternative: Kill by process name
taskkill /f /im "uvicorn.exe" >nul 2>&1
taskkill /f /im "streamlit.exe" >nul 2>&1
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq Fraud Detection*" >nul 2>&1

echo ✅ Services stopped!
pause