# 📦 Moving Recipe Manager App

## Quick Move Guide

Follow these steps to safely move your Recipe Manager app to a new location.

---

## 🎯 Moving to: `C:\Users\chefm\Iterum Innovation`

### Method 1: Using File Explorer (Easiest)

1. **Close all running instances** of the app
   - Close any terminal windows
   - Stop web server if running (Ctrl+C)
   - Close Python scripts

2. **Open File Explorer**
   - Go to: `C:\Users\chefm\OneDrive\Desktop\Recipe Organizer`

3. **Cut the folder**
   - Right-click on `recipe-library-system` folder
   - Click "Cut" (or press Ctrl+X)

4. **Navigate to new location**
   - Go to: `C:\Users\chefm\Iterum Innovation`
   - If folder doesn't exist, create it first

5. **Paste**
   - Right-click in the folder
   - Click "Paste" (or press Ctrl+V)
   - Wait for move to complete

**Done!**

---

### Method 2: Using PowerShell (Command Line)

Open PowerShell and run:

```powershell
# Create destination folder if it doesn't exist
New-Item -ItemType Directory -Path "C:\Users\chefm\Iterum Innovation" -Force

# Move the entire folder
Move-Item -Path "C:\Users\chefm\OneDrive\Desktop\Recipe Organizer\recipe-library-system" -Destination "C:\Users\chefm\Iterum Innovation\recipe-library-system"
```

---

## ✅ After Moving

### Update Your Working Directory

When you open terminal/PowerShell, navigate to new location:

```powershell
cd "C:\Users\chefm\Iterum Innovation\recipe-library-system"
```

### Test Everything Works

```powershell
# Test 1: Check files are there
dir

# Test 2: Test Python
py --version

# Test 3: Test web app
py web_app.py
```

---

## 📝 What Gets Moved

Everything in `recipe-library-system/` including:

✅ All Python scripts
✅ All batch files  
✅ All documentation
✅ `recipe_library/` folder (with database and recipes)
✅ `converted_iterum/` folder (converted recipes)
✅ `templates/` folder (web UI)
✅ All configuration files

**Nothing will break!** All paths are relative.

---

## 🔧 Optional: Create Desktop Shortcut

### For Web Interface

1. Right-click on Desktop → New → Shortcut
2. Location: `C:\Users\chefm\Iterum Innovation\recipe-library-system\start_web_app.bat`
3. Name: "Recipe Manager Web"
4. Click Finish

Now you can launch from desktop!

### For Quick Access Folder

1. Right-click on Desktop → New → Shortcut
2. Location: `C:\Users\chefm\Iterum Innovation\recipe-library-system`
3. Name: "Recipe Manager"
4. Click Finish

---

## 🚀 New Working Paths

After move:

| Item | New Path |
|------|----------|
| **Main Folder** | `C:\Users\chefm\Iterum Innovation\recipe-library-system` |
| **Database** | `C:\Users\chefm\Iterum Innovation\recipe-library-system\recipe_library\recipe_library.db` |
| **Converted Files** | `C:\Users\chefm\Iterum Innovation\recipe-library-system\converted_iterum` |
| **Web App** | `C:\Users\chefm\Iterum Innovation\recipe-library-system\web_app.py` |

---

## ⚠️ Important Notes

1. **All recipes and data move with it** - Nothing is lost!
2. **Relative paths still work** - No code changes needed
3. **Google Drive credentials** - token.pickle and credentials.json move too
4. **OneDrive** - If old location was in OneDrive, new location won't be (good for performance!)

---

## 🎉 Benefits of New Location

✅ Cleaner organization (not on Desktop)
✅ Professional folder structure
✅ Not in OneDrive (faster, no sync conflicts)
✅ Easier to backup
✅ Better for IT management

---

## 🔄 If You Need to Move Back

Same process, just reverse the paths:

```powershell
Move-Item -Path "C:\Users\chefm\Iterum Innovation\recipe-library-system" -Destination "C:\Users\chefm\OneDrive\Desktop\Recipe Organizer\recipe-library-system"
```

---

## ✅ Verification Checklist

After moving, verify:

- [ ] Folder exists in new location
- [ ] Can open folder and see all files
- [ ] Can run: `py web_app.py`
- [ ] Web interface opens at localhost:5000
- [ ] Can see all recipes in web interface
- [ ] Database intact (check recipe count)
- [ ] Converted files still there

---

**You're all set! Your app is now in the new location! 🎉**

