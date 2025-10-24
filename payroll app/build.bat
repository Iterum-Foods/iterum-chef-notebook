@echo off
echo ========================================
echo    Professional Payroll System Builder
echo ========================================
echo.

echo Installing dependencies...
py -3 -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Building executable...
py -3 build_app.py
if %errorlevel% neq 0 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo Your executable is in: dist\PayrollApp\
echo ========================================
pause
