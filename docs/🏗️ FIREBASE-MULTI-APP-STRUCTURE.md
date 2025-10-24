# 🏗️ Firebase Multi-App Deployment Structure

## Your Current Apps

### **Iterum Foods Ecosystem:**
1. **Main Landing** - iterumfoods.xyz
2. **Culinary R&D** - Recipe development
3. **Business Planner** - Restaurant business planning
4. **Payroll System** - Restaurant payroll
5. **Usta** - Professional skills platform (separate product)

---

## 🎯 Recommended Structure

### **Option A: Multi-Site Hosting (RECOMMENDED)** ⭐

**One Firebase Project, Multiple Sites**

```
Firebase Project: iterum-foods
├── Site 1: iterum-foods (default)
│   └── iterumfoods.xyz (main landing)
│
├── Site 2: culinary-rd
│   └── rd.iterumfoods.xyz
│
├── Site 3: business-planner
│   └── planner.iterumfoods.xyz
│
├── Site 4: payroll
│   └── payroll.iterumfoods.xyz
│
└── Shared Firestore, Auth, Storage
```

**Separate Project for Usta:**
```
Firebase Project: usta-app
└── usta-app.web.app (or usta.iterumfoods.xyz)
```

### **Why This is Best:**
✅ **Shared Backend:** All Iterum apps share database, auth  
✅ **Cost Efficient:** One Firestore, one Auth system  
✅ **Easy Management:** One dashboard for Iterum suite  
✅ **Clean URLs:** Subdomains for each app  
✅ **Usta Separate:** Independent product, separate analytics  

---

## 📊 Comparison of All Options

### **Option A: Multi-Site (Recommended)**
```
1 Project: iterum-foods (4 sites)
1 Project: usta-app (1 site)
```
**Pros:**
- ✅ Shared resources (database, auth)
- ✅ Cost efficient ($0 for all)
- ✅ Unified analytics for Iterum
- ✅ Easy cross-app features
- ✅ Single billing

**Cons:**
- ⚠️ All apps in same quota
- ⚠️ Slightly more setup

**Cost:** FREE (stays in free tier)

---

### **Option B: Separate Projects**
```
5 Firebase Projects:
- iterum-main
- iterum-rd
- iterum-planner
- iterum-payroll
- usta-app
```
**Pros:**
- ✅ Complete isolation
- ✅ Independent scaling
- ✅ Separate analytics
- ✅ Individual quotas

**Cons:**
- ❌ No shared database
- ❌ Duplicate auth setup
- ❌ More management overhead
- ❌ Higher costs if scale

**Cost:** Still FREE but separate limits

---

### **Option C: Two Projects**
```
Project 1: iterum-foods (all 4 apps, single site)
Project 2: usta-app
```
**Pros:**
- ✅ Simple setup
- ✅ Shared backend
- ✅ Minimal management

**Cons:**
- ❌ All apps on one URL
- ❌ Messy routing
- ❌ Not professional

**Cost:** FREE

---

## 🎯 My Recommendation: Multi-Site Setup

### **Firebase Project 1: iterum-foods**

**Contains 4 Hosting Sites:**
1. **iterum-foods** (default)
   - URL: `iterum-foods.web.app`
   - Custom: `iterumfoods.xyz`
   - Content: Main landing page

2. **culinary-rd**
   - URL: `culinary-rd-abc123.web.app`
   - Custom: `rd.iterumfoods.xyz`
   - Content: Recipe R&D app

3. **business-planner**
   - URL: `business-planner-abc123.web.app`
   - Custom: `planner.iterumfoods.xyz`
   - Content: Business planning app

4. **payroll**
   - URL: `payroll-abc123.web.app`
   - Custom: `payroll.iterumfoods.xyz`
   - Content: Payroll system

**Shared Resources:**
- Firestore Database (recipes, users, data)
- Firebase Authentication (single sign-on)
- Cloud Storage (images, files)
- Cloud Functions (backend logic)

---

### **Firebase Project 2: usta-app**

