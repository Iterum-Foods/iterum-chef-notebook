# 🚀 Quick Start Guide - Iterum R&D Chef Notebook

## How to Start the Application

**Single Command Startup:**

```bash
py start.py
```

or 

```bash
py start_full_app.py
```

*Note: Use `py` on Windows or `python` on Mac/Linux*

## What This Does

✅ **Starts Backend API** (FastAPI) on http://localhost:8000
✅ **Starts Frontend Server** on http://localhost:8080  
✅ **Opens Your Browser** automatically to http://localhost:8080
✅ **Handles Graceful Shutdown** with Ctrl+C

## Access Points

- **Main Application**: http://localhost:8080
- **API Documentation**: http://localhost:8000/docs
- **Menu Upload Feature**: Available in the main application
- **Health Check**: http://localhost:8000/health

## Menu Upload Features

The application now supports:
- **PDF Menu Upload** with text extraction
- **Word Document Upload** (.docx) with text extraction
- **Interactive Menu Building** with sections and items
- **Staff Training Materials** generation
- **Prep List Creation** for kitchen workflow

## User Session Management 👤

**The application now maintains your login session:**
- ✅ **Stays logged in** across page refreshes
- ✅ **Remembers your login** when navigating between pages  
- ✅ **Persists until** you explicitly log out or close the app
- ✅ **Switch users** without losing session data

**Default test login:**
- **Username:** `testuser`
- **Password:** `testpass123`

## Stopping the Application

Press **Ctrl+C** in the terminal to stop both servers gracefully.

## Troubleshooting

If you get Python errors, make sure you have the required dependencies:
```bash
pip install -r requirements.txt
```

If the servers don't start, check that ports 8000 and 8080 are available.