@echo off
REM Main entry point for Iterum R&D Chef Notebook
REM This is the primary file to start the application

echo =====================================
echo   Iterum R^&D Chef Notebook
echo   Main Application Launcher
echo =====================================
echo.
echo Starting the application...
echo.

REM Call the unified launcher
call launch_unified.bat %* 