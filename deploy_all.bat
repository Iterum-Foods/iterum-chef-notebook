@echo off
echo ========================================
echo ITERUM COMPLETE DEPLOYMENT SCRIPT
echo ========================================
echo.

echo This will:
echo - Commit and push both repositories
echo - Deploy main app to Firebase
echo - Deploy landing page to Firebase
echo - Deploy Firestore rules
echo.
set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Deployment cancelled.
    exit /b
)

echo.
echo [1/8] Committing Main App...
cd "C:\Users\chefm\my-culinary-app\Iterum App"
git add .
git status
set /p message="Enter commit message for main app: "
git commit -m "%message%"
if errorlevel 1 (
    echo No changes to commit in main app
) else (
    echo Pushing to GitHub...
    git push origin main
)
echo.

echo [2/8] Committing Landing Page...
cd "C:\Users\chefm\my-culinary-app\Iterumwebsite"
git add .
git status
set /p landingmessage="Enter commit message for landing (or press Enter for same): "
if "%landingmessage%"=="" set landingmessage=%message%
git commit -m "%landingmessage%"
if errorlevel 1 (
    echo No changes to commit in landing page
) else (
    echo Pushing to GitHub...
    git push origin main
)
echo.

echo [3/8] Switching to Main App...
cd "C:\Users\chefm\my-culinary-app\Iterum App"
firebase use iterum-culinary-app
echo.

echo [4/8] Deploying Firestore Rules...
set /p deployrules="Deploy Firestore rules? (Y/N): "
if /i "%deployrules%"=="Y" (
    firebase deploy --only "firestore:rules"
    echo Firestore rules deployed!
) else (
    echo Skipping Firestore rules
)
echo.

echo [5/8] Deploying Main App Hosting...
firebase deploy --only hosting
echo Main app deployed!
echo.

echo [6/8] Deploying Landing Page...
cd "C:\Users\chefm\my-culinary-app\Iterumwebsite"
firebase deploy --only hosting:landing
echo Landing page deployed!
echo.

echo [7/8] Deployment Summary...
echo.
echo Main App: https://iterum-culinary-app.web.app
echo Landing: https://iterum-landing.web.app
echo CRM: https://iterum-culinary-app.web.app/contact_management.html
echo.

echo [8/8] Testing URLs...
echo Opening main app in browser...
start https://iterum-culinary-app.web.app
timeout /t 2 /nobreak >nul
echo Opening landing page in browser...
start https://iterum-landing.web.app
echo.

echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Please verify:
echo 1. Main app loads correctly
echo 2. Landing page loads correctly
echo 3. No console errors
echo 4. Test login/signup
echo 5. Test waitlist signup
echo.
pause

