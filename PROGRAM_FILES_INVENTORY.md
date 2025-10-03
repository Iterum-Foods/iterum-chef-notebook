# Iterum R&D Chef Notebook - Program Files Inventory

## 🎉 Application Status: RUNNING SUCCESSFULLY
- **Backend API**: http://localhost:8000 ✅
- **Frontend App**: http://localhost:8080 ✅
- **API Docs**: http://localhost:8000/docs ✅
- **Health Check**: http://localhost:8000/health ✅

---

## 📁 Core Application Files

### **Backend API (FastAPI)**
```
app/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI application entry point
├── database.py                 # Database connection and setup
├── sqlite_database.py          # SQLite database utilities
├── schemas.py                  # Pydantic models for API validation
├── core/
│   ├── auth.py                 # Authentication logic
│   ├── config.py               # Application configuration
│   ├── error_handler.py        # Error handling middleware
│   ├── health.py               # Health check endpoints
│   ├── logger.py               # Logging configuration
│   ├── settings.py             # Settings management
│   └── test_settings.py        # Test environment settings
├── models/
│   ├── multi_tenant.py         # Multi-tenant data models
│   └── project.py              # Project-related models
├── routers/                    # API endpoint routers
│   ├── auth.py                 # Authentication endpoints
│   ├── autosave.py             # Auto-save functionality
│   ├── data.py                 # Data management endpoints
│   ├── images.py               # Image handling endpoints
│   ├── ingredients.py          # Ingredient management
│   ├── integrations.py         # Third-party integrations
│   ├── menu.py                 # Menu processing endpoints
│   ├── multi_tenant_auth.py    # Multi-tenant auth
│   ├── profiles.py             # User profile management
│   ├── projects.py             # Project management
│   ├── recipe_scaling.py       # Recipe scaling features
│   ├── recipes.py              # Recipe CRUD operations
│   ├── uploads.py              # File upload handling
│   ├── vendors.py              # Vendor management
│   ├── versions.py             # Version control
│   ├── waitlist.py             # Waitlist management
│   └── workflow.py             # Workflow automation
└── services/                   # Business logic services
    ├── complete_workflow.py    # End-to-end workflow
    ├── menu_parser.py          # Menu parsing logic
    ├── ocr_processor.py        # OCR processing (main)
    ├── ocr_processor_fallback.py # OCR fallback methods
    ├── recipe_finder.py        # Recipe discovery
    ├── recipe_parser.py        # Recipe parsing logic
    └── recipe_uploader.py      # Recipe upload handling
```

### **Frontend Application (HTML/JS)**
```
Main Pages:
├── index.html                  # Dashboard/Home page
├── dashboard.html              # Main dashboard
├── recipe-library.html         # Recipe management
├── recipe-developer.html       # Recipe development tools
├── recipe-upload.html          # Recipe upload interface
├── recipe-review.html          # Recipe review system
├── recipe-scaling-tool.html    # Recipe scaling calculator
├── ingredients.html            # Ingredient management
├── inventory.html              # Inventory tracking
├── menu-builder.html           # Menu creation tools
├── equipment-management.html   # Equipment database
├── vendor-management.html      # Vendor management
└── plant-sketches.html         # Plant sketches integration

Demo & Test Pages:
├── auto_save_demo.html         # Auto-save demonstration
├── automated-workflow.html     # Workflow automation demo
├── email_templates.html        # Email template system
├── google-test.html            # Google integration testing
├── ingredient_demo.html        # Ingredient demo
├── landing_page.html           # Alternative landing page
├── LOADING_SCREEN_DEMO.html    # Loading screen test
├── nordic-header-template.html # Header template
├── PROJECT_MODAL_DEMO.html     # Project modal demo
├── PROJECT_UI_TEST.html        # Project UI testing
├── test_auth_buttons_all_pages.html # Auth testing
├── test_main_login.html        # Login system testing
└── waitlist_admin.html         # Waitlist administration
```

### **JavaScript Modules**
```
assets/js/
├── auto_save_config.js         # Auto-save configuration
├── auto_save_system.js         # Auto-save implementation
├── bakers_percentage_calculator.js # Baking calculations
├── calendarManager.js          # Calendar functionality
├── data_export_import.js       # Data import/export
├── debug_auth_buttons.js       # Authentication debugging
├── enhanced_default_equipment.js # Equipment defaults
├── enhanced_loading_system.js  # Loading screen system
├── enhanced_search_system.js   # Search functionality
├── enhanced-project-modal.js   # Project modal
├── equipmentManager.js         # Equipment management
├── error_handler.js            # Frontend error handling
├── haccpManager.js             # HACCP compliance
├── imageUploadManager.js       # Image upload system
├── ingredient_search_widget.js # Ingredient search
├── ingredientLibrary.js        # Ingredient database
├── inventoryManager.js         # Inventory management
├── main.js                     # Main application JS
├── menuManager.js              # Menu management
├── modern_dashboard.js         # Dashboard functionality
├── profileManager.js           # User profile management
├── project-management-system.js # Project management
├── PROJECT_SELECTOR_FIX.js     # Project selector fixes
├── recipeImportExport.js       # Recipe import/export
├── recipeLibrary.js            # Recipe library
├── recipeReview.js             # Recipe review system
├── recipeScaling.js            # Recipe scaling logic
├── standardize-login-modals.js # Login standardization
├── startup-loading-config.js   # Startup loading control
├── unified_auth_system.js      # Unified authentication
└── userDataManager.js          # User data management
```

