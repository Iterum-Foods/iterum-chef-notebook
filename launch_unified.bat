@echo off
REM Unified Batch Launcher for Iterum R&D Chef Notebook
REM Uses the consolidated Python launcher with menu options

echo =====================================
echo   Iterum R^&D Chef Notebook
echo   Unified Launcher
echo =====================================
echo.

REM Parse command line arguments
set LAUNCH_MODE=interactive
set PYTHON_ARGS=

:parse_args
if "%~1"=="" goto :end_args
if "%~1"=="--full" set LAUNCH_MODE=full
if "%~1"=="--backend" set LAUNCH_MODE=backend
if "%~1"=="--frontend" set LAUNCH_MODE=frontend
if "%~1"=="--quiet" set LAUNCH_MODE=quiet
if "%~1"=="--help" goto :show_help
set PYTHON_ARGS=%PYTHON_ARGS% %1
shift
goto :parse_args
:end_args

REM If no mode specified, show menu
if "%LAUNCH_MODE%"=="interactive" goto :show_menu

REM Jump directly to launch
goto :launch_app

:show_menu
echo Select launch mode:
echo.
echo 1. Full Application     - Backend + Frontend + Browser (Recommended)
echo 2. Backend Only         - API server only (for development)
echo 3. Frontend Only        - Web interface only (API must run separately)
echo 4. Quiet Mode           - Full app without opening browser
echo 5. Run Tests            - Launch test suite instead
echo 6. Help                 - Show usage information
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" set LAUNCH_MODE=full
if "%choice%"=="2" set LAUNCH_MODE=backend
if "%choice%"=="3" set LAUNCH_MODE=frontend
if "%choice%"=="4" set LAUNCH_MODE=quiet
if "%choice%"=="5" goto :run_tests
if "%choice%"=="6" goto :show_help
if "%choice%"=="7" goto :exit

if "%LAUNCH_MODE%"=="interactive" (
    echo Invalid choice. Please select 1-7.
    goto :show_menu
)

:launch_app
REM Robust Python detection (same logic as launch-notebook.bat)
echo 🔍 Detecting Python installation...

REM Set the Python executable path (hardcoded working path)
set PYTHON_EXE="C:\Users\chefm\AppData\Local\Programs\Python\Python313\python.exe"

REM Check if Python exists at the specified path
if not exist %PYTHON_EXE% (
    echo Python not found at default location, searching alternatives...
    
    REM Try virtual environment first
    if exist "venv\Scripts\python.exe" (
        set PYTHON_EXE="venv\Scripts\python.exe"
        echo ✅ Found Python in virtual environment: %PYTHON_EXE%
        goto :python_found
    )
    
    REM Try other common Python locations
    if exist "C:\Python313\python.exe" (
        set PYTHON_EXE="C:\Python313\python.exe"
        echo ✅ Found Python at: %PYTHON_EXE%
        goto :python_found
    )
    
    if exist "C:\Program Files\Python313\python.exe" (
        set PYTHON_EXE="C:\Program Files\Python313\python.exe"
        echo ✅ Found Python at: %PYTHON_EXE%
        goto :python_found
    )
    
    REM Try system PATH as last resort
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_EXE=python
        echo ✅ Found Python in system PATH
        goto :python_found
    )
    
    echo ❌ Error: Could not find Python installation
    echo.
    echo Please install Python 3.9+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    echo Searched locations:
    echo   - C:\Users\chefm\AppData\Local\Programs\Python\Python313\python.exe
    echo   - venv\Scripts\python.exe
    echo   - C:\Python313\python.exe
    echo   - C:\Program Files\Python313\python.exe
    echo   - System PATH
    pause
    exit /b 1
)

:python_found
echo ✅ Using Python: %PYTHON_EXE%

REM Test Python installation
echo 🧪 Testing Python installation...
%PYTHON_EXE% --version
if errorlevel 1 (
    echo ❌ Error: Python executable is not working properly
    echo Please reinstall Python or check your installation.
    pause
    exit /b 1
)

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ No virtual environment found. Installing dependencies globally...
)

REM Install/update dependencies if needed
echo 🔧 Checking dependencies...
%PYTHON_EXE% -m pip install -q uvicorn fastapi

echo.
echo 🚀 Launching Iterum R&D Chef Notebook (%LAUNCH_MODE% mode)...
echo.

REM Launch the application using the unified Python launcher
%PYTHON_EXE% app_launcher.py --mode %LAUNCH_MODE% %PYTHON_ARGS%

goto :end

:run_tests
echo.
echo 🧪 Launching Test Suite...
echo.
call test_unified.bat
goto :end

:show_help
echo.
echo Iterum R&D Chef Notebook - Unified Launcher
echo ===========================================
echo.
echo Usage:
echo   %~nx0                    - Interactive menu
echo   %~nx0 --full             - Launch full application (default)
echo   %~nx0 --backend          - Launch backend API only
echo   %~nx0 --frontend         - Launch frontend only
echo   %~nx0 --quiet            - Full app without opening browser
echo   %~nx0 --help             - Show this help
echo.
echo Additional Options:
echo   --backend-port 8001      - Use custom backend port
echo   --frontend-port 8081     - Use custom frontend port
echo.
echo Examples:
echo   %~nx0 --backend --backend-port 9000
echo   %~nx0 --full --quiet
echo   %~nx0 --frontend --frontend-port 3000
echo.
echo Other Tools:
echo   test_unified.bat         - Run test suite
echo   clear_users.bat          - Clear user data
echo   python load_comprehensive_equipment.py  - Load equipment database
echo.
echo URLs (when running):
echo   Frontend:     http://localhost:8080
echo   Backend API:  http://localhost:8000
echo   API Docs:     http://localhost:8000/docs
echo.
goto :end

:exit
echo Goodbye!

:end
pause 