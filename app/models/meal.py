from app import db
from datetime import datetime
import json

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_name = db.Column(db.String(100), nullable=False)  # e.g., Breakfast, Lunch, Dinner, Snack
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    food_items = db.Column(db.Text, nullable=False)  # JSON string of food items
    
    def __repr__(self):
        return f'<Meal {self.meal_name} for user {self.user_id}>'
    
    @property
    def food_items_list(self):
        """Convert the food_items JSON string to a Python list"""
        if self.food_items:
            return json.loads(self.food_items)
        return []
    
    @food_items_list.setter
    def food_items_list(self, items):
        """Convert a Python list to a JSON string for storage"""
        self.food_items = json.dumps(items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meal_name': self.meal_name,
            'timestamp': self.timestamp.isoformat(),
            'food_items': self.food_items_list
        }