@echo off
echo ========================================
echo   USTA - Quick Firebase Setup
echo ========================================
echo.
echo This will guide you through setting up Firebase Hosting
echo.
pause

echo.
echo Step 1: Checking Firebase CLI...
firebase --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Firebase CLI not found!
    echo.
    echo Installing Firebase CLI...
    npm install -g firebase-tools
    echo.
) else (
    echo Firebase CLI is installed!
)

echo.
echo Step 2: Logging in to Firebase...
echo (This will open your browser)
echo.
pause
firebase login

echo.
echo Step 3: Initializing Firebase Hosting...
echo.
echo When prompted:
echo   - Choose: Use an existing project
echo   - Select: usta-app (or create new)
echo   - Public directory: usta-public
echo   - Single-page app: Yes
echo   - GitHub auto-deploy: No
echo.
pause

firebase init hosting --config firebase-usta.json

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next step: Run DEPLOY-USTA-TO-FIREBASE.bat
echo.
pause

