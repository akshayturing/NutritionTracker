from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.meal import Meal, MealFood
from app.models.food import FoodItem,FoodCategory,food_category_association
from app import db
from datetime import datetime
import iso8601
from sqlalchemy import desc

# Create a blueprint for meal routes
# Note: We're naming it 'nutrition_meals' to match the import in app/__init__.py
nutrition_meals = Blueprint('nutrition_meals', __name__)

@nutrition_meals.route('/api/meals', methods=['GET'])
@jwt_required()
def get_meals():
    """
    Get all meals for the current user with timestamp filtering and pagination
    
    Query parameters:
    - page: Page number (default=1)
    - per_page: Number of items per page (default=10, max=50)
    - date: Filter by specific date (format: YYYY-MM-DD)
    - start_date: Start date for range filter (format: YYYY-MM-DD)
    - end_date: End date for range filter (format: YYYY-MM-DD)
    - meal_type: Filter by meal type (breakfast, lunch, dinner, snack)
    - sort: Sort order (default=desc, options: asc, desc)
    """
    user_id = get_jwt_identity()
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)  # Cap at 50 items
    
    # Filter parameters
    date = request.args.get('date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    meal_type = request.args.get('meal_type')
    sort_order = request.args.get('sort', 'desc')
    
    # Start query for user's meals
    query = Meal.query.filter_by(user_id=user_id)
    
    # Apply date filters
    if date:
        try:
            filter_date = datetime.strptime(date, '%Y-%m-%d')
            next_date = datetime(filter_date.year, filter_date.month, filter_date.day, 23, 59, 59)
            query = query.filter(Meal.timestamp >= filter_date.replace(hour=0, minute=0, second=0))
            query = query.filter(Meal.timestamp <= next_date)
        except ValueError:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                      'message': 'Invalid date format. Use YYYY-MM-DD'}}), 400
    
    # Apply date range filter
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Meal.timestamp >= start.replace(hour=0, minute=0, second=0))
        except ValueError:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                      'message': 'Invalid start_date format. Use YYYY-MM-DD'}}), 400
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Meal.timestamp <= end.replace(hour=23, minute=59, second=59))
        except ValueError:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                      'message': 'Invalid end_date format. Use YYYY-MM-DD'}}), 400
    
    # Apply meal type filter
    if meal_type:
        valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        if meal_type.lower() not in valid_meal_types:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                    'message': f'Invalid meal_type. Must be one of: {", ".join(valid_meal_types)}'}}), 400
        query = query.filter(Meal.meal_type == meal_type.lower())
    
    # Apply sorting
    if sort_order.lower() == 'asc':
        query = query.order_by(Meal.timestamp)
    else:
        query = query.order_by(desc(Meal.timestamp))
    
    # Execute paginated query
    paginated_meals = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Format response
    result = {
        'meals': [meal.to_dict() for meal in paginated_meals.items],
        'pagination': {
            'total_items': paginated_meals.total,
            'total_pages': paginated_meals.pages,
            'current_page': page,
            'per_page': per_page,
            'next_page': paginated_meals.next_num if paginated_meals.has_next else None,
            'prev_page': paginated_meals.prev_num if paginated_meals.has_prev else None
        }
    }
    
    return jsonify(result), 200

@nutrition_meals.route('/api/meals/<int:meal_id>', methods=['GET'])
@jwt_required()
def get_meal(meal_id):
    """Get a specific meal by ID"""
    user_id = get_jwt_identity()
    
    meal = Meal.query.filter_by(id=meal_id).first()
    
    if not meal:
        return jsonify({'error': {'code': 'RESOURCE_NOT_FOUND', 
                                 'message': 'Meal not found'}}), 404
    
    # Ensure user owns this meal
    if meal.user_id != user_id:
        return jsonify({'error': {'code': 'PERMISSION_DENIED', 
                                 'message': 'You do not have permission to view this meal'}}), 403
    
    return jsonify(meal.to_dict(include_foods=True)), 200

