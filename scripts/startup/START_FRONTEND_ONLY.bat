@echo off
echo ===============================================
echo     Iterum Chef Notebook - Frontend Only
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

echo OK: Starting frontend server only...
echo Frontend will be available at: http://localhost:8080
echo.
echo NOTE: Backend APIs will not be available, but basic functionality works
echo.

REM Start frontend server
py scripts\serve_frontend.py

pause
