# 🚀 Firebase Deployment Guide - Usta Landing Page

## Overview

Deploy Usta landing page, investor materials, and demo to Firebase Hosting for live access.

---

## 🎯 What Will Be Deployed

### **Public URLs:**
- `usta-app.web.app` (or custom domain)
  - `/` - Investor Hub
  - `/pitch` - Interactive Pitch Deck
  - `/demo` - Live Demo App
  - `/signup` - Onboarding Flow
  - `/profile` - Profile Example
  - `/landing` - Public Landing Page

---

## 📋 Prerequisites

### **1. Firebase CLI Installed**
Check if installed:
```bash
firebase --version
```

If not installed:
```bash
npm install -g firebase-tools
```

### **2. Firebase Account**
- Go to https://console.firebase.google.com
- Sign in with Google account
- Ready to create new project

---

## 🔧 Step-by-Step Deployment

### **Step 1: Create Firebase Project**

1. Go to https://console.firebase.google.com
2. Click **"Add Project"**
3. Enter project name: **`usta-app`** (or `usta-production`)
4. **Disable** Google Analytics (not needed for hosting)
5. Click **"Create Project"**
6. Wait for project creation (~30 seconds)
7. Click **"Continue"**

---

### **Step 2: Login to Firebase CLI**

Open PowerShell in your project directory and run:

```powershell
firebase login
```

This will:
- Open browser for Google authentication
- Ask you to allow Firebase CLI access
- Show "Success! Logged in as [your-email]"

---

### **Step 3: Initialize Firebase Project**

```powershell
firebase init hosting
```

**Answer the prompts:**

1. **"Please select an option:"**
   - Choose: **"Use an existing project"**
   
2. **"Select a default Firebase project:"**
   - Choose: **usta-app** (the project you just created)
   
3. **"What do you want to use as your public directory?"**
   - Type: **`usta-public`**
   
4. **"Configure as a single-page app?"**
   - Type: **`y`** (yes)
   
5. **"Set up automatic builds with GitHub?"**
   - Type: **`N`** (no, not yet)

---

### **Step 4: Prepare Deployment Files**

The deployment script will automatically:
1. Create `usta-public` directory
2. Copy all necessary files
3. Update paths for production
4. Prepare for deployment

**Or manually run:**

```powershell
# Create public directory
mkdir usta-public -Force

# Copy landing pages
Copy-Item "Skills App\usta-landing-page.html" "usta-public\landing.html"
Copy-Item "Skills App\usta-demo-app.html" "usta-public\demo.html"
Copy-Item "Skills App\usta-onboarding.html" "usta-public\signup.html"
Copy-Item "Skills App\usta-challenge-detail.html" "usta-public\challenge.html"
Copy-Item "Skills App\usta-profile-professional.html" "usta-public\profile.html"
Copy-Item "Skills App\usta-notifications.html" "usta-public\notifications.html"

# Copy investor materials
Copy-Item "landing-pages\usta-app\index.html" "usta-public\index.html"
Copy-Item "landing-pages\usta-app\usta-pitch-deck-web.html" "usta-public\pitch.html"
Copy-Item "landing-pages\usta-app\USTA-EXECUTIVE-SUMMARY.md" "usta-public\"
Copy-Item "landing-pages\usta-app\USTA-BUSINESS-PLAN.md" "usta-public\"
Copy-Item "landing-pages\usta-app\USTA-TECH-ARCHITECTURE.md" "usta-public\"
Copy-Item "landing-pages\usta-app\USTA-FINANCIAL-MODEL-GUIDE.md" "usta-public\"

# Copy brand assets if you have any
# Copy-Item "assets\*" "usta-public\assets\" -Recurse
```

---

### **Step 5: Deploy to Firebase**

```powershell
firebase deploy --only hosting
```

This will:
- Upload all files from `usta-public`
- Configure hosting rules
- Make site live
- Show you the URL

**Expected output:**
```
✔  Deploy complete!

Project Console: https://console.firebase.google.com/project/usta-app/overview
Hosting URL: https://usta-app.web.app
```

---

## 🔗 URL Structure After Deployment

### **Main URLs:**
```
https://usta-app.web.app/              → Investor Hub
https://usta-app.web.app/pitch         → Pitch Deck
https://usta-app.web.app/demo          → Live Demo
https://usta-app.web.app/signup        → Sign Up / Onboarding
https://usta-app.web.app/landing       → Public Landing Page
https://usta-app.web.app/profile       → Profile Example
https://usta-app.web.app/challenge     → Challenge Example
```

---

## 🎨 Custom Domain Setup (Optional)

### **Option 1: Use Firebase Subdomain**
You get: `usta-app.web.app` (free)

### **Option 2: Connect Custom Domain**

**If you own `iterumfoods.xyz`:**

1. Go to Firebase Console → Hosting
2. Click **"Add custom domain"**
3. Enter: `usta.iterumfoods.xyz`
4. Follow DNS verification steps:
   - Add TXT record to your domain
   - Add A records provided by Firebase
5. Wait for SSL certificate (automatic, ~15 mins)

**Result:** `https://usta.iterumfoods.xyz`

---

## 🔄 Update & Redeploy

### **To Update the Site:**

1. Make changes to your files
2. Run deployment script again:
   ```powershell
   .\DEPLOY-USTA-TO-FIREBASE.bat
   ```
3. Or manually:
   ```powershell
   firebase deploy --only hosting
   ```

**Changes go live in ~30 seconds!**

---

## 📊 Firebase Console Features

### **After Deployment, You Can:**

1. **View Analytics:**
   - Go to Hosting tab
   - See page views, bandwidth usage
   - Track visitor countries

