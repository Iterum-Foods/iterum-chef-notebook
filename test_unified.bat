@echo off
REM Unified test script for Iterum R&D Chef Notebook
REM Combines quick, full, and CI testing modes in one script

echo =====================================
echo   Iterum R&D Chef Notebook
echo   Unified Test Suite
echo =====================================
echo.

REM Parse command line arguments
set TEST_MODE=interactive
set VERBOSE=
set NO_PAUSE=

:parse_args
if "%~1"=="" goto :end_args
if "%~1"=="--quick" set TEST_MODE=quick
if "%~1"=="--full" set TEST_MODE=full
if "%~1"=="--ci" set TEST_MODE=ci
if "%~1"=="--verbose" set VERBOSE=--verbose
if "%~1"=="--no-pause" set NO_PAUSE=1
shift
goto :parse_args
:end_args

REM If no mode specified, show menu
if "%TEST_MODE%"=="interactive" goto :show_menu

REM Jump to appropriate test mode
if "%TEST_MODE%"=="quick" goto :quick_test
if "%TEST_MODE%"=="full" goto :full_test
if "%TEST_MODE%"=="ci" goto :ci_test

:show_menu
echo Select test mode:
echo.
echo 1. Quick Test    - Essential tests only (fastest)
echo 2. Full Test     - Complete test suite with coverage
echo 3. CI Test       - Automated testing mode
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto :quick_test
if "%choice%"=="2" goto :full_test
if "%choice%"=="3" goto :ci_test
if "%choice%"=="4" goto :exit
echo Invalid choice. Please select 1-4.
goto :show_menu

:quick_test
echo.
echo Running Quick Test Suite...
echo ============================
echo.
goto :setup_environment

:full_test
echo.
echo Running Full Test Suite...
echo ===========================
echo This may take several minutes...
echo.
goto :setup_environment

:ci_test
echo.
echo Running CI Test Suite...
echo =========================
set CI=1
set PYTHONPATH=%CD%
set NO_PAUSE=1
goto :setup_environment

:setup_environment
REM Use shared Python detection module
set PYTHON_DETECTION_VERBOSE=1
call python_detection.bat
if %errorlevel% neq 0 (
    if not "%NO_PAUSE%"=="1" pause
    exit /b 1
)

REM Handle virtual environment for non-CI modes
if not "%TEST_MODE%"=="ci" (
    if not exist "venv\Scripts\activate.bat" (
        echo Warning: Virtual environment not found at venv\
        echo Creating virtual environment...
        %PYTHON_EXE% -m venv venv
        call venv\Scripts\activate.bat
        echo Installing dependencies...
        %PYTHON_EXE% -m pip install -r requirements.txt
    ) else (
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    )
) else (
    REM CI mode - install dependencies directly
    echo Installing Python dependencies...
    %PYTHON_EXE% -m pip install --no-cache-dir -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Python dependencies
        exit /b 1
    )
)

REM Check Node.js for full and CI tests
if "%TEST_MODE%"=="full" or "%TEST_MODE%"=="ci" (
    node --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Installing Node.js dependencies...
        if "%TEST_MODE%"=="ci" (
            npm ci --silent
        ) else (
            npm install
        )
        if %errorlevel% neq 0 (
            echo WARNING: Failed to install Node.js dependencies
        )
    ) else (
        echo WARNING: Node.js not found. Frontend tests will be skipped.
    )
)

goto :run_tests

:run_tests
echo.
echo Starting tests...
echo.

REM Run appropriate test suite based on mode
if "%TEST_MODE%"=="quick" (
    %PYTHON_EXE% run_tests.py --type fast --skip-lint --skip-perf %VERBOSE%
) else if "%TEST_MODE%"=="full" (
    %PYTHON_EXE% run_tests.py --type all %VERBOSE%
) else if "%TEST_MODE%"=="ci" (
    %PYTHON_EXE% run_tests.py --type all %VERBOSE% --no-cleanup
)

REM Handle test results
set TEST_RESULT=%errorlevel%
goto :show_results

:show_results
echo.
if %TEST_RESULT% equ 0 (
    echo =====================================
    echo   Tests completed successfully!
    echo =====================================
    echo.
    
    if "%TEST_MODE%"=="quick" (
        echo To run full test suite: %~nx0 --full
        echo To run in CI mode: %~nx0 --ci
    ) else if "%TEST_MODE%"=="full" (
        echo Test coverage report available at:
        echo   test_coverage\python\index.html
        echo   test_coverage\frontend\index.html
        echo.
        echo Opening coverage report...
        if exist "test_coverage\python\index.html" (
            start test_coverage\python\index.html
        )
    ) else if "%TEST_MODE%"=="ci" (
        echo SUCCESS: All tests passed
        exit /b 0
    )
) else (
    echo =====================================
    echo   Some tests failed!
    echo =====================================
    echo.
    
    if "%TEST_MODE%"=="quick" (
        echo Run full test suite for detailed analysis: %~nx0 --full
    ) else if "%TEST_MODE%"=="full" (
        echo Check detailed report at: test_coverage\test_report.json
        echo For quick testing: %~nx0 --quick
    ) else if "%TEST_MODE%"=="ci" (
        echo FAILURE: Some tests failed
        exit /b 1
    )
)

echo.
echo Usage examples:
echo   %~nx0                 - Interactive menu
echo   %~nx0 --quick         - Quick tests only
echo   %~nx0 --full          - Complete test suite
echo   %~nx0 --ci            - CI/CD mode
echo   %~nx0 --quick --verbose  - Quick tests with verbose output
echo.

:exit
if not "%NO_PAUSE%"=="1" pause
exit /b %TEST_RESULT% 