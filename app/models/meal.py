# # # # # # # # from app import db
# # # # # # # # from datetime import datetime
# # # # # # # # import json

# # # # # # # # class Meal(db.Model):
# # # # # # # #     __tablename__ = 'meals'
    
# # # # # # # #     id = db.Column(db.Integer, primary_key=True)
# # # # # # # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# # # # # # # #     meal_name = db.Column(db.String(100), nullable=False)  # e.g., Breakfast, Lunch, Dinner, Snack
# # # # # # # #     timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# # # # # # # #     food_items = db.Column(db.Text, nullable=False)  # JSON string of food items
    
# # # # # # # #     def __repr__(self):
# # # # # # # #         return f'<Meal {self.meal_name} for user {self.user_id}>'
    
# # # # # # # #     @property
# # # # # # # #     def food_items_list(self):
# # # # # # # #         """Convert the food_items JSON string to a Python list"""
# # # # # # # #         if self.food_items:
# # # # # # # #             return json.loads(self.food_items)
# # # # # # # #         return []
    
# # # # # # # #     @food_items_list.setter
# # # # # # # #     def food_items_list(self, items):
# # # # # # # #         """Convert a Python list to a JSON string for storage"""
# # # # # # # #         self.food_items = json.dumps(items)
    
# # # # # # # #     def to_dict(self):
# # # # # # # #         return {
# # # # # # # #             'id': self.id,
# # # # # # # #             'user_id': self.user_id,
# # # # # # # #             'meal_name': self.meal_name,
# # # # # # # #             'timestamp': self.timestamp.isoformat(),
# # # # # # # #             'food_items': self.food_items_list
# # # # # # # #         }

# # # # # # # from app import db
# # # # # # # from datetime import datetime

# # # # # # # # Junction table for the many-to-many relationship between meals and food items
# # # # # # # meal_food_items = db.Table('meal_food_items',
# # # # # # #     db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'), primary_key=True),
# # # # # # #     db.Column('food_item_id', db.Integer, db.ForeignKey('food_items.id'), primary_key=True),
# # # # # # #     db.Column('servings', db.Float, nullable=False, default=1.0),  # How many servings of this food
# # # # # # #     db.Column('notes', db.Text)
# # # # # # # )

# # # # # # # class Meal(db.Model):
# # # # # # #     __tablename__ = 'meals'
    
# # # # # # #     id = db.Column(db.Integer, primary_key=True)
# # # # # # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# # # # # # #     meal_name = db.Column(db.String(100), nullable=False)  # e.g., Breakfast, Lunch, Dinner, Snack
# # # # # # #     meal_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
# # # # # # #     meal_time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
# # # # # # #     notes = db.Column(db.Text)
# # # # # # #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
# # # # # # #     # Many-to-many relationship with food items
# # # # # # #     food_items = db.relationship('FoodItem', secondary=meal_food_items,
# # # # # # #                                backref=db.backref('meals', lazy='dynamic'),
# # # # # # #                                lazy='dynamic')
    
# # # # # # #     def __repr__(self):
# # # # # # #         return f'<Meal {self.meal_name} for user {self.user_id} on {self.meal_date}>'
    
# # # # # # #     def to_dict(self):
# # # # # # #         # Get food items with serving information
# # # # # # #         meal_foods = []
# # # # # # #         for food_item, association in db.session.query(
# # # # # # #             FoodItem, meal_food_items
# # # # # # #         ).filter(
# # # # # # #             meal_food_items.c.meal_id == self.id,
# # # # # # #             meal_food_items.c.food_item_id == FoodItem.id
# # # # # # #         ).all():
# # # # # # #             food_dict = food_item.to_dict()
# # # # # # #             food_dict['servings'] = association.servings
# # # # # # #             food_dict['notes'] = association.notes
            
# # # # # # #             # Calculate nutrition for the actual servings
# # # # # # #             food_dict['total_calories'] = food_dict['calories'] * association.servings
# # # # # # #             food_dict['total_protein'] = food_dict['protein'] * association.servings
# # # # # # #             food_dict['total_carbs'] = food_dict['carbs'] * association.servings
# # # # # # #             food_dict['total_fats'] = food_dict['fats'] * association.servings
            
