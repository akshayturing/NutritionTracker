# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Create database instance
db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from app.models.user import User
from app.models.meal import Meal
from app.models.food_item import FoodItem, UserCustomFood  # Add this import

# Define a specific import order
__all__ = ['db', 'User', 'FoodItem', 'UserCustomFood', 'Meal']