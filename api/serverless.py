import os
import json
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Load configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'mysql+pymysql://avnadmin:AVNS_KUiCMFzJ3QHxBt_jkJW@mysql-31a284a2-s7304690-462f.i.aivencloud.com:27671/defaultdb'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ENGINE_OPTIONS={
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 3,
        'max_overflow': 5,
    }
)

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Import models
from models import Course, Registration, Student, User, Parent, Class, Enrollment

def success_response(data, status_code=200):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(data)
    }

def error_response(message, status_code=500):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps({
            'error': message,
            'status': 'error'
        })
    }

def get_course_filters():
    """Get available course filters"""
    try:
        with app.app_context():
            categories = db.session.query(Course.category).filter(Course.is_active == True).distinct().all()
            categories = [cat[0] for cat in categories if cat[0]]
            
            levels = ['Beginner', 'Intermediate', 'Advanced']
            
            return success_response({
                'filters': {
                    'levels': levels,
                    'categories': categories or ['Business', 'Technology', 'Personal Development']
                },
                'status': 'success'
            })
    except Exception as e:
        logger.error(f"Error fetching course filters: {str(e)}")
        return error_response("Failed to fetch course filters")

def get_courses():
    """Get all active courses"""
    try:
        with app.app_context():
            courses = Course.query.filter_by(is_active=True).all()
            course_list = []
            for course in courses:
                registrations = Registration.query.filter_by(
                    course_id=course.id,
                    status='approved'
                ).count()
                
                course_list.append({
                    'id': course.id,
                    'name': course.name,
                    'description': course.description,
                    'price': float(course.price),
                    'category': course.category,
                    'max_students': course.max_students,
                    'available_seats': course.max_students - registrations,
                    'image_url': course.image_url
                })
            
            return success_response({
                'courses': course_list,
                'status': 'success',
                'message': 'Courses retrieved successfully'
            })
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        return error_response("Failed to fetch courses")

def login(request):
    """Handle login requests"""
    try:
        with app.app_context():
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return error_response("Email and password are required", 400)

            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                return error_response("Invalid credentials", 401)

            access_token = create_access_token(identity=user.id)
            return success_response({
                'token': access_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role
                },
                'status': 'success',
                'message': 'Login successful'
            })
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return error_response("Login failed")

def register_course(request):
    """Handle course registration"""
    try:
        with app.app_context():
            data = json.loads(request.body)
            course_id = data.get('course_id')
            student_id = data.get('student_id')

            if not course_id or not student_id:
                return error_response("Course ID and Student ID are required", 400)

            # Check if course exists and has available seats
            course = Course.query.get(course_id)
            if not course:
                return error_response("Course not found", 404)

            registration_count = Registration.query.filter_by(
                course_id=course_id,
                status='approved'
            ).count()

            if registration_count >= course.max_students:
                return error_response("No available seats", 409)

            # Create registration
            registration = Registration(
                course_id=course_id,
                student_id=student_id,
                status='pending'
            )
            db.session.add(registration)
            db.session.commit()

            return success_response({
                'message': 'Registration successful',
                'registration_id': registration.id,
                'status': 'success'
            }, 201)
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return error_response("Registration failed")

# For local development
if __name__ == '__main__':
    app.run(debug=True)
