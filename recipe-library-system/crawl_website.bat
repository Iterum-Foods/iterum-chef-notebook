@echo off
REM Website Recipe Crawler - Quick Launch
REM Crawls entire websites to find and extract all recipes

title Website Recipe Crawler

echo.
echo ========================================
echo    WEBSITE RECIPE CRAWLER
echo ========================================
echo.
echo This tool crawls entire websites to find
echo all recipe pages and exports them to JSON or PDF.
echo.

python website_recipe_crawler.py %*

if errorlevel 1 (
    echo.
    echo ERROR: Crawling failed!
    echo.
    pause
)

