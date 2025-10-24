# 🚀 Usta Full Launch - Deployment Guide

## Overview

This guide will take you through deploying Usta to production in ~1 hour.

**What we're deploying:**
- ✅ Frontend → Already on Firebase (`usta-app-a86db.web.app`)
- 🔧 Backend → Railway (free tier)
- 🔧 Database → PostgreSQL (included with Railway)
- 🔧 Storage → Firebase Storage (for videos)

**Total Cost:** $0 (free tiers)

---

## ✅ Pre-Deployment Checklist

**Files Created:**
- ✅ `Dockerfile` - Backend container configuration
- ✅ `railway.json` - Railway deployment settings
- ✅ `requirements-usta.txt` - Updated with production packages
- ✅ `.dockerignore` - Files to exclude from build
- ✅ `env.production` - Production environment template
- ✅ `usta-api.js` - Updated with production URL detection

**Your Backend is Ready to Deploy!** 🎉

---

## 🚂 Step 1: Deploy Backend to Railway (30 minutes)

### 1.1 Create Railway Account

1. Go to: https://railway.app/
2. Click **"Start a New Project"**
3. Sign up with **GitHub** (easiest for deployment)

✅ Free tier: 500 hours/month, $5 credit/month

---

### 1.2 Push Your Code to GitHub

**Option A: Use GitHub Desktop (Easiest)**
1. Download GitHub Desktop: https://desktop.github.com/
2. Open GitHub Desktop
3. Click **"Add"** → **"Create New Repository"**
4. Name: `usta-backend`
5. Local path: Browse to `C:\Users\chefm\Iterum Innovation\Skills App`
6. Click **"Create Repository"**
7. Click **"Publish repository"** to GitHub
8. Uncheck "Keep this code private" (or keep it private, Railway works either way)
9. Click **"Publish Repository"**

**Option B: Use Git Command Line**
```bash
cd "Skills App"
git init
git add .
git commit -m "Initial commit - Usta backend ready for deployment"
gh repo create usta-backend --public --source=. --push
```

---

### 1.3 Create Railway Project

1. Go to Railway dashboard: https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access GitHub (if first time)
5. Select **"usta-backend"** repository
6. Railway will detect the Dockerfile automatically!

✅ Railway starts building your backend!

---

### 1.4 Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway automatically connects it to your backend!

✅ Database created and linked!

---

### 1.5 Set Environment Variables

In Railway dashboard:

1. Click on your **backend service** (not the database)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**

**Add these variables:**

```bash
# Flask Configuration
FLASK_APP=backend/app_usta.py
FLASK_ENV=production

# Security Keys (IMPORTANT: Change these!)
SECRET_KEY=YOUR_RANDOM_SECRET_KEY_HERE_MAKE_IT_LONG_AND_RANDOM
JWT_SECRET_KEY=YOUR_JWT_SECRET_KEY_HERE_ALSO_LONG_AND_RANDOM

# Frontend URL (already deployed)
FRONTEND_URL=https://usta-app-a86db.web.app

# File Uploads
MAX_CONTENT_LENGTH=524288000
UPLOAD_FOLDER=uploads

# Firebase Storage
FIREBASE_STORAGE_BUCKET=usta-app-a86db.appspot.com
```

**To generate secure keys**, run this in PowerShell:
```powershell
# Secret Key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# JWT Secret Key  
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Copy the outputs and paste them into Railway!**

4. Click **"Add"** for each variable
5. Railway will automatically redeploy with new variables

---

### 1.6 Get Your Backend URL

1. In Railway, click on your backend service
2. Go to **"Settings"** tab
3. Scroll to **"Domains"**
4. Click **"Generate Domain"**

You'll get a URL like:
```
https://usta-backend-production-xxxx.up.railway.app
```

**Copy this URL!** We'll need it next.

---

### 1.7 Initialize Database

Railway needs to run migrations to set up the database schema.

**Option A: Railway Shell (Easiest)**
1. In Railway dashboard, click your backend service
2. Click the **"Shell"** tab (or **"Terminal"**)
3. Run these commands:

```bash
python
>>> from backend.app_usta import app, db
>>> with app.app_context():
...     db.create_all()
...     print("Database initialized!")
>>> exit()
```

**Option B: Add a startup script** (do this if Shell doesn't work)
I'll create a script that runs on startup.

---

### 1.8 Seed Demo Data

Still in the Railway shell:

```bash
python backend/seed_data.py
```

This adds:
- Demo users (chefs)
- Sample challenges (#KnifeSkills, #Plating, etc.)
- Sample videos

✅ **Backend is live and running!**

---

## 🔥 Step 2: Enable Firebase Storage (5 minutes)

### 2.1 Enable Storage in Firebase Console

1. Go to: https://console.firebase.google.com/project/usta-app-a86db/storage
2. Click **"Get Started"**
3. Select **"Start in production mode"**
4. Click **"Next"**
5. Choose location: **"us-central1"** (or your region)
6. Click **"Done"**

✅ Storage enabled!

---

### 2.2 Update Storage Rules

1. In Firebase Storage, click **"Rules"** tab
2. Replace everything with:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Videos - anyone can read, authenticated users can upload
    match /videos/{videoId} {
      allow read: if true;
      allow write: if request.auth != null
                   && request.resource.size < 500 * 1024 * 1024
                   && request.resource.contentType.matches('video/.*');
    }
    
    // Thumbnails  
    match /thumbnails/{thumbId} {
      allow read: if true;
      allow write: if request.auth != null
                   && request.resource.size < 5 * 1024 * 1024
                   && request.resource.contentType.matches('image/.*');
    }
  }
}
```

