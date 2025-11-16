@echo off
REM Full test script for Iterum R&D Chef Notebook
REM Runs comprehensive test suite including linting and performance tests

echo =====================================
echo   Iterum R&D Chef Notebook
echo   Full Test Suite
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

REM Check if Node.js is available for frontend tests
echo Checking for Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Node.js found. Installing npm dependencies...
    npm install
) else (
    echo Warning: Node.js not found. Frontend tests will be skipped.
)

echo.
echo Running full test suite...
echo This may take several minutes...
echo.

REM Run full test suite
python run_tests.py --type all --verbose

REM Check test results
if %errorlevel% equ 0 (
    echo.
    echo =====================================
    echo   All tests completed successfully!
    echo =====================================
    echo.
    echo Test coverage report available at:
    echo   test_coverage\python\index.html
    echo   test_coverage\frontend\index.html
    echo.
    echo Full test report available at:
    echo   test_coverage\test_report.json
    echo.
) else (
    echo.
    echo =====================================
    echo   Some tests failed!
    echo =====================================
    echo.
    echo Check the detailed report at:
    echo   test_coverage\test_report.json
    echo.
    echo For quick testing without linting:
    echo   test_quick.bat
    echo.
)

echo Opening test coverage report...
if exist "test_coverage\python\index.html" (
    start test_coverage\python\index.html
)

pause 