import http.server
import socketserver
import webbrowser
import os
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
Path('logs').mkdir(exist_ok=True)

# Configuration
PORT = int(os.getenv('PORT', 8000))
HOST = os.getenv('HOST', 'localhost')
WEB_FOLDER = os.getenv('WEB_FOLDER', 'web')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

class ProductionHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler with production improvements"""
    
    def end_headers(self):
        """Add security and caching headers"""
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-XSS-Protection', '1; mode=block')
        
        # Cache static assets
        if self.path.endswith(('.js', '.css', '.png', '.jpg', '.gif')):
            self.send_header('Cache-Control', 'public, max-age=31536000')
        else:
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        
        super().end_headers()
    
    def log_message(self, format, *args):
        """Log HTTP requests"""
        logger.info("%s - %s" % (self.client_address[0], format % args))

def start_server():
    """Start the web server"""
    try:
        # Change to web folder
        project_dir = os.path.dirname(os.path.abspath(__file__))
        web_dir = os.path.join(project_dir, WEB_FOLDER)
        
        if not os.path.isdir(web_dir):
            logger.error(f"Web folder not found: {web_dir}")
            sys.exit(1)
        
        os.chdir(web_dir)
        
        handler = ProductionHTTPRequestHandler
        
        server_url = f"http://{HOST}:{PORT}"
        logger.info(f"Starting server in {ENVIRONMENT} mode")
        logger.info(f"Serving files from {web_dir}")
        logger.info(f"Server running at {server_url}")
        
        # Try to open browser
        try:
            webbrowser.open(server_url)
            logger.info("Browser opened successfully")
        except Exception as e:
            logger.warning(f"Could not open browser: {e}")
        
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            logger.info(f"Server listening on port {PORT}")
            httpd.serve_forever()
    
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    start_server()

