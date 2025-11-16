@echo off
REM ============================================================
REM PYTHON DETECTION MODULE for Iterum R&D Chef Notebook
REM This module sets the PYTHON_EXE variable with a working Python path
REM Usage: call python_detection.bat
REM Output: Sets %PYTHON_EXE% variable for use in calling script
REM ============================================================

REM Don't echo the detection process unless requested
if not "%PYTHON_DETECTION_VERBOSE%"=="1" goto :quiet_detection
echo 🔍 Detecting Python installation...
:quiet_detection

REM Set the Python executable path (hardcoded working path)
set PYTHON_EXE="C:\Users\chefm\AppData\Local\Programs\Python\Python313\python.exe"

REM Check if Python exists at the specified path
if exist %PYTHON_EXE% goto :test_python

REM Try virtual environment first
if exist "venv\Scripts\python.exe" (
    set PYTHON_EXE="venv\Scripts\python.exe"
    if not "%PYTHON_DETECTION_VERBOSE%"=="1" goto :test_python
    echo ✅ Found Python in virtual environment: %PYTHON_EXE%
    goto :test_python
)

REM Try other common Python locations
if exist "C:\Python313\python.exe" (
    set PYTHON_EXE="C:\Python313\python.exe"
    if not "%PYTHON_DETECTION_VERBOSE%"=="1" goto :test_python
    echo ✅ Found Python at: %PYTHON_EXE%
    goto :test_python
)

if exist "C:\Program Files\Python313\python.exe" (
    set PYTHON_EXE="C:\Program Files\Python313\python.exe"
    if not "%PYTHON_DETECTION_VERBOSE%"=="1" goto :test_python
    echo ✅ Found Python at: %PYTHON_EXE%
    goto :test_python
)

REM Try system PATH as last resort
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=python
    if not "%PYTHON_DETECTION_VERBOSE%"=="1" goto :test_python
    echo ✅ Found Python in system PATH
    goto :test_python
)

REM Python not found
echo ❌ Error: Could not find Python installation
echo.
echo Please install Python 3.9+ from: https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
echo Searched locations:
echo   - C:\Users\chefm\AppData\Local\Programs\Python\Python313\python.exe
echo   - venv\Scripts\python.exe
echo   - C:\Python313\python.exe
echo   - C:\Program Files\Python313\python.exe
echo   - System PATH
exit /b 1

:test_python
if not "%PYTHON_DETECTION_VERBOSE%"=="1" goto :quiet_test
echo ✅ Using Python: %PYTHON_EXE%
echo 🧪 Testing Python installation...

:quiet_test
REM Test Python installation
%PYTHON_EXE% --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python executable is not working properly
    echo Please reinstall Python or check your installation.
    exit /b 1
)

REM Success - Python is ready
if "%PYTHON_DETECTION_VERBOSE%"=="1" echo ✅ Python detection successful
exit /b 0 