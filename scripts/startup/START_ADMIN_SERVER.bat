@echo off
echo 🍅 ITERUM RECIPE LIBRARY - ADMIN SERVER STARTUP
echo ================================================
echo.
echo Starting backend server for admin access...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "app\main.py" (
    echo ❌ Backend files not found
    echo Please ensure you're running this from the project root directory
    pause
    exit /b 1
)

echo ✅ Python found
echo ✅ Backend files found
echo.
echo 🚀 Starting backend server...
echo.
echo The server will be available at:
echo   - Backend API: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Admin Login: http://localhost:8080/admin-login.html
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the backend server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo 👋 Server stopped
pause
