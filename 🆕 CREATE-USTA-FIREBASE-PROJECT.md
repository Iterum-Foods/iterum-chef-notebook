# 🆕 Create New Firebase Project for Usta

## Why Separate Project?

### **Better URLs:**
- ❌ Old: `iterum-culinary-app.web.app`
- ✅ New: `usta-app.web.app` or `usta.web.app`

### **Benefits:**
- Separate analytics for each product
- Independent scaling & billing
- Cleaner for investors
- Professional branding
- Easy to manage multiple apps

---

## 🚀 CREATE NEW PROJECT (2 minutes)

### **Step 1: Create Firebase Project**

1. Go to https://console.firebase.google.com
2. Click **"Create a project"** or **"Add project"**
3. **Project name:** Enter `usta-app` (or just `usta`)
   - This creates URL: `usta-app.web.app`
4. **Google Analytics:** Click **Continue**
5. **Disable** Google Analytics toggle (not needed for hosting)
6. Click **"Create project"**
7. Wait ~30 seconds for project creation
8. Click **"Continue"**

**Done! Project created.** ✅

---

## 🔧 DEPLOY TO NEW PROJECT

### **Step 2: Login to Firebase**

Open PowerShell:
```powershell
firebase login
```

- Browser will open
- Sign in with Google
- Allow Firebase CLI access
- See "Success!"

---

### **Step 3: Link to New Project**

```powershell
firebase use --add
```

**Answer the prompts:**
1. **"Which project?"** → Select **`usta-app`** (your new project)
2. **"Alias?"** → Type: `usta` (or just press Enter for "default")

**Result:** Now using the new usta-app project! ✅

---

### **Step 4: Initialize Hosting**

```powershell
firebase init hosting
```

**Answer the prompts:**
1. **"Use an existing project?"** → YES
2. **"Select project:"** → **`usta-app`**
3. **"Public directory:"** → `usta-public`
4. **"Single-page app:"** → `Yes`
5. **"GitHub auto-deploy:"** → `No`
6. **"Overwrite index.html:"** → `No`

---

### **Step 5: Deploy!**

```powershell
firebase deploy --only hosting
```

Wait for deployment...

```
✔  Deploy complete!

Project Console: https://console.firebase.google.com/project/usta-app
Hosting URL: https://usta-app.web.app
```

---

## 🎉 YOUR NEW USTA URLS!

### **Live Site:**
```
https://usta-app.web.app/              → Investor Hub
https://usta-app.web.app/pitch         → Pitch Deck
https://usta-app.web.app/demo          → Live Demo
https://usta-app.web.app/landing       → Landing Page
https://usta-app.web.app/signup        → Sign Up
https://usta-app.web.app/profile       → Profile
```

**Perfect for sharing with investors!** 📧

---

## 📊 Managing Both Projects

### **Switch Between Projects:**

```powershell
# Use Iterum app
firebase use default

# Use Usta app
firebase use usta
```

### **Check Current Project:**

```powershell
firebase projects:list
```

### **Deploy to Specific Project:**

```powershell
firebase deploy --only hosting --project usta-app
```

---

## 🔗 Custom Domain (Optional)

### **If you own iterumfoods.xyz:**

**Option A: Subdomain**
1. Go to Firebase Console → Hosting
2. Add domain: `usta.iterumfoods.xyz`
3. Add DNS records (provided by Firebase)
4. Wait 15 mins for SSL

**Result:** `https://usta.iterumfoods.xyz` ✨

**Option B: New Domain**
1. Buy: `usta.app` or `usta.co`
2. Connect to Firebase
3. Instant professional URL

---

## 💰 Cost

**Free Tier:**
- 10 GB storage
- 360 MB/day bandwidth
- Custom domain
- SSL certificates

**You'll stay free unless you get massive traffic!**

---

## 🎯 RECOMMENDED SETUP

### **For Professional Launch:**

1. **Create project:** `usta-app`
2. **Deploy:** Get `usta-app.web.app`
3. **Custom domain:** Add `usta.iterumfoods.xyz`
4. **Share:** Professional URLs with investors

### **Project Structure:**
```
Firebase Projects:
├── iterum-culinary-app (Existing Iterum Apps)
│   └── iterum-culinary-app.web.app
│
└── usta-app (NEW - Usta Platform)
    └── usta-app.web.app
    └── usta.iterumfoods.xyz (custom domain)
```

**Clean separation, professional URLs!** ✨

---

## ✅ QUICK CHECKLIST

- [ ] Go to console.firebase.google.com
- [ ] Create project: "usta-app"
- [ ] Disable Analytics
- [ ] Run: `firebase login`
- [ ] Run: `firebase use --add` (select usta-app)
- [ ] Run: `firebase init hosting` (public: usta-public)
- [ ] Run: `firebase deploy --only hosting`
- [ ] Copy URL: `https://usta-app.web.app`
- [ ] Share with investors!

---

## 🚀 DO IT NOW!

**Estimated time: 3 minutes total**

1. Create project (1 min): https://console.firebase.google.com
2. Deploy (2 mins): Commands above

**Result:** Professional Usta website live! 🎉

---

**🔨 usta | Separate project, professional presence**