@nutrition_meals.route('/api/meals', methods=['POST'])
@jwt_required()
def create_meal():
    """Create a new meal with food items"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['meal_name', 'meal_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                     'message': f'Missing required field: {field}'}}), 400
    
    # Validate meal type
    valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    if data.get('meal_type').lower() not in valid_meal_types:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                 'message': f'Invalid meal_type. Must be one of: {", ".join(valid_meal_types)}'}}), 400
    
    # Process timestamp (default to now if not provided)
    timestamp = datetime.now()
    if 'timestamp' in data:
        try:
            timestamp = iso8601.parse_date(data['timestamp'])
        except (ValueError, iso8601.ParseError):
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                     'message': 'Invalid timestamp format. Use ISO 8601 format (e.g., 2025-06-21T12:30:00Z)'}}), 400
    
    # Create the meal
    meal = Meal(
        user_id=user_id,
        meal_name=data['meal_name'],
        meal_type=data['meal_type'].lower(),
        timestamp=timestamp,
        notes=data.get('notes', '')
    )
    
    # Process food items
    if 'foods' in data and isinstance(data['foods'], list):
        for food_item in data['foods']:
            # Validate food item format
            if not isinstance(food_item, dict) or 'food_id' not in food_item or 'portion_size' not in food_item:
                return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                         'message': 'Invalid food item format. Required fields: food_id, portion_size'}}), 400
            
            # Check if food exists
            food = Food.query.get(food_item['food_id'])
            if not food:
                return jsonify({'error': {'code': 'RESOURCE_NOT_FOUND', 
                                         'message': f'Food item with ID {food_item["food_id"]} not found'}}), 404
            
            # Create meal-food relationship
            meal_food = MealFood(
                food_id=food_item['food_id'],
                portion_size=float(food_item['portion_size']),
                portion_unit=food_item.get('portion_unit', 'serving')
            )
            meal.foods.append(meal_food)
    
    try:
        # Calculate meal nutrition totals
        meal.calculate_nutrition_totals()
        
        # Save to database
        db.session.add(meal)
        db.session.commit()
        
        return jsonify({
            'message': 'Meal created successfully',
            'meal_id': meal.id,
            'meal_name': meal.meal_name,
            'total_calories': meal.total_calories,
            'total_protein': meal.total_protein,
            'total_carbohydrates': meal.total_carbohydrates,
            'total_fat': meal.total_fat
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating meal: {str(e)}")
        return jsonify({'error': {'code': 'INTERNAL_ERROR', 
                                 'message': 'An error occurred while creating the meal'}}), 500

@nutrition_meals.route('/api/meals/<int:meal_id>', methods=['PUT'])
@jwt_required()
def update_meal(meal_id):
    """Update an existing meal"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Find the meal
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return jsonify({'error': {'code': 'RESOURCE_NOT_FOUND', 
                                 'message': 'Meal not found'}}), 404
    
    # Ensure user owns this meal
    if meal.user_id != user_id:
        return jsonify({'error': {'code': 'PERMISSION_DENIED', 
                                 'message': 'You do not have permission to update this meal'}}), 403
    
    # Update meal details
    if 'meal_name' in data:
        meal.meal_name = data['meal_name']
    
    if 'meal_type' in data:
        valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        if data['meal_type'].lower() not in valid_meal_types:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                     'message': f'Invalid meal_type. Must be one of: {", ".join(valid_meal_types)}'}}), 400
        meal.meal_type = data['meal_type'].lower()
    
    if 'timestamp' in data:
        try:
            meal.timestamp = iso8601.parse_date(data['timestamp'])
        except (ValueError, iso8601.ParseError):
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                     'message': 'Invalid timestamp format. Use ISO 8601 format (e.g., 2025-06-21T12:30:00Z)'}}), 400
    
    if 'notes' in data:
        meal.notes = data['notes']
    
    # Update food items if provided
    if 'foods' in data:
        if not isinstance(data['foods'], list):
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                     'message': 'Foods must be a list'}}), 400
        
        # Remove existing meal-food relationships
        MealFood.query.filter_by(meal_id=meal.id).delete()
        
        # Add new food items
        for food_item in data['foods']:
            # Validate food item format
            if not isinstance(food_item, dict) or 'food_id' not in food_item or 'portion_size' not in food_item:
                return jsonify({'error': {'code': 'VALIDATION_ERROR', 
                                         'message': 'Invalid food item format. Required fields: food_id, portion_size'}}), 400
            
            # Check if food exists
            food = Food.query.get(food_item['food_id'])
            if not food:
                return jsonify({'error': {'code': 'RESOURCE_NOT_FOUND', 
                                         'message': f'Food item with ID {food_item["food_id"]} not found'}}), 404
            
            # Create meal-food relationship
            meal_food = MealFood(
                meal_id=meal.id,
                food_id=food_item['food_id'],
                portion_size=float(food_item['portion_size']),
                portion_unit=food_item.get('portion_unit', 'serving')
            )
            db.session.add(meal_food)
    
    try:
        # Recalculate meal nutrition totals
        meal.calculate_nutrition_totals()
        
        # Save to database
        db.session.commit()
        
        return jsonify({
            'message': 'Meal updated successfully',
            'meal_id': meal.id,
            'total_calories': meal.total_calories,
            'total_protein': meal.total_protein,
            'total_carbohydrates': meal.total_carbohydrates,
            'total_fat': meal.total_fat
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating meal: {str(e)}")
        return jsonify({'error': {'code': 'INTERNAL_ERROR', 
                                 'message': 'An error occurred while updating the meal'}}), 500

@nutrition_meals.route('/api/meals/<int:meal_id>', methods=['DELETE'])
@jwt_required()
def delete_meal(meal_id):
    """Delete a meal"""
    user_id = get_jwt_identity()
    
    meal = Meal.query.get(meal_id)
    
    if not meal:
        return jsonify({'error': {'code': 'RESOURCE_NOT_FOUND', 
                                 'message': 'Meal not found'}}), 404
    
    # Ensure user owns this meal
    if meal.user_id != user_id:
        return jsonify({'error': {'code': 'PERMISSION_DENIED', 
                                 'message': 'You do not have permission to delete this meal'}}), 403
    
    try:
        # Delete associated meal-food relationships (can be automatic with cascade)
        MealFood.query.filter_by(meal_id=meal.id).delete()
        
        # Delete the meal itself
        db.session.delete(meal)
        db.session.commit()
        
        return jsonify({
            'message': 'Meal deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting meal: {str(e)}")
        return jsonify({'error': {'code': 'INTERNAL_ERROR', 
                                 'message': 'An error occurred while deleting the meal'}}), 500