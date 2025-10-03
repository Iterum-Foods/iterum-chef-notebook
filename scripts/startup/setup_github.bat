@echo off
title Iterum R^&D GitHub Setup
color 0A

echo.
echo 🍅 ITERUM R^&D GITHUB SETUP GUIDE
echo =======================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed on your system.
    echo.
    echo 📥 STEP 1: Install Git
    echo -------------------------
    echo 1. Go to: https://git-scm.com/download/windows
    echo 2. Download and install Git for Windows
    echo 3. During installation, choose these options:
    echo    - Use Git from Git Bash only ^(default^)
    echo    - Use the OpenSSL library
    echo    - Checkout Windows-style, commit Unix-style line endings
    echo    - Use MinTTY ^(the default terminal of MSYS2^)
    echo 4. Restart this script after installation
    echo.
    echo 🌐 Opening Git download page...
    start https://git-scm.com/download/windows
    echo.
    pause
    exit /b 1
)

echo ✅ Git is installed!
echo.

echo 📋 GITHUB SETUP CHECKLIST
echo ===========================
echo.
echo Before we start, make sure you have:
echo ✓ A GitHub account ^(sign up at github.com^)
echo ✓ Git installed ^(we just checked this^)
echo ✓ Your GitHub username and email ready
echo.
echo 🔧 AUTOMATIC SETUP STEPS
echo =========================
echo.

REM Configure Git (user will need to edit these)
echo 📝 Setting up Git configuration...
echo.
echo Enter your GitHub username:
set /p GITHUB_USERNAME=
echo Enter your GitHub email:
set /p GITHUB_EMAIL=

git config --global user.name "%GITHUB_USERNAME%"
git config --global user.email "%GITHUB_EMAIL%"

echo ✅ Git configured with:
echo    Name: %GITHUB_USERNAME%
echo    Email: %GITHUB_EMAIL%
echo.

REM Initialize repository
echo 🚀 Initializing Git repository...
git init
echo ✅ Repository initialized
echo.

REM Add files
echo 📁 Adding files to repository...
git add .
echo ✅ Files added
echo.

REM Create initial commit
echo 💾 Creating initial commit...
git commit -m "Initial commit: Iterum R&D Chef Notebook v2.0"
echo ✅ Initial commit created
echo.

echo 🌐 GITHUB REPOSITORY SETUP
echo ============================
echo.
echo Now you need to create a GitHub repository:
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: iterum-chef-notebook
echo 3. Description: Revolutionary culinary management platform for professional kitchens
echo 4. Set to Public ^(or Private if you prefer^)
echo 5. Do NOT initialize with README ^(we already have one^)
echo 6. Click "Create repository"
echo.
echo 🌐 Opening GitHub new repository page...
start https://github.com/new
echo.
echo Press any key after you've created the repository...
pause

echo.
echo 📤 PUSHING TO GITHUB
echo ====================
echo.
echo Enter your GitHub repository URL ^(e.g., https://github.com/username/iterum-chef-notebook.git^):
set /p REPO_URL=

echo 🔗 Adding remote origin...
git remote add origin %REPO_URL%

echo 📤 Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ⚠️  Push failed. This might be due to authentication.
    echo.
    echo 🔐 AUTHENTICATION OPTIONS:
    echo ============================
    echo.
    echo Option 1: Personal Access Token ^(Recommended^)
    echo ------------------------------------------------
    echo 1. Go to: https://github.com/settings/tokens
    echo 2. Click "Generate new token" ^> "Generate new token ^(classic^)"
    echo 3. Select scopes: repo, workflow
    echo 4. Copy the token
    echo 5. When prompted for password, use the token instead
    echo.
    echo Option 2: GitHub CLI
    echo --------------------
    echo 1. Install GitHub CLI from: https://cli.github.com/
    echo 2. Run: gh auth login
    echo 3. Follow the prompts
    echo.
    echo 🌐 Opening GitHub token page...
    start https://github.com/settings/tokens
    echo.
    echo After setting up authentication, run:
    echo git push -u origin main
    echo.
) else (
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo 🎉 SETUP COMPLETE!
    echo ==================
    echo.
    echo Your Iterum R^&D Chef Notebook is now on GitHub!
    echo Repository URL: %REPO_URL%
    echo.
    echo 📋 NEXT STEPS:
    echo ==============
    echo 1. Add a star to your repository
    echo 2. Set up GitHub Pages for the marketing site
    echo 3. Configure branch protection rules
    echo 4. Add collaborators if needed
    echo 5. Set up GitHub Actions for CI/CD
    echo.
    echo 🌐 Opening your repository...
    start %REPO_URL%
)

echo.
echo 📚 ADDITIONAL SETUP ^(OPTIONAL^)
echo ================================
echo.
echo GitHub Pages Setup:
echo 1. Go to repository Settings ^> Pages
echo 2. Source: Deploy from branch
echo 3. Branch: main / ^(root^)
echo 4. Your site will be available at: https://username.github.io/iterum-chef-notebook/
echo.
echo Repository Settings:
echo 1. Add repository description and tags
echo 2. Set up branch protection for main
echo 3. Configure issue templates
echo 4. Add repository topics: chef, cooking, recipe-management, fastapi, python
echo.
pause