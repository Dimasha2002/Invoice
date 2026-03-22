@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo Invoice Generator - Starting
echo ========================================
echo.

REM Kill any existing process on port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| find "8000"') do taskkill /f /pid %%a 2>nul

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting app at http://localhost:8000
echo.
timeout /t 3

REM Open browser
start http://localhost:8000

REM Start the app
python app.py

pause
