@echo off
REM Web Recipe Scraper - Quick Launch
REM Scrapes recipes from websites and imports to library

title Web Recipe Scraper

echo.
echo ========================================
echo    WEB RECIPE SCRAPER
echo ========================================
echo.
echo This tool scrapes recipes from websites
echo and imports them into your recipe library.
echo.

python web_recipe_scraper.py %*

if errorlevel 1 (
    echo.
    echo ERROR: Scraping failed!
    echo.
    pause
)

