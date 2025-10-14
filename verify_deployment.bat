@echo off
echo ========================================
echo ITERUM DEPLOYMENT VERIFICATION
echo ========================================
echo.

echo [1/6] Checking Main App Git Status...
cd "C:\Users\chefm\my-culinary-app\Iterum App"
git status
echo.

echo [2/6] Checking Landing Page Git Status...
cd "C:\Users\chefm\my-culinary-app\Iterumwebsite"
git status
echo.

echo [3/6] Checking Firebase Project...
cd "C:\Users\chefm\my-culinary-app\Iterum App"
firebase use
echo.

echo [4/6] Listing Hosting Sites...
firebase hosting:sites:list
echo.

echo [5/6] Checking Firestore Rules...
firebase firestore:rules
echo.

echo [6/6] Testing Live URLs...
echo Main App: https://iterum-culinary-app.web.app
echo Landing: https://iterum-landing.web.app
echo CRM: https://iterum-culinary-app.web.app/contact_management.html
echo.

echo ========================================
echo VERIFICATION COMPLETE
echo ========================================
echo.
echo Next Steps:
echo 1. Visit each URL above
echo 2. Test functionality
echo 3. Check browser console
echo 4. Verify no errors
echo.
pause

