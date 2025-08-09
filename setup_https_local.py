#!/usr/bin/env python3
"""
Setup HTTPS for local development using mkcert
This creates trusted certificates for localhost development
"""

import subprocess
import sys
import os
from pathlib import Path

def check_mkcert():
    """Check if mkcert is installed"""
    try:
        subprocess.run(["mkcert", "-version"], capture_output=True, check=True)
        print("✅ mkcert is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ mkcert is not installed")
        return False

def install_mkcert():
    """Install mkcert based on operating system"""
    print("Installing mkcert...")
    
    # Windows
    if os.name == 'nt':
        print("Please install mkcert manually:")
        print("1. Download from: https://github.com/FiloSottile/mkcert/releases")
        print("2. Or use chocolatey: choco install mkcert")
        print("3. Or use scoop: scoop bucket add extras && scoop install mkcert")
        return False
    
    # macOS
    elif sys.platform == 'darwin':
        try:
            subprocess.run(["brew", "install", "mkcert"], check=True)
            print("✅ mkcert installed via brew")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Please install Homebrew first: https://brew.sh/")
            return False
    
    # Linux
    else:
        print("Please install mkcert manually:")
        print("1. Download from: https://github.com/FiloSottile/mkcert/releases")
        print("2. Or use your package manager")
        return False

def setup_certificates():
    """Generate local certificates"""
    certs_dir = Path("certs")
    certs_dir.mkdir(exist_ok=True)
    
    try:
        # Install the local CA
        subprocess.run(["mkcert", "-install"], check=True)
        print("✅ Local CA installed")
        
        # Generate certificates for localhost
        subprocess.run([
            "mkcert", 
            "-cert-file", str(certs_dir / "localhost.pem"),
            "-key-file", str(certs_dir / "localhost-key.pem"),
            "localhost", "127.0.0.1", "::1"
        ], check=True, cwd=os.getcwd())
        
        print("✅ Certificates generated:")
        print(f"   📄 Certificate: {certs_dir / 'localhost.pem'}")
        print(f"   🔑 Private Key: {certs_dir / 'localhost-key.pem'}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating certificates: {e}")
        return False

def main():
    print("🔐 Setting up HTTPS for local development")
    print("=" * 50)
    
    # Check if mkcert is installed
    if not check_mkcert():
        if not install_mkcert():
            print("\n❌ Please install mkcert manually and run this script again")
            sys.exit(1)
    
    # Generate certificates
    if setup_certificates():
        print("\n🎉 HTTPS setup complete!")
        print("\nNext steps:")
        print("1. Run 'python start_https_app.py' to start with HTTPS")
        print("2. Access your app at https://localhost:8000 and https://localhost:8080")
        print("3. Your browser will trust the certificates automatically")
    else:
        print("\n❌ Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()