# # # # # # #             meal_foods.append(food_dict)
        
# # # # # # #         return {
# # # # # # #             'id': self.id,
# # # # # # #             'user_id': self.user_id,
# # # # # # #             'meal_name': self.meal_name,
# # # # # # #             'meal_date': self.meal_date.isoformat() if self.meal_date else None,
# # # # # # #             'meal_time': self.meal_time.isoformat() if self.meal_time else None,
# # # # # # #             'notes': self.notes,
# # # # # # #             'created_at': self.created_at.isoformat() if self.created_at else None,
# # # # # # #             'food_items': meal_foods,
# # # # # # #         }

# # # # # # from app import db
# # # # # # from datetime import datetime

# # # # # # class Meal(db.Model):
# # # # # #     """Model for user meals in the nutrition tracking app"""
# # # # # #     __tablename__ = 'meals'
    
# # # # # #     id = db.Column(db.Integer, primary_key=True)
# # # # # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# # # # # #     name = db.Column(db.String(100), nullable=False)
# # # # # #     description = db.Column(db.Text)
# # # # # #     date = db.Column(db.Date, default=datetime.utcnow().date)
# # # # # #     time = db.Column(db.Time, default=datetime.utcnow().time)
    
# # # # # #     # Timestamps
# # # # # #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
# # # # # #     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
# # # # # #     # Relationships
# # # # # #     user = db.relationship('User', back_populates='meals')
# # # # # #     meal_items = db.relationship('MealItem', back_populates='meal', cascade='all, delete-orphan')
    
# # # # # #     def __repr__(self):
# # # # # #         return f'<Meal {self.name} ({self.date})>'
    
# # # # # #     def to_dict(self):
# # # # # #         """Convert meal to dictionary for API responses"""
# # # # # #         return {
# # # # # #             'id': self.id,
# # # # # #             'user_id': self.user_id,
# # # # # #             'name': self.name,
# # # # # #             'description': self.description,
# # # # # #             'date': self.date.isoformat() if self.date else None,
# # # # # #             'time': self.time.isoformat() if self.time else None,
# # # # # #             'items': [item.to_dict() for item in self.meal_items],
# # # # # #             'created_at': self.created_at.isoformat() if self.created_at else None,
# # # # # #             'updated_at': self.updated_at.isoformat() if self.updated_at else None
# # # # # #         }


# # # # # # class MealItem(db.Model):
# # # # # #     """Model for individual food items in a meal"""
# # # # # #     __tablename__ = 'meal_items'
    
# # # # # #     id = db.Column(db.Integer, primary_key=True)
# # # # # #     meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
# # # # # #     food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
# # # # # #     quantity = db.Column(db.Float, nullable=False, default=1.0)
# # # # # #     unit = db.Column(db.String(50), nullable=False, default='serving')
    
# # # # # #     # Relationships
# # # # # #     meal = db.relationship('Meal', back_populates='meal_items')
# # # # # #     food = db.relationship('FoodItem')
    
# # # # # #     def __repr__(self):
# # # # # #         return f'<MealItem {self.food.name if self.food else "Unknown"} ({self.quantity} {self.unit})>'
    
# # # # # #     def to_dict(self):
# # # # # #         """Convert meal item to dictionary for API responses"""
# # # # # #         return {
# # # # # #             'id': self.id,
# # # # # #             'meal_id': self.meal_id,
# # # # # #             'food_id': self.food_id,
# # # # # #             'food_name': self.food.name if self.food else "Unknown",
# # # # # #             'quantity': self.quantity,
# # # # # #             'unit': self.unit,
# # # # # #             'food': self.food.to_dict() if self.food else None
# # # # # #         }

# # # # # """Meal model for Nutrition Tracking App."""
# # # # # from app import db
# # # # # from datetime import datetime

# # # # # class Meal(db.Model):
# # # # #     """Meal tracking model."""
# # # # #     __tablename__ = 'meals'
    
# # # # #     id = db.Column(db.Integer, primary_key=True)
# # # # #     name = db.Column(db.String(100), nullable=False)
# # # # #     calories = db.Column(db.Integer, nullable=True)
# # # # #     date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# # # # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
# # # # #     def __repr__(self):
# # # # #         """String representation of the meal."""
# # # # #         return f'<Meal {self.name}>'

