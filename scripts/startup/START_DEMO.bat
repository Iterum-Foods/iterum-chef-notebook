@echo off
echo ===============================================
echo     Iterum Chef Notebook - Demo Mode
echo ===============================================
echo.
echo This starts ONLY the frontend for immediate testing
echo No backend required - works with demo data
echo.

REM Change to project root
cd /d "%~dp0\..\..\"

REM Check if frontend exists
if not exist "scripts\serve_frontend.py" (
    echo ERROR: Frontend server not found
    pause
    exit /b 1
)

echo Starting frontend server...
echo.
echo Frontend will be available at: http://localhost:8080
echo.
echo NOTE: This is demo mode - backend features will not work
echo But you can test the UI and basic functionality
echo.

REM Start frontend without virtual environment (more reliable)
py scripts\serve_frontend.py

pause
