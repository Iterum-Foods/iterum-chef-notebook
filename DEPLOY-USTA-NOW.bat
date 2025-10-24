@echo off
echo ========================================
echo   DEPLOY USTA TO FIREBASE
echo   Project: usta-app-a86db
echo ========================================
echo.

echo Step 1: Switching to usta-app project...
firebase use usta-app-a86db

echo.
echo Step 2: Deploying to Firebase...
firebase deploy --only hosting --public usta-public

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo   DEPLOYMENT SUCCESSFUL!
    echo ========================================
    echo.
    echo Your Usta site is now LIVE at:
    echo https://usta-app-a86db.web.app
    echo.
    echo URLs:
    echo - Investor Hub: https://usta-app-a86db.web.app/
    echo - Pitch Deck:   https://usta-app-a86db.web.app/pitch
    echo - Live Demo:    https://usta-app-a86db.web.app/demo
    echo - Landing Page: https://usta-app-a86db.web.app/landing
    echo - Sign Up:      https://usta-app-a86db.web.app/signup
    echo - Profile:      https://usta-app-a86db.web.app/profile
    echo.
    echo Ready to share with investors!
    echo.
) else (
    echo ========================================
    echo   DEPLOYMENT FAILED
    echo ========================================
    echo.
    echo Try: firebase login --reauth
    echo.
)

pause

