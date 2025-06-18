# app/meals/__init__.py
from flask import Blueprint

# Create a blueprint for meal tracking endpoints
meals_bp = Blueprint('meals', __name__, url_prefix='/api/meals')

# Import routes after blueprint is created
from app.meals.routes import *

def register_meals_blueprint(app):
    """Register the meals blueprint with the Flask app"""
    app.register_blueprint(meals_bp)