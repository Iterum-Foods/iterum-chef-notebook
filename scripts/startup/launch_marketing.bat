@echo off
title Iterum R^&D Marketing Launch
color 0A

echo.
echo 🍅 ITERUM R^&D MARKETING WEBSITE
echo ================================
echo.
echo Starting marketing website and waitlist system...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Launch the marketing system
python launch_marketing.py

pause