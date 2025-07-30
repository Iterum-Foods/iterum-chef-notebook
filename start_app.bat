@echo off
title Iterum R&D Chef Notebook
color 0A

echo.
echo ========================================
echo   🍳 Iterum R&D Chef Notebook
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ⚠️  Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

:: Install requirements if needed
if not exist "venv\Lib\site-packages\fastapi" (
    echo 📦 Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)

:: Start the application
echo 🚀 Starting Iterum R&D Chef Notebook...
echo.
python start_full_app.py

:: If we get here, the app has stopped
echo.
echo 👋 Application stopped
pause 