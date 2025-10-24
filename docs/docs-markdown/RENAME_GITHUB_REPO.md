# 🔄 Rename GitHub Repository

## Current vs Desired Names

**Current GitHub Repo**: `iterum-chef-notebook`  
**Firebase Project**: `iterum-culinary-app`  
**Desired**: Make them match!

---

## 🎯 Recommended: Rename to `iterum-culinary-app`

This will match your Firebase project name and app branding.

---

## 📋 How to Rename GitHub Repository

### **Option 1: Rename on GitHub** (Recommended - 2 minutes)

#### **Step 1: Go to Repository Settings**
1. **Open**: https://github.com/Iterum-Foods/iterum-chef-notebook/settings
2. **Scroll down** to "Repository name" section

#### **Step 2: Change the Name**
1. **Current name**: `iterum-chef-notebook`
2. **New name**: `iterum-culinary-app`
3. **Click**: "Rename" button
4. **Confirm**: Type the repository name to confirm

#### **Step 3: Update Local Repository**
After renaming on GitHub, update your local git remote:

```bash
git remote set-url origin https://github.com/Iterum-Foods/iterum-culinary-app.git
```

#### **Step 4: Verify**
```bash
git remote -v
```

Should show:
```
origin  https://github.com/Iterum-Foods/iterum-culinary-app.git (fetch)
origin  https://github.com/Iterum-Foods/iterum-culinary-app.git (push)
```

---

### **Option 2: Create New Repository** (If you want a fresh start)

1. Create new repo: `iterum-culinary-app`
2. Push your code to new repo
3. Archive or delete old repo

---

## ⚠️ Important Notes

### **After Renaming**:
- **GitHub automatically redirects** old URLs to new URLs
- **Clone URLs change** - update anywhere you have them
- **CI/CD workflows** - Update any external integrations
- **Documentation** - Update repo links

### **What Updates Automatically**:
- ✅ Issues and Pull Requests
- ✅ Releases and Tags
- ✅ Wiki pages
- ✅ GitHub Pages (if enabled)
- ✅ Redirects from old URL

### **What You Need to Update**:
- Local git remote (Step 3 above)
- Any scripts referencing the repo
- Documentation with repo URLs
- CI/CD configurations

---

## 🎯 Recommended New Names

Choose one:

### **Option A: `iterum-culinary-app`** ✅ (Recommended)
- Matches Firebase project
- Professional
- Clear purpose

### **Option B: `iterum-chef-platform`**
- Broader scope
- Platform vs app

### **Option C: `iterum-rnd-platform`**
- R&D focus
- Professional

---

## 🚀 Quick Rename Steps

### **Do This Now**:

1. **Go to**: https://github.com/Iterum-Foods/iterum-chef-notebook/settings

2. **Find**: "Repository name" section

3. **Change**: `iterum-chef-notebook` → `iterum-culinary-app`

4. **Click**: "Rename"

5. **In your terminal**, run:
   ```bash
   git remote set-url origin https://github.com/Iterum-Foods/iterum-culinary-app.git
   git remote -v
   ```

6. **Done!** ✅

---

## 📊 After Renaming

**New GitHub URL**: https://github.com/Iterum-Foods/iterum-culinary-app

**Old URL redirects**: https://github.com/Iterum-Foods/iterum-chef-notebook → Auto-redirects to new URL

**Your app**: Still works at https://iterum-culinary-app.web.app (no change)

---

## ✅ Benefits

- Consistent naming across platforms
- Easier to remember
- Professional branding
- Matches Firebase project
- Clear app identity

---

**Ready to rename?** Go to the settings link above! 🔄


