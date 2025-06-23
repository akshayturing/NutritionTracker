from app.extensions import db

# Import all models so they register with metadata
from .user import User
from .meal import Meal
from .meal import MealFood
from .meal import MealItem
from .food import FoodItem
# from .user_custom_food import UserCustomFood