**Single Hosting Site:**
- URL: `usta-app.web.app`
- Custom: `usta.iterumfoods.xyz` or separate domain
- Content: Usta platform

**Separate Resources:**
- Own Firestore (user skills, challenges)
- Own Authentication (separate user base)
- Own Analytics (track separately)
- Own Functions

**Why Separate:**
- Different product/business model
- Separate investor pitch
- Independent scaling
- May sell separately

---

## 🚀 Implementation Guide

### **Step 1: Create Projects**

**Project 1:**
```
Name: iterum-foods
Enable: Firestore, Authentication, Storage, Hosting
```

**Project 2:**
```
Name: usta-app
Enable: Firestore, Authentication, Hosting
```

---

### **Step 2: Set Up Multi-Site Hosting**

```powershell
# Switch to iterum-foods project
firebase use iterum-foods

# Create additional sites
firebase hosting:sites:create culinary-rd
firebase hosting:sites:create business-planner
firebase hosting:sites:create payroll
```

---

### **Step 3: Configure firebase.json**

Create separate hosting configs:

```json
{
  "hosting": [
    {
      "site": "iterum-foods",
      "public": "public/main",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    },
    {
      "site": "culinary-rd",
      "public": "public/rd",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    },
    {
      "site": "business-planner",
      "public": "public/planner",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    },
    {
      "site": "payroll",
      "public": "public/payroll",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    }
  ]
}
```

---

### **Step 4: Organize Files**

```
Iterum Innovation/
├── public/
│   ├── main/              (Main landing)
│   │   └── index.html
│   ├── rd/                (Culinary R&D)
│   │   └── index.html
│   ├── planner/           (Business Planner)
│   │   └── index.html
│   └── payroll/           (Payroll)
│       └── index.html
│
├── usta-public/           (Usta - separate)
│   └── index.html
│
└── firebase.json
```

---

### **Step 5: Deploy All Sites**

**Deploy Iterum Apps:**
```powershell
firebase use iterum-foods

# Deploy all sites at once
firebase deploy --only hosting

# Or deploy specific site
firebase deploy --only hosting:culinary-rd
```

**Deploy Usta:**
```powershell
firebase use usta-app
firebase deploy --only hosting
```

---

## 🔗 URL Structure After Setup

### **Iterum Foods Apps:**
```
https://iterumfoods.xyz/                     → Main Landing
https://rd.iterumfoods.xyz/                  → Culinary R&D
https://planner.iterumfoods.xyz/             → Business Planner
https://payroll.iterumfoods.xyz/             → Payroll System
```

### **Usta (Separate):**
```
https://usta-app.web.app/                    → Usta Platform
https://usta.iterumfoods.xyz/                → (optional subdomain)
```

**Or keep completely separate:**
```
https://usta.app/                            → Buy separate domain
```

---

## 💰 Cost Analysis

### **Multi-Site (Recommended):**
```
1 Firebase Project (iterum-foods)
├── 4 Hosting Sites: FREE
├── Shared Firestore: FREE (up to 50K reads/day)
├── Shared Auth: FREE (unlimited)
└── Shared Storage: FREE (5GB)

1 Firebase Project (usta-app)
└── Separate resources: FREE

Total: $0/month (stays in free tier)
```

### **Separate Projects:**
```
5 Firebase Projects × FREE tier = Still FREE
But: Separate quotas, more overhead
```

**Both stay FREE unless massive traffic!**

---

## 🎯 Step-by-Step Setup (Multi-Site)

### **Phase 1: Create & Configure (10 minutes)**

1. **Create iterum-foods project**
   - Go to console.firebase.google.com
   - Create project: `iterum-foods`
   - Enable Analytics

2. **Create additional sites**
   ```powershell
   firebase use iterum-foods
   firebase hosting:sites:create culinary-rd
   firebase hosting:sites:create business-planner
   firebase hosting:sites:create payroll
   ```

3. **Create usta-app project**
   - Create project: `usta-app`
   - Separate from Iterum

