# # # 

# # """Food item model for Nutrition Tracking App."""
# # from app import db
# # from datetime import datetime

# # class FoodItem(db.Model):
# #     """Model for food items with nutritional information."""
# #     __tablename__ = 'food_items'
    
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(100), nullable=False)
# #     description = db.Column(db.Text, nullable=True)
    
# #     # Nutritional information
# #     calories = db.Column(db.Float, nullable=True)
# #     protein = db.Column(db.Float, nullable=True)
# #     carbohydrates = db.Column(db.Float, nullable=True)
# #     fat = db.Column(db.Float, nullable=True)
# #     fiber = db.Column(db.Float, nullable=True)
    
# #     # Metadata
# #     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# #     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
# #     # Define the relationship to MealItem, but defer the foreign key to the MealItem model
# #     # This prevents the circular reference issue
# #     meals = db.relationship('MealItem', back_populates='food', lazy='dynamic')
    
# #     def __repr__(self):
# #         """String representation of the food item."""
# #         return f'<FoodItem {self.name}>'

# """FoodItem model for nutrition data."""
# from app import db
# from datetime import datetime

# class FoodItem(db.Model):
#     """Model for food items with nutritional data."""
#     __tablename__ = 'food_items'
    
#     # Add extend_existing to allow table redefinition
#     __table_args__ = {'extend_existing': True}
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     calories = db.Column(db.Float, nullable=True)
#     protein = db.Column(db.Float, nullable=True)  # in grams
#     carbs = db.Column(db.Float, nullable=True)    # in grams
#     fat = db.Column(db.Float, nullable=True)      # in grams
#     fiber = db.Column(db.Float, nullable=True)    # in grams
#     sugar = db.Column(db.Float, nullable=True)    # in grams
#     sodium = db.Column(db.Float, nullable=True)   # in milligrams
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # Relationship with meals through meal_items
#     meals = db.relationship('MealItem', back_populates='food_item')
    
#     def __repr__(self):
#         """String representation of FoodItem"""
#         return f'<FoodItem {self.name}>'

# app/models/food_item.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import json
from app import db

class FoodItem(db.Model):
    """Model for standard food items in the database"""
    __tablename__ = 'food_items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    portion_size = Column(Float, nullable=False)  # in grams
    calories = Column(Float, nullable=False)
    _macronutrients = Column(String(255), nullable=False, default="{}")
    
    @property
    def macronutrients(self):
        return json.loads(self._macronutrients)
    
    @macronutrients.setter
    def macronutrients(self, value):
        self._macronutrients = json.dumps(value)
    
    def __repr__(self):
        return f"<FoodItem {self.id}: {self.name}>"


# class UserCustomFood(db.Model):
#     """Model for user-created custom food items"""
#     __tablename__ = 'user_custom_foods'
    
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     name = Column(String(100), nullable=False)
#     portion_size = Column(Float, nullable=False)  # in grams
#     calories = Column(Float, nullable=False)
#     _macronutrients = Column(String(255), nullable=False, default="{}")
    
#     # Relationship to User
#     user = relationship('User', backref=db.backref('custom_foods', lazy=True))
    
#     @property
#     def macronutrients(self):
#         return json.loads(self._macronutrients)
    
#     @macronutrients.setter
#     def macronutrients(self, value):
#         self._macronutrients = json.dumps(value)
    
#     def __repr__(self):
#         return f"<UserCustomFood {self.id}: {self.name}>"
