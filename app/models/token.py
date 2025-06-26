# # # from app import db
# # # from datetime import datetime

# # # class TokenBlacklist(db.Model):
# # #     __tablename__ = 'token_blacklist'
    
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     jti = db.Column(db.String(36), nullable=False, unique=True)
# # #     token_type = db.Column(db.String(10), nullable=False)
# # #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# # #     revoked = db.Column(db.Boolean, nullable=False, default=True)
# # #     expires = db.Column(db.DateTime, nullable=False)
# # #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
# # #     def to_dict(self):
# # #         return {
# # #             'token_id': self.id,
# # #             'jti': self.jti,
# # #             'token_type': self.token_type,
# # #             'user_id': self.user_id,
# # #             'revoked': self.revoked,
# # #             'expires': self.expires,
# # #             'created_at': self.created_at
# # #         }
        
# # #     @classmethod
# # #     def is_token_revoked(cls, jti):
# # #         token = cls.query.filter_by(jti=jti).first()
# # #         return token is not None and token.revoked

# # """Token blacklist model for JWT token revocation."""
# # from app import db
# # from datetime import datetime

# # class TokenBlacklist(db.Model):
# #     """Model for storing revoked JWT tokens."""
# #     __tablename__ = 'token_blacklist'
    
# #     id = db.Column(db.Integer, primary_key=True)
# #     jti = db.Column(db.String(36), nullable=False, unique=True)
# #     token_type = db.Column(db.String(10), nullable=False)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     revoked = db.Column(db.Boolean, nullable=False, default=True)
# #     expires = db.Column(db.DateTime, nullable=False)
# #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
# #     def to_dict(self):
# #         """Convert the model instance to a dictionary.
        
# #         Returns:
# #             dict: Dictionary representation of the token
# #         """
# #         return {
# #             'token_id': self.id,
# #             'jti': self.jti,
# #             'token_type': self.token_type,
# #             'user_id': self.user_id,
# #             'revoked': self.revoked,
# #             'expires': self.expires,
# #             'created_at': self.created_at
# #         }
        
# #     @classmethod
# #     def is_token_revoked(cls, jti):
# #         """Check if a token with the given JTI is revoked.
        
# #         Args:
# #             jti: JWT ID to check
            
# #         Returns:
# #             bool: True if token is revoked, False otherwise
# #         """
# #         token = cls.query.filter_by(jti=jti).first()
# #         return token is not None and token.revoked

# """Token blacklist model for JWT token revocation."""
# from app.extensions import db
# from datetime import datetime

# class TokenBlacklist(db.Model):
#     """Model for storing revoked JWT tokens."""
#     __tablename__ = 'token_blacklist'
    
#     # Add extend_existing to allow table redefinition
#     __table_args__ = {'extend_existing': True}
    
#     id = db.Column(db.Integer, primary_key=True)
#     jti = db.Column(db.String(36), nullable=False, unique=True)
#     token_type = db.Column(db.String(10), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     revoked = db.Column(db.Boolean, nullable=False, default=True)
#     expires = db.Column(db.DateTime, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     @classmethod
#     def is_token_revoked(cls, jti):
#         """Check if a token with the given JTI is revoked."""
#         token = cls.query.filter_by(jti=jti).first()
#         return token is not None and token.revoked

"""Token blacklist model for JWT token management."""
from datetime import datetime
from app.extensions import db

class TokenBlacklist(db.Model):
    """Stores blacklisted JWT tokens for logout functionality."""
    __tablename__ = 'token_blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<TokenBlacklist {self.jti}>'
    
    @classmethod
    def is_blacklisted(cls, jti):
        """Check if a token JTI is blacklisted."""
        return cls.query.filter_by(jti=jti).first() is not None