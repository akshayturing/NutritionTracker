# # app/models/__init__.py
# from app.models.user import User
# from app.models.meal import Meal
# from app.models.food_item import FoodItem

# # This allows you to import all models from app.models
# __all__ = ['User', 'Meal', 'FoodItem']
from app.models.food_database import db
from app.models.user import User
from app.models.food import FoodItem, Nutrient, NutrientValue, FoodCategory, food_category_association
from app.models.custom_food import UserCustomFood
from app.models.meal import Meal
# This ensures all models are imported when you import from models
__all__ = [
    'db', 
    'User', 
    'FoodItem', 
    'Nutrient', 
    'NutrientValue', 
    'FoodCategory',
    'UserCustomFood',
    'food_category_association','Meal'
]
