# 🌐 Site Structure Guide - Where Everything Lives

**Date:** October 16, 2025  
**Your Firebase Sites:** 2 sites configured

---

## 🎯 Your Two Firebase Sites

### **1. Main Application Site** 🚀
**URL:** `https://iterum-culinary-app.web.app`  
**Purpose:** The actual application where users work

**Entry Point:** `launch.html` (Login page) ✅ **NOW FIXED**

**Pages:**
- `/` → `launch.html` (Login/Signup page)
- `/index.html` → Dashboard (after login)
- `/recipe-library.html` → Recipe library
- `/recipe-developer.html` → Recipe developer
- `/menu-builder.html` → Menu builder
- `/ingredients.html` → Ingredients database
- `/user_management.html` → User management
- And all other app pages...

---

### **2. Landing/Marketing Site** 🎨
**URL:** `https://iterum-landing.web.app`  
**Purpose:** Public marketing/waitlist page

**Entry Point:** Marketing landing page

---

## 🔄 User Flow (After Deployment)

```
User visits: https://iterum-culinary-app.web.app
           ↓
    Shows: launch.html (Login page)
           ↓
User signs in/signs up
           ↓
Redirects to: index.html (Dashboard)
           ↓
    User can navigate:
    - Recipe Library
    - Menu Builder
    - Recipe Developer
    - Ingredients
    - etc.
```

---

## 📝 What Was Fixed

### **Before:**
```json
"rewrites": [
  {
    "source": "**",
    "destination": "/index.html"  ❌ Wrong!
  }
]
```
**Problem:** Everything redirected to dashboard (index.html)  
**Issue:** Users couldn't access login page properly

### **After:**
```json
"rewrites": [
  {
    "source": "/",
    "destination": "/launch.html"  ✅ Correct!
  }
]
```
**Result:** Root URL shows login page  
**Benefit:** Proper entry point, users see login first

---

## 🌍 URL Map (After Deploy)

| URL | Page | Purpose | Auth Required |
|-----|------|---------|---------------|
| `/` | launch.html | Login/Signup | No |
| `/launch.html` | launch.html | Login/Signup | No |
| `/index.html` | index.html | Dashboard | Yes |
| `/recipe-library.html` | recipe-library.html | Recipes | Yes |
| `/menu-builder.html` | menu-builder.html | Menus | Yes |
| `/recipe-developer.html` | recipe-developer.html | Developer | Yes |
| `/ingredients.html` | ingredients.html | Ingredients | Yes |
| `/user_management.html` | user_management.html | Admin | Yes |

---

## 🎯 How Users Access Your App

### **Main Site:**
```
https://iterum-culinary-app.web.app
         ↓
   Shows launch.html (Login page)
```

### **Direct Page Access:**
```
https://iterum-culinary-app.web.app/recipe-library.html
         ↓
   Auth Guard checks login
         ↓
   If not logged in → Shows sign-in modal
   If logged in → Shows page
```

---

## 🔧 Local vs Production

### **Local Development:**
```
http://localhost:8080/launch.html  - Login page
http://localhost:8080/index.html   - Dashboard
http://localhost:8080/recipe-library.html  - Recipes
```

### **Production (After Firebase Deploy):**
```
https://iterum-culinary-app.web.app/  - Login page
https://iterum-culinary-app.web.app/index.html  - Dashboard
https://iterum-culinary-app.web.app/recipe-library.html  - Recipes
```

---

## 🚀 Deployment Status

### **GitHub:** ✅ **DEPLOYED**
```
Latest commit includes firebase.json fix
Entry point: launch.html
```

### **Firebase:** ⏳ **Ready to Deploy**
```
Command needed: firebase deploy --only hosting
After deploy: https://iterum-culinary-app.web.app will show launch.html
```

---

## 📋 Quick Reference

### **Your Two Sites:**

**Main App:**
- **URL:** https://iterum-culinary-app.web.app
- **Entry:** launch.html (login)
- **Purpose:** Application
- **Users:** Your customers/chefs

**Landing:**
- **URL:** https://iterum-landing.web.app
- **Entry:** Landing page
- **Purpose:** Marketing/Waitlist
- **Users:** Potential customers

---

## 🎯 After You Deploy

When you run `firebase deploy --only hosting`, here's what happens:

1. **Uploads all files** to Firebase
2. **Sets launch.html as entry point** ✅
3. **Makes live at:** `https://iterum-culinary-app.web.app`

Then when users visit:
```
https://iterum-culinary-app.web.app
         ↓
   See beautiful login page (launch.html)
         ↓
   Sign in
         ↓
   Go to dashboard (index.html)
         ↓
   Use the app!
```

---

## ✅ Summary

**Launch Page Location:**
- **File:** `launch.html`
- **Local:** `http://localhost:8080/launch.html`
- **Production (after deploy):** `https://iterum-culinary-app.web.app/`

**The launch page is your login/signup page** - it's where users start their journey!

---

**To deploy and make it live:**
```bash
firebase login --reauth
firebase deploy --only hosting
```

Then visit: `https://iterum-culinary-app.web.app` to see it! 🚀

