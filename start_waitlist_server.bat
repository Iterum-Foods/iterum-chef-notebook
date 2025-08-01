@echo off
echo 🍅 ITERUM RECIPE LIBRARY - WAITLIST SERVER
echo ========================================
echo.
echo Starting the waitlist backend server...
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo ✅ Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✅ Installing dependencies...
    pip install fastapi uvicorn pydantic[email] python-multipart
)

echo.
echo 🚀 Starting FastAPI server for waitlist functionality...
echo.
echo The server will start on: http://localhost:8000
echo Waitlist API docs: http://localhost:8000/docs
echo Admin interface: http://localhost:8000/waitlist_admin.html
echo.

REM Change to app directory and start server
cd /d "%~dp0"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause