#!/usr/bin/env python3
"""
Unified Application Launcher for Iterum R&D Chef Notebook
Consolidates all launch functionality with multiple modes and error handling
"""

import subprocess
import sys
import time
import threading
import os
import webbrowser
import http.server
import socketserver
import argparse
from pathlib import Path

class IterumAppLauncher:
    def __init__(self, mode="full", port_backend=8000, port_frontend=8080):
        self.mode = mode
        self.port_backend = port_backend
        self.port_frontend = port_frontend
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def check_environment(self):
        """Check if we're in the right directory and have necessary files"""
        if not Path("app").exists():
            print("❌ Error: Please run this script from the project root directory")
            return False
            
        if not Path("app/main.py").exists():
            print("❌ Error: FastAPI application not found (app/main.py)")
            return False
            
        return True
    
    def start_backend(self):
        """Start the FastAPI backend server"""
        print(f"🔧 Starting FastAPI Backend (Port {self.port_backend})...")
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "app.main:app", 
                "--host", "0.0.0.0", 
                "--port", str(self.port_backend), 
                "--reload" if self.mode != "production" else "--no-reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            
            # Wait for startup
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ Backend server started successfully")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"❌ Backend server failed to start")
                print(f"Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
    
    def start_frontend_server(self):
        """Start the frontend HTTP server"""
        print(f"🌐 Starting Frontend Server (Port {self.port_frontend})...")
        
        class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                # Add CORS headers
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                super().end_headers()
            
            def guess_type(self, path):
                # Override MIME type detection
                if path.endswith('.js'):
                    return 'application/javascript'
                elif path.endswith('.css'):
                    return 'text/css'
                elif path.endswith('.html'):
                    return 'text/html'
                elif path.endswith('.json'):
                    return 'application/json'
                return super().guess_type(path)
            
            def log_message(self, format, *args):
                # Suppress access logs in quiet mode
                if hasattr(self.server, 'quiet') and self.server.quiet:
                    return
                super().log_message(format, *args)
        
        def run_server():
            try:
                with socketserver.TCPServer(("", self.port_frontend), CustomHTTPRequestHandler) as httpd:
                    if self.mode == "quiet":
                        httpd.quiet = True
                    print(f"✅ Frontend server started successfully")
                    httpd.serve_forever()
            except Exception as e:
                print(f"❌ Error starting frontend server: {e}")
        
        # Start frontend server in a separate thread
        frontend_thread = threading.Thread(target=run_server, daemon=True)
        frontend_thread.start()
        time.sleep(1)  # Give it a moment to start
        return True
    
    def open_browser(self):
        """Open the application in the default browser"""
        url = f"http://localhost:{self.port_frontend}/index.html"
        print("🌐 Opening app in your default browser...")
        
        try:
            opened = webbrowser.open_new_tab(url)
            if not opened:
                raise Exception("webbrowser.open_new_tab returned False")
            print(f"✅ Browser opened: {url}")
        except Exception as e:
            print(f"⚠️ Could not open browser automatically: {e}")
            if sys.platform.startswith('win'):
                try:
                    os.system(f'start {url}')
                    print(f"✅ Browser opened via system command")
                except:
                    print(f"Please open this URL manually: {url}")
            else:
                print(f"Please open this URL manually: {url}")
    
    def display_info(self):
        """Display application information"""
        print("=" * 60)
        print("✅ Iterum R&D Chef Notebook Started Successfully!")
        print()
        print("📱 Application URLs:")
        print(f"   • Frontend: http://localhost:{self.port_frontend}")
        print(f"   • Backend API: http://localhost:{self.port_backend}")
        print(f"   • API Documentation: http://localhost:{self.port_backend}/docs")
        print(f"   • Health Check: http://localhost:{self.port_backend}/health")
        print()
        print("💾 Storage Features:")
        print("   • SQLite database: culinary_data.db")
        print("   • User profiles: profiles/")
        print("   • Recipe uploads: uploads/")
        print("   • Application logs: logs/")
        print()
        print("🔧 Available Tools:")
        print("   • Clear users: clear_users.bat")
        print("   • Run tests: test_unified.bat")
        print("   • Load equipment: python load_comprehensive_equipment.py")
        print()
        print("🛑 Press Ctrl+C to stop all servers")
        print("=" * 60)
    
    def launch_full_app(self):
        """Launch both backend and frontend servers"""
        if not self.check_environment():
            return False
        
        print("🚀 Starting Iterum R&D Chef Notebook (Full Mode)...")
        print("=" * 60)
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Start frontend
        if not self.start_frontend_server():
            return False
        
        # Display information
        self.display_info()
        
        # Open browser unless in quiet mode
        if self.mode != "quiet":
            time.sleep(2)
            self.open_browser()
        
        return True
    
    def launch_backend_only(self):
        """Launch only the backend server"""
        if not self.check_environment():
            return False
        
        print("🚀 Starting Iterum R&D Chef Notebook Backend Only...")
        print("=" * 60)
        
        if not self.start_backend():
            return False
        
        print("✅ Backend server running")
        print(f"📡 API Available at: http://localhost:{self.port_backend}")
        print(f"📖 API Docs: http://localhost:{self.port_backend}/docs")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        return True
    
    def launch_frontend_only(self):
        """Launch only the frontend server"""
        print("🚀 Starting Iterum R&D Chef Notebook Frontend Only...")
        print("=" * 60)
        
        if not self.start_frontend_server():
            return False
        
        print("✅ Frontend server running")
        print(f"📱 Application: http://localhost:{self.port_frontend}")
        print("⚠️ Note: Backend API must be running separately")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        if self.mode != "quiet":
            time.sleep(2)
            self.open_browser()
        
        return True
    
    def run(self):
        """Main run method"""
        try:
            if self.mode == "backend":
                if not self.launch_backend_only():
                    return 1
                
                # Keep backend running
                try:
                    self.backend_process.wait()
                except KeyboardInterrupt:
                    pass
                    
            elif self.mode == "frontend":
                if not self.launch_frontend_only():
                    return 1
                
                # Keep script running
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass
                    
            else:  # full mode
                if not self.launch_full_app():
                    return 1
                
                # Keep both servers running
                try:
                    self.backend_process.wait()
                except KeyboardInterrupt:
                    pass
            
            return 0
            
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown all servers"""
        print("\n🛑 Shutting down servers...")
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        print("✅ Servers stopped")

def main():
    parser = argparse.ArgumentParser(description="Unified Iterum R&D Chef Notebook Launcher")
    parser.add_argument("--mode", choices=["full", "backend", "frontend", "quiet"], 
                       default="full", help="Launch mode")
    parser.add_argument("--backend-port", type=int, default=8000, 
                       help="Backend server port")
    parser.add_argument("--frontend-port", type=int, default=8080, 
                       help="Frontend server port")
    
    args = parser.parse_args()
    
    launcher = IterumAppLauncher(
        mode=args.mode,
        port_backend=args.backend_port,
        port_frontend=args.frontend_port
    )
    
    return launcher.run()

if __name__ == "__main__":
    sys.exit(main()) 