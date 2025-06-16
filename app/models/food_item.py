from app import db
from sqlalchemy.dialects.sqlite import JSON

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    brand = db.Column(db.String(100))
    serving_size = db.Column(db.Float, nullable=False)
    serving_unit = db.Column(db.String(50), nullable=False)  # g, ml, oz, etc.
    
    # Macronutrients (required fields)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    
    # Additional macronutrient details
    fiber = db.Column(db.Float)
    sugar = db.Column(db.Float)
    saturated_fats = db.Column(db.Float)
    unsaturated_fats = db.Column(db.Float)
    trans_fats = db.Column(db.Float)
    
    # Micronutrients stored as JSON for flexibility
    # Example: {"vitamin_a": 200, "vitamin_c": 15, "calcium": 50, "iron": 2.5}
    micronutrients = db.Column(JSON)
    
    # Metadata
    is_verified = db.Column(db.Boolean, default=False)  # For admin-verified entries
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())
    
    # Relationships
    creator = db.relationship('User', backref=db.backref('created_foods', lazy=True))
    
    def __repr__(self):
        return f'<FoodItem {self.name} ({self.serving_size} {self.serving_unit})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'serving_size': self.serving_size,
            'serving_unit': self.serving_unit,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fats': self.fats,
            'fiber': self.fiber,
            'sugar': self.sugar,
            'saturated_fats': self.saturated_fats,
            'unsaturated_fats': self.unsaturated_fats,
            'trans_fats': self.trans_fats,
            'micronutrients': self.micronutrients,
            'is_verified': self.is_verified,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }