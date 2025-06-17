# from app import db
# from datetime import datetime

# class User(db.Model):
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     age = db.Column(db.Integer, db.CheckConstraint('age > 0'), nullable=True)
#     weight = db.Column(db.Float, db.CheckConstraint('weight > 0'), nullable=True)
#     activity_level = db.Column(db.String(50), nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # Relationship with meals
#     meals = db.relationship('Meal', backref='user', lazy=True, cascade='all, delete-orphan')
    
#     def __repr__(self):
#         return f'<User {self.name}>'
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'email': self.email,
#             'age': self.age,
#             'weight': self.weight,
#             'activity_level': self.activity_level,
#             'created_at': self.created_at.isoformat() if self.created_at else None
#         }

from app.models.food_database import db
class User(db.Model):
    """User model for authentication and personalization"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Define relationship but defer the foreign key to avoid circular reference
    custom_foods = db.relationship('UserCustomFood', back_populates='user',
                                  cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'