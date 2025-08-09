#!/usr/bin/env python3
"""
Start Iterum R&D Chef Notebook with HTTPS enabled
"""

import subprocess
import sys
import time
import threading
import os
import webbrowser
import ssl
import http.server
import socketserver
from pathlib import Path

class HTTPSAppManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        self.certs_dir = Path("certs")
        
    def check_certificates(self):
        """Check if SSL certificates exist"""
        cert_file = self.certs_dir / "localhost.pem"
        key_file = self.certs_dir / "localhost-key.pem"
        
        if not cert_file.exists() or not key_file.exists():
            print("❌ SSL certificates not found!")
            print("Run 'python setup_https_local.py' first to generate certificates")
            return False
            
        print("✅ SSL certificates found")
        return True
        
    def start_backend(self):
        """Start the FastAPI backend with HTTPS"""
        print("🚀 Starting HTTPS Backend Server...")
        try:
            python_cmd = "py" if os.name == 'nt' else sys.executable
            
            # Start uvicorn with SSL
            self.backend_process = subprocess.Popen([
                python_cmd, "-m", "uvicorn", "app.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--ssl-keyfile", str(self.certs_dir / "localhost-key.pem"),
                "--ssl-certfile", str(self.certs_dir / "localhost.pem"),
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ HTTPS Backend server started successfully")
                print("   📚 API Documentation: https://localhost:8000/docs")
                print("   💚 Health Check: https://localhost:8000/health")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"❌ Backend server failed to start")
                print(f"   Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"Error starting HTTPS backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the frontend with HTTPS"""
        print("🌐 Starting HTTPS Frontend Server...")
        
        def run_https_server():
            # Change to the directory containing this script
            os.chdir(Path(__file__).parent)
            
            PORT = 8080
            
            class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
                def end_headers(self):
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                    super().end_headers()
                
                def guess_type(self, path):
                    if path.endswith('.js'):
                        return 'application/javascript'
                    elif path.endswith('.css'):
                        return 'text/css'
                    elif path.endswith('.html'):
                        return 'text/html'
                    elif path.endswith('.json'):
                        return 'application/json'
                    return super().guess_type(path)
            
            try:
                # Create SSL context
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain(
                    certfile=str(self.certs_dir / "localhost.pem"),
                    keyfile=str(self.certs_dir / "localhost-key.pem")
                )
                
                # Create HTTPS server
                with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
                    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
                    print(f"✅ HTTPS Frontend server started on https://localhost:{PORT}")
                    httpd.serve_forever()
                    
            except Exception as e:
                print(f"❌ Error starting HTTPS frontend: {e}")
        
        # Run frontend server in a separate thread
        self.frontend_thread = threading.Thread(target=run_https_server)
        self.frontend_thread.daemon = True
        self.frontend_thread.start()
        
        time.sleep(2)
        return True
    
    def open_browser(self):
        """Open the application in the default browser"""
        time.sleep(3)
        try:
            print("Opening Iterum R&D Chef Notebook in your browser...")
            webbrowser.open("https://localhost:8080")
        except Exception as e:
            print(f"Could not open browser: {e}")
    
    def stop_servers(self):
        """Stop both servers"""
        print("\nShutting down HTTPS servers...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            print("HTTPS Backend server stopped")
    
    def run(self):
        """Run the complete HTTPS application"""
        print("🔐" + "=" * 48 + "🔐")
        print("      Iterum R&D Chef Notebook (HTTPS)")
        print("   Professional Recipe R&D and Publishing System")
        print("🔐" + "=" * 48 + "🔐")
        
        # Check certificates
        if not self.check_certificates():
            return False
        
        # Start backend
        if not self.start_backend():
            print("Failed to start HTTPS backend. Exiting...")
            return False
        
        # Start frontend
        if not self.start_frontend():
            print("Failed to start HTTPS frontend. Stopping backend...")
            self.stop_servers()
            return False
        
        # Open browser
        browser_thread = threading.Thread(target=self.open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("\n🎉" + "=" * 48 + "🎉")
        print("    ✨ Iterum R&D Chef Notebook is now running with HTTPS! ✨")
        print("")
        print("    🔐 Frontend Application: https://localhost:8080")
        print("    📚 API Documentation: https://localhost:8000/docs")
        print("    💚 Health Check: https://localhost:8000/health")
        print("")
        print("    🔒 All connections are now encrypted and secure!")
        print("    Press Ctrl+C to stop the servers")
        print("🎉" + "=" * 48 + "🎉")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_servers()
            print("\nThanks for using Iterum R&D Chef Notebook!")
        
        return True

def main():
    """Main entry point"""
    os.chdir(Path(__file__).parent)
    
    # Check if required files exist
    if not Path("app/main.py").exists():
        print("Backend application not found. Please ensure app/main.py exists.")
        return False
    
    # Create and run the HTTPS app manager
    app_manager = HTTPSAppManager()
    return app_manager.run()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)