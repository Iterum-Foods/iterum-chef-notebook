@echo off
echo ===============================================
echo     Iterum Chef Notebook - Backend Only
echo ===============================================
echo.

REM Change to project root
cd /d "%~dp0\..\..\"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check Python
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo OK: Starting backend server only...
echo Backend API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

REM Start backend server with uvicorn
py -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
