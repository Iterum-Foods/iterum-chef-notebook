#!/usr/bin/env python3
"""
Unified startup script for Iterum R&D Chef Notebook
Runs both backend and frontend servers with proper error handling
"""

import subprocess
import sys
import time
import threading
import os
import webbrowser
from pathlib import Path

class AppManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def start_backend(self):
        """Start the FastAPI backend server"""
        print("Starting Iterum R&D Chef Notebook Backend...")
        try:
            # Use uvicorn to run the FastAPI app
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "app.main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000", 
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            
            # Wait a moment for startup
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("Backend server started successfully")
                print("API Documentation: http://localhost:8000/docs")
                print("Health Check: http://localhost:8000/health")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"Backend server failed to start")
                print(f"Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"Error starting backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the frontend HTTP server"""
        print("Starting Iterum R&D Chef Notebook Frontend...")
        try:
            self.frontend_process = subprocess.Popen([
                sys.executable, "serve_frontend.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            
            # Wait a moment for startup
            time.sleep(2)
            
            if self.frontend_process.poll() is None:
                print("Frontend server started successfully")
                print("Frontend: http://localhost:8080")
                return True
            else:
                stdout, stderr = self.frontend_process.communicate()
                print(f"Frontend server failed to start")
                print(f"Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"Error starting frontend: {e}")
            return False
    
    def open_browser(self):
        """Open the application in the default browser"""
        time.sleep(2)  # Wait for servers to fully start
        try:
            print("Opening Iterum R&D Chef Notebook in your browser...")
            webbrowser.open("http://localhost:8080")
        except Exception as e:
            print(f"Could not open browser: {e}")
    
    def stop_servers(self):
        """Stop both servers"""
        print("\nShutting down servers...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            print("Backend server stopped")
            
        if self.frontend_process:
            self.frontend_process.terminate()
            print("Frontend server stopped")
    
    def run(self):
        """Run the complete application"""
        print("=" * 50)
        print("Iterum R&D Chef Notebook")
        print("Professional Recipe R&D and Publishing System")
        print("=" * 50)
        
        # Start backend
        if not self.start_backend():
            print("Failed to start backend. Exiting...")
            return False
        
        # Start frontend
        if not self.start_frontend():
            print("Failed to start frontend. Stopping backend...")
            self.stop_servers()
            return False
        
        # Open browser in a separate thread
        browser_thread = threading.Thread(target=self.open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("\n" + "=" * 50)
        print("Iterum R&D Chef Notebook is now running!")
        print("Frontend: http://localhost:8080")
        print("API Docs: http://localhost:8000/docs")
        print("Press Ctrl+C to stop the servers")
        print("=" * 50)
        
        try:
            # Keep the script running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_servers()
            print("\nThanks for using Iterum R&D Chef Notebook!")
        
        return True

def main():
    """Main entry point"""
    # Change to the script's directory
    os.chdir(Path(__file__).parent)
    
    # Check if required files exist
    if not Path("app/main.py").exists():
        print("Backend application not found. Please ensure app/main.py exists.")
        return False
    
    if not Path("serve_frontend.py").exists():
        print("Frontend server not found. Please ensure serve_frontend.py exists.")
        return False
    
    # Create and run the app manager
    app_manager = AppManager()
    return app_manager.run()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 