# # # # """Meal model for Nutrition Tracking App."""
# # # # from app import db
# # # # from datetime import datetime

# # # # class Meal(db.Model):
# # # #     """Model for user meals."""
# # # #     __tablename__ = 'meals'
    
# # # #     id = db.Column(db.Integer, primary_key=True)
# # # #     name = db.Column(db.String(100), nullable=False)
# # # #     date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# # # #     notes = db.Column(db.Text, nullable=True)
# # # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# # # #     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
# # # #     # Define the relationship to MealItem
# # # #     food_items = db.relationship('MealItem', back_populates='meal', lazy='dynamic', cascade='all, delete-orphan')
    
# # # #     @property
# # # #     def calories(self):
# # # #         """Calculate total calories for the meal."""
# # # #         total = 0
# # # #         for item in self.food_items:
# # # #             if item.food and item.food.calories:
# # # #                 total += item.food.calories * item.quantity
# # # #         return total
    
# # # #     def __repr__(self):
# # # #         """String representation of the meal."""
# # # #         return f'<Meal {self.name} ({self.date_time})>'

# # # """Meal model for Nutrition Tracking App."""
# # # from app import db
# # # from datetime import datetime

# # # class Meal(db.Model):
# # #     """Meal tracking model."""
# # #     __tablename__ = 'meals'
    
# # #     # Add extend_existing to allow table redefinition
# # #     __table_args__ = {'extend_existing': True}
    
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     name = db.Column(db.String(100), nullable=False)
# # #     description = db.Column(db.Text, nullable=True)
# # #     date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
# # #     # Relationship with food items through meal_items
# # #     food_items = db.relationship('MealItem', back_populates='meal', cascade='all, delete-orphan')
    
# # #     # Relationship with user
# # #     user = db.relationship('User', back_populates='meals')
    
# # #     def __repr__(self):
# # #         """String representation of the meal."""
# # #         return f'<Meal {self.name}>'

# # # app/models/meal.py
# # from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
# # from datetime import datetime
# # import json
# # from app.models import db

# # class Meal(db.Model):
# #     __tablename__ = 'meals'
    
# #     id = Column(Integer, primary_key=True)
# #     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
# #     meal_name = Column(String(100), nullable=False)
# #     portion_size = Column(Float, nullable=False)  # in grams
# #     timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
# #     calories = Column(Float, nullable=False)
    
# #     # Store macronutrients as JSON
# #     _macronutrients = Column(String(255), nullable=False, default="{}")
    
# #     @property
# #     def macronutrients(self):
# #         return json.loads(self._macronutrients)
    
# #     @macronutrients.setter
# #     def macronutrients(self, value):
# #         self._macronutrients = json.dumps(value)
    
# #     # Relationship with User model
# #     user = db.relationship('User', backref=db.backref('meals', lazy=True))
    
# #     def __init__(self, user_id, meal_name, portion_size, calories, macronutrients=None, timestamp=None):
# #         self.user_id = user_id
# #         self.meal_name = meal_name
# #         self.portion_size = portion_size
# #         self.calories = calories
        
# #         # Set default macronutrients if none provided
# #         if macronutrients is None:
# #             macronutrients = {'protein': 0, 'carbs': 0, 'fat': 0}
# #         self.macronutrients = macronutrients
        
# #         if timestamp:
# #             self.timestamp = timestamp
    
# #     def __repr__(self):
# #         return f"<Meal {self.id}: {self.meal_name} ({self.calories} calories)>"
    
# #     def calculate_nutrition_totals(self):
# #         """Calculate and update total nutrition values for the meal"""
# #         self.total_calories = 0
# #         self.total_protein = 0
# #         self.total_carbohydrates = 0
# #         self.total_fat = 0
        
# #         for meal_food in self.foods:
# #             food = Food.query.get(meal_food.food_id)
# #             if food:
# #                 # Adjust based on portion size
# #                 portion_ratio = meal_food.portion_size / food.reference_portion_size
# #                 self.total_calories += food.calories * portion_ratio
# #                 self.total_protein += food.protein * portion_ratio
# #                 self.total_carbohydrates += food.carbohydrates * portion_ratio
# #                 self.total_fat += food.fat * portion_ratio
        
