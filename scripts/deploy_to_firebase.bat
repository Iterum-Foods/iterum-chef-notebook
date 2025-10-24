@echo off
echo.
echo ========================================
echo   Firebase Deployment Script
echo   Iterum Culinary App
echo ========================================
echo.

REM Change to project directory
cd /d "%~dp0"

echo Step 1: Checking Firebase CLI...
firebase --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Firebase CLI not found!
    echo Please install: npm install -g firebase-tools
    pause
    exit /b 1
)
echo   Firebase CLI found!
echo.

echo Step 2: Checking authentication...
firebase projects:list >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not authenticated with Firebase
    echo.
    echo Please run this command first:
    echo   firebase login --reauth
    echo.
    pause
    exit /b 1
)
echo   Authenticated!
echo.

echo Step 3: Setting active project...
firebase use iterum-culinary-app
if errorlevel 1 (
    echo ERROR: Could not set project
    pause
    exit /b 1
)
echo.

echo Step 4: Deploying to Firebase Hosting...
echo This may take a few minutes...
echo.
firebase deploy --only hosting
if errorlevel 1 (
    echo.
    echo ERROR: Deployment failed!
    echo Check the errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Your app is now live at:
echo   https://iterum-culinary-app.web.app
echo.
echo Next steps:
echo   1. Test the live site in incognito mode
echo   2. Sign in and verify everything works
echo   3. Check console for any errors
echo.
pause

