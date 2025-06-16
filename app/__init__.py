from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Create Flask app
    app = Flask(__name__)
    
    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrition_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Import and register blueprints/routes
    from app.routes.user_routes import user_bp
    from app.routes.meal_routes import meal_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(meal_bp, url_prefix='/api/meals')
    
    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()
    
    return app