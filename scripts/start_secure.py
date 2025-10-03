#!/usr/bin/env python3
"""
Quick start script for Iterum R&D Chef Notebook with HTTPS options
"""

import sys
import subprocess
from pathlib import Path

def print_banner():
    print("🔐" + "=" * 50 + "🔐")
    print("    Iterum R&D Chef Notebook - Secure Startup")
    print("🔐" + "=" * 50 + "🔐")

def check_certificates():
    """Check if SSL certificates exist"""
    cert_path = Path("certs/localhost.pem")
    key_path = Path("certs/localhost-key.pem")
    return cert_path.exists() and key_path.exists()

def setup_certificates():
    """Setup SSL certificates"""
    print("\n🔧 Setting up SSL certificates...")
    try:
        result = subprocess.run([sys.executable, "setup_https_local.py"], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("❌ Failed to setup certificates")
        return False
    except FileNotFoundError:
        print("❌ setup_https_local.py not found")
        return False

def start_https():
    """Start with HTTPS"""
    print("\n🚀 Starting with HTTPS...")
    try:
        subprocess.run([sys.executable, "start_https_app.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to start HTTPS app")
        return False
    except FileNotFoundError:
        print("❌ start_https_app.py not found")
        return False

def start_http():
    """Start with HTTP (fallback)"""
    print("\n🚀 Starting with HTTP...")
    try:
        subprocess.run([sys.executable, "start_full_app.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to start HTTP app")
        return False
    except FileNotFoundError:
        print("❌ start_full_app.py not found")
        return False

def main():
    print_banner()
    
    print("\nChoose your startup option:")
    print("1. 🔐 Start with HTTPS (recommended)")
    print("2. 🌐 Start with HTTP (standard)")
    print("3. 🔧 Setup HTTPS certificates only")
    print("4. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                # HTTPS startup
                if not check_certificates():
                    print("\n⚠️  SSL certificates not found!")
                    setup_choice = input("Setup certificates now? (y/N): ").strip().lower()
                    if setup_choice in ['y', 'yes']:
                        if not setup_certificates():
                            print("❌ Certificate setup failed. Falling back to HTTP.")
                            return start_http()
                    else:
                        print("❌ Cannot start HTTPS without certificates. Falling back to HTTP.")
                        return start_http()
                
                return start_https()
            
            elif choice == "2":
                # HTTP startup
                return start_http()
            
            elif choice == "3":
                # Setup certificates only
                return setup_certificates()
            
            elif choice == "4":
                # Exit
                print("👋 Goodbye!")
                return True
            
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return True
        except EOFError:
            print("\n👋 Goodbye!")
            return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)