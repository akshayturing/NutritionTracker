# # """API package for Nutrition Tracking App."""
# # from flask import Blueprint

# # # Create the API blueprint
# # api_bp = Blueprint('api', __name__)

# # # Import routes after blueprint creation to avoid circular imports
# # from app.api import routes

# from app.models.user import User
# from app.models.token import TokenBlacklist

# # Then import models with dependencies in the correct order
# from app.models.food_item import FoodItem
# from app.models.meal import Meal
# from app.models.meal_item import MealItem

# # You can add __all__ to explicitly define what gets imported with 'from app.models import *'
# __all__ = ['User', 'TokenBlacklist', 'FoodItem', 'Meal', 'MealItem']
from flask import Blueprint

api_bp = Blueprint("api", __name__)

from app.api import routes