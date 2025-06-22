# from app import db

# class UserCustomFood(db.Model):
#     """Model for user-created custom foods"""
#     __tablename__ = 'user_custom_foods'
#     __table_args__ = {'extend_existing': True} 
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    
#     # If user created this food or just modified it
#     is_created = db.Column(db.Boolean, default=True)
    
#     # Relationships - using string references to avoid circular imports
#     food = db.relationship('FoodItem', back_populates='custom_food_entries')
#     user = db.relationship('User', back_populates='custom_foods')
    
#     def __repr__(self):
#         return f'<UserCustomFood {self.user_id} - {self.food_id}>'