# 🔧 Google Drive Integration Setup Guide

## ☁️ What You'll Get

With Google Drive integration, you can:
- ✅ **Backup** all recipes to the cloud automatically
- ✅ **Access** recipes from any device (phone, tablet, computer)
- ✅ **Sync** recipes across multiple computers
- ✅ **Share** recipes with team members via link
- ✅ **Collaborate** with others on recipe development
- ✅ **Never lose** your recipes (automatic backups)

---

## 🚀 Quick Setup (15 minutes)

### Step 1: Install Required Libraries

```powershell
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### Step 2: Set Up Google Cloud Project

#### 2.1: Go to Google Cloud Console
https://console.cloud.google.com/

#### 2.2: Create a New Project
1. Click "Select a project" at the top
2. Click "NEW PROJECT"
3. Name it: **"Recipe Manager"**
4. Click "CREATE"

#### 2.3: Enable Google Drive API
1. In the search bar, type: **"Google Drive API"**
2. Click on "Google Drive API"
3. Click "ENABLE"

---

### Step 3: Create OAuth Credentials

#### 3.1: Configure OAuth Consent Screen
1. Go to: **APIs & Services → OAuth consent screen**
2. Choose: **External** (unless you have Google Workspace)
3. Click "CREATE"

4. Fill in required fields:
   - **App name**: Recipe Manager
   - **User support email**: your-email@gmail.com
   - **Developer contact**: your-email@gmail.com

5. Click "SAVE AND CONTINUE"

6. On "Scopes" page: Click "SAVE AND CONTINUE" (no changes needed)

7. On "Test users" page:
   - Click "ADD USERS"
   - Add your Gmail address
   - Click "SAVE AND CONTINUE"

8. Click "BACK TO DASHBOARD"

#### 3.2: Create OAuth Client ID
1. Go to: **APIs & Services → Credentials**
2. Click "CREATE CREDENTIALS"
3. Choose "OAuth client ID"
4. Application type: **Desktop app**
5. Name: **Recipe Manager Desktop**
6. Click "CREATE"

#### 3.3: Download Credentials
1. You'll see your Client ID created
2. Click the **Download** button (⬇️) 
3. Save the file as: **`credentials.json`**
4. Move `credentials.json` to your recipe-library-system folder:
   ```
   C:\Users\chefm\OneDrive\Desktop\Recipe Organizer\recipe-library-system\credentials.json
   ```

---

### Step 4: First Run & Authentication

```powershell
cd recipe-library-system
py google_drive_integration.py
```

**What happens:**
1. A browser window will open
2. Sign in with your Google account
3. You'll see: "Recipe Manager wants to access your Google Account"
4. Click "Continue" or "Allow"
5. You'll see: "The authentication flow has completed"
6. Close the browser window

**Done!** A `token.pickle` file is created for future use.

---

## 📋 Usage Examples

### Upload All Recipes to Google Drive

```powershell
py google_drive_integration.py
# Choose: 1. Upload all recipes to Google Drive
```

**Result:** All 12 recipes uploaded to "Recipe Library" folder in your Google Drive

---

### Auto-Sync (Upload New/Modified Recipes)

```powershell
py google_drive_integration.py
# Choose: 2. Sync to Google Drive
```

**What it does:**
- Compares local vs Google Drive recipes
- Only uploads new or modified recipes
- Skips unchanged recipes (faster!)

---

### Get Share Link for a Recipe

```powershell
py google_drive_integration.py
# Choose: 5. Get share link for a recipe
# Enter recipe title: Caramelized Onions
```

**Result:** 
```
Share link: https://drive.google.com/file/d/1abc123xyz.../view
```

Anyone with this link can view (but not edit) the recipe!

---

### Create Full Backup

```powershell
py google_drive_integration.py
# Choose: 6. Create full backup
```

**Result:**
- Creates timestamped backup folder: `Recipe_Backup_20251020_150000`
- Uploads ALL recipe files
- Uploads database
- Perfect for weekly/monthly backups!

---

## 🔄 Automatic Sync Workflow

### Daily Workflow

```powershell
# Morning: Download any new recipes from Drive
py google_drive_integration.py
# Choose: 3. Sync from Google Drive

# Work on recipes during the day...

