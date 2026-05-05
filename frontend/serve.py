#!/usr/bin/env python3
"""
TerraPulse-AI Frontend Development Server
Serves the frontend on port 3000 with SPA routing and API proxy
"""

import os
import sys
import http.server
import socketserver
import json
import urllib.request
import urllib.error
from pathlib import Path

PORT = 3000
FRONTEND_DIR = Path(__file__).parent

class FrontendHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def do_GET(self):
        """Handle GET requests with SPA routing and API proxy"""
        path = self.path.split('?')[0]  # Remove query parameters
        
        # Proxy API calls to backend
        if path.startswith('/api'):
            self.proxy_to_backend()
            return
        
        # Check if it's a file request
        if '.' in path.split('/')[-1]:
            # It's likely a file request (has extension)
            return super().do_GET()
        
        # For routes without extensions, serve index.html (SPA routing)
        self.path = '/index.html'
        return super().do_GET()
    
    def proxy_to_backend(self):
        """Proxy API requests to the backend server"""
        backend_url = f"http://localhost:8000{self.path}"
        
        try:
            req = urllib.request.Request(backend_url, method=self.command)
            
            # Forward headers
            if self.headers.get('Content-Length'):
                content_length = int(self.headers.get('Content-Length'))
                body = self.rfile.read(content_length)
                req.data = body
            
            # Add auth headers if present
            if 'Authorization' in self.headers:
                req.add_header('Authorization', self.headers['Authorization'])
            
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() not in ['content-encoding', 'transfer-encoding']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_msg = {"error": f"Backend error: {e.reason}"}
            self.wfile.write(json.dumps(error_msg).encode())
        except urllib.error.URLError as e:
            self.send_response(502)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_msg = {"error": "Backend unavailable - is it running on :8000?"}
            self.wfile.write(json.dumps(error_msg).encode())
    
    def end_headers(self):
        """Add security and cache headers"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        if '200' in str(args):
            return  # Skip 200 OK logs
        print(f"{self.client_address[0]} - {format%args}")

def main():
    """Start the development server"""
    try:
        handler = FrontendHandler
        with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
            print(f"""
╔════════════════════════════════════════════════════════════╗
║      TerraPulse-AI Frontend Dev Server - RUNNING           ║
╚════════════════════════════════════════════════════════════╝

🌐 Frontend:    http://localhost:{PORT}
🔙 Backend:     http://localhost:8000
📚 API Docs:    http://localhost:8000/api/docs

✅ SPA Routing: Enabled
✅ API Proxy:   Enabled (/api → :8000)
✅ Hot Reload:  Ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Press Ctrl+C to stop...
""")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped gracefully.")
        sys.exit(0)
    except OSError as e:
        print(f"❌ Error: {e}")
        print(f"Make sure port {PORT} is not in use.")
        sys.exit(1)

if __name__ == "__main__":
    main()
