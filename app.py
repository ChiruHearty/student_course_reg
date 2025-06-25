# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Initialize Flask app
app = Flask(__name__)

# --- Configuration ---
# You would typically load these from environment variables or a config file
# For demonstration, hardcoding for simplicity.
# IMPORTANT: In a production environment, use secure methods for database credentials.
DB_USER = os.environ.get('MYSQL_USER', 'your_mysql_user')  # Replace with your MySQL username
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'your_mysql_password') # Replace with your MySQL password
DB_HOST = os.environ.get('MYSQL_HOST', 'localhost')
DB_PORT = os.environ.get('MYSQL_PORT', '3306')
DB_NAME = os.environ.get('MYSQL_DB_NAME', 'student_course_db')

# MySQL database connection URI using PyMySQL driver
# Ensure you have 'PyMySQL' installed (pip install PyMySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Dynamically import blueprints after db is initialized to avoid circular imports
from routes.student import student_bp
from routes.course import course_bp

# Register blueprints
app.register_blueprint(student_bp, url_prefix='/students')
app.register_blueprint(course_bp, url_prefix='/courses')

# Health check endpoint
@app.route('/health')
def health_check():
    """
    Endpoint to check the health of the application and database connection.
    """
    try:
        # Attempt to connect to the database to verify connectivity
        db.session.execute(db.text('SELECT 1'))
        return jsonify({"status": "healthy", "database_connection": "successful"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database_connection": "failed", "error": str(e)}), 500

if __name__ == '__main__':
    # Create database tables if they don't exist (only for development/initial setup)
    # In a real application, use Flask-Migrate or Alembic for migrations
    with app.app_context():
        db.create_all()
    # Run the Flask application
    # debug=True should NOT be used in production
    app.run(debug=True, host='0.0.0.0', port=5000)
