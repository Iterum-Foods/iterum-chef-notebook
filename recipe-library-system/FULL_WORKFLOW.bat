@echo off
REM Complete Workflow: Organize, Convert, and Prepare for Iterum

title Complete Recipe Workflow

echo ============================================================
echo           COMPLETE RECIPE WORKFLOW
echo ============================================================
echo.
echo This will:
echo   1. Scan and organize recipes into library
echo   2. Convert to standardized Iterum format
echo   3. Prepare for upload to Chef's Notebook
echo.
echo ============================================================
pause

echo.
echo Step 1: Organizing recipes into library...
echo ============================================================
py organize_recipes.py

echo.
echo Step 2: Converting to Iterum format...
echo ============================================================
py standardize_recipes.py

echo.
echo ============================================================
echo           WORKFLOW COMPLETE!
echo ============================================================
echo.
echo Your recipes are now:
echo   - Organized in: recipe_library/
echo   - Standardized in: converted_iterum/
echo   - Ready for Iterum Chef's Notebook
echo.
echo ============================================================
pause

