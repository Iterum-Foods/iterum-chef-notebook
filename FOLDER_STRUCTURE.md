# 📁 Iterum Innovation - Folder Structure

**New Location:** `C:\Users\chefm\Iterum Innovation`

This document explains the organized folder structure of the Iterum Culinary App.

---

## 🏠 Root Directory Files

### Essential Files (Keep at Root):
- `index.html` - Main application entry point
- `launch.html` - Landing/marketing page
- `package.json` / `package-lock.json` - Node.js dependencies
- `firebase.json` / `.firebaserc` - Firebase configuration
- `firestore.rules` - Database security rules
- `.env` - Environment variables
- `.gitignore` - Git ignore rules
- `LICENSE` - Software license

---

## 📂 Main Folders

### `/pages` (61 HTML pages)
**Application Pages** - All main feature pages
- Recipe management: `recipe-developer.html`, `recipe-library.html`, `recipe-upload.html`
- Menu management: `menu-builder.html`
- Ingredients: `ingredients.html`, `bulk-ingredient-import.html`
- Equipment: `equipment-management.html`
- Vendors: `vendor-management.html`, `vendor-price-comparison.html`
- Kitchen: `kitchen-management.html`, `production-planning.html`, `inventory.html`
- User management: `user-profile.html`, `user_management.html`
- Project: `project-hub.html`
- Data: `data-backup-center.html`, `data-management-dashboard.html`
- Admin: `chef-dashboard.html`, `audit-log.html`
- And more...

### `/test-pages` (34 HTML pages)
**Testing & Diagnostics** - All test and verification pages
- Authentication tests: `test_auth_*.html`
- Feature tests: `test_recipe_*.html`, `test_menu_*.html`
- Cross-device sync tests
- Firebase connection tests
- Debug pages

### `/docs-markdown` (247 MD files)
**Documentation** - All markdown documentation
- Implementation guides
- Feature summaries
- Deployment instructions
- Testing checklists
- System architecture docs
- Change logs
- Quick reference guides

### `/assets`
**Frontend Resources** (128 files)
- `/css` - Stylesheets (design system, themes, component styles)
- `/js` - JavaScript modules (managers, utilities, systems)
- `/images` - Images and icons
- `/fonts` - Custom fonts (if any)

### `/data-files` (10 files)
**Data Files** - JSON exports and databases
- `89-charles-recipes.json`
- `89-charles-fall-menu.json`
- `89-charles-prep-specs.json`
- `*.db` - SQLite databases
- `*.csv` - Ingredient/equipment data
- `*.pdf` - Recipe PDFs

### `/config-files` (19 files)
**Configuration Files**
- `.eslintrc.js` - Linting rules
- `.prettierrc` - Code formatting
- `tailwind.config.js` - Tailwind CSS config
- `jest.config.js` - Testing framework
- `playwright.config.js` - E2E testing
- `postcss.config.js` - CSS processing
- And other config files

### `/scripts` (71 files)
**Automation Scripts**
- `deploy_to_firebase.bat` - Firebase deployment
- `start_app_simple.bat` - Local development
- `*.py` - Python utility scripts
- `*.ps1` - PowerShell scripts
- `*.js` - Node.js scripts

### `/data`
**User Data Storage** (4 files)
- `base-ingredients-database.json`
- User-specific data files

### `/venv` (28,697 files)
**Python Virtual Environment**
- Python packages and dependencies
- Backend requirements

### `/node_modules` (3,319 files)
**Node.js Packages**
- Frontend JavaScript libraries
- Development dependencies

---

## 🗄️ Archive & Backup Folders

### `/archive` (159 files)
Old versions and deprecated files

### `/archive-old-pages` (17 files)
Deprecated HTML pages

### `/Recipe Library` (316 files)
Legacy recipe library system

### `/recipe-library-system` (410 files)
Alternative recipe system implementation

---

## 🏢 Additional App Folders

### `/app`
Core application files (90 files)

### `/App-starting a business` (70,558 files)
Business startup application module

### `/Skills App` (38,759 files)
Skills management application

### `/payroll app` (73 files)
Payroll management module

### `/landing-pages` (33 files)
Marketing and landing page templates

---

## 🔧 Development Folders

### `/tests` (8 files)
Unit and integration test files

### `/test` (11 files)
Additional test files

### `/Test files` (11 files)
Test data and fixtures

### `/migrations` (5 files)
Database migration scripts

### `/logs` (1 file)
Application and server logs

---

## 🎨 Frontend Folders

### `/static`
Static assets served directly

### `/templates` (6 files)
HTML templates for backend rendering

### `/docs` (16 files)
Additional documentation

### `/documentation` (67 files)
Extended documentation files

---

## 📦 Other Folders

### `/profiles` (5 files)
User profile data

### `/users` (1 file)
User-related files

### `/uploads` (37 files)
User-uploaded content

### `/incoming_recipes` (1 file)
Recipe import queue

### `/iterum-test-distribution` (89 files)
Test distribution package

---

## 🚀 Quick Start

### Local Development:
```bash
cd "C:\Users\chefm\Iterum Innovation"
start scripts\start_app_simple.bat
```

### Open in Browser:
```
http://localhost:8000
```

### Deploy to Firebase:
```bash
cd "C:\Users\chefm\Iterum Innovation"
.\scripts\deploy_to_firebase.bat
```

---

## 📋 File Count Summary

| Folder | Files |
|--------|-------|
| Total Project | ~175,000+ files |
| Application Pages | 61 |
| Test Pages | 34 |
| Documentation | 247 |
| Assets (CSS/JS) | 128 |
| Data Files | 10 |
| Scripts | 71 |
| Node Modules | 3,319 |
| Python venv | 28,697 |

---

## 🔍 Finding Files

### Main Application Pages:
Look in `/pages`

### Feature Documentation:
Look in `/docs-markdown`

### Test & Debug Pages:
Look in `/test-pages`

### Data Files:
Look in `/data-files`

### Scripts:
Look in `/scripts`

---

## 💡 Tips

1. **Keep root clean** - Only essential config files at root
2. **Pages organized** - All `.html` pages in `/pages` or `/test-pages`
3. **Docs centralized** - All `.md` files in `/docs-markdown`
4. **Data separated** - Data files in `/data-files`
5. **Scripts together** - All automation in `/scripts`

---

**Last Updated:** October 21, 2025  
**Organization Completed:** ✅

---

*This structure makes it easy to find files, deploy to Firebase, and maintain the codebase.*


