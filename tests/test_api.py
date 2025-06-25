# tests/test_api.py
import unittest
import json
import os
import tempfile
import sys

# Add the project root to the path so modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Student, Course, Registration

class ApiTestCase(unittest.TestCase):
    """
    Test case for the Flask API endpoints.
    """
    def setUp(self):
        """
        Set up the test environment:
        - Create a temporary database.
        - Initialize the Flask app in testing mode.
        - Push application context.
        - Create database tables.
        """
        self.db_fd, self.db_path = tempfile.mkstemp()
        os.environ['DATABASE_URL'] = f'sqlite:///{self.db_path}' # Use a temporary database
        os.environ['FLASK_DEBUG'] = 'True' # Set debug for testing, though not strictly necessary for this.
        os.environ['SECRET_KEY'] = 'test_secret_key' # For Flask-SocketIO in tests

        # Create app instance, but we don't need the socketio object for REST API tests
        self.app, _ = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Tear down the test environment:
        - Remove database session.
        - Drop all database tables.
        - Close and remove the temporary database file.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_path)
        # Clean up instance folder and migration history if they were created during tests
        # This is more robust for a full test suite
        instance_folder = os.path.join(self.app.root_path, 'instance')
        if os.path.exists(instance_folder):
            for filename in os.listdir(instance_folder):
                file_path = os.path.join(instance_folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            # os.rmdir(instance_folder) # Only remove if empty and you are sure no other test created it

    def test_create_student(self):
        """
        Test the POST /api/students endpoint for creating a new student.
        """
        response = self.client.post('/api/students/', json={'name': 'Alice', 'email': 'alice@example.com'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Alice')
        self.assertEqual(data['email'], 'alice@example.com')
        self.assertIn('id', data)

        # Test invalid input
        response = self.client.post('/api/students/', json={'name': 'Bob'}) # Missing email
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/students/', json={}) # Empty data
        self.assertEqual(response.status_code, 400)

        # Test duplicate email
        response = self.client.post('/api/students/', json={'name': 'Charlie', 'email': 'alice@example.com'})
        self.assertEqual(response.status_code, 400) # Expecting a database integrity error

    def test_get_students(self):
        """
        Test the GET /api/students endpoint for retrieving all students.
        """
        self.client.post('/api/students/', json={'name': 'Alice', 'email': 'alice@example.com'})
        self.client.post('/api/students/', json={'name': 'Bob', 'email': 'bob@example.com'})

        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[1]['name'], 'Bob')

    def test_get_student_by_id(self):
        """
        Test the GET /api/students/<int:student_id> endpoint.
        """
        post_response = self.client.post('/api/students/', json={'name': 'David', 'email': 'david@example.com'})
        student_id = json.loads(post_response.data)['id']

        get_response = self.client.get(f'/api/students/{student_id}')
        self.assertEqual(get_response.status_code, 200)
        data = json.loads(get_response.data)
        self.assertEqual(data['name'], 'David')

        # Test non-existent student
        not_found_response = self.client.get('/api/students/999')
        self.assertEqual(not_found_response.status_code, 404)

    def test_create_course(self):
        """
        Test the POST /api/courses endpoint.
        """
        response = self.client.post('/api/courses/', json={'title': 'Math 101', 'code': 'MA101'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Math 101')
        self.assertEqual(data['code'], 'MA101')
        self.assertIn('id', data)

        # Test invalid input
        response = self.client.post('/api/courses/', json={'title': 'Physics'}) # Missing code
        self.assertEqual(response.status_code, 400)

        # Test duplicate code
        response = self.client.post('/api/courses/', json={'title': 'Calculus', 'code': 'MA101'})
        self.assertEqual(response.status_code, 400)

    def test_get_courses(self):
        """
        Test the GET /api/courses endpoint.
        """
        self.client.post('/api/courses/', json={'title': 'Chemistry', 'code': 'CH101'})
        self.client.post('/api/courses/', json={'title': 'Biology', 'code': 'BI101'})

        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'Chemistry')

    def test_register_student_for_course(self):
        """
        Test the POST /api/students/<int:student_id>/register endpoint.
        """
        # Create a student
        student_response = self.client.post('/api/students/', json={'name': 'Eve', 'email': 'eve@example.com'})
        student_id = json.loads(student_response.data)['id']

        # Create a course
        course_response = self.client.post('/api/courses/', json={'title': 'Database Fundamentals', 'code': 'DB201'})
        course_id = json.loads(course_response.data)['id']

        # Register student for course
        register_response = self.client.post(f'/api/students/{student_id}/register', json={'course_id': course_id})
        self.assertEqual(register_response.status_code, 201)
        reg_data = json.loads(register_response.data)
        self.assertEqual(reg_data['student_id'], student_id)
        self.assertEqual(reg_data['course_id'], course_id)

        # Try to register again (should fail with 409 Conflict)
        register_again_response = self.client.post(f'/api/students/{student_id}/register', json={'course_id': course_id})
        self.assertEqual(register_again_response.status_code, 409)

        # Test registration with non-existent student/course
        invalid_student_response = self.client.post('/api/students/999/register', json={'course_id': course_id})
        self.assertEqual(invalid_student_response.status_code, 404)

        invalid_course_response = self.client.post(f'/api/students/{student_id}/register', json={'course_id': 999})
        self.assertEqual(invalid_course_response.status_code, 404)

    def test_get_student_courses(self):
        """
        Test the GET /api/students/<int:student_id>/courses endpoint.
        """
        student_response = self.client.post('/api/students/', json={'name': 'Frank', 'email': 'frank@example.com'})
        student_id = json.loads(student_response.data)['id']

        course1_response = self.client.post('/api/courses/', json={'title': 'Web Dev Basics', 'code': 'WD101'})
        course1_id = json.loads(course1_response.data)['id']

        course2_response = self.client.post('/api/courses/', json={'title': 'Data Structures', 'code': 'DS201'})
        course2_id = json.loads(course2_response.data)['id']

        # Register Frank for both courses
        self.client.post(f'/api/students/{student_id}/register', json={'course_id': course1_id})
        self.client.post(f'/api/students/{student_id}/register', json={'course_id': course2_id})

        get_courses_response = self.client.get(f'/api/students/{student_id}/courses')
        self.assertEqual(get_courses_response.status_code, 200)
        data = json.loads(get_courses_response.data)
        self.assertEqual(len(data), 2)
        self.assertIn('Web Dev Basics', [c['title'] for c in data])
        self.assertIn('Data Structures', [c['title'] for c in data])

        # Test a student with no registrations
        student_no_reg_response = self.client.post('/api/students/', json={'name': 'Grace', 'email': 'grace@example.com'})
        student_no_reg_id = json.loads(student_no_reg_response.data)['id']
        no_reg_courses_response = self.client.get(f'/api/students/{student_no_reg_id}/courses')
        self.assertEqual(no_reg_courses_response.status_code, 200)
        self.assertEqual(json.loads(no_reg_courses_response.data), [])


if __name__ == '__main__':
    unittest.main()
