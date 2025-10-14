# 🔍 Firebase Project Audit - iterum-chef-notebook

**Date:** October 14, 2025  
**Purpose:** Check what's in `iterum-chef-notebook-26949` before archiving  
**Current Active Project:** `iterum-culinary-app`

---

## 📊 Project Information

### **iterum-chef-notebook-26949**

| Detail | Value |
|--------|-------|
| **Project ID** | `iterum-chef-notebook-26949` |
| **Project Number** | 34478776055 |
| **Last Deployment** | July 3, 2025, 8:24 PM |
| **Hosted URL** | `https://iterum-chef-notebook-26949.web.app` |
| **Status** | ⚠️ Inactive (3+ months old) |
| **Has Firestore** | ✅ Yes - (default) database exists |

---

## ✅ Checklist: What to Check Before Archiving

### **1. Firestore Database** 🗄️

**Check for:**
- [ ] User accounts/profiles
- [ ] Recipe data
- [ ] Menu data
- [ ] Ingredient libraries
- [ ] Equipment lists
- [ ] Vendor information
- [ ] Trial user data
- [ ] Waitlist contacts
- [ ] Any custom collections

**How to check:**
1. Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/firestore`
2. Look at all collections
3. Export any important data

**Export command (if data exists):**
```bash
firebase use iterum-chef-notebook-26949
firebase firestore:export gs://iterum-chef-notebook-26949.appspot.com/backups/$(date +%Y%m%d)
```

---

### **2. Firebase Authentication Users** 👥

**Check for:**
- [ ] Registered users
- [ ] Email/password accounts
- [ ] Google OAuth accounts
- [ ] User count
- [ ] Admin accounts

**How to check:**
1. Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/authentication/users`
2. See if any users are registered
3. Export user list if needed

**Important:** User accounts CANNOT be automatically transferred between projects. You would need users to re-register.

---

### **3. Firebase Storage** 📁

**Check for:**
- [ ] Uploaded images
- [ ] Recipe photos
- [ ] User avatars
- [ ] Menu PDFs
- [ ] Equipment manuals
- [ ] Any files

**How to check:**
1. Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/storage`
2. Browse all folders
3. Download any important files

**Download command:**
```bash
gsutil -m cp -r gs://iterum-chef-notebook-26949.appspot.com/* ./backup-storage/
```

---

### **4. Hosted Website/Files** 🌐

**Check for:**
- [ ] HTML/CSS/JS files
- [ ] Custom features not in current app
- [ ] Configuration files
- [ ] API integrations
- [ ] Third-party scripts

**How to check:**
1. Visit: `https://iterum-chef-notebook-26949.web.app`
2. Browse the site
3. Check browser DevTools for unique features
4. View source code

**Download deployed files:**
```bash
# Note: Firebase doesn't provide a direct download of hosted files
# But you should have them in your local repo if it was deployed from there
```

---

### **5. Firebase Functions** ⚡

**Check for:**
- [ ] Cloud Functions
- [ ] Backend API endpoints
- [ ] Scheduled jobs
- [ ] Triggers
- [ ] Custom logic

**How to check:**
1. Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/functions`
2. List all deployed functions
3. Review function code

**List functions:**
```bash
firebase use iterum-chef-notebook-26949
firebase functions:list
```

---

### **6. Firebase Realtime Database** 📊

**Check for:**
- [ ] Any data in Realtime Database (different from Firestore)
- [ ] Real-time sync data
- [ ] Legacy data structures

**How to check:**
1. Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/database`
2. See if Realtime Database is enabled
3. Export data if exists

---

### **7. Environment Variables & Secrets** 🔐

**Check for:**
- [ ] API keys
- [ ] Third-party service credentials
- [ ] Email service config (SendGrid, etc.)
- [ ] Payment processor keys (Stripe, etc.)
- [ ] Custom environment variables

**How to check:**
1. Check Firebase Functions config
2. Review project settings
3. Document any integrations

**List config:**
```bash
firebase use iterum-chef-notebook-26949
firebase functions:config:get
```

---

### **8. Firestore Security Rules** 🔒

