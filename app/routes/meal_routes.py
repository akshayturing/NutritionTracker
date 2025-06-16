from flask import Blueprint, request, jsonify
from app.models.meal import Meal
from app.models.user import User
from app import db
from datetime import datetime

meal_bp = Blueprint('meals', __name__)

@meal_bp.route('/', methods=['GET'])
def get_meals():
    user_id = request.args.get('user_id', type=int)
    if user_id:
        meals = Meal.query.filter_by(user_id=user_id).all()
    else:
        meals = Meal.query.all()
    return jsonify([meal.to_dict() for meal in meals])

@meal_bp.route('/<int:id>', methods=['GET'])
def get_meal(id):
    meal = Meal.query.get_or_404(id)
    return jsonify(meal.to_dict())

@meal_bp.route('/', methods=['POST'])
def create_meal():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('user_id') or not data.get('meal_name') or not data.get('food_items'):
        return jsonify({'error': 'User ID, meal name, and food items are required'}), 400
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create a new meal
    meal = Meal(
        user_id=data['user_id'],
        meal_name=data['meal_name'],
        food_items=json.dumps(data['food_items']),
        timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else datetime.utcnow()
    )
    
    db.session.add(meal)
    db.session.commit()
    
    return jsonify(meal.to_dict()), 201
