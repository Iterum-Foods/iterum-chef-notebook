@echo off
echo ========================================
echo   USTA - Prepare Firebase Deployment
echo ========================================
echo.

echo Creating deployment directory...
mkdir usta-public 2>nul
mkdir usta-public\assets 2>nul

echo.
echo Copying main application files...
copy "Skills App\usta-landing-page.html" "usta-public\landing.html" >nul
copy "Skills App\usta-demo-app.html" "usta-public\demo.html" >nul
copy "Skills App\usta-onboarding.html" "usta-public\signup.html" >nul
copy "Skills App\usta-challenge-detail.html" "usta-public\challenge.html" >nul
copy "Skills App\usta-profile-professional.html" "usta-public\profile.html" >nul
copy "Skills App\usta-profile-full.html" "usta-public\profile-alt.html" >nul
copy "Skills App\usta-notifications.html" "usta-public\notifications.html" >nul

echo.
echo Copying investor materials...
copy "landing-pages\usta-app\index.html" "usta-public\index.html" >nul
copy "landing-pages\usta-app\usta-pitch-deck-web.html" "usta-public\pitch.html" >nul
copy "landing-pages\usta-app\USTA-EXECUTIVE-SUMMARY.md" "usta-public\" >nul
copy "landing-pages\usta-app\USTA-BUSINESS-PLAN.md" "usta-public\" >nul
copy "landing-pages\usta-app\USTA-TECH-ARCHITECTURE.md" "usta-public\" >nul
copy "landing-pages\usta-app\USTA-FINANCIAL-MODEL-GUIDE.md" "usta-public\" >nul
copy "landing-pages\usta-app\USTA-PRD.md" "usta-public\" >nul
copy "landing-pages\usta-app\USTA-CONTENT-STRATEGY.md" "usta-public\" >nul

echo.
echo Creating 404 page...
echo ^<!DOCTYPE html^> > "usta-public\404.html"
echo ^<html^>^<head^>^<title^>404 - Page Not Found^</title^>^</head^> >> "usta-public\404.html"
echo ^<body style="font-family: Arial; text-align: center; padding: 100px;"^> >> "usta-public\404.html"
echo ^<h1^>404 - Page Not Found^</h1^> >> "usta-public\404.html"
echo ^<p^>The page you're looking for doesn't exist.^</p^> >> "usta-public\404.html"
echo ^<a href="/"^>Go to Home^</a^> >> "usta-public\404.html"
echo ^</body^>^</html^> >> "usta-public\404.html"

echo.
echo ========================================
echo   Deployment Ready!
echo ========================================
echo.
echo Files prepared in: usta-public\
echo.
echo Next steps:
echo 1. Run: firebase login
echo 2. Run: firebase init hosting
echo 3. Run: firebase deploy --only hosting
echo.
echo Or use: DEPLOY-USTA-TO-FIREBASE.bat
echo.
pause

