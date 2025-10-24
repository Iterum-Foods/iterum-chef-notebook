# ⚡ Google Drive Quick Start (5 Minutes)

## Already Have Google Account? Start Here!

### Step 1: Install Libraries (1 minute)
```powershell
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 2: Get Credentials (3 minutes)
1. Go to: https://console.cloud.google.com/
2. Create project: "Recipe Manager"
3. Enable "Google Drive API"
4. Create OAuth credentials → Desktop app
5. Download as `credentials.json`
6. Put in `recipe-library-system/` folder

### Step 3: Run! (1 minute)
```powershell
py google_drive_integration.py
```
- Browser opens → Sign in → Allow access
- Done!

### Step 4: Upload Your Recipes
```
Choose: 1. Upload all recipes to Google Drive
```

**That's it! Your recipes are now in Google Drive! ☁️**

---

## What You Can Do Now

### 📱 View on Your Phone
1. Open Google Drive app
2. Go to "Recipe Library" folder
3. View any recipe!

### 🔄 Auto-Sync
```powershell
py google_drive_integration.py
# Choose: 2. Sync to Google Drive
```

### 🔗 Share a Recipe
```powershell
py google_drive_integration.py
# Choose: 5. Get share link
# Enter recipe name
# Send link to anyone!
```

### 💾 Create Backup
```powershell
py google_drive_integration.py
# Choose: 6. Create full backup
```

---

## Batch Files (Even Easier!)

### Upload All Recipes
Just double-click: **`google_drive_upload_all.bat`**

### Daily Sync
Just double-click: **`google_drive_sync.bat`**

---

## Need Detailed Instructions?

See: **`GOOGLE_DRIVE_SETUP.md`** for complete step-by-step guide with screenshots.

---

**Questions?**
- Where are my recipes? → Google Drive → "Recipe Library" folder
- How do I sync? → Run script, choose option 2
- Can I share? → Yes! Option 5 gives you a shareable link
- Is it safe? → Yes! OAuth 2.0, industry standard security

**Happy Cloud Cooking! ☁️**

