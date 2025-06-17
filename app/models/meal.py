# # # # from app import db
# # # # from datetime import datetime
# # # # import json

# # # # class Meal(db.Model):
# # # #     __tablename__ = 'meals'
    
# # # #     id = db.Column(db.Integer, primary_key=True)
# # # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# # # #     meal_name = db.Column(db.String(100), nullable=False)  # e.g., Breakfast, Lunch, Dinner, Snack
# # # #     timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# # # #     food_items = db.Column(db.Text, nullable=False)  # JSON string of food items
    
# # # #     def __repr__(self):
# # # #         return f'<Meal {self.meal_name} for user {self.user_id}>'
    
# # # #     @property
# # # #     def food_items_list(self):
# # # #         """Convert the food_items JSON string to a Python list"""
# # # #         if self.food_items:
# # # #             return json.loads(self.food_items)
# # # #         return []
    
# # # #     @food_items_list.setter
# # # #     def food_items_list(self, items):
# # # #         """Convert a Python list to a JSON string for storage"""
# # # #         self.food_items = json.dumps(items)
    
# # # #     def to_dict(self):
# # # #         return {
# # # #             'id': self.id,
# # # #             'user_id': self.user_id,
# # # #             'meal_name': self.meal_name,
# # # #             'timestamp': self.timestamp.isoformat(),
# # # #             'food_items': self.food_items_list
# # # #         }

# # # from app import db
# # # from datetime import datetime

# # # # Junction table for the many-to-many relationship between meals and food items
# # # meal_food_items = db.Table('meal_food_items',
# # #     db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'), primary_key=True),
# # #     db.Column('food_item_id', db.Integer, db.ForeignKey('food_items.id'), primary_key=True),
# # #     db.Column('servings', db.Float, nullable=False, default=1.0),  # How many servings of this food
# # #     db.Column('notes', db.Text)
# # # )

# # # class Meal(db.Model):
# # #     __tablename__ = 'meals'
    
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# # #     meal_name = db.Column(db.String(100), nullable=False)  # e.g., Breakfast, Lunch, Dinner, Snack
# # #     meal_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
# # #     meal_time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
# # #     notes = db.Column(db.Text)
# # #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
# # #     # Many-to-many relationship with food items
# # #     food_items = db.relationship('FoodItem', secondary=meal_food_items,
# # #                                backref=db.backref('meals', lazy='dynamic'),
# # #                                lazy='dynamic')
    
# # #     def __repr__(self):
# # #         return f'<Meal {self.meal_name} for user {self.user_id} on {self.meal_date}>'
    
# # #     def to_dict(self):
# # #         # Get food items with serving information
# # #         meal_foods = []
# # #         for food_item, association in db.session.query(
# # #             FoodItem, meal_food_items
# # #         ).filter(
# # #             meal_food_items.c.meal_id == self.id,
# # #             meal_food_items.c.food_item_id == FoodItem.id
# # #         ).all():
# # #             food_dict = food_item.to_dict()
# # #             food_dict['servings'] = association.servings
# # #             food_dict['notes'] = association.notes
            
# # #             # Calculate nutrition for the actual servings
# # #             food_dict['total_calories'] = food_dict['calories'] * association.servings
# # #             food_dict['total_protein'] = food_dict['protein'] * association.servings
# # #             food_dict['total_carbs'] = food_dict['carbs'] * association.servings
# # #             food_dict['total_fats'] = food_dict['fats'] * association.servings
            
# # #             meal_foods.append(food_dict)
        
# # #         return {
# # #             'id': self.id,
# # #             'user_id': self.user_id,
# # #             'meal_name': self.meal_name,
# # #             'meal_date': self.meal_date.isoformat() if self.meal_date else None,
# # #             'meal_time': self.meal_time.isoformat() if self.meal_time else None,
# # #             'notes': self.notes,
# # #             'created_at': self.created_at.isoformat() if self.created_at else None,
# # #             'food_items': meal_foods,
# # #         }

# # from app import db
# # from datetime import datetime

# # class Meal(db.Model):
# #     """Model for user meals in the nutrition tracking app"""
# #     __tablename__ = 'meals'
    
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     name = db.Column(db.String(100), nullable=False)
# #     description = db.Column(db.Text)
# #     date = db.Column(db.Date, default=datetime.utcnow().date)
# #     time = db.Column(db.Time, default=datetime.utcnow().time)
    
# #     # Timestamps
# #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
# #     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
# #     # Relationships
# #     user = db.relationship('User', back_populates='meals')
# #     meal_items = db.relationship('MealItem', back_populates='meal', cascade='all, delete-orphan')
    
# #     def __repr__(self):
# #         return f'<Meal {self.name} ({self.date})>'
    
# #     def to_dict(self):
# #         """Convert meal to dictionary for API responses"""
# #         return {
# #             'id': self.id,
# #             'user_id': self.user_id,
# #             'name': self.name,
# #             'description': self.description,
# #             'date': self.date.isoformat() if self.date else None,
# #             'time': self.time.isoformat() if self.time else None,
# #             'items': [item.to_dict() for item in self.meal_items],
# #             'created_at': self.created_at.isoformat() if self.created_at else None,
# #             'updated_at': self.updated_at.isoformat() if self.updated_at else None
# #         }


# # class MealItem(db.Model):
# #     """Model for individual food items in a meal"""
# #     __tablename__ = 'meal_items'
    
# #     id = db.Column(db.Integer, primary_key=True)
# #     meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
# #     food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
# #     quantity = db.Column(db.Float, nullable=False, default=1.0)
# #     unit = db.Column(db.String(50), nullable=False, default='serving')
    
# #     # Relationships
# #     meal = db.relationship('Meal', back_populates='meal_items')
# #     food = db.relationship('FoodItem')
    
# #     def __repr__(self):
# #         return f'<MealItem {self.food.name if self.food else "Unknown"} ({self.quantity} {self.unit})>'
    
# #     def to_dict(self):
# #         """Convert meal item to dictionary for API responses"""
# #         return {
# #             'id': self.id,
# #             'meal_id': self.meal_id,
# #             'food_id': self.food_id,
# #             'food_name': self.food.name if self.food else "Unknown",
# #             'quantity': self.quantity,
# #             'unit': self.unit,
# #             'food': self.food.to_dict() if self.food else None
# #         }

# """Meal model for Nutrition Tracking App."""
# from app import db
# from datetime import datetime

# class Meal(db.Model):
#     """Meal tracking model."""
#     __tablename__ = 'meals'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     calories = db.Column(db.Integer, nullable=True)
#     date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
#     def __repr__(self):
#         """String representation of the meal."""
#         return f'<Meal {self.name}>'

"""Meal model for Nutrition Tracking App."""
from app import db
from datetime import datetime

class Meal(db.Model):
    """Model for user meals."""
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Define the relationship to MealItem
    food_items = db.relationship('MealItem', back_populates='meal', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def calories(self):
        """Calculate total calories for the meal."""
        total = 0
        for item in self.food_items:
            if item.food and item.food.calories:
                total += item.food.calories * item.quantity
        return total
    
    def __repr__(self):
        """String representation of the meal."""
        return f'<Meal {self.name} ({self.date_time})>'