---

### **Phase 2: Organize Files (5 minutes)**

Create folder structure:
```powershell
mkdir public\main -Force
mkdir public\rd -Force
mkdir public\planner -Force
mkdir public\payroll -Force
```

Copy files:
```powershell
# Main landing
Copy-Item "landing-pages\main-landing\*" "public\main\" -Recurse

# R&D app
Copy-Item "landing-pages\culinary-rd\*" "public\rd\" -Recurse

# Business Planner
Copy-Item "landing-pages\business-planner\*" "public\planner\" -Recurse

# Payroll
Copy-Item "landing-pages\payroll\*" "public\payroll\" -Recurse
```

---

### **Phase 3: Deploy (2 minutes)**

```powershell
# Deploy all Iterum apps
firebase use iterum-foods
firebase deploy --only hosting

# Deploy Usta
firebase use usta-app
firebase deploy --only hosting
```

**Done! All 5 apps live!**

---

## 🔄 Daily Workflow

### **Update Iterum App:**
```powershell
# Make changes to files in public/rd/
firebase use iterum-foods
firebase deploy --only hosting:culinary-rd
```

### **Update Usta:**
```powershell
# Make changes to usta-public/
firebase use usta-app
firebase deploy --only hosting
```

### **Update All:**
```powershell
firebase use iterum-foods
firebase deploy --only hosting

firebase use usta-app
firebase deploy --only hosting
```

---

## 🎨 Custom Domain Setup

### **Main Domain: iterumfoods.xyz**

In Firebase Console (iterum-foods project):

1. **Default site** → Add `iterumfoods.xyz`
2. **culinary-rd** → Add `rd.iterumfoods.xyz`
3. **business-planner** → Add `planner.iterumfoods.xyz`
4. **payroll** → Add `payroll.iterumfoods.xyz`

**DNS Records (all point to Firebase):**
```
iterumfoods.xyz          → A records from Firebase
rd.iterumfoods.xyz       → A records from Firebase
planner.iterumfoods.xyz  → A records from Firebase
payroll.iterumfoods.xyz  → A records from Firebase
```

### **Usta Domain:**

**Option A: Subdomain**
```
usta.iterumfoods.xyz → Points to usta-app project
```

**Option B: Separate Domain**
```
usta.app → Buy new domain, point to usta-app
```

---

## 📊 Analytics Structure

### **Iterum Project:**
- Combined analytics for all 4 apps
- See total Iterum ecosystem usage
- Track cross-app user journeys
- Unified metrics for investors

### **Usta Project:**
- Separate analytics
- Independent metrics
- Separate investor reporting
- Different product funnel

---

## ✅ Final Recommendation

### **Setup:**
```
Firebase Project 1: iterum-foods
├── Multi-site hosting (4 sites)
├── Shared Firestore
├── Shared Authentication
└── Combined analytics

Firebase Project 2: usta-app
├── Single site
├── Separate Firestore
├── Separate Authentication
└── Independent analytics
```

### **URLs:**
```
iterumfoods.xyz              → Main landing
rd.iterumfoods.xyz           → Culinary R&D
planner.iterumfoods.xyz      → Business Planner
payroll.iterumfoods.xyz      → Payroll

usta-app.web.app             → Usta Platform
(or usta.iterumfoods.xyz)
```

### **Why:**
- ✅ Professional URL structure
- ✅ Shared resources for Iterum suite
- ✅ Usta independent (different product)
- ✅ Free tier covers everything
- ✅ Easy to manage
- ✅ Scales well

---

## 🚀 Next Steps

1. Create `iterum-foods` Firebase project
2. Set up multi-site hosting
3. Create `usta-app` Firebase project
4. Deploy all apps
5. Configure custom domains
6. Done!

**Total setup time: 30 minutes**  
**Result: Professional multi-app infrastructure!**

---

**🔨 Ready to structure your Firebase deployment like a pro!**

*One project for Iterum suite, separate for Usta. Clean, professional, scalable.*

