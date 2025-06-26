from app.extensions import db
from datetime import datetime

class TokenBlacklist(db.Model):
    """Model for storing blacklisted JWT tokens"""
    __tablename__ = 'token_blacklist'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)
    token_type = db.Column(db.String(10), nullable=False)  # 'access' or 'refresh'
    user_id = db.Column(db.Integer, nullable=True)  # Optional reference to user
    blacklisted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<TokenBlacklist {self.jti}>'
    
    @classmethod
    def is_blacklisted(cls, jti):
        """Check if a token is blacklisted"""
        return cls.query.filter_by(jti=jti).first() is not None
    
    @classmethod
    def add_to_blacklist(cls, jti, token_type, user_id, expires):
        """Add a token to the blacklist"""
        blacklisted_token = cls(
            jti=jti,
            token_type=token_type,
            user_id=user_id,
            expires=expires,
            blacklisted_on=datetime.utcnow()
        )
        db.session.add(blacklisted_token)
        db.session.commit()
        return blacklisted_token
    
    @classmethod
    def prune_blacklist(cls):
        """Remove expired tokens from the blacklist"""
        now = datetime.utcnow()
        expired = cls.query.filter(cls.expires < now).delete()
        db.session.commit()
        return expired
