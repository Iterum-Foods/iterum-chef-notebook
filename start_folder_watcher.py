#!/usr/bin/env python3
"""
Startup script for the Recipe Folder Watcher
This script starts the folder watcher and handles any startup issues.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import watchdog
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def create_folders():
    """Create necessary folders if they don't exist."""
    folders = ["incoming_recipes", "incoming_recipes/archive"]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created folder: {folder}")

def check_backend():
    """Check if the backend is running."""
    try:
        import requests
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print("❌ Backend is not responding properly")
            return False
    except requests.exceptions.RequestException:
        print("❌ Backend is not running")
        print("Please start the backend with: python run.py")
        return False

def start_watcher():
    """Start the folder watcher."""
    print("\n🚀 Starting Recipe Folder Watcher...")
    print("=" * 50)
    
    try:
        # Run the folder watcher
        subprocess.run([sys.executable, "recipe_folder_watcher.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Stopping folder watcher...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running folder watcher: {e}")
        return False
    except FileNotFoundError:
        print("❌ recipe_folder_watcher.py not found")
        return False
    
    return True

def main():
    """Main function."""
    print("🍳 Recipe Folder Watcher Startup")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Create folders
    create_folders()
    
    # Check backend
    if not check_backend():
        print("\n💡 To start the backend:")
        print("1. Open a new terminal")
        print("2. Navigate to your project directory")
        print("3. Run: python run.py")
        print("\nThen run this script again.")
        return False
    
    # Start watcher
    return start_watcher()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 