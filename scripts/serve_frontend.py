#!/usr/bin/env python3
"""
Simple HTTP server for serving frontend files
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

def main():
    # Change to the project root directory (parent of scripts)
    os.chdir(Path(__file__).parent.parent)
    
    # Set up the server
    PORT = 8080
    
    # Create a custom handler that serves files with proper MIME types
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            super().end_headers()
        
        def guess_type(self, path):
            # Override MIME type detection for better browser compatibility
            if path.endswith('.js'):
                return 'application/javascript'
            elif path.endswith('.css'):
                return 'text/css'
            elif path.endswith('.html'):
                return 'text/html'
            elif path.endswith('.json'):
                return 'application/json'
            return super().guess_type(path)
    
    # Try to find an available port
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
                print(f"Frontend server running on http://localhost:{PORT}")
                print(f"Serving files from: {os.getcwd()}")
                print("Press Ctrl+C to stop the server")
                httpd.serve_forever()
                break
        except KeyboardInterrupt:
            print("\nFrontend server stopped")
            break
        except OSError as e:
            if e.errno == 10048 or e.errno == 48:  # Address already in use (Windows/Linux)
                if attempt < max_attempts - 1:
                    PORT += 1
                    print(f"Port {PORT-1} is busy, trying port {PORT}...")
                    continue
                else:
                    print(f"Error: Ports 8080-{PORT} are all in use. Please stop other servers.")
                    sys.exit(1)
            else:
                print(f"Error starting server: {e}")
                sys.exit(1)

if __name__ == "__main__":
    main() 