# #         # Round to 1 decimal place for better display
# #         self.total_calories = round(self.total_calories, 1)
# #         self.total_protein = round(self.total_protein, 1)
# #         self.total_carbohydrates = round(self.total_carbohydrates, 1)
# #         self.total_fat = round(self.total_fat, 1)

# #     def to_dict(self, include_foods=True):
# #         """Convert meal to dictionary for JSON serialization"""
# #         result = {
# #             'id': self.id,
# #             'user_id': self.user_id,
# #             'meal_name': self.meal_name,
# #             'meal_type': self.meal_type,
# #             'timestamp': self.timestamp.isoformat(),
# #             'notes': self.notes,
# #             'total_calories': self.total_calories,
# #             'total_protein': self.total_protein,
# #             'total_carbohydrates': self.total_carbohydrates,
# #             'total_fat': self.total_fat
# #         }
        
# #         if include_foods:
# #             result['foods'] = []
# #             for meal_food in self.foods:
# #                 food = Food.query.get(meal_food.food_id)
# #                 if food:
# #                     portion_ratio = meal_food.portion_size / food.reference_portion_size
# #                     food_data = {
# #                         'food_id': food.id,
# #                         'name': food.name,
# #                         'portion_size': meal_food.portion_size,
# #                         'portion_unit': meal_food.portion_unit,
# #                         'calories': round(food.calories * portion_ratio, 1),
# #                         'protein': round(food.protein * portion_ratio, 1),
# #                         'carbohydrates': round(food.carbohydrates * portion_ratio, 1),
# #                         'fat': round(food.fat * portion_ratio, 1)
# #                     }
# #                     result['foods'].append(food_data)
        
# #         return result

# # app/models/meal.py
# from app import db
# from datetime import datetime
# from sqlalchemy.ext.hybrid import hybrid_property

# class Meal(db.Model):
#     """Association model between Meal and Food with portion information"""
#     __tablename__ = 'meal_foods'
    
#     id = db.Column(db.Integer, primary_key=True)
#     meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
#     food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
#     portion_size = db.Column(db.Float, nullable=False, default=1.0)
#     portion_unit = db.Column(db.String(50), default='serving')  # e.g., cup, ounce, gram
    
#     # Relationships
#     meal = db.relationship("Meal", back_populates="foods")
#     food = db.relationship("Food", back_populates="meal_foods")  # Changed from "meals" to "meal_foods"
# # class Meal(db.Model):
# #     __tablename__ = 'meals'
    
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     meal_name = db.Column(db.String(100), nullable=False)
# #     meal_type = db.Column(db.String(50))  # breakfast, lunch, dinner, snack
# #     timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# #     notes = db.Column(db.Text)
    
# #     # Nutritional totals
# #     total_calories = db.Column(db.Float, default=0)
# #     total_protein = db.Column(db.Float, default=0)
# #     total_carbohydrates = db.Column(db.Float, default=0)
# #     total_fat = db.Column(db.Float, default=0)
    
# #     # Relationships
# #     foods = db.relationship('MealFood', back_populates='meal', lazy='dynamic', cascade='all, delete-orphan')
# #     user = db.relationship('User', back_populates='meals')
    
#     def __repr__(self):
#         return f'<Meal {self.meal_name} ({self.meal_type}) - {self.timestamp}>'
    
#     def calculate_nutrition_totals(self):
#         """Calculate and update total nutrition values for the meal"""
#         from app.models.food import Food
        
#         self.total_calories = 0
#         self.total_protein = 0
#         self.total_carbohydrates = 0
#         self.total_fat = 0
        
#         for meal_food in self.foods:
#             # Load the food
#             food = Food.query.get(meal_food.food_id)
#             if food:
#                 # Calculate portion ratio
#                 reference_size = getattr(food, 'reference_portion_size', 1)
#                 if reference_size == 0:  # Avoid division by zero
#                     reference_size = 1
                    
#                 portion_ratio = meal_food.portion_size / reference_size
                
