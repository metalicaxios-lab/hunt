from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

        if '/api/courses/filters' in self.path:
            response = {
                'filters': {
                    'levels': ['Beginner', 'Intermediate', 'Advanced'],
                    'categories': ['Business', 'Technology', 'Personal Development']
                },
                'status': 'success'
            }
        elif '/api/courses' in self.path:
            response = {
                'courses': [],  # Empty array for now
                'status': 'success',
                'message': 'Courses retrieved successfully'
            }
        else:
            response = {
                'status': 'success',
                'message': 'API is working'
            }

        self.wfile.write(json.dumps(response).encode())
