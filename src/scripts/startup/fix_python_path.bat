@echo off
echo ============================================================
echo FIX PYTHON PATH - Iterum R&D Chef Notebook
echo ============================================================
echo.
echo This script will help fix Python path issues on Windows.
echo.

echo Step 1: Disable Microsoft Store Python aliases
echo ----------------------------------------------
echo Please follow these steps manually:
echo.
echo 1. Press Windows + I to open Settings
echo 2. Go to Apps ^> Advanced app settings ^> App execution aliases
echo 3. Find "python.exe" and "python3.exe" entries
echo 4. Turn OFF both toggles for Python entries
echo 5. Close Settings and restart this script
echo.
echo OR you can continue and we'll use the full path to Python
echo.
pause

echo.
echo Step 2: Test Python installation
echo ---------------------------------

REM Try to find Python in common locations
set PYTHON_EXE=
if exist "venv\Scripts\python.exe" (
    set PYTHON_EXE=venv\Scripts\python.exe
    echo Found Python in virtual environment: %PYTHON_EXE%
    goto :test_python
)

if exist "C:\Python313\python.exe" (
    set PYTHON_EXE=C:\Python313\python.exe
    echo Found Python at: %PYTHON_EXE%
    goto :test_python
)

if exist "C:\Program Files\Python313\python.exe" (
    set PYTHON_EXE=C:\Program Files\Python313\python.exe
    echo Found Python at: %PYTHON_EXE%
    goto :test_python
)

echo Searching for Python installations...
for /d %%i in ("C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        set PYTHON_EXE=%%i\python.exe
        echo Found Python at: %%i\python.exe
        goto :test_python
    )
)

echo ERROR: Could not find Python installation
echo Please install Python from https://python.org/downloads
pause
exit /b 1

:test_python
echo.
echo Testing Python installation...
"%PYTHON_EXE%" --version
if errorlevel 1 (
    echo ERROR: Python executable is not working properly
    pause
    exit /b 1
)

echo.
echo SUCCESS: Python is working!
echo.
echo Creating fixed batch files...

REM Create fixed test scripts
echo @echo off > test_quick_fixed.bat
echo echo Running Quick Tests with Fixed Python Path... >> test_quick_fixed.bat
echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat >> test_quick_fixed.bat
echo "%PYTHON_EXE%" run_tests.py --type fast --skip-lint --skip-perf --verbose >> test_quick_fixed.bat
echo pause >> test_quick_fixed.bat

echo @echo off > test_full_fixed.bat
echo echo Running Full Tests with Fixed Python Path... >> test_full_fixed.bat
echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat >> test_full_fixed.bat
echo "%PYTHON_EXE%" -m pip install -r requirements.txt --quiet >> test_full_fixed.bat
echo "%PYTHON_EXE%" run_tests.py --type all --verbose >> test_full_fixed.bat
echo pause >> test_full_fixed.bat

echo @echo off > clear_users_fixed.bat
echo echo Clearing Users with Fixed Python Path... >> clear_users_fixed.bat
echo if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat >> clear_users_fixed.bat
echo "%PYTHON_EXE%" clear_users.py >> clear_users_fixed.bat
echo pause >> clear_users_fixed.bat

echo.
echo Created fixed batch files:
echo - test_quick_fixed.bat
echo - test_full_fixed.bat  
echo - clear_users_fixed.bat
echo.
echo These files use the full path to Python and should work correctly.
echo.
pause 