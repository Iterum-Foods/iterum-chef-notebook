@echo off
echo ========================================
echo   USTA - Deploy to Firebase
echo ========================================
echo.

echo Step 1: Preparing deployment files...
call PREPARE-USTA-DEPLOYMENT.bat

echo.
echo ========================================
echo Step 2: Deploying to Firebase...
echo ========================================
echo.

firebase deploy --only hosting --config firebase-usta.json

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo   Deployment Successful!
    echo ========================================
    echo.
    echo Your Usta app is now live!
    echo.
    echo Check your Firebase Console for the URL:
    echo https://console.firebase.google.com
    echo.
    echo Typical URL: https://usta-app.web.app
    echo.
) else (
    echo ========================================
    echo   Deployment Failed
    echo ========================================
    echo.
    echo Possible issues:
    echo - Not logged in: Run 'firebase login'
    echo - No project: Run 'firebase init hosting'
    echo - Check internet connection
    echo.
)

pause

