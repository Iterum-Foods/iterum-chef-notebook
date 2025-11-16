@echo off
echo 🍳 Starting Iterum R&D Chef Notebook with Enhanced Menu Parsing...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies.
    pause
    exit /b 1
)

REM Start backend server
echo 🚀 Starting backend server...
start "Iterum Backend" cmd /k "call venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server
echo 🌐 Starting frontend server...
start "Iterum Frontend" cmd /k "npm start"

REM Wait a moment for frontend to start
timeout /t 3 /nobreak >nul

echo.
echo ✅ Iterum R&D Chef Notebook is starting up!
echo.
echo 📱 Frontend: http://localhost:8080
echo 🔧 Backend API: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo 🧪 Test Menu Parsing:
echo    - Basic test: http://localhost:8000/api/menu/test-parsing
echo    - Debug text: POST to http://localhost:8000/api/menu/debug-text-parsing
echo    - Test Word doc: POST to http://localhost:8000/api/menu/test-word-parsing
echo.
echo Press any key to open the application...
pause >nul

REM Open browser
start http://localhost:8080

echo.
echo 🎉 Application opened in browser!
echo.
echo To stop the servers, close the command windows or press Ctrl+C in each window.
pause
