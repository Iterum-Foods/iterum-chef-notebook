@echo off
REM Quick Recipe Scanner - Scan any folder for recipe files

echo ============================================
echo        Recipe Folder Scanner
echo ============================================
echo.

set /p folder="Enter folder path to scan: "

if not exist "%folder%" (
    echo ERROR: Folder not found!
    pause
    exit /b
)

py scan_any_folder.py "%folder%"

echo.
echo ============================================
pause