3. Click **"Publish"**

✅ Storage rules set!

---

### 2.3 Get Firebase Config

1. Click **⚙️** (gear icon) → **"Project settings"**
2. Scroll to **"Your apps"** section
3. You should see a Web app, or click **"Add app"** → **Web (</>)**
4. Copy the `firebaseConfig` object

It looks like:
```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "usta-app-a86db.firebaseapp.com",
  projectId: "usta-app-a86db",
  storageBucket: "usta-app-a86db.appspot.com",
  messagingSenderId: "123...",
  appId: "1:123..."
};
```

**Send me these values and I'll update `firebase-config.js`!**

---

## 🌐 Step 3: Update Frontend with Backend URL (5 minutes)

I need to update the frontend to point to your live Railway backend.

**Give me your Railway URL from Step 1.6**

Example: `https://usta-backend-production-xxxx.up.railway.app`

I'll update:
1. `usta-public/js/usta-api.js` with your Railway URL
2. `usta-public/js/firebase-config.js` with your Firebase config
3. Deploy to Firebase

---

## 🚀 Step 4: Deploy Frontend to Firebase (2 minutes)

After I update the files:

```bash
cd "C:\Users\chefm\Iterum Innovation"
firebase use usta-app-a86db
firebase deploy --only hosting
```

✅ **Frontend deployed with backend connection!**

---

## ✅ Step 5: Test Everything! (10 minutes)

### 5.1 Test Authentication

1. Visit: https://usta-app-a86db.web.app/signup.html
2. Create an account
3. Sign up successfully → ✅ Backend works!

---

### 5.2 Test Video Feed

1. Go to: https://usta-app-a86db.web.app/demo.html
2. You should see demo videos
3. Try liking a video → ✅ API works!
4. Try validating → ✅ XP system works!

---

### 5.3 Test Video Upload

1. Go to: https://usta-app-a86db.web.app/upload.html
2. Drag & drop a video
3. Select a challenge
4. Add caption
5. Click "Post Video"
6. Watch progress bar → ✅ Firebase Storage works!

---

### 5.4 Test Profile

1. Go to: https://usta-app-a86db.web.app/profile.html
2. See your XP, level, stats → ✅ Database works!

---

## 🎉 Success Checklist

When everything is working:

- ✅ Backend live on Railway
- ✅ Database working (PostgreSQL)
- ✅ Frontend deployed to Firebase
- ✅ API calls successful
- ✅ Firebase Storage for videos
- ✅ Can sign up new users
- ✅ Can upload videos
- ✅ Can like/validate videos
- ✅ XP system working
- ✅ Profiles loading

**YOU'RE LIVE! 🚀**

---

## 📊 Monitor Your App

### Railway Dashboard
- View logs: Railway → Service → Logs tab
- Monitor usage: Railway → Service → Metrics tab
- Database stats: Railway → PostgreSQL → Metrics

### Firebase Console
- Storage usage: Firebase → Storage → Usage tab
- Hosting traffic: Firebase → Hosting → Usage tab
- Analytics: Firebase → Analytics (if enabled)

---

## 🐛 Troubleshooting

### "Backend not responding"
1. Check Railway logs for errors
2. Verify DATABASE_URL is set
3. Make sure database is initialized
4. Check environment variables are correct

### "Firebase Storage upload fails"
1. Check storage rules are published
2. Verify firebase-config.js has correct config
3. Check user is authenticated
4. Verify file size < 500MB

### "CORS errors"
1. Check backend config.py has correct FRONTEND_URL
2. Verify Railway environment variable is set
3. Make sure backend is using ProductionConfig

---

## 💰 Cost Monitoring

**Free Tier Limits:**
- Railway: 500 hours/month (always on = ~16 days)
- Railway: $5 credit/month
- Firebase Storage: 5GB, 1GB/day downloads
- Firebase Hosting: 10GB/month

**What happens when you exceed:**
- Railway: Add $5/month payment, or service pauses
- Firebase: Need to upgrade to Blaze plan (pay-as-you-go)

**Estimated costs with 100 beta users:**
- Railway: $0-10/month
- Firebase: $0-5/month
- **Total: $0-15/month**

---

## 🎯 Next Steps After Launch

1. **Share with chef friends!**
   - Get 5-10 people testing
   - Collect feedback
   - Fix bugs

2. **Add monitoring**
   - Set up error tracking (Sentry - free tier)
   - Add Google Analytics
   - Monitor Railway logs

3. **Improve features**
   - Video compression
   - Better notifications
   - Enhanced challenges
   - Community features

4. **Scale when ready**
   - Migrate to Cloud Run (more scalable)
   - Add CDN for videos
   - Optimize database queries

---

## 📞 Ready to Deploy?

**Tell me:**
1. ✅ Created Railway account? (Yes/No)
2. ✅ Pushed code to GitHub? (Yes/No)
3. Need help with any step?

**Then send me:**
1. Your Railway backend URL
2. Your Firebase config values

**And I'll:**
1. Update the frontend files
2. Deploy to Firebase
3. Test everything
4. Give you the go-ahead to share with chefs!

**Let's launch this! 🚀**

