# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import blueprints and database object
from models import db
from routes.student import student_bp, set_socketio as set_student_socketio
from routes.course import course_bp

def create_app():
    app = Flask(__name__)

    # --- Configuration ---
    # Use SQLite for simplicity. For production, consider PostgreSQL or MySQL.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here_please_change_this') # Needed for SocketIO
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # Ensure the instance directory exists for SQLite
    instance_path = os.path.join(app.root_path, 'instance')
    os.makedirs(instance_path, exist_ok=True)

    # --- Initialize Extensions ---
    db.init_app(app) # Initialize SQLAlchemy with the app
    migrate = Migrate(app, db) # Initialize Flask-Migrate
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet') # Allow all origins for development

    # Pass the socketio instance to blueprints that need it
    set_student_socketio(socketio)

    # --- Register Blueprints ---
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)

    # --- SocketIO Event Handlers ---
    @socketio.on('connect')
    def handle_connect():
        print('Client connected:', request.sid)
        # You could emit initial data here, e.g., current registrations

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected:', request.sid)

    # Basic route for testing the frontend/SocketIO connection
    @app.route('/')
    def index():
        return render_template('index.html') # A simple HTML page to test real-time updates

    return app, socketio

# Create app and socketio instances
app, socketio = create_app()

# This block allows you to run the app directly using `python app.py`
# It's better to use `flask run` or a production WSGI server like Gunicorn/Eventlet
# For development with SocketIO, running with eventlet directly is often simpler:
if __name__ == '__main__':
    # To run with Eventlet for SocketIO support:
    # pip install eventlet
    # Then run: python app.py
    # Do NOT use app.run() directly when using Flask-SocketIO unless in a very simple debug scenario.
    print(f"Running in debug mode: {app.config['DEBUG']}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    if app.config['DEBUG']:
        print("NOTE: For real-time functionality (SocketIO), run with `eventlet.wsgi.server` or `flask run` with async_mode set.")
        # Fallback for simple flask run, but won't support SocketIO in some environments
        # app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Starting production server with Eventlet...")
    import eventlet
    import eventlet.wsgi
    # Set the logging level for eventlet to suppress verbose output
    eventlet.logging.getLogger().setLevel(eventlet.logging.WARNING)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

