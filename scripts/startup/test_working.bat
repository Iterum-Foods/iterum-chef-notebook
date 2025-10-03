@echo off
echo ============================================================
echo ITERUM R&D CHEF NOTEBOOK - TESTING SUITE
echo ============================================================
echo.

set PYTHON_EXE="C:\Users\chefm\AppData\Local\Programs\Python\Python313\python.exe"

echo Using Python: %PYTHON_EXE%
%PYTHON_EXE% --version
echo.

echo Installing dependencies...
%PYTHON_EXE% -m pip install -r requirements.txt --quiet

echo.
echo ============================================================
echo RUNNING COMPREHENSIVE TEST SUITE
echo ============================================================
echo.

echo Running Python tests with coverage...
%PYTHON_EXE% run_tests.py --type python --verbose

echo.
echo ============================================================
echo TEST COMPLETE
echo ============================================================
pause 