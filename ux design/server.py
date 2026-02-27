#!/usr/bin/env python3
import http.server
import socketserver
import os

# Change to the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = int(os.getenv("PORT", 3000))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_GET(self):
        # Handle OAuth callback routes -> serve login.html (auth.js reads query params)
        from urllib.parse import urlparse
        parsed = urlparse(self.path)
        if parsed.path in ('/auth/google/callback', '/auth/linkedin/callback'):
            # Redirect to login.html preserving query string
            qs = '?' + parsed.query if parsed.query else ''
            self.send_response(302)
            self.send_header('Location', '/login.html' + qs)
            self.end_headers()
            return
        super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    run_server()
