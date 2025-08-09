@echo off
echo 🌟 Opening Iterum R&D Chef Notebook Frontend
echo ============================================

:: Check if we're in the correct directory
if not exist "index.html" (
    echo ❌ Error: Please run this from the Iterum App directory
    echo Current directory: %CD%
    echo Expected file: index.html
    pause
    exit /b 1
)

echo 🚀 Opening main application (with 3-second loading screen)...
start index.html

echo ⏰ Opening 3-second loading screen demo...
start LOADING_SCREEN_DEMO.html

echo 🧪 Opening project creation demo...
start PROJECT_MODAL_DEMO.html

echo 🔬 Opening project UI test page...
start PROJECT_UI_TEST.html

echo.
echo ✅ Frontend pages opened in your default browser
echo.
echo 📋 Available Pages:
echo   - Main App: index.html (NEW: 3-second loading!)
echo   - Loading Demo: LOADING_SCREEN_DEMO.html (NEW!)
echo   - Project Demo: PROJECT_MODAL_DEMO.html  
echo   - Project Test: PROJECT_UI_TEST.html
echo   - Recipe Library: recipe-library.html
echo.
echo ⏰ NEW: Loading screen now shows for 3 seconds by default
echo 💡 Make sure the backend server is running (use START_SERVERS.bat)
echo.

pause