# models.py
from app import db # Import the db object from the main app

# Define the association table for the many-to-many relationship between students and courses
student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Student(db.Model):
    """
    Student model representing a student in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Many-to-many relationship with Course
    courses = db.relationship('Course', secondary=student_courses, lazy='subquery',
                              backref=db.backref('students', lazy=True))

    def __repr__(self):
        """
        String representation of the Student object.
        """
        return f'<Student {self.name}>'

    def to_dict(self):
        """
        Converts the Student object to a dictionary, including enrolled courses.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'courses': [course.to_dict_simple() for course in self.courses] # Simplified course data
        }

    def to_dict_simple(self):
        """
        Converts the Student object to a simplified dictionary, for embedding in other objects.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Course(db.Model):
    """
    Course model representing a course in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """
        String representation of the Course object.
        """
        return f'<Course {self.name}>'

    def to_dict(self):
        """
        Converts the Course object to a dictionary, including enrolled students.
        """
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'students': [student.to_dict_simple() for student in self.students] # Simplified student data
        }

    def to_dict_simple(self):
        """
        Converts the Course object to a simplified dictionary, for embedding in other objects.
        """
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description
        }
