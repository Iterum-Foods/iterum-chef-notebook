@echo off
echo ============================================================
echo CLEAR ALL USERS - Iterum R&D Chef Notebook
echo ============================================================
echo.
echo This script will clear ALL users from the system.
echo Make sure the application is not running before proceeding.
echo.

REM Use shared Python detection module
set PYTHON_DETECTION_VERBOSE=1
call python_detection.bat
if %errorlevel% neq 0 (
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: No virtual environment found. Using system Python.
)

REM Run the clear users script
echo.
echo Running user clearing script...
echo.
%PYTHON_EXE% clear_users.py

echo.
echo Script completed.
pause 