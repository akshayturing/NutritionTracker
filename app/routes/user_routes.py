from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create a new user
    user = User(
        name=data.get('name'),
        email=data.get('email'),
        age=data.get('age'),
        weight=data.get('weight'),
        activity_level=data.get('activity_level')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201