# Evening: Upload your changes
py google_drive_integration.py
# Choose: 2. Sync to Google Drive
```

---

## 📱 Access from Any Device

### On Your Phone
1. Open Google Drive app
2. Go to "Recipe Library" folder
3. View any recipe!

### On Another Computer
1. Install the recipe system
2. Run: `py google_drive_integration.py`
3. Choose: "Sync from Google Drive"
4. All recipes downloaded automatically!

---

## 👥 Team Collaboration

### Share Individual Recipe
```python
# Get shareable link
py google_drive_integration.py
# Choose: 5. Get share link
# Send link to team member
```

### Share Entire Folder
1. Go to Google Drive
2. Find "Recipe Library" folder
3. Right-click → Share
4. Add team members' emails
5. Set permissions (Viewer/Editor)

**Now your team can:**
- View all recipes
- Download recipes
- Add new recipes (if Editor)

---

## 🔐 Security & Privacy

### Your Data is Safe
- ✅ OAuth 2.0 authentication (industry standard)
- ✅ Only YOU can access your recipes
- ✅ Credentials stored locally
- ✅ Token encrypted by Google
- ✅ You can revoke access anytime

### Revoke Access
1. Go to: https://myaccount.google.com/permissions
2. Find "Recipe Manager"
3. Click "Remove Access"

---

## 🛠️ Troubleshooting

### Issue: "credentials.json not found"
**Solution:** 
1. Make sure you downloaded credentials from Google Cloud Console
2. Rename to exactly: `credentials.json`
3. Place in: `recipe-library-system/` folder

---

### Issue: "Access blocked: This app's request is invalid"
**Solution:**
1. Go back to OAuth consent screen
2. Make sure your email is added as a Test User
3. Make sure app status is "Testing" (not "In Production")

---

### Issue: "The user did not consent"
**Solution:**
1. When browser opens, make sure you click "Continue"
2. Don't close browser until you see "Authentication complete"
3. Try running the script again

---

### Issue: "Token has been expired or revoked"
**Solution:**
1. Delete `token.pickle` file
2. Run script again
3. Re-authenticate in browser

---

## 🎯 Advanced Features

### Automated Daily Backup

Create a Windows Task Scheduler job:

**backup_to_drive.bat:**
```batch
@echo off
cd "C:\Users\chefm\OneDrive\Desktop\Recipe Organizer\recipe-library-system"
py google_drive_integration.py --backup
```

Schedule to run daily at 6 PM.

---

### Sync on Startup

Add to Windows Startup folder:

**sync_on_startup.bat:**
```batch
@echo off
cd "C:\Users\chefm\OneDrive\Desktop\Recipe Organizer\recipe-library-system"
py google_drive_integration.py --sync-from
```

---

### Command Line Usage

```powershell
# Upload all
py google_drive_integration.py --upload-all

# Sync to Drive
py google_drive_integration.py --sync-to

# Sync from Drive
py google_drive_integration.py --sync-from

# Create backup
py google_drive_integration.py --backup

# List Drive recipes
py google_drive_integration.py --list
```

---

## 📊 Benefits Summary

| Feature | Without Google Drive | With Google Drive |
|---------|---------------------|-------------------|
| **Backup** | Manual | Automatic |
| **Access** | One computer only | Any device |
| **Sharing** | Email files | Share links |
| **Collaboration** | Not possible | Real-time |
| **Security** | Local only | Cloud + Local |
| **Sync** | Manual copying | Automatic |

---

## 🎉 You're Ready!

After setup, you'll have:
- ☁️ All recipes backed up to Google Drive
- 📱 Access from phone, tablet, any computer
- 🔄 Automatic sync across devices
- 🤝 Easy sharing with team
- 🔒 Secure cloud storage

**Next Steps:**
1. Complete setup above
2. Upload all recipes
3. Access from your phone!

---

## 📞 Need Help?

**Common Questions:**

**Q: Will this use a lot of my Google Drive storage?**
A: No! Recipe Excel files are tiny (usually 50-100 KB each). 100 recipes = ~10 MB.

**Q: Can I use this with Google Workspace (work account)?**
A: Yes! Just choose "Internal" instead of "External" when setting up OAuth consent screen.

**Q: What if I already have recipes in Google Drive?**
A: Use "Sync from Google Drive" to download them into your library.

**Q: Can multiple people edit recipes at the same time?**
A: Google Drive will create versions if multiple people edit. Best practice: One person edits at a time.

**Q: Is this free?**
A: Yes! Google Drive API is free for personal use. You get 15 GB free storage with any Google account.

---

**Happy Cloud Cooking! ☁️🍳**

