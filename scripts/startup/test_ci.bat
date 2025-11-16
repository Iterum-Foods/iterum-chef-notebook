@echo off
REM CI/CD test script for Iterum R&D Chef Notebook
REM Designed for automated testing environments

echo =====================================
echo   Iterum R&D Chef Notebook
echo   CI/CD Test Suite
echo =====================================

REM Set CI environment variable
set CI=1
set PYTHONPATH=%CD%

REM Check Python version
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not available
    exit /b 1
)

REM Install dependencies
echo Installing Python dependencies...
pip install --no-cache-dir -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    exit /b 1
)

REM Check if npm is available
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing Node.js dependencies...
    npm ci --silent
    if %errorlevel% neq 0 (
        echo WARNING: Failed to install Node.js dependencies
    )
) else (
    echo WARNING: Node.js not available, skipping frontend tests
)

REM Run tests with CI-specific settings
echo.
echo Running CI test suite...
python run_tests.py --type all --verbose --no-cleanup

REM Set exit code based on test results
if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: All tests passed
    exit /b 0
) else (
    echo.
    echo FAILURE: Some tests failed
    exit /b 1
) 