2. **Manage Versions:**
   - See deployment history
   - Rollback to previous versions
   - Compare changes

3. **Set Up Redirects:**
   - Create short URLs
   - Redirect old paths
   - Configure rewrites

4. **Monitor Performance:**
   - Page load times
   - Asset sizes
   - Traffic patterns

---

## 🛡️ Security & Performance

### **Automatic Features:**
✓ **SSL Certificate** - HTTPS enabled automatically  
✓ **Global CDN** - Fast worldwide delivery  
✓ **DDoS Protection** - Built-in security  
✓ **Compression** - Gzip/Brotli enabled  
✓ **Cache Control** - Optimal caching  
✓ **HTTP/2** - Modern protocol  

---

## 💰 Pricing

### **Free Tier Includes:**
- 10 GB storage
- 360 MB/day bandwidth
- Custom domain support
- SSL certificates
- 1 GB hosting data transfer/month

**Perfect for:**
- Landing pages
- Demo sites
- Investor presentations
- Beta launches

**You'll stay in free tier unless you get massive traffic!**

---

## 🐛 Troubleshooting

### **Problem: "Firebase command not found"**
**Solution:**
```powershell
npm install -g firebase-tools
```

### **Problem: "Not authorized"**
**Solution:**
```powershell
firebase login --reauth
```

### **Problem: "Public directory not found"**
**Solution:**
Make sure `usta-public` folder exists and has files.

### **Problem: "Links broken after deployment"**
**Solution:**
Use relative paths (already configured in deployment script).

### **Problem: "CSS/JS not loading"**
**Solution:**
Check paths in HTML files - should be relative, not absolute.

---

## 📱 Testing After Deployment

### **Test These URLs:**
1. Main page loads: `https://usta-app.web.app/`
2. Pitch deck works: `https://usta-app.web.app/pitch`
3. Demo is interactive: `https://usta-app.web.app/demo`
4. Signup flow works: `https://usta-app.web.app/signup`
5. Navigation between pages works
6. All links functional
7. Images/assets load
8. Mobile responsive

---

## 🚀 Quick Deploy Commands

### **First Time:**
```powershell
# 1. Login
firebase login

# 2. Initialize
firebase init hosting
# Choose: existing project, public: usta-public, SPA: yes

# 3. Prepare files
.\PREPARE-USTA-DEPLOYMENT.bat

# 4. Deploy
firebase deploy --only hosting
```

### **Subsequent Deploys:**
```powershell
# Just run the deploy script
.\DEPLOY-USTA-TO-FIREBASE.bat
```

---

## 📧 Share With Investors

### **After Deployment:**

**Update your emails:**
```
Old: "Check out our demo at file://..."
New: "Check out our demo at https://usta-app.web.app"
```

**Professional URLs:**
- Investor Hub: `https://usta-app.web.app`
- Pitch Deck: `https://usta-app.web.app/pitch`
- Live Demo: `https://usta-app.web.app/demo`

---

## 🎯 Next Steps After Deployment

### **1. Add Google Analytics (Optional)**
```bash
firebase init analytics
```

### **2. Set Up Custom Domain**
- Buy domain or use existing
- Configure DNS records
- Connect to Firebase

### **3. Enable Email Collection**
- Add form to capture emails
- Set up Firebase Firestore
- Store waitlist signups

### **4. Add Authentication (For Beta)**
- Enable Firebase Auth
- Add sign-in flow
- Protect demo pages

---

## 🔥 Advanced: Multiple Environments

### **Production:**
```powershell
firebase use production
firebase deploy --only hosting
```

### **Staging:**
```powershell
firebase use staging
firebase deploy --only hosting
```

### **Create Staging Project:**
1. Create new Firebase project: `usta-staging`
2. Initialize with different public folder
3. Test before production deployment

---

## 📊 Monitoring After Launch

### **Track These Metrics:**
1. **Visitors:** How many investors/users visiting
2. **Bounce Rate:** Are they staying?
3. **Page Views:** Which pages most popular
4. **Load Time:** Is site fast enough
5. **Devices:** Mobile vs Desktop split
6. **Countries:** Where visitors from

**Access:** Firebase Console → Analytics

---

## ✅ Deployment Checklist

Before deploying, verify:

- [ ] All HTML files have correct paths
- [ ] Images/assets copied to public folder
- [ ] Links between pages work locally
- [ ] Mobile responsive on all pages
- [ ] No console errors in browser
- [ ] Forms work (if any)
- [ ] Navigation flows correctly
- [ ] SSL will be enabled (automatic)
- [ ] Analytics configured (optional)
- [ ] Custom domain ready (optional)

---

## 🎊 You're Live!

After deployment:
- ✅ Share URL with investors
- ✅ Add to pitch deck emails
- ✅ Update LinkedIn profile
- ✅ Share on social media
- ✅ Add to business cards
- ✅ Include in presentations

**Your Usta app is now live and accessible worldwide! 🌍**

---

## 📞 Support

### **Firebase Help:**
- Docs: https://firebase.google.com/docs/hosting
- Community: https://stackoverflow.com/questions/tagged/firebase
- Status: https://status.firebase.google.com

### **Common Commands:**
```powershell
firebase login                    # Authenticate
firebase projects:list            # See all projects
firebase use [project-id]         # Switch project
firebase deploy                   # Deploy everything
firebase deploy --only hosting    # Deploy only hosting
firebase hosting:channel:deploy preview  # Preview channel
firebase open hosting             # Open in console
```

---

**🔨 usta | Now Live on Firebase**

*Deploy once. Update anytime. Share everywhere.*

