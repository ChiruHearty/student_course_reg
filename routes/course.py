# routes/course.py
from flask import Blueprint, request, jsonify
from app import db # Import the db object from the main app
from models import Course, Student # Import Course and Student models

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/', methods=['POST'])
def create_course():
    """
    Creates a new course.
    Expected JSON: {"name": "Course Name", "code": "C101", "description": "Course Description"}
    """
    data = request.get_json()
    if not data or not data.get('name') or not data.get('code'):
        return jsonify({"message": "Name and code are required"}), 400

    if Course.query.filter_by(code=data['code']).first():
        return jsonify({"message": "Course with this code already exists"}), 409

    new_course = Course(
        name=data['name'],
        code=data['code'],
        description=data.get('description')
    )
    try:
        db.session.add(new_course)
        db.session.commit()
        return jsonify(new_course.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating course", "error": str(e)}), 500

@course_bp.route('/', methods=['GET'])
def get_all_courses():
    """
    Retrieves all courses.
    """
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200

@course_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """
    Retrieves a single course by ID.
    """
    course = Course.query.get(course_id)
    if course:
        return jsonify(course.to_dict()), 200
    return jsonify({"message": "Course not found"}), 404

@course_bp.route('/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    Updates an existing course's details.
    Expected JSON: {"name": "New Course Name", "description": "New Description"}
    """
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided for update"}), 400

    if 'name' in data:
        course.name = data['name']
    if 'code' in data:
        # Check if new code already exists for another course
        existing_course_with_code = Course.query.filter(
            Course.code == data['code'], Course.id != course_id
        ).first()
        if existing_course_with_code:
            return jsonify({"message": "Course code already exists for another course"}), 409
        course.code = data['code']
    if 'description' in data:
        course.description = data['description']

    try:
        db.session.commit()
        return jsonify(course.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating course", "error": str(e)}), 500

@course_bp.route('/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Deletes a course by ID.
    """
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting course", "error": str(e)}), 500
