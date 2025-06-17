# app/api/routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.meal import Meal

api_bp = Blueprint('api', __name__)

@api_bp.route('/meals', methods=['GET'])
@jwt_required()
def get_meals():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    meals = Meal.query.filter_by(user_id=user_id).all()
    
    result = []
    for meal in meals:
        meal_data = {
            'id': meal.id,
            'name': meal.name,
            'calories': meal.calories,
            'date': meal.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        result.append(meal_data)
    
    return jsonify({
        'meals': result
    }), 200