**Check for:**
- [ ] Custom security rules
- [ ] Role-based access rules
- [ ] Data validation rules
- [ ] Complex permission logic

**How to check:**
1. Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/firestore/rules`
2. Copy the rules
3. Compare with current project rules

**Get rules:**
```bash
firebase use iterum-chef-notebook-26949
firebase firestore:rules
```

---

### **9. Analytics & Insights** 📈

**Check for:**
- [ ] Google Analytics data
- [ ] User behavior patterns
- [ ] Popular features
- [ ] Error logs
- [ ] Performance metrics

**How to check:**
1. Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/analytics`
2. Review historical data
3. Export reports if valuable

---

### **10. Project Configuration** ⚙️

**Check for:**
- [ ] Custom domain settings
- [ ] OAuth configurations
- [ ] Email templates
- [ ] Dynamic links
- [ ] Remote config values

**How to check:**
1. Go to Project Settings
2. Review all tabs
3. Document any custom configurations

---

## 🎯 What to Migrate to `iterum-culinary-app`

### **Priority 1: MUST MIGRATE** 🔴

| Item | Why | How |
|------|-----|-----|
| **User Data** | Don't lose customer info | Export Firestore, manual import |
| **Recipe Library** | Your core content | Firestore export/import |
| **Security Rules** | Protect your data | Copy & paste rules |
| **Environment Configs** | API integrations | Document & reconfigure |

### **Priority 2: SHOULD MIGRATE** 🟡

| Item | Why | How |
|------|-----|-----|
| **Storage Files** | Images, documents | gsutil copy |
| **Cloud Functions** | Custom backend logic | Redeploy code |
| **Analytics History** | Insights & trends | Export reports |
| **Auth Config** | OAuth settings | Reconfigure in new project |

### **Priority 3: NICE TO HAVE** 🟢

| Item | Why | How |
|------|-----|-----|
| **Old Logs** | Debugging history | Export if needed |
| **Test Data** | Development reference | Copy if useful |
| **Experiment Configs** | A/B test results | Document findings |

---

## 📋 Step-by-Step Migration Guide

### **Step 1: Audit Current Project**

```bash
# Switch to old project
firebase use iterum-chef-notebook-26949

# Check what's there
firebase functions:list
firebase firestore:databases:list
firebase hosting:channel:list
```

### **Step 2: Export Firestore Data**

```bash
# Visit Firebase Console
# Go to Firestore > Import/Export
# Export to Cloud Storage bucket
# Or use command:
firebase firestore:export gs://iterum-chef-notebook-26949.appspot.com/backup-$(date +%Y%m%d)
```

### **Step 3: Download Storage Files**

```bash
# Install Google Cloud SDK if not already installed
# Then:
gsutil -m cp -r gs://iterum-chef-notebook-26949.appspot.com/* ./backup-storage/
```

### **Step 4: Export Authentication Users**

```bash
# Visit: https://console.firebase.google.com/project/iterum-chef-notebook-26949/authentication/users
# Click "Export Users" (top right)
# Download CSV file
```

### **Step 5: Copy Security Rules**

```bash
# Get current rules
firebase use iterum-chef-notebook-26949
firebase firestore:rules > old-firestore-rules.txt

# Compare with new project
firebase use iterum-culinary-app
firebase firestore:rules > current-firestore-rules.txt

# Manually merge any custom rules
```

### **Step 6: Document Configurations**

Create a file: `old-project-config.md` with:
- API keys used
- OAuth client IDs
- Email templates
- Custom domains
- Third-party integrations

### **Step 7: Switch Back to Current Project**

```bash
firebase use iterum-culinary-app
```

---

## 🚨 Before You Archive Checklist

### **Final Verification:**

- [ ] ✅ Exported all Firestore data
- [ ] ✅ Downloaded all Storage files
- [ ] ✅ Exported user list
- [ ] ✅ Copied security rules
- [ ] ✅ Documented all API keys/configs
- [ ] ✅ Saved Cloud Functions code
- [ ] ✅ Exported Analytics reports
- [ ] ✅ Took screenshots of important configs
- [ ] ✅ Verified nothing critical left behind
- [ ] ✅ Imported key data to new project

