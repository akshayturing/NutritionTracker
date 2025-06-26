# # from flask import Blueprint, request, jsonify
# # from flask_jwt_extended import (
# #     create_access_token, create_refresh_token, 
# #     jwt_required, get_jwt_identity, get_jwt
# # )
# # from datetime import datetime, timezone
# # from app import db
# # from app.models.user import User
# # from app.models.token import TokenBlacklist

# # auth_bp = Blueprint('auth', __name__)

# # @auth_bp.route('/register', methods=['POST'])
# # def register():
# #     data = request.get_json()
    
# #     # Validate input
# #     if not data or not data.get('email') or not data.get('password'):
# #         return jsonify({'message': 'Missing required fields'}), 400
    
# #     # Check if user already exists
# #     if User.query.filter_by(email=data['email']).first():
# #         return jsonify({'message': 'User already exists'}), 409
    
# #     # Create new user
# #     new_user = User(
# #         email=data['email'],
# #         password=data['password']  # password hashing done in model
# #     )
    
# #     # Save to database
# #     db.session.add(new_user)
# #     db.session.commit()
    
# #     return jsonify({'message': 'User created successfully'}), 201

# # @auth_bp.route('/login', methods=['POST'])
# # def login():
# #     data = request.get_json()
    
# #     # Validate input
# #     if not data or not data.get('email') or not data.get('password'):
# #         return jsonify({'message': 'Missing required fields'}), 400
    
# #     # Find user
# #     user = User.query.filter_by(email=data['email']).first()
    
# #     # Check if user exists and password is correct
# #     if not user or not user.verify_password(data['password']):
# #         return jsonify({'message': 'Invalid credentials'}), 401
    
# #     # Create tokens
# #     access_token = create_access_token(identity=user.id)
# #     refresh_token = create_refresh_token(identity=user.id)
    
# #     return jsonify({
# #         'access_token': access_token,
# #         'refresh_token': refresh_token,
# #         'user_id': user.id,
# #         'email': user.email
# #     }), 200

# # @auth_bp.route('/refresh', methods=['POST'])
# # @jwt_required(refresh=True)
# # def refresh():
# #     current_user = get_jwt_identity()
# #     access_token = create_access_token(identity=current_user)
    
# #     return jsonify({
# #         'access_token': access_token
# #     }), 200

# # @auth_bp.route('/logout', methods=['POST'])
# # @jwt_required()
# # def logout():
# #     jti = get_jwt()["jti"]
# #     now = datetime.now(timezone.utc)
    
# #     # Add token to blacklist
# #     token = TokenBlacklist(
# #         jti=jti,
# #         token_type="access",
# #         user_id=get_jwt_identity(),
# #         expires=datetime.fromtimestamp(get_jwt()["exp"], timezone.utc)
# #     )
# #     db.session.add(token)
# #     db.session.commit()
    
# #     return jsonify({'message': 'Successfully logged out'}), 200

# # app/meals/routes.py
# from flask import request, jsonify, Blueprint
# from sqlalchemy import desc
# from datetime import datetime, timedelta

# from app.models import db, Meal
# from app.auth.jwt_callbacks import jwt_required  # Updated import
# from app.meals import meals_bp
# from app.meals.utils import validate_meal_data

# """Authentication routes for Nutrition Tracking App."""
# from flask import request, jsonify,Blueprint
# from flask_jwt_extended import (
#     create_access_token, create_refresh_token, 
#     jwt_required, get_jwt_identity, get_jwt
# )
# from datetime import datetime, timezone
# from app import db
# from app.models.user import User
# from app.models.token import TokenBlacklist

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     """Register a new user."""
#     data = request.get_json()
    
#     # Validate input
#     if not data or not data.get('email') or not data.get('password'):
#         return jsonify({'message': 'Missing required fields'}), 400
    
#     # Check if user already exists
#     if User.query.filter_by(email=data['email']).first():
#         return jsonify({'message': 'User already exists'}), 409
    
#     # Create new user
#     new_user = User(
#         email=data['email'],
#         password=data['password']  # password hashing done in model
#     )
    
#     # Save to database
#     db.session.add(new_user)
#     db.session.commit()
    
#     return jsonify({'message': 'User created successfully'}), 201

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     """Login a user and return JWT tokens."""
#     data = request.get_json()
    
#     # Validate input
#     if not data or not data.get('email') or not data.get('password'):
#         return jsonify({'message': 'Missing required fields'}), 400
    
#     # Find user
#     user = User.query.filter_by(email=data['email']).first()
    
#     # Check if user exists and password is correct
#     if not user or not user.verify_password(data['password']):
#         return jsonify({'message': 'Invalid credentials'}), 401
    
#     # Create tokens
#     access_token = create_access_token(identity=user.id)
#     refresh_token = create_refresh_token(identity=user.id)
    
#     return jsonify({
#         'access_token': access_token,
#         'refresh_token': refresh_token,
#         'user_id': user.id,
#         'email': user.email
#     }), 200

# @auth_bp.route('/refresh', methods=['POST'])
# @jwt_required(refresh=True)
# def refresh():
#     """Refresh access token using refresh token."""
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)
    
#     return jsonify({
#         'access_token': access_token
#     }), 200

# @auth_bp.route('/logout', methods=['POST'])
# @jwt_required()
# def logout():
#     """Logout a user and blacklist the current token."""
#     jti = get_jwt()["jti"]
#     user_id = get_jwt_identity()
    
#     # Add token to blacklist
#     token = TokenBlacklist(
#         jti=jti,
#         token_type="access",
#         user_id=user_id,
#         expires=datetime.fromtimestamp(get_jwt()["exp"], timezone.utc)
#     )
#     db.session.add(token)
#     db.session.commit()
    
#     return jsonify({'message': 'Successfully logged out'}), 200