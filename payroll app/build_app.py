#!/usr/bin/env python3
"""
Build script for Payroll App
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed successfully!")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # PyInstaller command with optimized settings
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=PayrollApp",            # Executable name
        "--icon=icon.ico",              # Icon (if available)
        "--add-data=profiles;profiles", # Include profiles directory
        "--hidden-import=tkcalendar",   # Ensure tkcalendar is included
        "--hidden-import=openpyxl",     # Ensure openpyxl is included
        "--hidden-import=babel",        # Ensure babel is included
        "--clean",                      # Clean cache
        "payroll_gui_advanced.py"
    ]
    
    # Remove icon option if icon doesn't exist
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    subprocess.run(cmd, check=True)
    print("Executable built successfully!")

def create_distribution():
    """Create distribution folder with executable and necessary files"""
    print("Creating distribution...")
    
    # Create dist folder structure
    dist_dir = "dist/PayrollApp"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Copy executable
    if os.path.exists("dist/PayrollApp.exe"):
        shutil.copy("dist/PayrollApp.exe", dist_dir)
    
    # Copy profiles directory
    if os.path.exists("profiles"):
        shutil.copytree("profiles", os.path.join(dist_dir, "profiles"))
    
    # Create README
    readme_content = """# Professional Payroll System

## Installation
1. Extract all files to a folder
2. Run PayrollApp.exe
3. Create or select a profile to get started

## Features
- Multi-profile support for different businesses
- Employee management
- Payroll calculation and processing
- Tax calculations
- Export to Excel and CSV
- Auto-save functionality

## System Requirements
- Windows 10 or later
- No additional software required (standalone executable)

## Support
For support, contact your system administrator.
"""
    
    with open(os.path.join(dist_dir, "README.txt"), "w") as f:
        f.write(readme_content)
    
    print(f"Distribution created in: {dist_dir}")

def main():
    """Main build process"""
    print("=== Payroll App Build Process ===")
    
    try:
        # Step 1: Install dependencies
        install_dependencies()
        
        # Step 2: Build executable
        build_executable()
        
        # Step 3: Create distribution
        create_distribution()
        
        print("\n=== Build Complete! ===")
        print("Your executable is ready in: dist/PayrollApp/")
        print("You can distribute the entire PayrollApp folder.")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
