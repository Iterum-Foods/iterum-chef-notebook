# Iterum R&D Chef Notebook - Tester Setup Instructions

## 🚀 Quick Start for Testers

This is a **professional recipe R&D and publishing system** for home and commercial kitchens.

### 📋 What You're Testing

**Iterum R&D Chef Notebook** includes:
- Professional recipe R&D and publishing system
- User authentication and profiles  
- Recipe management with versioning
- Ingredient database
- File upload and processing
- Vendor and equipment management
- Menu building capabilities
- Automated workflow processing
- Data export/import functionality

---

## 🔧 Setup Requirements

### 1. Python Installation
You need **Python 3.11 or higher**. Check if installed:
```bash
python --version
```

If not installed, download from: https://python.org/downloads

### 2. Required Dependencies
Install core dependencies:
```bash
python -m pip install fastapi uvicorn sqlalchemy pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart pandas openpyxl
```

---

## 🧪 Testing Process

### Step 1: Quick System Test
Run the system validation test:
```bash
python simple_test.py
```

**Expected Result:** 5-6 tests should pass, showing:
- ✅ Python environment working
- ✅ Project structure complete
- ✅ Core imports working
- ✅ Database models functional
- ✅ FastAPI application creation

### Step 2: Clear Users (Optional)
If you need to reset all user data:
```bash
python clear_users.py
```

### Step 3: Start the Backend API
```bash
python -c "import uvicorn; from app.main import app; uvicorn.run(app, host='0.0.0.0', port=8000)"
```

The API will be available at: http://localhost:8000

### Step 4: API Documentation
Once running, visit:
- **Interactive API docs:** http://localhost:8000/docs
- **Alternative docs:** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/health

---

## 🎯 Key API Endpoints to Test

### Authentication
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - User login

### Recipes
- `GET /api/recipes/` - List recipes
- `POST /api/recipes/` - Create recipe
- `GET /api/recipes/{id}` - Get specific recipe

### Ingredients  
- `GET /api/ingredients/` - List ingredients
- `POST /api/ingredients/` - Add ingredient

### Health Checks
- `GET /` - Basic status
- `GET /health` - Simple health check
- `GET /health/detailed` - Detailed system status

---

## 🗂️ Project Structure

```
iterum-test-distribution/
├── app/                    # FastAPI backend application
│   ├── core/              # Core configuration and utilities
│   ├── routers/           # API route handlers
│   ├── main.py           # Application entry point
│   ├── database.py       # Database models
│   └── schemas.py        # Pydantic schemas
├── tests/                 # Test files
├── simple_test.py        # System validation script
├── clear_users.py        # User management script
├── requirements.txt      # Python dependencies
├── package.json         # Node.js dependencies
└── pytest.ini          # Test configuration
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "python not recognized"**
- Solution: Install Python from python.org
- Or use full path: `"C:\Users\[USERNAME]\AppData\Local\Programs\Python\Python313\python.exe"`

**2. "Module not found" errors**
- Solution: Install missing dependencies:
  ```bash
  python -m pip install [missing-module]
  ```

**3. Database errors**
- The app uses SQLite (no setup required)
- Database files are created automatically

**4. Port already in use**
- Change port: `uvicorn app.main:app --port 8001`

---

## 📊 Testing Checklist

### ✅ Backend API Testing
- [ ] System validation test passes
- [ ] API server starts successfully
- [ ] Health check endpoints respond
- [ ] User registration works
- [ ] User login works
- [ ] Recipe creation works
- [ ] Recipe listing works
- [ ] Ingredient management works

### ✅ Data Testing
- [ ] User data persists
- [ ] Recipe data saves correctly
- [ ] Database relationships work
- [ ] Data export functions

### ✅ Error Handling
- [ ] Invalid login attempts
- [ ] Missing data validation
- [ ] API error responses

---

## 📞 Support

If you encounter issues:

1. **Run the diagnostic test:** `python simple_test.py`
2. **Check the error logs** in the terminal output
3. **Verify all dependencies** are installed
4. **Ensure Python 3.11+** is being used

---

## 🎉 Success Criteria

The system is working correctly when:
- ✅ System test shows 5-6 passing tests
- ✅ API server starts without errors
- ✅ Health check returns "healthy" status
- ✅ You can create and login users
- ✅ You can create and view recipes
- ✅ Database operations work correctly

**This is a professional-grade recipe R&D system ready for kitchen use!** 