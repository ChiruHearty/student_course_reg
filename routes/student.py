# routes/student.py
from flask import Blueprint, request, jsonify
from app import db # Import the db object from the main app
from models import Student, Course # Import Student and Course models

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/', methods=['POST'])
def create_student():
    """
    Creates a new student.
    Expected JSON: {"name": "Student Name", "email": "student@example.com"}
    """
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"message": "Name and email are required"}), 400

    if Student.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Student with this email already exists"}), 409

    new_student = Student(name=data['name'], email=data['email'])
    try:
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating student", "error": str(e)}), 500

@student_bp.route('/', methods=['GET'])
def get_all_students():
    """
    Retrieves all students.
    """
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students]), 200

@student_bp.route('/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """
    Retrieves a single student by ID.
    """
    student = Student.query.get(student_id)
    if student:
        return jsonify(student.to_dict()), 200
    return jsonify({"message": "Student not found"}), 404

@student_bp.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """
    Updates an existing student's details.
    Expected JSON: {"name": "New Name", "email": "new_email@example.com"}
    """
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided for update"}), 400

    if 'name' in data:
        student.name = data['name']
    if 'email' in data:
        # Check if new email already exists for another student
        existing_student_with_email = Student.query.filter(
            Student.email == data['email'], Student.id != student_id
        ).first()
        if existing_student_with_email:
            return jsonify({"message": "Email already registered to another student"}), 409
        student.email = data['email']

    try:
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating student", "error": str(e)}), 500

@student_bp.route('/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    Deletes a student by ID.
    """
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting student", "error": str(e)}), 500

@student_bp.route('/<int:student_id>/register_course', methods=['POST'])
def register_for_course(student_id):
    """
    Registers a student for a course.
    Expected JSON: {"course_id": 1}
    """
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({"message": "Course ID is required"}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    if course in student.courses:
        return jsonify({"message": "Student already registered for this course"}), 409

    student.courses.append(course)
    try:
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error registering student for course", "error": str(e)}), 500

@student_bp.route('/<int:student_id>/unregister_course', methods=['POST'])
def unregister_from_course(student_id):
    """
    Unregisters a student from a course.
    Expected JSON: {"course_id": 1}
    """
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({"message": "Course ID is required"}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    if course not in student.courses:
        return jsonify({"message": "Student not registered for this course"}), 409

    student.courses.remove(course)
    try:
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error unregistering student from course", "error": str(e)}), 500
