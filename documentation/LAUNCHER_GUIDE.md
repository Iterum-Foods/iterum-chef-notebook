# 🚀 Application Launcher Guide

## Which Files Should I Use? (Clear Answer!)

### ✅ **MAIN ENTRY POINTS** (Use These!)

1. **`start.bat`** - **PRIMARY APP LAUNCHER** 
   - **Double-click this file to start the main application**
   - Simple, clear entry point for the full culinary app
   - Automatically launches with recommended settings

2. **`launch_marketing.bat`** - **MARKETING WEBSITE LAUNCHER** 
   - **Double-click this file to start the marketing website**
   - Launches landing page, waitlist system, and demos
   - Perfect for showcasing the app to potential users

3. **`test_unified.bat`** - **TESTING**
   - Run this to test the application
   - Interactive menu with quick/full/CI test options

### 🔧 **ADVANCED OPTIONS** (For Power Users)

4. **`launch_unified.bat`** - **ADVANCED APP LAUNCHER**
   - Interactive menu with multiple launch modes
   - Command-line options available
   - Backend-only, frontend-only, quiet modes

5. **`launch_marketing.py`** - **MARKETING SCRIPT LAUNCHER**
   - Python script for marketing website
   - Automated backend + frontend server startup
   - Used by `launch_marketing.bat`

6. **`app_launcher.py`** - **PROGRAMMATIC APP LAUNCHER**
   - Python script for main application
   - Full control over ports and launch modes
   - Used by the main batch files above

---

## ❌ **OLD FILES** (Don't Use These!)

These files are outdated and will be removed:

- ❌ `launch-notebook.bat` - **OUTDATED** (use `start.bat` instead)
- ❌ `launch-notebook.py` - **OUTDATED** (functionality merged into `app_launcher.py`)
- ❌ `start_app.bat` - **OUTDATED** (use `start.bat` instead)  
- ❌ `start_full_app.py` - **OUTDATED** (functionality merged into `app_launcher.py`)
- ❌ `serve_frontend.py` - **OUTDATED** (functionality merged into `app_launcher.py`)
- ❌ `start_here.bat` - **MISSING** (archived, use `start.bat` instead)

---

## 🎯 **Quick Decision Guide**

**Just want to start the main app?**
👉 **Double-click `start.bat`**

**Want to show the marketing website?**
👉 **Double-click `launch_marketing.bat`**

**Want to test the app?**
👉 **Double-click `test_unified.bat`**

**Need advanced launch options?**
👉 **Use `launch_unified.bat`**

**Developing/scripting the main app?**
👉 **Use `python app_launcher.py --mode <option>`**

**Developing/scripting the marketing site?**
👉 **Use `python launch_marketing.py`**

---

## 🧹 **Clean Up Old Files**

Run this to remove the outdated files:
```bash
python cleanup_consolidated_files.py
```

This will safely archive old files and leave only the current ones.

---

## 🔄 **Migration Summary**

| Old File | New File | Notes |
|----------|----------|-------|
| `launch-notebook.bat` | `start.bat` or `launch_unified.bat` | Simplified main entry |
| `start_app.bat` | `start.bat` or `launch_unified.bat` | Unified launcher |
| `start_here.bat` | `start.bat` | Clear main entry point |
| `launch-notebook.py` | `app_launcher.py` | All functionality preserved |
| `start_full_app.py` | `app_launcher.py` | Consolidated features |
| `serve_frontend.py` | `app_launcher.py` | Integrated server |

**Result**: 6+ confusing files → 2 main files (`start.bat` + `test_unified.bat`) ✨ 