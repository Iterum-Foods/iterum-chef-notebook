#!/usr/bin/env python3
"""
Automated Recipe Workflow Startup Script
Quick start script for the Iterum Automated Recipe Workflow system.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print the startup banner"""
    print("=" * 70)
    print("🍳 Iterum Automated Recipe Workflow System")
    print("=" * 70)
    print("This system will help you:")
    print("1. Find and analyze recipe files automatically")
    print("2. Organize them by cuisine and category")
    print("3. Upload them to your Iterum app backend")
    print("4. Archive processed files")
    print("=" * 70)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'requests',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_folders():
    """Check if required folders exist"""
    print("\n📁 Checking folder structure...")
    
    required_folders = [
        'uploads',
        'app',
        'app/routers',
        'app/services'
    ]
    
    missing_folders = []
    
    for folder in required_folders:
        if Path(folder).exists():
            print(f"✅ {folder}/")
        else:
            print(f"❌ {folder}/ (missing)")
            missing_folders.append(folder)
    
    if missing_folders:
        print(f"\n⚠️  Missing folders: {', '.join(missing_folders)}")
        print("Please ensure you're running this from the Iterum App directory.")
        return False
    
    print("✅ All required folders exist!")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("\n🚀 Starting backend server...")
    
    try:
        # Check if backend is already running
        import requests
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is already running!")
                return True
        except:
            pass
        
        # Start the backend
        print("Starting FastAPI server on http://localhost:8000")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the backend server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped by user")
        return False
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def open_workflow_interface():
    """Open the workflow interface in the default browser"""
    import webbrowser
    import time
    
    print("\n🌐 Opening workflow interface...")
    time.sleep(2)  # Give backend time to start
    
    try:
        webbrowser.open("http://localhost:8000/automated-workflow.html")
        print("✅ Workflow interface opened in browser!")
        print("\n📋 Next steps:")
        print("1. Configure your source folder (default: 'uploads')")
        print("2. Set your backend URL (default: 'http://localhost:8000')")
        print("3. Add optional authentication credentials")
        print("4. Click 'Validate Prerequisites' to check everything")
        print("5. Click 'Start Complete Workflow' to begin")
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        print("Please manually open: http://localhost:8000/automated-workflow.html")

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        return
    
    # Check folders
    if not check_folders():
        print("\n❌ Please ensure you're in the correct directory and try again.")
        return
    
    print("\n✅ System is ready to start!")
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Start backend server only")
    print("2. Start backend and open workflow interface")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            start_backend()
            break
        elif choice == "2":
            # Start backend in background
            print("\n🚀 Starting backend server in background...")
            try:
                # Start backend process
                backend_process = subprocess.Popen([
                    sys.executable, "-m", "uvicorn", 
                    "app.main:app", 
                    "--host", "0.0.0.0", 
                    "--port", "8000", 
                    "--reload"
                ])
                
                # Wait a moment for server to start
                time.sleep(3)
                
                # Open workflow interface
                open_workflow_interface()
                
                print("\n🔄 Backend server is running in the background.")
                print("Press Enter to stop the server when you're done...")
                input()
                
                # Stop the backend
                backend_process.terminate()
                print("🛑 Backend server stopped.")
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping backend server...")
                if 'backend_process' in locals():
                    backend_process.terminate()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break
                
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 