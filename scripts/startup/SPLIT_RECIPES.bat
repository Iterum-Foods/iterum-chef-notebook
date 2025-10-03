@echo off
echo ===============================================
echo      Recipe Splitter - Multiple to Individual
echo ===============================================
echo.

REM Change to project root
cd /d "%~dp0\..\..\"

REM Activate virtual environment
call venv\Scripts\activate.bat

echo This tool will split a Word document with multiple recipes
echo into individual recipe files.
echo.

REM Get input file from user
set /p INPUT_FILE="Enter path to Word document: "

REM Check if file exists
if not exist "%INPUT_FILE%" (
    echo ERROR: File not found: %INPUT_FILE%
    pause
    exit /b 1
)

echo.
echo Processing: %INPUT_FILE%
echo.

REM First run in preview mode
echo Running preview to show what recipes will be extracted...
echo.
py scripts\recipe_splitter.py "%INPUT_FILE%" --preview

echo.
set /p CONTINUE="Continue with extraction? (y/n): "

if /i "%CONTINUE%"=="y" (
    echo.
    echo Extracting recipes...
    py scripts\recipe_splitter.py "%INPUT_FILE%"
    echo.
    echo Done! Check the output directory for individual recipe files.
) else (
    echo.
    echo Extraction cancelled.
)

echo.
pause
