# 🐙 GitHub Setup & Deployment Guide

## Step-by-Step Guide to Get Your Code on GitHub

---

## ✅ Prerequisites

You need a GitHub account. If you don't have one:
1. Go to https://github.com/signup
2. Sign up (takes 2 minutes)
3. Verify your email

---

## 🎯 Option A: GitHub Desktop (EASIEST) ⭐

### Step 1: Install GitHub Desktop

1. Download: https://desktop.github.com/
2. Install and open
3. Sign in with your GitHub account

### Step 2: Create Repository

1. In GitHub Desktop, click **"File"** → **"New Repository"**
2. Fill in:
   - **Name:** `usta-backend`
   - **Description:** `Backend API for Usta - Community platform for craftspeople`
   - **Local Path:** Click "Choose..." and select:
     ```
     C:\Users\chefm\Iterum Innovation\Skills App
     ```
   - **Git Ignore:** Python
   - **License:** MIT License (optional)
3. Click **"Create Repository"**

### Step 3: Review Files

GitHub Desktop will show all files to be committed.

**Should see:**
- ✅ backend/ folder (all Python files)
- ✅ Dockerfile
- ✅ railway.json
- ✅ requirements-usta.txt
- ✅ README.md
- ✅ .gitignore

**Should NOT see:**
- ❌ *.db files
- ❌ __pycache__/
- ❌ venv/
- ❌ .env files
- ❌ *.bat files

If you see unwanted files, they'll be filtered by .gitignore on commit.

### Step 4: Make First Commit

1. In GitHub Desktop, bottom left:
2. **Summary:** `Initial commit - Usta backend ready for deployment`
3. **Description (optional):** 
   ```
   - Flask backend with JWT auth
   - PostgreSQL database models
   - Video upload & validation
   - Challenge system
   - XP & leveling
   - Ready for Railway deployment
   ```
4. Click **"Commit to main"**

### Step 5: Publish to GitHub

1. Click **"Publish repository"** button at top
2. Dialog appears:
   - **Name:** usta-backend (already filled)
   - **Description:** Backend API for Usta (already filled)
   - **Keep this code private:** ✅ Check this (recommended)
   - **Organization:** None (your personal account)
3. Click **"Publish Repository"**

### Step 6: Verify on GitHub

1. In GitHub Desktop, click **"View on GitHub"** button
2. Your browser opens to your new repository
3. You should see all your files!

✅ **DONE! Code is on GitHub!**

---

## 🎯 Option B: Git Command Line

### Step 1: Check Git Installation

```powershell
git --version
```

If not installed, download: https://git-scm.com/download/win

### Step 2: Configure Git

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Navigate to Project

```powershell
cd "C:\Users\chefm\Iterum Innovation\Skills App"
```

### Step 4: Initialize Git

```powershell
git init
```

### Step 5: Add Files

```powershell
git add .
```

### Step 6: Commit

```powershell
git commit -m "Initial commit - Usta backend ready for deployment"
```

### Step 7: Create GitHub Repository

**Option 1: Using GitHub CLI (if installed)**
```powershell
gh auth login
gh repo create usta-backend --private --source=. --push
```

**Option 2: Using Web**
1. Go to https://github.com/new
2. Repository name: `usta-backend`
3. Description: `Backend API for Usta`
4. Private repository: ✅ Yes
5. Don't initialize with README (we already have one)
6. Click **"Create repository"**

### Step 8: Connect and Push

