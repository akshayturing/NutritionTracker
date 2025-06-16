from flask import Blueprint, request, jsonify
from app.models.food_item import FoodItem
from app import db

food_item_bp = Blueprint('food_items', __name__)

@food_item_bp.route('/', methods=['GET'])
def get_food_items():
    # Handle search and filtering
    name_filter = request.args.get('name')
    
    query = FoodItem.query
    
    if name_filter:
        query = query.filter(FoodItem.name.ilike(f'%{name_filter}%'))
    
    items = query.all()
    return jsonify([item.to_dict() for item in items])

@food_item_bp.route('/<int:id>', methods=['GET'])
def get_food_item(id):
    item = FoodItem.query.get_or_404(id)
    return jsonify(item.to_dict())

@food_item_bp.route('/', methods=['POST'])
def create_food_item():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'serving_size', 'serving_unit', 'calories', 'protein', 'carbs', 'fats']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create the food item
    food_item = FoodItem(
        name=data['name'],
        brand=data.get('brand'),
        serving_size=data['serving_size'],
        serving_unit=data['serving_unit'],
        calories=data['calories'],
        protein=data['protein'],
        carbs=data['carbs'],
        fats=data['fats'],
        fiber=data.get('fiber'),
        sugar=data.get('sugar'),
        saturated_fats=data.get('saturated_fats'),
        unsaturated_fats=data.get('unsaturated_fats'),
        trans_fats=data.get('trans_fats'),
        micronutrients=data.get('micronutrients', {}),
        is_verified=data.get('is_verified', False),
        created_by=data.get('created_by')
    )
    
    db.session.add(food_item)
    db.session.commit()
    
    return jsonify(food_item.to_dict()), 201
