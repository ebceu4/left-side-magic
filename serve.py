#!/usr/bin/env python3
"""
Simple HTTP server to serve the interactive book locally.
This helps avoid CORS issues when loading images from file:// protocol.

Usage:
    python serve.py
    
Then open: http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import os
import sys

def main():
    PORT = 8000
    
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Add CORS headers to avoid any potential issues
    class CORSHTTPRequestHandler(Handler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
            print(f"🚀 Starting server at http://localhost:{PORT}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print(f"📚 Open http://localhost:{PORT} in your browser")
            print(f"🛑 Press Ctrl+C to stop the server")
            print("-" * 50)
            
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print("🌐 Browser opened automatically")
            except:
                print("⚠️  Could not open browser automatically")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print(f"💡 Try a different port or stop the other server")
            print(f"🔧 You can also try: python serve.py {PORT + 1}")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
