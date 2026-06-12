import http.server
import socketserver
import webbrowser
import os

# The port where the browser will open.
PORT = 8000

# Folder with the website files.
WEB_FOLDER = "web"

# Change working folder to the web folder.
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(project_dir, WEB_FOLDER))

handler = http.server.SimpleHTTPRequestHandler

print(f"Serving files from {WEB_FOLDER} on http://localhost:{PORT}")
try:
    webbrowser.open(f"http://localhost:{PORT}")
except Exception:
    pass

with socketserver.TCPServer(("", PORT), handler) as httpd:
    httpd.serve_forever()
