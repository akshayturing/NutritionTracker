# 

"""Food item model for Nutrition Tracking App."""
from app import db
from datetime import datetime

class FoodItem(db.Model):
    """Model for food items with nutritional information."""
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Nutritional information
    calories = db.Column(db.Float, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    carbohydrates = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    fiber = db.Column(db.Float, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Define the relationship to MealItem, but defer the foreign key to the MealItem model
    # This prevents the circular reference issue
    meals = db.relationship('MealItem', back_populates='food', lazy='dynamic')
    
    def __repr__(self):
        """String representation of the food item."""
        return f'<FoodItem {self.name}>'