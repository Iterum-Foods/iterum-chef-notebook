#!/usr/bin/env python3
"""
Simple startup script for Iterum R&D Chef Notebook
This is a wrapper that calls the main startup script.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Main entry point - calls the full app startup script"""
    print("🚀 Starting Iterum R&D Chef Notebook...")
    
    # Get the path to the main startup script
    startup_script = Path(__file__).parent / "start_full_app.py"
    
    if not startup_script.exists():
        print("❌ Startup script not found. Please ensure start_full_app.py exists.")
        return False
    
    # Execute the main startup script
    try:
        result = subprocess.run([sys.executable, str(startup_script)], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Shutdown requested by user")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)