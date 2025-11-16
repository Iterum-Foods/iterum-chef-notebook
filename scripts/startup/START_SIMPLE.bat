@echo off
echo ===============================================
echo     Iterum Chef Notebook - Simple Startup
echo ===============================================
echo.

REM Change to project root
cd /d "%~dp0\..\..\"

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Starting servers manually to avoid loading screen issues...
echo.

echo 1. Starting Backend Server...
start "Backend Server" py -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo 2. Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo 3. Starting Frontend Server...
start "Frontend Server" py scripts\serve_frontend.py

echo.
echo 4. Waiting 3 seconds for frontend to start...
timeout /t 3 /nobreak >nul

echo.
echo ===============================================
echo   Servers should now be running!
echo ===============================================
echo.
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:8080
echo API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
echo Opening frontend in browser...
start http://localhost:8080

pause
