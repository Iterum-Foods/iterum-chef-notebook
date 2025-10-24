@echo off
echo 📚 Recipe Library System
echo ==================================================
echo A library-style system for organizing recipes
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import sqlite3, json, pandas" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install pandas
    if errorlevel 1 (
        echo ❌ Failed to install required packages
        pause
        exit /b 1
    )
)

echo ✅ Dependencies ready
echo.

REM Run the recipe library system
python run_library.py

echo.
echo Press any key to exit...
pause >nul 