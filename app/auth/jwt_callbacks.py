# # """JWT callback functions for token validation and handling."""
# # from flask import jsonify
# # from app.models.token import TokenBlacklist

# # def register_jwt_callbacks(jwt):
# #     """Register all JWT callbacks with the Flask-JWT-Extended instance.
    
# #     Args:
# #         jwt: Flask-JWT-Extended JWTManager instance
# #     """
    
# #     @jwt.token_in_blocklist_loader
# #     def check_if_token_revoked(jwt_header, jwt_payload):
# #         """Check if the token has been revoked.
        
# #         Args:
# #             jwt_header: JWT header data
# #             jwt_payload: JWT payload data
            
# #         Returns:
# #             bool: True if token is revoked, False otherwise
# #         """
# #         jti = jwt_payload["jti"]
# #         return TokenBlacklist.is_token_revoked(jti)

# #     @jwt.expired_token_loader
# #     def expired_token_callback(jwt_header, jwt_data):
# #         """Handle expired token error.
        
# #         Args:
# #             jwt_header: JWT header data
# #             jwt_data: JWT payload data
            
# #         Returns:
# #             tuple: JSON response and status code
# #         """
# #         return jsonify({
# #             'status': 401,
# #             'message': 'The token has expired.',
# #             'error': 'token_expired'
# #         }), 401

# #     @jwt.invalid_token_loader
# #     def invalid_token_callback(error):
# #         """Handle invalid token error.
        
# #         Args:
# #             error: Error message
            
# #         Returns:
# #             tuple: JSON response and status code
# #         """
# #         return jsonify({
# #             'status': 401,
# #             'message': 'Signature verification failed.',
# #             'error': 'invalid_token'
# #         }), 401

# #     @jwt.unauthorized_loader
# #     def missing_token_callback(error):
# #         """Handle missing token error.
        
# #         Args:
# #             error: Error message
            
# #         Returns:
# #             tuple: JSON response and status code
# #         """
# #         return jsonify({
# #             'status': 401,
# #             'message': 'Request does not contain an access token.',
# #             'error': 'authorization_required'
# #         }), 401

# #     @jwt.needs_fresh_token_loader
# #     def token_not_fresh_callback(jwt_header, jwt_data):
# #         """Handle non-fresh token error when fresh token is required.
        
# #         Args:
# #             jwt_header: JWT header data
# #             jwt_data: JWT payload data
            
# #         Returns:
# #             tuple: JSON response and status code
# #         """
# #         return jsonify({
# #             'status': 401,
# #             'message': 'The token is not fresh.',
# #             'error': 'fresh_token_required'
# #         }), 401
        
# #     @jwt.revoked_token_loader
# #     def revoked_token_callback(jwt_header, jwt_data):

# # app/auth/jwt_callbacks.py
# from functools import wraps
# from flask import request, g, jsonify
# import jwt
# from datetime import datetime, timedelta
# from app import db
# from app.models import User
# import uuid
# # Configuration values (should match your app.config)
# JWT_SECRET_KEY = 'your-secret-key'  # In production, get this from app.config
# JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
# JWT_ALGORITHM = 'HS256'

# class TokenBlacklist(db.Model):
#     """Model for storing blacklisted JWT tokens"""
#     __tablename__ = 'token_blacklist'
    
#     id = db.Column(db.Integer, primary_key=True)
#     jti = db.Column(db.String(36), nullable=False, unique=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def __repr__(self):
#         return f'<BlacklistedToken {self.jti}>'

# def generate_token(user_id, expires_delta=None):
#     """
#     Generate a JWT token for the given user
    
#     Args:
#         user_id (int): The user ID to encode in the token
#         expires_delta (timedelta, optional): Custom expiration time
        
#     Returns:
#         str: JWT token
#     """
#     now = datetime.utcnow()
#     expires = now + (expires_delta or JWT_ACCESS_TOKEN_EXPIRES)
    
#     payload = {
#         'user_id': user_id,
#         'iat': now,
#         'exp': expires,
#         'jti': str(uuid.uuid4())  # Unique token ID for potential blacklisting
#     }
    
#     return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# def decode_token(token):
#     """
#     Decode and validate a JWT token
    
#     Args:
#         token (str): JWT token to decode
        
