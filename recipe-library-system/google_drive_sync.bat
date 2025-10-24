@echo off
REM Sync recipes to Google Drive

title Sync to Google Drive

echo ============================================================
echo           SYNCING RECIPES TO GOOGLE DRIVE
echo ============================================================
echo.

py -c "from google_drive_integration import GoogleDriveRecipeManager; manager = GoogleDriveRecipeManager(); manager.sync_to_drive()"

echo.
echo ============================================================
pause

