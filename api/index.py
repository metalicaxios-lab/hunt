from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import logging
import os
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.app import create_app
from api.models import db, Course, Registration, Student, User, Parent, Class, Enrollment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
flask_app = create_app()

class handler(BaseHTTPRequestHandler):
    """Ultra-minimal Vercel handler - no imports, no classes, no WSGI"""
    def init_flask_env(self):
        """Initialize Flask environment for request"""
        path = self.path
        method = self.command
        headers = dict(self.headers)
        
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': urlparse(path).path,
            'QUERY_STRING': urlparse(path).query,
            'wsgi.input': self.rfile,
            'wsgi.errors': self.wfile,
            'wsgi.version': (1, 0),
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': True,
            'wsgi.url_scheme': 'https',
            'SERVER_NAME': 'vercel.app',
            'SERVER_PORT': '443',
            'HTTP_HOST': headers.get('Host', 'vercel.app'),
            'HTTP_AUTHORIZATION': headers.get('Authorization', ''),
            'CONTENT_TYPE': headers.get('Content-Type', ''),
            'CONTENT_LENGTH': headers.get('Content-Length', '0'),
            'HTTP_ORIGIN': headers.get('Origin', '*'),
        }
        return environ

    def handle_flask_response(self, response):
        """Handle Flask response and send it to client"""
        status_code = response.status_code
        self.send_response(status_code)
        
        # Set headers
        for header, value in response.headers.items():
            self.send_header(header, value)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        # Send response body
        if response.data:
            self.wfile.write(response.data)

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    def do_GET(self):
        """Handle GET requests"""
        try:
            with flask_app.app_context():
                environ = self.init_flask_env()
                response = flask_app.wsgi_app(environ, lambda *args: None)
                self.handle_flask_response(response)
        except Exception as e:
            logger.error(f"GET request error: {str(e)}")
            self.send_error(500, str(e))

    def do_POST(self):
        """Handle POST requests"""
        try:
            with flask_app.app_context():
                environ = self.init_flask_env()
                response = flask_app.wsgi_app(environ, lambda *args: None)
                self.handle_flask_response(response)
        except Exception as e:
            logger.error(f"POST request error: {str(e)}")
            self.send_error(500, str(e))

# Export for Vercel
app = handler

def handle_complex_endpoint(path, method, request):
    """Handle complex endpoints with delayed Flask import"""
    try:
        # Only import Flask when absolutely necessary
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Import app creation function (not the app itself)
        from app import create_app
        
        # Create fresh app instance
        flask_app = create_app()
        
        # Create minimal WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': '',
            'CONTENT_TYPE': 'application/json',
            'CONTENT_LENGTH': '0',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '443',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': None,
            'wsgi.errors': None,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': True
        }
        
        # Response capture
        response_data = {'status': '200 OK', 'headers': [], 'body': b''}
        
        def start_response(status, headers):
            response_data['status'] = status
            response_data['headers'] = headers
        
        # Call Flask app
        with flask_app.app_context():
            result = flask_app.wsgi_app(environ, start_response)
            if result:
                response_data['body'] = b''.join(result)
        
        # Convert to Vercel response
        status_code = int(response_data['status'].split(' ')[0])
        headers = dict(response_data['headers'])
        body = response_data['body'].decode('utf-8') if response_data['body'] else '{}'
        
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': body
        }
        
    except Exception as flask_error:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': '{"error": "Flask Error", "message": "' + str(flask_error).replace('"', '\\"') + '"}'
        }

# Simple function for WSGI compatibility - NO CLASSES AT ALL
def application(environ, start_response):
    """Minimal WSGI function"""
    try:
        path = environ.get('PATH_INFO', '/')
        method = environ.get('REQUEST_METHOD', 'GET')
        
        # Create mock request
        mock_request = {'path': path, 'method': method}
        
        # Call handler
        response = handler(mock_request)
        
        # Return WSGI response
        status = str(response['statusCode']) + ' OK'
        headers = list(response.get('headers', {}).items())
        
        start_response(status, headers)
        return [response['body'].encode('utf-8')]
        
    except Exception as e:
        start_response('500 Internal Server Error', [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*')
        ])
        return [b'{"error": "WSGI Error"}']

# Export for Vercel - NO CLASS REFERENCES
app = application

# For testing
if __name__ == '__main__':
    test_request = {'path': '/api/test', 'method': 'GET'}
    result = handler(test_request)
    print("Test result:", result)
