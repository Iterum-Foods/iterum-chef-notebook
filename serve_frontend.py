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
    # Change to the directory containing this script
    os.chdir(Path(__file__).parent)
    
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
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"Frontend server running on http://localhost:{PORT}")
            print(f"Serving files from: {os.getcwd()}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nFrontend server stopped")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Please stop any other servers using this port.")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 