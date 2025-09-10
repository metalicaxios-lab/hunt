from http.server import BaseHTTPRequestHandler
import json
import time
from datetime import datetime, timedelta

SAMPLE_COURSES = [
    {
        "id": 1,
        "title": "Business Fundamentals",
        "description": "Learn the basics of business management",
        "level": "Beginner",
        "category": "Business",
        "price": 99.99,
        "duration": "8 weeks",
        "start_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "available_seats": 20
    },
    {
        "id": 2,
        "title": "Advanced Technology",
        "description": "Deep dive into modern tech",
        "level": "Advanced",
        "category": "Technology",
        "price": 149.99,
        "duration": "12 weeks",
        "start_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        "available_seats": 15
    }
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

        if '/api/auth/login' in self.path:
            response = {
                'status': 'success',
                'message': 'Login successful',
                'token': 'dummy-jwt-token-' + str(time.time()),
                'user': {
                    'id': 1,
                    'email': data.get('email', ''),
                    'role': 'user'
                }
            }
            self.wfile.write(json.dumps(response).encode())
            return

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
                'courses': SAMPLE_COURSES,
                'status': 'success',
                'message': 'Courses retrieved successfully'
            }
        else:
            response = {
                'status': 'success',
                'message': 'API is working'
            }

        self.wfile.write(json.dumps(response).encode())
