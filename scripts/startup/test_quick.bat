@echo off
REM Quick test script for Iterum R&D Chef Notebook
REM Runs essential tests without full linting and performance testing

echo =====================================
echo   Iterum R&D Chef Notebook
echo   Quick Test Suite
echo =====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python and add it to PATH.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Warning: Virtual environment not found at venv\
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo Running quick tests...
echo.

REM Run quick Python tests (skip slow tests)
python run_tests.py --type fast --skip-lint --skip-perf --verbose

REM Check test results
if %errorlevel% equ 0 (
    echo.
    echo =====================================
    echo   Quick tests completed successfully!
    echo =====================================
    echo.
    echo To run full test suite:
    echo   test_full.bat
    echo.
    echo To run specific test types:
    echo   python run_tests.py --type unit
    echo   python run_tests.py --type integration
    echo   python run_tests.py --type auth
    echo.
) else (
    echo.
    echo =====================================
    echo   Some tests failed!
    echo =====================================
    echo.
    echo Check the output above for details.
    echo Run 'python run_tests.py --verbose' for more information.
    echo.
)

pause 