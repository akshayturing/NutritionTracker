# # """Junction model for meals and food items."""
# # from app import db
# # from datetime import datetime

# # class MealItem(db.Model):
# #     """Many-to-many relationship between Meals and FoodItems."""
# #     __tablename__ = 'meal_items'
    
# #     id = db.Column(db.Integer, primary_key=True)
# #     meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
# #     food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
# #     quantity = db.Column(db.Float, nullable=False, default=1.0)
# #     serving_size = db.Column(db.String(50), nullable=True)
# #     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
# #     # Define relationships to parent models
# #     meal = db.relationship('Meal', back_populates='food_items')
# #     food = db.relationship('FoodItem', back_populates='meals')
    
# #     def __repr__(self):
# #         """String representation of the meal item."""
# #         return f'<MealItem: {self.quantity} of food_id {self.food_id} in meal_id {self.meal_id}>'

# """MealItem model for junction between Meals and FoodItems."""
# from app import db

# class MealItem(db.Model):
#     """Junction model for many-to-many relationship between Meal and FoodItem."""
#     __tablename__ = 'meal_items'
    
#     # Add extend_existing to allow table redefinition
#     __table_args__ = {'extend_existing': True}
    
#     id = db.Column(db.Integer, primary_key=True)
#     meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
#     food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
#     quantity = db.Column(db.Float, nullable=False, default=1.0)
#     serving_size = db.Column(db.String(50), nullable=True)
    
#     # Relationships
#     meal = db.relationship('Meal', back_populates='food_items')
#     food_item = db.relationship('FoodItem', back_populates='meals')
    
#     def __repr__(self):
#         """String representation of MealItem"""
#         return f'<MealItem meal_id={self.meal_id} food_id={self.food_item_id}>'

from app.extensions import db
