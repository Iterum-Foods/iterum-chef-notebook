@echo off
echo 🚀 Starting Iterum R&D Chef Notebook Servers
echo =============================================

:: Check if we're in the correct directory
if not exist "app\main.py" (
    echo ❌ Error: Please run this from the Iterum App directory
    echo Current directory: %CD%
    echo Expected file: app\main.py
    pause
    exit /b 1
)

:: Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found at venv\Scripts\activate.bat
    echo Continuing without virtual environment...
)

:: Start the FastAPI backend server
echo 🌐 Starting FastAPI backend server on http://localhost:8000...
echo.
echo Backend will be available at:
echo   - API Health: http://localhost:8000/health
echo   - API Docs: http://localhost:8000/docs
echo   - Projects API: http://localhost:8000/api/projects/
echo.
echo ⚠️ Keep this window open - the backend server will run here
echo ⚠️ Press Ctrl+C to stop the server
echo.

py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause