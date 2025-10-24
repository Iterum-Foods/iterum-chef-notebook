@echo off
REM Upload all recipes to Google Drive

title Upload All Recipes to Google Drive

echo ============================================================
echo           UPLOADING ALL RECIPES TO GOOGLE DRIVE
echo ============================================================
echo.

py -c "from google_drive_integration import GoogleDriveRecipeManager; manager = GoogleDriveRecipeManager(); manager.upload_all_recipes()"

echo.
echo ============================================================
pause

