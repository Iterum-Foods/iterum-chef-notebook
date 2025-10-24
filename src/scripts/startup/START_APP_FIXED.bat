@echo off
echo ===============================================
echo       Iterum Chef Notebook Launcher
echo    Professional Recipe Management System
echo ===============================================
echo.

REM Change to the project root directory
cd /d "%~dp0\..\..\"

REM Check if Python is available (try both 'python' and 'py' commands)
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python not found. Please ensure Python is installed and in your PATH.
        echo.
        echo Try running: python --version or py --version
        pause
        exit /b 1
    ) else (
        echo OK: Python found (using 'py' command)
        set PYTHON_CMD=py
    )
) else (
    echo OK: Python found (using 'python' command)
    set PYTHON_CMD=python
)

REM Check if required files exist
if not exist "app\main.py" (
    echo ERROR: Backend application not found.
    echo    Expected: app\main.py
    pause
    exit /b 1
)

if not exist "scripts\serve_frontend.py" (
    echo ERROR: Frontend server not found.
    echo    Expected: scripts\serve_frontend.py
    pause
    exit /b 1
)

if not exist "scripts\start_full_app.py" (
    echo ERROR: Startup script not found.
    echo    Expected: scripts\start_full_app.py
    pause
    exit /b 1
)

echo OK: All required files found
echo Starting Iterum Chef Notebook...

REM Run the Python startup script using the detected Python command
%PYTHON_CMD% scripts\start_full_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start properly.
    echo.
    echo Troubleshooting tips:
    echo    1. Check if ports 8000 and 8080 are available
    echo    2. Ensure all dependencies are installed: %PYTHON_CMD% -m pip install -r requirements.txt
    echo    3. Check if another instance is already running
    echo    4. Try running: %PYTHON_CMD% scripts\start_full_app.py directly
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo SUCCESS: Application started successfully!
    echo Frontend: http://localhost:8080
    echo API Docs: http://localhost:8000/docs
    echo.
    echo Press any key to exit...
)

pause
