#!/usr/bin/env python3
"""
Simple mock backend server for TerraPulse-AI
Serves authentication endpoints without requiring full FastAPI setup
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import base64
from datetime import datetime, timedelta
import hashlib
import hmac

# Mock database (in-memory)
users_db = {
    "user@example.com": {
        "id": 1,
        "username": "demouser",
        "email": "user@example.com",
        "full_name": "Demo User",
        "password_hash": hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000).hex(),
        "created_at": (datetime.now() - timedelta(days=30)).isoformat()
    }
}

cities_data = [
    {"id": 1, "name": "Ahmedabad", "latitude": 23.0225, "longitude": 72.5714, "aqi_value": 156, "pm25": 78.4, "pm10": 142.2},
    {"id": 2, "name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777, "aqi_value": 142, "pm25": 65.2, "pm10": 128.5},
    {"id": 3, "name": "Surat", "latitude": 21.1702, "longitude": 72.8311, "aqi_value": 138, "pm25": 61.8, "pm10": 125.2},
    {"id": 4, "name": "Delhi", "latitude": 28.7041, "longitude": 77.1025, "aqi_value": 189, "pm25": 95.2, "pm10": 165.8},
    {"id": 5, "name": "Bangalore", "latitude": 12.9716, "longitude": 77.5946, "aqi_value": 98, "pm25": 42.3, "pm10": 78.1},
]

def hash_password(password):
    """Hash password using PBKDF2"""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash

def generate_token(user_id, email):
    """Generate a simple JWT-like token"""
    header = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip('=')
    payload = base64.b64encode(json.dumps({
        "sub": user_id,
        "email": email,
        "iat": int(datetime.now().timestamp()),
        "exp": int((datetime.now() + timedelta(hours=24)).timestamp())
    }).encode()).decode().rstrip('=')
    
    signature = base64.b64encode(
        hmac.new(b"secret", f"{header}.{payload}".encode(), hashlib.sha256).digest()
    ).decode().rstrip('=')
    
    return f"{header}.{payload}.{signature}"

class MockBackendHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mock backend"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        if path == '/api/health':
            self.wfile.write(json.dumps({"status": "ok", "database": "connected"}).encode())
        elif path == '/api/cities/all':
            self.wfile.write(json.dumps(cities_data).encode())
        else:
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        # CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        if path == '/api/auth/register':
            response = self._handle_register(data)
        elif path == '/api/auth/login':
            response = self._handle_login(data)
        else:
            self.send_response(404)
            response = {"error": "Endpoint not found"}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _handle_register(self, data):
        """Handle user registration"""
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        full_name = data.get('full_name', '').strip()
        
        # Validation
        if not email or '@' not in email:
            return {"detail": "Invalid email format"}
        if not username or len(username) < 3:
            return {"detail": "Username must be at least 3 characters"}
        if not password or len(password) < 8:
            return {"detail": "Password must be at least 8 characters"}
        if email in users_db:
            return {"detail": "Email already registered"}
        
        # Create user
        user_id = len(users_db) + 1
        users_db[email] = {
            "id": user_id,
            "username": username,
            "email": email,
            "full_name": full_name,
            "password_hash": hash_password(password),
            "created_at": datetime.now().isoformat()
        }
        
        # Generate token
        token = generate_token(user_id, email)
        user = users_db[email]
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "created_at": user["created_at"]
            }
        }
    
    def _handle_login(self, data):
        """Handle user login"""
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return {"detail": "Email and password required"}
        
        if email not in users_db:
            return {"detail": "Invalid email or password"}
        
        user = users_db[email]
        if not verify_password(password, user["password_hash"]):
            return {"detail": "Invalid email or password"}
        
        # Generate token
        token = generate_token(user["id"], email)
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "created_at": user["created_at"]
            }
        }
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('0.0.0.0', port), MockBackendHandler)
    print(f"🚀 Mock Backend Server running on http://localhost:{port}")
    print(f"✅ Demo Account: user@example.com / password")
    print(f"📊 Endpoints ready at http://localhost:3000")
    print(f"⚠️  Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✋ Server stopped")
        sys.exit(0)
