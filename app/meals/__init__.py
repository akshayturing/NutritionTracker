# app/meals/__init__.py
from flask import Blueprint

# Create a blueprint with a more specific name to avoid conflicts
meals_bp = Blueprint('nutrition_meals', __name__, url_prefix='/api/meals')

# Import routes after blueprint is created
from app.meals.routes import *

def register_meals_blueprint(app):
    """Register the meals blueprint with the Flask app"""
    app.register_blueprint(meals_bp)