#!/usr/bin/env python3
"""
Start script for Iterum R&D Chef Notebook with permanent storage
This script starts both the FastAPI backend and the frontend server
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def main():
    print("🚀 Starting Iterum R&D Chef Notebook with Permanent Storage...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Start FastAPI backend
    print("🔧 Starting FastAPI Backend (Port 8000)...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.main:app", 
        "--host", "0.0.0.0", "--port", "8000", "--reload"
    ])
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend server
    print("🌐 Starting Frontend Server (Port 8080)...")
    frontend_process = subprocess.Popen([
        sys.executable, "serve_frontend.py"
    ])
    
    print("=" * 60)
    print("✅ Both servers started successfully!")
    print()
    print("📱 Frontend URL: http://localhost:8080")
    print("🔧 Backend API: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print()
    print("💾 Permanent Storage Features:")
    print("   • SQLite database: culinary_data.db")
    print("   • Data export/import via JSON")
    print("   • Backup to local storage")
    print("   • Automatic data persistence")
    print()
    print("🛑 Press Ctrl+C to stop both servers")
    print("=" * 60)

    # Wait a moment for frontend server to start, then open browser
    time.sleep(2)
    print("🌐 Opening app in your default browser...")
    url = "http://localhost:8080/index.html"
    try:
        import webbrowser
        opened = webbrowser.open_new_tab(url)
        if not opened:
            raise Exception("webbrowser.open_new_tab returned False")
    except Exception as e:
        print(f"[WARN] Could not open browser automatically: {e}")
        if sys.platform.startswith('win'):
            os.system(f'start {url}')
        else:
            print(f"Please open this URL manually: {url}")
    
    try:
        # Keep the script running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main() 