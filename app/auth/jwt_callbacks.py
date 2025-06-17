"""JWT callback functions for token validation and handling."""
from flask import jsonify
from app.models.token import TokenBlacklist

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
        return TokenBlacklist.is_token_revoked(jti)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        """Handle expired token error.
        
        Args:
            jwt_header: JWT header data
            jwt_data: JWT payload data
            
        Returns:
            tuple: JSON response and status code
        """
        return jsonify({
            'status': 401,
            'message': 'The token has expired.',
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid token error.
        
        Args:
            error: Error message
            
        Returns:
            tuple: JSON response and status code
        """
        return jsonify({
            'status': 401,
            'message': 'Signature verification failed.',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing token error.
        
        Args:
            error: Error message
            
        Returns:
            tuple: JSON response and status code
        """
        return jsonify({
            'status': 401,
            'message': 'Request does not contain an access token.',
            'error': 'authorization_required'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_data):
        """Handle non-fresh token error when fresh token is required.
        
        Args:
            jwt_header: JWT header data
            jwt_data: JWT payload data
            
        Returns:
            tuple: JSON response and status code
        """
        return jsonify({
            'status': 401,
            'message': 'The token is not fresh.',
            'error': 'fresh_token_required'
        }), 401
        
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_data):
        """Handle revoked token error.
        
        Args:
            jwt_header: JWT header data
            jwt_data: JWT payload data
            
        Returns:
            tuple: JSON response and status code
        """
        return jsonify({
            'status': 401,
            'message': 'The token has been revoked.',
            'error': 'token_revoked'
        }), 401