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

from app.models.token_blacklist import TokenBlacklist
from app.models.user import User

# Then import food model
from app.models.food import Food, UserCustomFood  # Assuming UserCustomFood exists

# Finally, import meal which depends on both user and food
from app.models.meal import Meal, MealFood