"""
Authentication routes for Nutrition Tracking App.
Handles user registration, login, token refresh, and logout.
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt,
    verify_jwt_in_request
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from app.extensions import db
from app import jwt
from app.models.user import User
from app.models.token import TokenBlacklist

auth_bp = Blueprint('auth', __name__)

# Standardized response format
def auth_response(success=True, message=None, data=None, status_code=200):
    """Create standardized API response"""
    response = {
        'success': success
    }
    if message:
        response['message'] = message
    if data:
        response['data'] = data
        
    return jsonify(response), status_code

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user and return JWT tokens."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data:
                return auth_response(
                    success=False, 
                    message=f"Missing required field: {field}", 
                    status_code=400
                )
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return auth_response(
                success=False, 
                message="Email already registered", 
                status_code=409
            )
        
        # Create new user with hashed password
        password_hash = generate_password_hash(data['password'])
        
        user = User(
            email=data['email'],
            password_hash=password_hash,
            name=data['name'],
            age=data.get('age'),
            weight=data.get('weight'),
            height=data.get('height'),
            gender=data.get('gender'),
            activity_level=data.get('activity_level', 'moderate')
        )
        
        # Add nutritional goals if provided
        if 'calorie_goal' in data:
            user.calorie_goal = data['calorie_goal']
        if 'protein_goal' in data:
            user.protein_goal = data['protein_goal']
        if 'carbs_goal' in data:
            user.carbs_goal = data['carbs_goal']
        if 'fat_goal' in data:
            user.fat_goal = data['fat_goal']
        
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return auth_response(
            message="User registered successfully",
            data={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            },
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        return auth_response(
            success=False, 
            message=f"Registration failed: {str(e)}", 
            status_code=500
        )

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user and return JWT tokens."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'email' not in data or 'password' not in data:
            return auth_response(
                success=False, 
                message="Email and password are required", 
                status_code=400
            )
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password_hash, data['password']):
            return auth_response(
                success=False, 
                message="Invalid credentials", 
                status_code=401
            )
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return auth_response(
            message="Login successful",
            data={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }
        )
    
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return auth_response(
            success=False, 
            message=f"Login failed: {str(e)}", 
            status_code=500
        )

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token."""
    try:
        # Get user identity from refresh token
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return auth_response(
                success=False, 
                message="User not found", 
                status_code=401
            )
        
        # Create new access token
        access_token = create_access_token(identity=current_user_id)
        
        return auth_response(
            message="Token refreshed successfully",
            data={
                'access_token': access_token,
                'user': user.to_dict()
            }
        )
        
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return auth_response(
            success=False, 
            message=f"Token refresh failed: {str(e)}", 
            status_code=500
        )

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout by blacklisting the current token."""
    try:
        # Get JWT token data
        token = get_jwt()
        jti = token["jti"]
        
        # Add token to blacklist
        now = datetime.now()
        token_blacklist = TokenBlacklist(
            jti=jti,
            created_at=now
        )
        db.session.add(token_blacklist)
        db.session.commit()
        
        return auth_response(message="Logout successful")
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Logout error: {str(e)}")
        return auth_response(
            success=False, 
            message=f"Logout failed: {str(e)}", 
            status_code=500
        )

@auth_bp.route('/verify-token', methods=['GET'])
def verify_token():
    """Verify if a token is valid without requiring a full endpoint."""
    try:
        # Extract token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return auth_response(
                success=False, 
                message="Missing or invalid Authorization header", 
                status_code=401
            )
        
        # Verify token
        verify_jwt_in_request()
        
        # If no exceptions were raised, token is valid
        return auth_response(message="Token is valid")
    
    except Exception as e:
        return auth_response(
            success=False, 
            message=f"Invalid token: {str(e)}", 
            status_code=401
        )