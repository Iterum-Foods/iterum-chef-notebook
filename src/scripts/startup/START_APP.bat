@echo off
echo 🍴===============================================🍴
echo       Iterum R&D Chef Notebook Launcher
echo    Professional Recipe R&D and Publishing System
echo 🍴===============================================🍴
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the Python startup script
py start_full_app.py

pause