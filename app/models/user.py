from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint('age > 0'), nullable=True)
    weight = db.Column(db.Float, db.CheckConstraint('weight > 0'), nullable=True)
    activity_level = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with meals
    meals = db.relationship('Meal', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'weight': self.weight,
            'activity_level': self.activity_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }