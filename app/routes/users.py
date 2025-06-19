# app/routes/users.py
from flask import Blueprint, request, jsonify
from app.models.user import User, db
from app.auth.jwt_callbacks import jwt_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile(current_user):
    return jsonify(current_user.to_dict()), 200

@users_bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile(current_user):
    data = request.get_json()
    
    # Update basic profile fields
    if 'name' in data:
        current_user.name = data['name']
    if 'age' in data:
        current_user.age = data['age']
    if 'weight' in data:
        current_user.weight = data['weight']
    if 'height' in data:
        current_user.height = data['height']
    if 'gender' in data:
        current_user.gender = data['gender']
    if 'activity_level' in data:
        current_user.activity_level = data['activity_level']
        
    # Update nutritional targets
    if 'calorie_goal' in data:
        current_user.calorie_goal = data['calorie_goal']
    if 'protein_goal' in data:
        current_user.protein_goal = data['protein_goal']
    if 'carbs_goal' in data:
        current_user.carbs_goal = data['carbs_goal']
    if 'fat_goal' in data:
        current_user.fat_goal = data['fat_goal']
    
    db.session.commit()
    return jsonify(current_user.to_dict()), 200