#                 # Add nutritional values adjusted for portion size
#                 self.total_calories += food.calories * portion_ratio
#                 self.total_protein += food.protein * portion_ratio
#                 self.total_carbohydrates += food.carbohydrates * portion_ratio
#                 self.total_fat += food.fat * portion_ratio
        
#         # Round to 1 decimal place for better display
#         self.total_calories = round(self.total_calories, 1)
#         self.total_protein = round(self.total_protein, 1)
#         self.total_carbohydrates = round(self.total_carbohydrates, 1)
#         self.total_fat = round(self.total_fat, 1)
    
#     def to_dict(self, include_foods=True):
#         """Convert meal to dictionary for JSON serialization"""
#         from app.models.food import Food
        
#         result = {
#             'id': self.id,
#             'user_id': self.user_id,
#             'meal_name': self.meal_name,
#             'meal_type': self.meal_type,
#             'timestamp': self.timestamp.isoformat(),
#             'notes': self.notes,
#             'total_calories': self.total_calories,
#             'total_protein': self.total_protein,
#             'total_carbohydrates': self.total_carbohydrates,
#             'total_fat': self.total_fat
#         }
        
#         if include_foods:
#             result['foods'] = []
#             for meal_food in self.foods:
#                 food = Food.query.get(meal_food.food_id)
#                 if food:
#                     # Calculate portion ratio
#                     reference_size = getattr(food, 'reference_portion_size', 1)
#                     if reference_size == 0:  # Avoid division by zero
#                         reference_size = 1
                    
#                     portion_ratio = meal_food.portion_size / reference_size
                    
#                     food_data = {
#                         'food_id': food.id,
#                         'name': food.name,
#                         'portion_size': meal_food.portion_size,
#                         'portion_unit': meal_food.portion_unit,
#                         'calories': round(food.calories * portion_ratio, 1),
#                         'protein': round(food.protein * portion_ratio, 1),
#                         'carbohydrates': round(food.carbohydrates * portion_ratio, 1),
#                         'fat': round(food.fat * portion_ratio, 1)
#                     }
#                     result['foods'].append(food_data)
        
#         return result


# # Add the missing MealFood class that's being imported in __init__.py
# class MealFood(db.Model):
#     __tablename__ = 'meal_foods'
#     __table_args__ = {'extend_existing': True} 
#     id = db.Column(db.Integer, primary_key=True)
#     meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
#     food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
#     portion_size = db.Column(db.Float, default=1.0, nullable=False)  # Amount of food
#     portion_unit = db.Column(db.String(50), default='serving')  # Unit of measurement (serving, cup, oz, etc.)
    
#     # Relationships
#     meal = db.relationship('Meal', back_populates='foods')
#     food = db.relationship('Food')  # Simple reference to the food item
    
#     def __repr__(self):
#         return f'<MealFood {self.id}: Meal {self.meal_id} - Food {self.food_id}>'

from app.extensions import db
from datetime import datetime

class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_name = db.Column(db.String(100), nullable=False)
    meal_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    total_calories = db.Column(db.Float, default=0)
    total_protein = db.Column(db.Float, default=0)
    total_carbohydrates = db.Column(db.Float, default=0)
    total_fat = db.Column(db.Float, default=0)

    foods = db.relationship('MealFood', back_populates='meal', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='meals')

    def __repr__(self):
        return f'<Meal {self.meal_name} ({self.meal_type})>'

class MealFood(db.Model):
    __tablename__ = 'meal_foods'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)

    portion_size = db.Column(db.Float, default=1.0, nullable=False)
    portion_unit = db.Column(db.String(50), default='serving')

    meal = db.relationship('Meal', back_populates='foods')
    food = db.relationship('Food', back_populates='meal_foods')

    def __repr__(self):
        return f'<MealFood {self.id}: Meal {self.meal_id} - Food {self.food_id}>'


class MealItem(db.Model):
    __tablename__ = 'meal_items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    serving_size = db.Column(db.String(50), nullable=True)

    meal = db.relationship('Meal', backref='meal_items')
    food_item = db.relationship('FoodItem', backref='meal_items')

    def __repr__(self):
        return f'<MealItem meal_id={self.meal_id} food_id={self.food_item_id}>'
