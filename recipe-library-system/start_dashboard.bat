@echo off
REM Unified Recipe Management Dashboard
REM Desktop application combining all features

title Recipe Management Dashboard

echo.
echo ========================================
echo    RECIPE MANAGEMENT DASHBOARD
echo ========================================
echo.
echo Starting unified desktop dashboard...
echo.

python unified_dashboard.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start dashboard!
    echo.
    pause
)

