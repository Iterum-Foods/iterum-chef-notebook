@echo off
REM Start Recipe Manager Web Interface

title Recipe Manager - Web Interface

echo ============================================================
echo           RECIPE MANAGER - WEB INTERFACE
echo ============================================================
echo.
echo Starting web server...
echo.
echo Once started, open your browser and go to:
echo    http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

py web_app.py

pause


