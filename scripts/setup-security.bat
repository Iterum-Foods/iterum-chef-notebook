@echo off
echo.
echo 🔐 GitHub Security Setup for Iterum Culinary App
echo ================================================
echo.

REM Check if PowerShell is available
powershell -Command "Get-Command powershell" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PowerShell not found. Please install PowerShell to run this script.
    pause
    exit /b 1
)

REM Run the PowerShell script
echo 🚀 Starting security setup...
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0quick-security-setup.ps1"

echo.
echo ✅ Setup script completed!
echo.
pause
