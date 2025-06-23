# # # # # # from app import db
# # # # # # from datetime import datetime

# # # # # # class User(db.Model):
# # # # # #     __tablename__ = 'users'
    
# # # # # #     id = db.Column(db.Integer, primary_key=True)
# # # # # #     name = db.Column(db.String(100), nullable=False)
# # # # # #     email = db.Column(db.String(120), unique=True, nullable=False)
# # # # # #     age = db.Column(db.Integer, db.CheckConstraint('age > 0'), nullable=True)
# # # # # #     weight = db.Column(db.Float, db.CheckConstraint('weight > 0'), nullable=True)
# # # # # #     activity_level = db.Column(db.String(50), nullable=True)
# # # # # #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
# # # # # #     # Relationship with meals
# # # # # #     meals = db.relationship('Meal', backref='user', lazy=True, cascade='all, delete-orphan')
    
# # # # # #     def __repr__(self):
# # # # # #         return f'<User {self.name}>'
    
# # # # # #     def to_dict(self):
# # # # # #         return {
# # # # # #             'id': self.id,
# # # # # #             'name': self.name,
# # # # # #             'email': self.email,
# # # # # #             'age': self.age,
# # # # # #             'weight': self.weight,
# # # # # #             'activity_level': self.activity_level,
# # # # # #             'created_at': self.created_at.isoformat() if self.created_at else None
# # # # # #         }

# # # # # from flask_sqlalchemy import SQLAlchemy
# # # # # from werkzeug.security import generate_password_hash, check_password_hash
# # # # # from datetime import datetime
# # # # # from app.models.food_database import db

# # # # # class User(db.Model):
# # # # #     __tablename__ = 'users'
    
# # # # #     id = db.Column(db.Integer, primary_key=True)
# # # # #     username = db.Column(db.String(80), unique=True, nullable=False)
# # # # #     email = db.Column(db.String(255), unique=True, nullable=False, index=True)
# # # # #     password_hash = db.Column(db.String(128), nullable=False)
# # # # #     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
# # # # #     # Relationships (if needed)
# # # # #     meals = db.relationship('Meal', backref='user', lazy=True, cascade='all, delete-orphan')
    
# # # # #     # Define relationship but defer the foreign key to avoid circular reference
# # # # #     custom_foods = db.relationship('UserCustomFood', back_populates='user',
# # # # #                                   cascade='all, delete-orphan')
# # # # #     def __init__(self, email, password):
# # # # #         self.email = email
# # # # #         self.password = password  # This will use the password.setter method
    
# # # # #     @property
# # # # #     def password(self):
# # # # #         raise AttributeError('Password is not a readable attribute')
    
# # # # #     @password.setter
# # # # #     def password(self, password):
# # # # #         self.password_hash = generate_password_hash(password)
    
# # # # #     def verify_password(self, password):
# # # # #         return check_password_hash(self.password_hash, password)
    
# # # # #     def __repr__(self):
# # # # #         return f'<User {self.email}>'

# # # # """User model for Nutrition Tracking App."""
# # # # from app import db
# # # # from werkzeug.security import generate_password_hash, check_password_hash
# # # # from datetime import datetime

# # # # class User(db.Model):
# # # #     """User model with authentication support."""
# # # #     __tablename__ = 'users'
    
# # # #     id = db.Column(db.Integer, primary_key=True)
# # # #     email = db.Column(db.String(255), unique=True, nullable=False, index=True)
# # # #     password_hash = db.Column(db.String(128), nullable=False)
# # # #     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
# # # #     def __init__(self, email, password):
# # # #         self.email = email
# # # #         self.password = password  # Uses the password.setter method
    
# # # #     @property
# # # #     def password(self):
# # # #         """Prevent password from being accessed."""
# # # #         raise AttributeError('Password is not a readable attribute')
    
# # # #     @password.setter
# # # #     def password(self, password):
# # # #         """Create hashed password."""
# # # #         self.password_hash = generate_password_hash(password)
    
# # # #     def verify_password(self, password):
# # # #         """Check if the provided password matches the stored hash."""
# # # #         return check_password_hash(self.password_hash, password)
    
# # # #     def __repr__(self):
# # # #         """String representation of the user."""
# # # #         return f'<User {self.email}>'

# # # """User model for Nutrition Tracking App."""
# # # from app import db
# # # from werkzeug.security import generate_password_hash, check_password_hash
# # # from datetime import datetime

# # # class User(db.Model):
# # #     """User model with authentication support."""
# # #     __tablename__ = 'users'
    
# # #     # Add extend_existing to allow table redefinition
# # #     __table_args__ = {'extend_existing': True}
    
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     email = db.Column(db.String(255), unique=True, nullable=False, index=True)
# # #     password_hash = db.Column(db.String(128), nullable=False)
# # #     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
# # #     # Relationships
# # #     meals = db.relationship('Meal', back_populates='user', cascade='all, delete-orphan')
    
