@echo off
REM Vendor Price Importer - Quick Launch
REM Import vendor price lists from Excel files

title Vendor Price Importer

echo.
echo ========================================
echo    VENDOR PRICE IMPORTER
echo ========================================
echo.
echo Import vendor price lists from Excel files
echo and automatically update ingredient costs.
echo.

python vendor_price_importer.py %*

if errorlevel 1 (
    echo.
    echo ERROR: Import failed!
    echo.
    pause
)