**Only after ALL checks are complete, proceed with archival!**

---

## 🗄️ How to Archive (Not Delete)

### **Option 1: Keep Project (Paused)**

**Benefits:**
- Can reactivate if needed
- No data loss
- Free (no usage = no charges)

**How:**
1. Don't delete the project
2. Leave it inactive
3. It costs nothing if not used

### **Option 2: Export & Delete**

**Benefits:**
- Clean up Firebase dashboard
- Prevent confusion

**How:**
1. Complete all exports above
2. Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/settings/general`
3. Scroll to bottom
4. Click "Delete project"
5. Type project ID to confirm
6. Click "Delete"

**⚠️ WARNING:** This is permanent! Cannot be undone!

---

## 🔍 Quick Audit Commands

Run these to quickly see what's in the old project:

```bash
# Switch to old project
firebase use iterum-chef-notebook-26949

# Check hosting
firebase hosting:channel:list

# Check functions
firebase functions:list

# Check what's configured
firebase projects:list

# Get config variables
firebase functions:config:get

# Switch back
firebase use iterum-culinary-app
```

---

## 📊 Comparison: Old vs New

### **iterum-chef-notebook-26949** (OLD)

| Feature | Status |
|---------|--------|
| Last Updated | July 3, 2025 (3+ months ago) |
| Active Users | ❓ Unknown (check console) |
| Current URL | `https://iterum-chef-notebook-26949.web.app` |
| Usage | ⚠️ Possibly outdated |

### **iterum-culinary-app** (CURRENT)

| Feature | Status |
|---------|--------|
| Last Updated | October 13, 2025 (today!) |
| Active Users | ✅ Current user base |
| Current URL | `https://iterum-culinary-app.web.app` |
| Usage | ✅ Active & deployed |
| CRM | ✅ Fully integrated |
| Features | ✅ Most recent version |

---

## 💡 Recommendations

### **1. Visit the Old Site First**

Open: `https://iterum-chef-notebook-26949.web.app`

**Check if:**
- Does it load?
- Does it have different features?
- Is the UI different?
- Are there unique integrations?

### **2. Check for Data in Firebase Console**

Visit: `https://console.firebase.google.com/project/iterum-chef-notebook-26949`

**Navigate to:**
- Firestore → See if there are collections with data
- Authentication → See if there are registered users
- Storage → See if there are uploaded files
- Functions → See if there are deployed functions

### **3. Export Everything Important**

Better safe than sorry! Export:
- Firestore data
- User lists
- Storage files
- Security rules
- Configuration

### **4. Keep Project Paused (Don't Delete Yet)**

**Why?**
- Firebase doesn't charge for inactive projects
- You can reactivate if you find something needed
- No rush to delete
- Better to be cautious

### **5. After 30 Days**

If you haven't needed anything from it:
- Archive is successful
- Safe to delete the project

---

## 🎯 Action Plan

### **Today:**
1. ✅ Switch to old project: `firebase use iterum-chef-notebook-26949`
2. 🔍 Visit: `https://iterum-chef-notebook-26949.web.app` (check what's there)
3. 🔍 Visit: Firebase Console and check Firestore
4. 🔍 Check Authentication users
5. 🔍 Check Storage files

### **If Data Exists:**
1. 📥 Export Firestore data
2. 📥 Export user list
3. 📥 Download storage files
4. 📝 Document configurations
5. ✅ Switch back: `firebase use iterum-culinary-app`

### **If Empty/Not Needed:**
1. ✅ Document findings
2. ⏸️ Leave project inactive
3. 🗑️ Delete after 30 days (optional)

---

## 📞 Next Steps

**Want me to help you:**
1. Check the old project's Firestore database?
2. Export the data if it exists?
3. Compare features between old and new sites?
4. Create a migration script?

**Just let me know what you'd like to investigate!** 🔍

---

**Generated:** October 14, 2025  
**Purpose:** Pre-archival audit of iterum-chef-notebook-26949  
**Current Project:** iterum-culinary-app ✅