#     Returns:
#         dict: Decoded token payload
    
#     Raises:
#         jwt.ExpiredSignatureError: If token is expired
#         jwt.InvalidTokenError: If token is invalid
#     """
#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
#         # Check if token is blacklisted
#         jti = payload.get('jti')
#         if jti and TokenBlacklist.query.filter_by(jti=jti).first():
#             raise jwt.InvalidTokenError('Token has been blacklisted')
            
#         return payload
#     except jwt.ExpiredSignatureError:
#         raise jwt.ExpiredSignatureError('Token has expired')
#     except jwt.InvalidTokenError as e:
#         raise jwt.InvalidTokenError(f'Invalid token: {str(e)}')

# def jwt_required(f):
#     """
#     Decorator to protect routes with JWT authentication
    
#     Usage:
#         @app.route('/protected')
#         @jwt_required
#         def protected_route():
#             # Access current user with g.current_user
#             return jsonify(user_id=g.current_user.id)
#     """
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         auth_header = request.headers.get('Authorization')
        
#         # Check if Authorization header exists and has the right format
#         if auth_header and auth_header.startswith('Bearer '):
#             token = auth_header.split(' ')[1]
        
#         if not token:
#             return jsonify({'error': 'Missing authentication token'}), 401
        
#         try:
#             # Decode and validate token
#             payload = decode_token(token)
            
#             # Get the user from database
#             user_id = payload.get('user_id')
#             user = User.query.get(user_id)
            
#             if not user:
#                 return jsonify({'error': 'User not found'}), 401
            
#             # Store user in flask.g for access in the view function
#             g.current_user = user
            
#             # Call the actual view function
#             return f(*args, **kwargs)
            
#         except jwt.ExpiredSignatureError:
#             return jsonify({'error': 'Token has expired'}), 401
#         except jwt.InvalidTokenError as e:
#             return jsonify({'error': f'Invalid token: {str(e)}'}), 401
#         except Exception as e:
#             return jsonify({'error': f'Authentication error: {str(e)}'}), 500
    
#     return decorated

# def blacklist_token(token):
#     """Add a token to the blacklist"""
#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options={'verify_exp': False})
#         jti = payload.get('jti')
        
#         if jti:
#             blacklist_entry = TokenBlacklist(jti=jti)
#             db.session.add(blacklist_entry)
#             db.session.commit()
            
#         return True
#     except:
#         return False
# #         """Handle revoked token error.
        
# #         Args:
# #             jwt_header: JWT header data
# #             jwt_data: JWT payload data
            
# #         Returns:
# #             tuple: JSON response and status code
# #         """
# #         return jsonify({
# #             'status': 401,
# #             'message': 'The token has been revoked.',
# #             'error': 'token_revoked'
# #         }), 401

"""JWT callback functions for token validation and handling."""
from flask import jsonify
from datetime import datetime
import logging
from app.models.token import TokenBlacklist

logger = logging.getLogger(__name__)

def register_jwt_callbacks(jwt):
    """Register all JWT callbacks with the Flask-JWT-Extended instance.
    
    Args:
        jwt: Flask-JWT-Extended JWTManager instance
    """
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Check if the token has been revoked.
        
        Args:
            jwt_header: JWT header data
            jwt_payload: JWT payload data
            
        Returns:
            bool: True if token is revoked, False otherwise
        """
        jti = jwt_payload["jti"]
        return TokenBlacklist.is_blacklisted(jti)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        """Handle expired token error."""
        return jsonify({
            'success': False,
            'message': 'The token has expired',
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid token error."""
        return jsonify({
            'success': False,
            'message': 'Signature verification failed',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing token error."""
        return jsonify({
            'success': False,
            'message': 'Request does not contain an access token',
            'error': 'authorization_required'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_data):
        """Handle non-fresh token error when fresh token is required."""
        return jsonify({
            'success': False,
            'message': 'The token is not fresh',
            'error': 'fresh_token_required'
        }), 401
        
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_data):
        """Handle revoked token error."""
        return jsonify({
            'success': False,
            'message': 'The token has been revoked',
            'error': 'token_revoked'
        }), 401
    
    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        """Convert user object to a JWT identity."""
        return user_id
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Load user from database based on JWT identity."""
        from app.models.user import User
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()