# # #     def __init__(self, email, password):
# # #         self.email = email
# # #         self.password = password  # Uses the password.setter method
    
# # #     @property
# # #     def password(self):
# # #         """Prevent password from being accessed."""
# # #         raise AttributeError('Password is not a readable attribute')
    
# # #     @password.setter
# # #     def password(self, password):
# # #         """Create hashed password."""
# # #         self.password_hash = generate_password_hash(password)
    
# # #     def verify_password(self, password):
# # #         """Check if the provided password matches the stored hash."""
# # #         return check_password_hash(self.password_hash, password)
    
# # #     def __repr__(self):
# # #         """String representation of the user."""
# # #         return f'<User {self.email}>'

# # # app/models/user.py
# # from sqlalchemy import Column, Integer, String, Float, DateTime
# # from datetime import datetime
# # from app.models import db

# # class User(db.Model):
# #     """User model for authentication and profile information"""
# #     __tablename__ = 'users'
    
# #     id = Column(Integer, primary_key=True)
# #     email = Column(String(120), unique=True, nullable=False)
# #     password_hash = Column(String(128), nullable=False)
# #     name = Column(String(100), nullable=False)
# #     age = Column(Integer, nullable=True)
# #     weight = Column(Float, nullable=True)  # in kg
# #     activity_level = Column(String(20), nullable=True)
# #     created_at = Column(DateTime, default=datetime.utcnow)
    
# #     def __repr__(self):
# #         return f"<User {self.id}: {self.email}>"

# # app/models/user.py
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime

# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False, index=True)
#     password_hash = db.Column(db.String(256), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # User profile data
#     age = db.Column(db.Integer)
#     weight = db.Column(db.Float)  # in kg
#     height = db.Column(db.Float)  # in cm
#     gender = db.Column(db.String(10))
#     activity_level = db.Column(db.String(20))
    
#     # Nutritional targets
#     calorie_goal = db.Column(db.Integer)
#     protein_goal = db.Column(db.Integer)  # in grams
#     carbs_goal = db.Column(db.Integer)    # in grams
#     fat_goal = db.Column(db.Integer)      # in grams
    
#     # Relationships
#     meals = db.relationship('Meal', back_populates='user', lazy='dynamic')
#     custom_foods = db.relationship('UserCustomFood', back_populates='user', lazy='dynamic')
#     custom_foods = db.relationship("UserCustomFood", back_populates="user", cascade="all, delete-orphan")
#     def __init__(self, name, email, password, **kwargs):
#         self.name = name
#         self.email = email
#         self.set_password(password)
        
#         # Set optional profile attributes
#         self.age = kwargs.get('age')
#         self.weight = kwargs.get('weight')
#         self.height = kwargs.get('height')
#         self.gender = kwargs.get('gender')
#         self.activity_level = kwargs.get('activity_level')
        
#         # Set nutritional targets
#         self.calorie_goal = kwargs.get('calorie_goal')
#         self.protein_goal = kwargs.get('protein_goal')
#         self.carbs_goal = kwargs.get('carbs_goal')
#         self.fat_goal = kwargs.get('fat_goal')
    
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
        
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'email': self.email,
#             'age': self.age,
#             'weight': self.weight,
#             'height': self.height,
#             'gender': self.gender,
#             'activity_level': self.activity_level,
#             'calorie_goal': self.calorie_goal,
#             'protein_goal': self.protein_goal,
#             'carbs_goal': self.carbs_goal,
#             'fat_goal': self.fat_goal,
#             'created_at': self.created_at.isoformat() if self.created_at else None
#         }

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    gender = db.Column(db.String(10))
    activity_level = db.Column(db.String(20))

    calorie_goal = db.Column(db.Integer)
    protein_goal = db.Column(db.Integer)
    carbs_goal = db.Column(db.Integer)
    fat_goal = db.Column(db.Integer)

    meals = db.relationship('Meal', back_populates='user', lazy='dynamic')
    custom_foods = db.relationship('UserCustomFood', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, name, email, password, **kwargs):
        self.name = name
        self.email = email
        self.set_password(password)
        self.age = kwargs.get('age')
        self.weight = kwargs.get('weight')
        self.height = kwargs.get('height')
        self.gender = kwargs.get('gender')
        self.activity_level = kwargs.get('activity_level')
        self.calorie_goal = kwargs.get('calorie_goal')
        self.protein_goal = kwargs.get('protein_goal')
        self.carbs_goal = kwargs.get('carbs_goal')
        self.fat_goal = kwargs.get('fat_goal')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'gender': self.gender,
            'activity_level': self.activity_level,
            'calorie_goal': self.calorie_goal,
            'protein_goal': self.protein_goal,
            'carbs_goal': self.carbs_goal,
            'fat_goal': self.fat_goal,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
