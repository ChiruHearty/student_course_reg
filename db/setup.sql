-- db/setup.sql

-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS student_course_db;

-- Use the newly created database
USE student_course_db;

-- Create the 'student' table
CREATE TABLE IF NOT EXISTS student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the 'course' table
CREATE TABLE IF NOT EXISTS course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the 'student_courses' junction table for many-to-many relationship
CREATE TABLE IF NOT EXISTS student_courses (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
);

-- Optional: Add some initial data for testing
INSERT INTO student (name, email) VALUES
    ('Alice Smith', 'alice@example.com'),
    ('Bob Johnson', 'bob@example.com');

INSERT INTO course (name, code, description) VALUES
    ('Introduction to Programming', 'CS101', 'Fundamentals of programming.'),
    ('Database Management', 'DB201', 'Principles of database systems.');

-- You can also add initial registrations here if needed
INSERT INTO student_courses (student_id, course_id) VALUES
     (1, 1), -- Alice takes CS101
     (1, 2), -- Alice takes DB201
     (2, 1); -- Bob takes CS101
