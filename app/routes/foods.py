from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.food import Food, UserCustomFood
from app.models.user import User
from app import db
from datetime import datetime
from sqlalchemy import desc

foods_bp = Blueprint('foods', __name__)

@foods_bp.route('/api/foods/custom', methods=['POST'])
@jwt_required()
def create_custom_food():
    """Create a new custom food item for the current user"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'calories', 'protein', 'carbohydrates', 'fat']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                     'message': f'Missing required field: {field}'}}), 400
    
    try:
        # Create the base food item
        new_food = Food(
            name=data['name'],
            category=data.get('category'),
            reference_portion_size=data.get('reference_portion_size', 1.0),
            reference_portion_unit=data.get('reference_portion_unit', 'serving'),
            is_custom=True,
            calories=data['calories'],
            protein=data['protein'],
            carbohydrates=data['carbohydrates'],
            fat=data['fat'],
            fiber=data.get('fiber', 0),
            sugar=data.get('sugar'),
            sodium=data.get('sodium'),
            cholesterol=data.get('cholesterol')
        )
        
        db.session.add(new_food)
        db.session.flush()  # Get ID without committing
        
        # Create the association to the user
        user_custom_food = UserCustomFood(
            user_id=user_id,
            food_id=new_food.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(user_custom_food)
        db.session.commit()
        
        return jsonify({
            'message': 'Custom food item created successfully',
            'food_id': new_food.id,
            'name': new_food.name
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating custom food: {str(e)}")
        return jsonify({'error': {'code': 'INTERNAL_ERROR', 
                                 'message': 'An error occurred while creating the food item'}}), 500

@foods_bp.route('/api/foods/custom/<int:food_id>', methods=['PUT'])
@jwt_required()
def update_custom_food(food_id):
    """Update an existing custom food item"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check if the food exists and belongs to the user
    custom_food = UserCustomFood.query.filter_by(food_id=food_id, user_id=user_id).first()
    
    if not custom_food:
        return jsonify({'error': {'code': 'PERMISSION_DENIED', 
                                 'message': 'Food item not found or you do not have permission to update it'}}), 403
    
    food = Food.query.get(food_id)
    if not food:
        return jsonify({'error': {'code': 'RESOURCE_NOT_FOUND', 
                                 'message': 'Food item not found'}}), 404
    
    # Update the food details
    if 'name' in data:
        food.name = data['name']
    if 'category' in data:
        food.category = data['category']
    if 'reference_portion_size' in data:
        food.reference_portion_size = data['reference_portion_size']
    if 'reference_portion_unit' in data:
        food.reference_portion_unit = data['reference_portion_unit']
    if 'calories' in data:
        food.calories = data['calories']
    if 'protein' in data:
        food.protein = data['protein']
    if 'carbohydrates' in data:
        food.carbohydrates = data['carbohydrates']
    if 'fat' in data:
        food.fat = data['fat']
    if 'fiber' in data:
        food.fiber = data['fiber']
    if 'sugar' in data:
        food.sugar = data['sugar']
    if 'sodium' in data:
        food.sodium = data['sodium']
    if 'cholesterol' in data:
        food.cholesterol = data['cholesterol']
    
    try:
        db.session.commit()
        
        return jsonify({
            'message': 'Custom food item updated successfully',
            'food_id': food.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating custom food: {str(e)}")
        return jsonify({'error': {'code': 'INTERNAL_ERROR', 
                                 'message': 'An error occurred while updating the food item'}}), 500

@foods_bp.route('/api/foods/custom/<int:food_id>', methods=['DELETE'])
@jwt_required()
def delete_custom_food(food_id):
    """Delete a custom food item"""
    user_id = get_jwt_identity()
    
    # Check if the food exists and belongs to the user
    custom_food = UserCustomFood.query.filter_by(food_id=food_id, user_id=user_id).first()
    
    if not custom_food:
        return jsonify({'error': {'code': 'PERMISSION_DENIED', 
                                 'message': 'Food item not found or you do not have permission to delete it'}}), 403
    
    food = Food.query.get(food_id)
    if not food:
        return jsonify({'error': {'code': 'RESOURCE_NOT_FOUND', 
                                 'message': 'Food item not found'}}), 404
    
    try:
        # Delete the custom food association first
        db.session.delete(custom_food)
        
        # Delete the food item itself
        db.session.delete(food)
        db.session.commit()
        
        return jsonify({
            'message': 'Custom food item deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting custom food: {str(e)}")
        return jsonify({'error': {'code': 'INTERNAL_ERROR', 
                                 'message': 'An error occurred while deleting the food item'}}), 500

@foods_bp.route('/api/foods/custom', methods=['GET'])
@jwt_required()
def get_user_custom_foods():
    """Get all custom food items for the current user"""
    user_id = get_jwt_identity()
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    
    # Search parameter
    search = request.args.get('search', '')
    
    # Query custom foods for the user
    custom_food_ids = db.session.query(UserCustomFood.food_id) \
                                .filter(UserCustomFood.user_id == user_id)
    
    query = Food.query.filter(Food.id.in_(custom_food_ids))
    
    # Apply search filter if provided
    if search:
        query = query.filter(Food.name.ilike(f'%{search}%'))
    
    # Sort by newest first
    query = query.order_by(desc(Food.id))
    
    # Paginate results
    paginated_foods = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Format response
    result = {
        'foods': [food.to_dict(detailed=True) for food in paginated_foods.items],
        'pagination': {
            'total_items': paginated_foods.total,
            'total_pages': paginated_foods.pages,
            'current_page': page,
            'per_page': per_page,
            'next_page': paginated_foods.next_num if paginated_foods.has_next else None,
            'prev_page': paginated_foods.prev_num if paginated_foods.has_prev else None
        }
    }
    
    return jsonify(result), 200