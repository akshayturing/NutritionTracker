# app/auth/auth_bp.py
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from app.models import db, User
from app.auth import auth_bp
from app.auth.jwt_callbacks import generate_token, blacklist_token

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    required = ['email', 'password', 'name']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create new user
    password_hash = generate_password_hash(data['password'])
    
    user = User(
        email=data['email'],
        password_hash=password_hash,
        name=data['name'],
        age=data.get('age'),
        weight=data.get('weight'),
        activity_level=data.get('activity_level', 'moderate')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get access token"""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Check user credentials
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout by blacklisting the current token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token'}), 400
    
    token = auth_header.split(' ')[1]
    
    # Add token to blacklist
    if blacklist_token(token):
        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'error': 'Logout failed'}), 500
