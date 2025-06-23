# # app/routes/users.py
# from flask import Blueprint, request, jsonify
# from app.models.user import User, db
# from app.auth.jwt_callbacks import jwt_required

# users_bp = Blueprint('users', __name__)

# @users_bp.route('/profile', methods=['GET'])
# @jwt_required
# def get_profile(current_user):
#     return jsonify(current_user.to_dict()), 200

# @users_bp.route('/profile', methods=['PUT'])
# @jwt_required
# def update_profile(current_user):
#     data = request.get_json()
    
#     # Update basic profile fields
#     if 'name' in data:
#         current_user.name = data['name']
#     if 'age' in data:
#         current_user.age = data['age']
#     if 'weight' in data:
#         current_user.weight = data['weight']
#     if 'height' in data:
#         current_user.height = data['height']
#     if 'gender' in data:
#         current_user.gender = data['gender']
#     if 'activity_level' in data:
#         current_user.activity_level = data['activity_level']
        
#     # Update nutritional targets
#     if 'calorie_goal' in data:
#         current_user.calorie_goal = data['calorie_goal']
#     if 'protein_goal' in data:
#         current_user.protein_goal = data['protein_goal']
#     if 'carbs_goal' in data:
#         current_user.carbs_goal = data['carbs_goal']
#     if 'fat_goal' in data:
#         current_user.fat_goal = data['fat_goal']
    
#     db.session.commit()
#     return jsonify(current_user.to_dict()), 200

# app/routes/users.py
from flask import Blueprint, request, jsonify, current_app
from marshmallow import Schema, fields, validate, ValidationError
from app.models.user import User, db
from app.auth.jwt_callbacks import jwt_required
from sqlalchemy.exc import IntegrityError
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create blueprint
users_bp = Blueprint('users', __name__)

# Validation schemas
class UserProfileSchema(Schema):
    """Schema for validating user profile data"""
    name = fields.String(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    age = fields.Integer(validate=validate.Range(min=12, max=120), allow_none=True)
    weight = fields.Float(validate=validate.Range(min=20, max=500), allow_none=True)
    height = fields.Float(validate=validate.Range(min=50, max=300), allow_none=True)
    gender = fields.String(validate=validate.OneOf(['male', 'female', 'other']), allow_none=True)
    activity_level = fields.String(validate=validate.OneOf(['sedentary', 'light', 'moderate', 'active', 'very_active']), allow_none=True)
    
    # Nutritional goals
    calorie_goal = fields.Integer(validate=validate.Range(min=500, max=10000), allow_none=True)
    protein_goal = fields.Float(validate=validate.Range(min=0, max=500), allow_none=True)
    carbs_goal = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True)
    fat_goal = fields.Float(validate=validate.Range(min=0, max=500), allow_none=True)

# Initialize schemas
profile_schema = UserProfileSchema()

# -----------------------------------------------
# Protected routes (require authentication)
# -----------------------------------------------

@users_bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile(current_user):
    """Get the current user's profile"""
    try:
        return jsonify({
            'success': True, 
            'data': current_user.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving user profile: {str(e)}")
        return jsonify({
            'success': False, 
            'message': 'Error retrieving profile'
        }), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile(current_user):
    """Update the current user's profile"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False, 
                'message': 'No data provided'
            }), 400
            
        # Validate input data
        errors = profile_schema.validate(data)
        if errors:
            return jsonify({
                'success': False, 
                'message': 'Validation error', 
                'errors': errors
            }), 400
        
        # Update user fields efficiently
        for field in profile_schema.fields.keys():
            if field in data:
                setattr(current_user, field, data[field])
        
        # Save changes
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Profile updated successfully',
            'data': current_user.to_dict()
        }), 200
            
    except ValidationError as e:
        return jsonify({
            'success': False, 
            'message': 'Validation error', 
            'errors': str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user profile: {str(e)}")
        return jsonify({
            'success': False, 
            'message': 'Error updating profile'
        }), 500

@users_bp.route('/nutritional-goals', methods=['PUT'])
@jwt_required
def update_nutritional_goals(current_user):
    """Update just the nutritional goals for the current user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False, 
                'message': 'No data provided'
            }), 400
            
        # Extract only nutritional goal fields
        nutrition_data = {
            k: v for k, v in data.items() 
            if k in ['calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal']
        }
        
        # Validate nutritional goal data
        errors = profile_schema.validate(nutrition_data, partial=True)
        if errors:
            return jsonify({
                'success': False, 
                'message': 'Validation error', 
                'errors': errors
            }), 400
        
        # Update nutrition fields
        for field, value in nutrition_data.items():
            setattr(current_user, field, value)
        
        # Save changes
        db.session.commit()
        
        # Return just the nutritional goals
        nutrition_response = {
            field: getattr(current_user, field) 
            for field in ['calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal']
        }
        
        return jsonify({
            'success': True, 
            'message': 'Nutritional goals updated',
            'data': nutrition_response
        }), 200
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating nutritional goals: {str(e)}")
        return jsonify({
            'success': False, 
            'message': 'Error updating nutritional goals'
        }), 500

# -----------------------------------------------
# Admin routes (these would typically have admin permission checks)
# -----------------------------------------------

@users_bp.route('/admin/users', methods=['GET'])
@jwt_required
def get_users(current_user):
    """Get list of all users (admin only)"""
    # In a real app, check if current_user is an admin
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Limit max items per page
        
        users = User.query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': {
                'users': [user.to_dict() for user in users.items],
                'pagination': {
                    'total': users.total,
                    'pages': users.pages,
                    'page': users.page,
                    'per_page': per_page,
                    'next': users.next_num,
                    'prev': users.prev_num
                }
            }
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error retrieving users'
        }), 500

@users_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_user(current_user, user_id):
    """Get a specific user by ID (admin only)"""
    # In a real app, check if current_user is an admin
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404

# -----------------------------------------------
# Public routes (user registration)
# -----------------------------------------------

@users_bp.route('/register', methods=['POST'])
def create_user():
    """Register a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Ensure required fields are present
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Check for additional validations
        if len(data['password']) < 8:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 8 characters'
            }), 400
        
        # Validate other fields using schema
        user_data = {k: v for k, v in data.items() if k != 'password'}
        errors = profile_schema.validate(user_data, partial=True)
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation error',
                'errors': errors
            }), 400
        
        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email'],
        )
        
        # Set password (assuming User model has a set_password method)
        new_user.set_password(data['password'])
        
        # Add optional fields
        optional_fields = [
            'age', 'weight', 'height', 'gender', 'activity_level',
            'calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal'
        ]
        
        for field in optional_fields:
            if field in data:
                setattr(new_user, field, data[field])
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        # Return success with user data (excluding sensitive info)
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': new_user.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Email already exists'
        }), 409
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error creating user'
        }), 500

# Error handlers
@users_bp.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404

@users_bp.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500