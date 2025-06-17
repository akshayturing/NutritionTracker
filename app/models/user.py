# # # from app import db
# # # from datetime import datetime

# # # class User(db.Model):
# # #     __tablename__ = 'users'
    
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     name = db.Column(db.String(100), nullable=False)
# # #     email = db.Column(db.String(120), unique=True, nullable=False)
# # #     age = db.Column(db.Integer, db.CheckConstraint('age > 0'), nullable=True)
# # #     weight = db.Column(db.Float, db.CheckConstraint('weight > 0'), nullable=True)
# # #     activity_level = db.Column(db.String(50), nullable=True)
# # #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
# # #     # Relationship with meals
# # #     meals = db.relationship('Meal', backref='user', lazy=True, cascade='all, delete-orphan')
    
# # #     def __repr__(self):
# # #         return f'<User {self.name}>'
    
# # #     def to_dict(self):
# # #         return {
# # #             'id': self.id,
# # #             'name': self.name,
# # #             'email': self.email,
# # #             'age': self.age,
# # #             'weight': self.weight,
# # #             'activity_level': self.activity_level,
# # #             'created_at': self.created_at.isoformat() if self.created_at else None
# # #         }

# # from flask_sqlalchemy import SQLAlchemy
# # from werkzeug.security import generate_password_hash, check_password_hash
# # from datetime import datetime
# # from app.models.food_database import db

# # class User(db.Model):
# #     __tablename__ = 'users'
    
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(80), unique=True, nullable=False)
# #     email = db.Column(db.String(255), unique=True, nullable=False, index=True)
# #     password_hash = db.Column(db.String(128), nullable=False)
# #     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
# #     # Relationships (if needed)
# #     meals = db.relationship('Meal', backref='user', lazy=True, cascade='all, delete-orphan')
    
# #     # Define relationship but defer the foreign key to avoid circular reference
# #     custom_foods = db.relationship('UserCustomFood', back_populates='user',
# #                                   cascade='all, delete-orphan')
# #     def __init__(self, email, password):
# #         self.email = email
# #         self.password = password  # This will use the password.setter method
    
# #     @property
# #     def password(self):
# #         raise AttributeError('Password is not a readable attribute')
    
# #     @password.setter
# #     def password(self, password):
# #         self.password_hash = generate_password_hash(password)
    
# #     def verify_password(self, password):
# #         return check_password_hash(self.password_hash, password)
    
# #     def __repr__(self):
# #         return f'<User {self.email}>'

# """User model for Nutrition Tracking App."""
# from app import db
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime

# class User(db.Model):
#     """User model with authentication support."""
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False, index=True)
#     password_hash = db.Column(db.String(128), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
#     def __init__(self, email, password):
#         self.email = email
#         self.password = password  # Uses the password.setter method
    
#     @property
#     def password(self):
#         """Prevent password from being accessed."""
#         raise AttributeError('Password is not a readable attribute')
    
#     @password.setter
#     def password(self, password):
#         """Create hashed password."""
#         self.password_hash = generate_password_hash(password)
    
#     def verify_password(self, password):
#         """Check if the provided password matches the stored hash."""
#         return check_password_hash(self.password_hash, password)
    
#     def __repr__(self):
#         """String representation of the user."""
#         return f'<User {self.email}>'

"""User model for Nutrition Tracking App."""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """User model with authentication support."""
    __tablename__ = 'users'
    
    # Add extend_existing to allow table redefinition
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    meals = db.relationship('Meal', back_populates='user', cascade='all, delete-orphan')
    
    def __init__(self, email, password):
        self.email = email
        self.password = password  # Uses the password.setter method
    
    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """String representation of the user."""
        return f'<User {self.email}>'
