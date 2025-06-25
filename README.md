Student Course Registration API
This is a real-time Flask project for managing student course registrations, connected to a MySQL database.

Project Structure
student-course-registration/
│
├── app.py
├── models.py
├── routes/
│   ├── student.py
│   ├── course.py
│
├── db/
│   └── setup.sql
│
├── tests/
│   └── test_api.py  (Placeholder - not implemented in this response)
│
├── requirements.txt
└── README.md

Features
Student Management: Create, retrieve, update, and delete student records.

Course Management: Create, retrieve, update, and delete course records.

Course Registration: Register students for courses and unregister them.

MySQL Database: Persistent storage using MySQL.

RESTful API: Exposes API endpoints for interaction.

Setup Instructions
1. Prerequisites
Python 3.8+

MySQL Server running

2. Database Setup
Start MySQL Server: Ensure your MySQL server is running.

Create Database and Tables:

Open your MySQL client (e.g., MySQL Workbench, mysql command-line client).

Log in as a user with sufficient privileges (e.g., root).

Execute the SQL script located at db/setup.sql.

mysql -u your_mysql_user -p < db/setup.sql

(Replace your_mysql_user with your MySQL username. You will be prompted for the password.)

This script will:

Create a database named student_course_db.

Create student, course, and student_courses tables.

Insert some sample data.

3. Project Setup
Clone the repository (if applicable, otherwise create the directory structure manually and place the files):

git clone <your-repo-url>
cd student-course-registration

Create a Python Virtual Environment (recommended):

python -m venv venv

Activate the Virtual Environment:

On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install Dependencies:

pip install -r requirements.txt

4. Configure Database Credentials
Edit app.py and replace the placeholder database credentials with your actual MySQL username, password, host, and port. Alternatively, you can set these as environment variables before running the application:

# Example for Linux/macOS
export MYSQL_USER="your_mysql_user"
export MYSQL_PASSWORD="your_mysql_password"
export MYSQL_HOST="localhost"
export MYSQL_PORT="3306"
export MYSQL_DB_NAME="student_course_db"

# Example for Windows (Command Prompt)
set MYSQL_USER="your_mysql_user"
set MYSQL_PASSWORD="your_mysql_password"
set MYSQL_HOST="localhost"
set MYSQL_PORT="3306"
set MYSQL_DB_NAME="student_course_db"

5. Run the Application
python app.py

The Flask application will start and be accessible at http://localhost:5000.

API Endpoints
The API is accessible at http://localhost:5000.

Students (/students)
POST /students/: Create a new student.

Request Body: {"name": "Alice Smith", "email": "alice@example.com"}

Response: 201 Created, Student object

GET /students/: Get all students.

Response: 200 OK, Array of Student objects

GET /students/<int:student_id>: Get a specific student by ID.

Response: 200 OK, Student object or 404 Not Found

PUT /students/<int:student_id>: Update a student.

Request Body: {"name": "Alice Wonderland"}

Response: 200 OK, Updated Student object or 404 Not Found

DELETE /students/<int:student_id>: Delete a student.

Response: 200 OK, Success message or 404 Not Found

POST /students/<int:student_id>/register_course: Register a student for a course.

Request Body: {"course_id": 1}

Response: 200 OK, Updated Student object or 404 Not Found, 400 Bad Request, 409 Conflict

POST /students/<int:student_id>/unregister_course: Unregister a student from a course.

Request Body: {"course_id": 1}

Response: 200 OK, Updated Student object or 404 Not Found, 400 Bad Request, 409 Conflict

Courses (/courses)
POST /courses/: Create a new course.

Request Body: {"name": "Introduction to Programming", "code": "CS101", "description": "Fundamentals of programming."}

Response: 201 Created, Course object

GET /courses/: Get all courses.

Response: 200 OK, Array of Course objects

GET /courses/<int:course_id>: Get a specific course by ID.

Response: 200 OK, Course object or 404 Not Found

PUT /courses/<int:course_id>: Update a course.

Request Body: {"name": "Advanced Programming"}

Response: 200 OK, Updated Course object or 404 Not Found

DELETE /courses/<int:course_id>: Delete a course.

Response: 200 OK, Success message or 404 Not Found

Health Check
GET /health: Check application and database health.

Response: 200 OK, {"status": "healthy", "database_connection": "successful"} or 500 Internal Server Error

Testing
A tests/test_api.py file is included as a placeholder. You can add unit and integration tests for your API endpoints here.

Technologies Used
Flask

Flask-SQLAlchemy

PyMySQL

MySQL