---

## 🔧 Startup & Configuration Files

### **Startup Scripts**
```
scripts/startup/
├── START_APP_FIXED.bat         # Fixed Windows launcher (RECOMMENDED)
├── START_APP.bat               # Basic Windows launcher
├── START_ADMIN_SERVER.bat      # Admin server launcher
├── START_SERVERS.bat           # Multi-server launcher
└── OPEN_FRONTEND.bat           # Frontend-only launcher

scripts/
├── start_full_app.py           # Python full app launcher (MAIN)
├── serve_frontend.py           # Frontend HTTP server
├── start.py                    # Alternative startup
├── start_https_app.py          # HTTPS startup
├── start_secure.py             # Secure startup
└── start_waitlist_server.py    # Waitlist server
```

### **Configuration Files**
```
Root Level:
├── requirements.txt            # Python dependencies
├── package.json               # Node.js dependencies
├── pytest.ini                 # Testing configuration
├── env.https.example           # Environment variables example
└── README.md                   # Main documentation

Config Directory:
config/
└── (API configuration files)
```

---

## 🗄️ Data & Database Files

### **Database Files**
```
data/
├── culinary_data.db           # Main application database
├── iterum_rnd.db              # R&D database
└── waitlist.db                # Waitlist database

Root Level:
└── culinary_data.db           # Backup/alternative database
```

### **Data Files**
```
├── equipment_database.csv     # Equipment database
├── Ingredient Database-Sheet1.csv.txt # Ingredient data
└── Korean-Inspired Bulgogi-Spiced... .pdf # Sample recipe
```

---

## 📚 Documentation & Templates

### **Documentation**
```
documentation/
├── API_FIX_SUMMARY.md
├── APP_OPENING_STEPS.md        # How to start the app
├── AUTOMATED_UPLOAD_GUIDE.md
├── BRAND_GUIDE.md
├── COMPREHENSIVE_README.md
├── DEPLOYMENT.md
├── FEATURE_MAP.md
├── LOADING_SCREEN_FIX.md       # Loading screen fixes
├── ORGANIZATION_SUMMARY.md     # File organization
├── QUICK_START_GUIDE.md
├── TESTING_GUIDE.md
└── [60+ more documentation files]
```

### **Template Files**
```
templates/
├── shared-login-modal.html     # Shared login template
├── uniform-header-template.html # Standard header
├── uniform-footer-template.html # Standard footer
└── nordic-header-template.html  # Alternative header
```

---

## 🧪 Testing & Development Files

### **Test Files**
```
tests/
├── test_api.py                 # API testing
├── test_auth.py                # Authentication tests
├── test_recipes.py             # Recipe functionality tests
├── test_startup.py             # Startup process tests
└── __init__.py

Test Scripts:
scripts/
├── test_app.py                 # Application testing
├── test_loading_screen.py      # Loading screen tests
├── test_menu_processing.py     # Menu processing tests
├── test_ocr_system.py          # OCR system tests
└── run_tests.py                # Test runner
```

### **Migration Files**
```
migrations/
├── 001_add_review_fields.py
├── 002_add_user_profile_fields.py
├── 003_add_project_system.py
└── 004_add_ocr_fields.py
```

---

## 🌐 Website & Documentation

### **Public Website Files**
```
docs/
├── index.html                  # Main landing page
├── about.html                  # About page
├── company.html                # Company information
├── ecosystem.html              # App ecosystem
├── lifetime-companion.html     # Product positioning
├── sandbox.html                # Sandbox concept
├── research.html               # User research
├── admin-login.html            # Admin interface
└── waitlist_admin.html         # Waitlist management
```

---

## 📦 Build & Deployment Files

### **Environment & Packaging**
```
├── venv/                       # Python virtual environment
├── node_modules/               # Node.js dependencies
├── package-lock.json           # Locked dependency versions
├── LICENSE                     # Software license
└── organize_files.ps1          # File organization script
```

---

## 🎯 Quick Start Commands

### **To Start the Application:**
```bash
# Method 1: Use the fixed batch file (RECOMMENDED)
cd scripts\startup
.\START_APP_FIXED.bat

# Method 2: Manual Python startup
.\venv\Scripts\Activate.ps1
py scripts\start_full_app.py
```

### **Application URLs:**
- **Main App**: http://localhost:8080
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📊 File Statistics
- **Total Python Files**: ~100+
- **Total JavaScript Files**: ~35
- **Total HTML Files**: ~40+
- **Total Documentation Files**: ~70+
- **Database Files**: 3
- **Configuration Files**: ~10

**Status**: ✅ All critical files verified and application running successfully!
