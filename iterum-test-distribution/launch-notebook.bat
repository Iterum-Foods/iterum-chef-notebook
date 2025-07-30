@echo off
echo ============================================================
echo ITERUM R&D CHEF NOTEBOOK - LAUNCHER
echo ============================================================
echo.

REM Set the Python executable path
set PYTHON_EXE="C:\Users\chefm\AppData\Local\Programs\Python\Python313\python.exe"

REM Check if Python exists at the specified path
if not exist %PYTHON_EXE% (
    echo ERROR: Python not found at %PYTHON_EXE%
    echo.
    echo Trying to find Python in common locations...
    
    REM Try virtual environment first
    if exist "venv\Scripts\python.exe" (
        set PYTHON_EXE="venv\Scripts\python.exe"
        echo Found Python in virtual environment: %PYTHON_EXE%
        goto :run_launcher
    )
    
    REM Try other common Python locations
    if exist "C:\Python313\python.exe" (
        set PYTHON_EXE="C:\Python313\python.exe"
        echo Found Python at: %PYTHON_EXE%
        goto :run_launcher
    )
    
    if exist "C:\Program Files\Python313\python.exe" (
        set PYTHON_EXE="C:\Program Files\Python313\python.exe"
        echo Found Python at: %PYTHON_EXE%
        goto :run_launcher
    )
    
    echo ERROR: Could not find Python installation
    echo Please install Python from https://python.org/downloads
    echo.
    pause
    exit /b 1
)

:run_launcher
echo Using Python: %PYTHON_EXE%
echo.

REM Test Python installation
echo Testing Python installation...
%PYTHON_EXE% --version
if errorlevel 1 (
    echo ERROR: Python executable is not working properly
    pause
    exit /b 1
)

echo.
echo ============================================================
echo LAUNCHING ITERUM R&D CHEF NOTEBOOK
echo ============================================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the launcher
%PYTHON_EXE% launch-notebook.py

REM Check if launcher failed
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo ERROR: Launcher failed with exit code %errorlevel%
    echo ============================================================
    echo.
    echo Troubleshooting steps:
    echo 1. Make sure you're in the correct directory
    echo 2. Check that all required files are present
    echo 3. Verify Python and dependencies are installed
    echo 4. Try running: %PYTHON_EXE% -m pip install -r requirements.txt
    echo.
    pause
    exit /b %errorlevel%
)

echo.
echo ============================================================
echo ITERUM R&D CHEF NOTEBOOK LAUNCHER COMPLETED
echo ============================================================
pause 