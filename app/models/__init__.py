# app/models/__init__.py
from app.models.user import User
from app.models.meal import Meal
from app.models.food_item import FoodItem

# This allows you to import all models from app.models
__all__ = ['User', 'Meal', 'FoodItem']