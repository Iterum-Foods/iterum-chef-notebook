#!/usr/bin/env python3
"""
Launch script for the Iterum R&D marketing website and waitlist system.
This script starts the FastAPI backend and serves the marketing assets.
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def check_python_packages():
    """Check if required packages are installed"""
    required_packages = ['fastapi', 'uvicorn', 'pydantic', 'email-validator']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            if package == 'email-validator':
                # pydantic[email] includes email-validator
                try:
                    from pydantic import EmailStr
                except ImportError:
                    missing_packages.append('pydantic[email]')
            else:
                missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n💡 Install with: pip install fastapi uvicorn pydantic[email]")
        return False
    
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting Iterum R&D Marketing Backend...")
    
    try:
        # Start the backend server
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it a moment to start
        time.sleep(3)
        
        # Check if it's running
        if backend_process.poll() is None:
            print("✅ Backend server started on http://localhost:8000")
            return backend_process
        else:
            stdout, stderr = backend_process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the frontend server for static files"""
    print("🌐 Starting Frontend Server...")
    
    try:
        # Start the frontend server
        frontend_process = subprocess.Popen([
            sys.executable, "serve_frontend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if it's running
        if frontend_process.poll() is None:
            print("✅ Frontend server started on http://localhost:8080")
            return frontend_process
        else:
            stdout, stderr = frontend_process.communicate()
            print(f"❌ Frontend failed to start:")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def open_browser():
    """Open the marketing website in the default browser"""
    marketing_url = "http://localhost:8080/landing_page.html"
    admin_url = "http://localhost:8080/waitlist_admin.html"
    
    print(f"🌐 Opening marketing website: {marketing_url}")
    webbrowser.open(marketing_url)
    
    print(f"📊 Admin dashboard available at: {admin_url}")

def main():
    """Main launch function"""
    print("🍅 ITERUM R&D MARKETING LAUNCH")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("landing_page.html"):
        print("❌ landing_page.html not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check Python packages
    if not check_python_packages():
        sys.exit(1)
    
    print("✅ All requirements satisfied")
    print()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server")
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend server")
        backend_process.terminate()
        sys.exit(1)
    
    print()
    print("🎉 MARKETING WEBSITE LAUNCHED!")
    print("=" * 40)
    print("📝 Landing Page:     http://localhost:8080/landing_page.html")
    print("📊 Admin Dashboard:  http://localhost:8080/waitlist_admin.html")
    print("🔧 API Docs:         http://localhost:8000/docs")
    print("🍅 App Demo:         http://localhost:8080/ingredient_demo.html")
    print()
    
    # Open browser
    open_browser()
    
    try:
        print("⌨️  Press Ctrl+C to stop all servers")
        
        # Keep the script running and monitor processes
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process died unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process died unexpectedly")
                break
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        
        # Terminate processes
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            print("✅ Backend server stopped")
        
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            print("✅ Frontend server stopped")
        
        print("👋 Marketing website shutdown complete")

if __name__ == "__main__":
    main()