# models/food.py
from app import db
from datetime import datetime

# Association table for food categories
food_category_association = db.Table('food_category_association',
    db.Column('food_id', db.Integer, db.ForeignKey('food_items.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('food_categories.id'), primary_key=True)
)

class FoodItem(db.Model):
    """Model for food items in the database"""
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    # Food composition basics
    serving_size = db.Column(db.Float, nullable=False, default=100.0)
    serving_unit = db.Column(db.String(50), nullable=False, default='g')
    serving_description = db.Column(db.String(255))
    
    # Source information
    source = db.Column(db.String(255), default='internal')
    source_id = db.Column(db.String(255))  # External ID if imported
    verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    nutrients = db.relationship('NutrientValue', back_populates='food', cascade='all, delete-orphan')
    categories = db.relationship('FoodCategory', secondary=food_category_association, 
                                back_populates='foods')
    # Define relationship to UserCustomFood but defer the implementation
    custom_food_entries = db.relationship('UserCustomFood', back_populates='food')
    
    def __repr__(self):
        return f'<FoodItem {self.name}>'

    def to_dict(self):
        """Convert food item to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'description': self.description,
            'serving_size': self.serving_size,
            'serving_unit': self.serving_unit,
            'serving_description': self.serving_description,
            'categories': [category.name for category in self.categories],
            'nutrients': {nv.nutrient.code: {
                'value': nv.value,
                'unit': nv.nutrient.unit,
                'name': nv.nutrient.name
            } for nv in self.nutrients},
            'verified': self.verified,
            'source': self.source
        }

class Nutrient(db.Model):
    """Model for nutrient definitions"""
    __tablename__ = 'nutrients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), nullable=False, unique=True)
    unit = db.Column(db.String(20), nullable=False)
    
    # Nutrient categories (macros, vitamins, minerals, etc.)
    category = db.Column(db.String(50))
    
    # For organizing display
    display_order = db.Column(db.Integer)
    
    # Relationships
    nutrient_values = db.relationship('NutrientValue', back_populates='nutrient')
    
    def __repr__(self):
        return f'<Nutrient {self.code}: {self.name}>'

class NutrientValue(db.Model):
    """Model for nutrient values per food item"""
    __tablename__ = 'nutrient_values'

    # Composite primary key
    food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), primary_key=True)
    nutrient_id = db.Column(db.Integer, db.ForeignKey('nutrients.id'), primary_key=True)
    
    # Value per serving size of the food
    value = db.Column(db.Float, nullable=False)
    
    # Relationships
    food = db.relationship('FoodItem', back_populates='nutrients')
    nutrient = db.relationship('Nutrient', back_populates='nutrient_values')
    
    def __repr__(self):
        return f'<NutrientValue {self.food.name} - {self.nutrient.name}: {self.value} {self.nutrient.unit}>'

class FoodCategory(db.Model):
    """Model for food categories"""
    __tablename__ = 'food_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relationships
    foods = db.relationship('FoodItem', secondary=food_category_association, 
                           back_populates='categories')
                           
    def __repr__(self):
        return f'<FoodCategory {self.name}>'