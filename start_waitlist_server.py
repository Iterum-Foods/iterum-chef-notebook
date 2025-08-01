#!/usr/bin/env python3
"""
Iterum Recipe Library - Waitlist Server Launcher
Starts the FastAPI backend server for waitlist functionality
"""

import os
import sys
import subprocess
import platform

def print_banner():
    print("🍅 ITERUM RECIPE LIBRARY - WAITLIST SERVER")
    print("=" * 50)
    print()

def check_python():
    """Check if Python is available"""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print("❌ Python 3.7+ required. Current version:", sys.version)
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "fastapi", "uvicorn[standard]", "pydantic[email]", "python-multipart"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    print()
    print("Server will be available at:")
    print("  • Main API: http://localhost:8000")
    print("  • API Docs: http://localhost:8000/docs") 
    print("  • Waitlist Admin: http://localhost:8000/waitlist_admin.html")
    print("  • Landing Page: http://localhost:8000/index.html")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to the directory containing this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def main():
    print_banner()
    
    if not check_python():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check if dependencies are installed
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies already installed")
    except ImportError:
        if not install_dependencies():
            input("Press Enter to exit...")
            sys.exit(1)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()