GitHub will show you commands. Copy and run them:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/usta-backend.git
git branch -M main
git push -u origin main
```

✅ **DONE! Code is on GitHub!**

---

## 🚂 Now Deploy to Railway

### Step 1: Create Railway Account

1. Go to https://railway.app/
2. Click **"Sign in with GitHub"**
3. Authorize Railway to access GitHub
4. ✅ Account created!

### Step 2: Create New Project

1. Railway Dashboard → Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select **"usta-backend"**
4. Railway automatically detects your Dockerfile!
5. Click **"Deploy Now"**

✅ Railway starts building!

### Step 3: Add Database

1. In Railway project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway creates database and connects it automatically!

✅ Database added!

### Step 4: Set Environment Variables

1. Click on your **backend service** (not the database)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**

**Add these one by one:**

```bash
FLASK_APP=backend/app_usta.py
FLASK_ENV=production
SECRET_KEY=GENERATE_RANDOM_KEY_HERE
JWT_SECRET_KEY=GENERATE_RANDOM_KEY_HERE
FRONTEND_URL=https://usta-app-a86db.web.app
MAX_CONTENT_LENGTH=524288000
UPLOAD_FOLDER=uploads
FIREBASE_STORAGE_BUCKET=usta-app-a86db.appspot.com
```

**To generate secure keys:**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Run this twice, once for each key.

4. Railway automatically redeploys after you add variables

### Step 5: Generate Domain

1. Still in your backend service, click **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**

You'll get a URL like:
```
https://usta-backend-production-xxxx.up.railway.app
```

**📋 COPY THIS URL!** You'll need it next.

### Step 6: Initialize Database

1. In Railway, click your backend service
2. Open the **"Deployments"** tab
3. Find the latest deployment, click **"View Logs"**
4. Click **"Open Shell"** or **"Terminal"** button

Run these commands:
```bash
python init_database.py
python backend/seed_data.py
```

✅ Database initialized with demo data!

### Step 7: Test Backend

Visit in your browser:
```
https://your-railway-url.up.railway.app/api/health
```

Should return:
```json
{
  "status": "ok",
  "message": "Usta API is running"
}
```

✅ **Backend is LIVE!**

---

## 🔥 Update Frontend with Backend URL

**Send me your Railway URL** and I'll:
1. Update `usta-public/js/usta-api.js` with your URL
2. Enable Firebase Storage (you'll do this in console)
3. Deploy frontend to Firebase
4. Test everything end-to-end

---

## 📊 Monitor Your Deployment

### Railway Dashboard

**View logs:**
1. Railway → Your Project → Backend Service
2. Click **"Deployments"** tab
3. Click latest deployment → **"View Logs"**

**Check metrics:**
1. Backend Service → **"Metrics"** tab
2. See CPU, memory, network usage

**Database stats:**
1. Click **"PostgreSQL"** service
2. See connection count, size, queries

### GitHub

**View repository:**
- https://github.com/YOUR_USERNAME/usta-backend

**Make updates:**
1. Edit code locally
2. Commit changes in GitHub Desktop (or CLI)
3. Push to GitHub
4. Railway automatically redeploys! 🎉

---

## 🔄 How to Update Your App

### Using GitHub Desktop:

1. Make changes to your code
2. GitHub Desktop shows changed files
3. Write commit message
4. Click **"Commit to main"**
5. Click **"Push origin"**
6. Railway automatically builds and deploys!

### Using Command Line:

```powershell
cd "C:\Users\chefm\Iterum Innovation\Skills App"
git add .
git commit -m "Description of changes"
git push
```

Railway auto-deploys in ~2-3 minutes!

---

## ✅ Success Checklist

After completing everything:

- ✅ Code on GitHub (private repository)
- ✅ Backend deployed to Railway
- ✅ PostgreSQL database running
- ✅ Environment variables set
- ✅ Domain generated
- ✅ Database initialized
- ✅ Demo data seeded
- ✅ Health check passes

**Next:** Send me your Railway URL so I can update the frontend!

---

## 💡 Tips

### Keep Your Code Updated

**Always commit and push after making changes!**

### Monitor Railway Usage

Free tier: 500 hours/month
- Check usage in Railway dashboard
- Plan shows remaining time
- Set up billing before running out (if needed)

### Secure Your Secrets

**NEVER commit to GitHub:**
- .env files
- Database files (*.db)
- API keys
- Firebase admin credentials

These are already in .gitignore!

### View Live Logs

While testing, keep Railway logs open to see:
- API requests
- Errors
- Database queries
- Performance issues

---

## 🐛 Troubleshooting

### "git: command not found"
Install Git: https://git-scm.com/download/win

### "GitHub CLI not found"
Install: https://cli.github.com/
Or use GitHub Desktop (easier!)

### "Permission denied"
In GitHub Desktop: File → Options → Sign in

### "Railway build failed"
1. Check Railway logs for errors
2. Verify Dockerfile is correct
3. Check requirements-usta.txt has all dependencies

### "Database connection failed"
1. Verify PostgreSQL service is running in Railway
2. Check DATABASE_URL is automatically set
3. Run init_database.py again

---

## 🎉 Ready to Start?

**Choose your method:**
- 🖱️ GitHub Desktop (easiest, recommended)
- 💻 Command Line (faster if you know git)

**Then follow the steps above!**

**When done, tell me:**
1. ✅ "Code is on GitHub"
2. ✅ "Deployed to Railway"
3. 📋 Send me your Railway URL

**And I'll finish the frontend connection!** 🚀

