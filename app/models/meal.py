# from app import db
# from datetime import datetime
# import json

# class Meal(db.Model):
#     __tablename__ = 'meals'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     meal_name = db.Column(db.String(100), nullable=False)  # e.g., Breakfast, Lunch, Dinner, Snack
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     food_items = db.Column(db.Text, nullable=False)  # JSON string of food items
    
#     def __repr__(self):
#         return f'<Meal {self.meal_name} for user {self.user_id}>'
    
#     @property
#     def food_items_list(self):
#         """Convert the food_items JSON string to a Python list"""
#         if self.food_items:
#             return json.loads(self.food_items)
#         return []
    
#     @food_items_list.setter
#     def food_items_list(self, items):
#         """Convert a Python list to a JSON string for storage"""
#         self.food_items = json.dumps(items)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'meal_name': self.meal_name,
#             'timestamp': self.timestamp.isoformat(),
#             'food_items': self.food_items_list
#         }

from app import db
from datetime import datetime

# Junction table for the many-to-many relationship between meals and food items
meal_food_items = db.Table('meal_food_items',
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'), primary_key=True),
    db.Column('food_item_id', db.Integer, db.ForeignKey('food_items.id'), primary_key=True),
    db.Column('servings', db.Float, nullable=False, default=1.0),  # How many servings of this food
    db.Column('notes', db.Text)
)

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_name = db.Column(db.String(100), nullable=False)  # e.g., Breakfast, Lunch, Dinner, Snack
    meal_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    meal_time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with food items
    food_items = db.relationship('FoodItem', secondary=meal_food_items,
                               backref=db.backref('meals', lazy='dynamic'),
                               lazy='dynamic')
    
    def __repr__(self):
        return f'<Meal {self.meal_name} for user {self.user_id} on {self.meal_date}>'
    
    def to_dict(self):
        # Get food items with serving information
        meal_foods = []
        for food_item, association in db.session.query(
            FoodItem, meal_food_items
        ).filter(
            meal_food_items.c.meal_id == self.id,
            meal_food_items.c.food_item_id == FoodItem.id
        ).all():
            food_dict = food_item.to_dict()
            food_dict['servings'] = association.servings
            food_dict['notes'] = association.notes
            
            # Calculate nutrition for the actual servings
            food_dict['total_calories'] = food_dict['calories'] * association.servings
            food_dict['total_protein'] = food_dict['protein'] * association.servings
            food_dict['total_carbs'] = food_dict['carbs'] * association.servings
            food_dict['total_fats'] = food_dict['fats'] * association.servings
            
            meal_foods.append(food_dict)
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meal_name': self.meal_name,
            'meal_date': self.meal_date.isoformat() if self.meal_date else None,
            'meal_time': self.meal_time.isoformat() if self.meal_time else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'food_items': meal_foods,
        }