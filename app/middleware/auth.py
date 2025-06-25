# app/middleware/auth.py
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required():
    """
    Decorator to require an admin role for a route
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            # Check if the role claim exists and is 'admin'
            if claims.get("role") != "admin":
                return jsonify({'message': 'Admin privilege required'}), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper