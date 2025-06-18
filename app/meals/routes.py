# app/meals/routes.py
from flask import request, jsonify, g
from sqlalchemy import desc
from datetime import datetime, timedelta

from app.models import db, Meal
from app.auth.jwt_callbacks import jwt_required
from app.meals import meals_bp
from app.meals.utils import validate_meal_data

@meals_bp.route('/', methods=['POST'])
@jwt_required
def log_meal():
    """
    Log a new meal for the authenticated user
    """
    data = request.get_json()
    
    # Validate meal data
    validation_result = validate_meal_data(data)
    if validation_result:
        return jsonify({'error': validation_result}), 400
    
    # Get the current user ID from the JWT token
    user_id = g.current_user.id
    
    # Extract macronutrients if provided
    macronutrients = data.get('macronutrients', {'protein': 0, 'carbs': 0, 'fat': 0})
    
    # Create timestamp from provided date or use current time
    timestamp = datetime.utcnow()
    if 'timestamp' in data:
        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            return jsonify({'error': 'Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    # Create a new meal record
    meal = Meal(
        user_id=user_id,
        meal_name=data['meal_name'],
        portion_size=data['portion_size'],
        calories=data['calories'],
        macronutrients=macronutrients,
        timestamp=timestamp
    )
    
    # Add to database
    db.session.add(meal)
    db.session.commit()
    
    # Return the created meal
    return jsonify({
        'id': meal.id,
        'meal_name': meal.meal_name,
        'portion_size': meal.portion_size,
        'calories': meal.calories,
        'macronutrients': meal.macronutrients,
        'timestamp': meal.timestamp.isoformat()
    }), 201

@meals_bp.route('/', methods=['GET'])
@jwt_required
def get_meals():
    """
    Get meals for the authenticated user with optional date filtering
    """
    user_id = g.current_user.id
    
    # Optional query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', default=20, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    # Build the query
    query = Meal.query.filter_by(user_id=user_id)
    
    # Apply date filters if provided
    if start_date:
        try:
            start_datetime = datetime.fromisoformat(start_date)
            query = query.filter(Meal.timestamp >= start_datetime)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use ISO format (YYYY-MM-DD)'}), 400
    
    if end_date:
        try:
            end_datetime = datetime.fromisoformat(end_date)
            # Include the entire day
            end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
            query = query.filter(Meal.timestamp <= end_datetime)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use ISO format (YYYY-MM-DD)'}), 400
    
    # Order by most recent first
    query = query.order_by(desc(Meal.timestamp))
    
    # Apply pagination
    total_count = query.count()
    meals = query.limit(limit).offset(offset).all()
    
    # Format the response
    result = []
    for meal in meals:
        result.append({
            'id': meal.id,
            'meal_name': meal.meal_name,
            'portion_size': meal.portion_size,
            'calories': meal.calories,
            'macronutrients': meal.macronutrients,
            'timestamp': meal.timestamp.isoformat()
        })
    
    return jsonify({
        'meals': result,
        'total': total_count,
        'limit': limit,
        'offset': offset
    })

@meals_bp.route('/<int:meal_id>', methods=['GET'])
@jwt_required
def get_meal(meal_id):
    """
    Get a specific meal by ID
    """
    user_id = g.current_user.id
    
    # Get meal and ensure it belongs to the current user
    meal = Meal.query.filter_by(id=meal_id, user_id=user_id).first()
    
    if not meal:
        return jsonify({'error': 'Meal not found or access denied'}), 404
    
    return jsonify({
        'id': meal.id,
        'meal_name': meal.meal_name,
        'portion_size': meal.portion_size,
        'calories': meal.calories,
        'macronutrients': meal.macronutrients,
        'timestamp': meal.timestamp.isoformat()
    })

@meals_bp.route('/summary', methods=['GET'])
@jwt_required
def get_meal_summary():
    """
    Get a summary of meals grouped by day, including total calories and macronutrients
    """
    user_id = g.current_user.id
    days = request.args.get('days', default=7, type=int)
    
    # Calculate date range
    end_date = datetime.utcnow().replace(hour=23, minute=59, second=59)
    start_date = (end_date - timedelta(days=days)).replace(hour=0, minute=0, second=0)
    
    # Get meals within the date range
    meals = Meal.query.filter_by(user_id=user_id) \
                      .filter(Meal.timestamp >= start_date) \
                      .filter(Meal.timestamp <= end_date) \
                      .all()
    
    # Group meals by day and calculate totals
    summary = {}
    for meal in meals:
        day = meal.timestamp.date().isoformat()
        
        if day not in summary:
            summary[day] = {
                'date': day,
                'total_calories': 0,
                'total_protein': 0,
                'total_carbs': 0,
                'total_fat': 0,
                'meal_count': 0
            }
        
        summary[day]['total_calories'] += meal.calories
        summary[day]['total_protein'] += meal.macronutrients.get('protein', 0)
        summary[day]['total_carbs'] += meal.macronutrients.get('carbs', 0)
        summary[day]['total_fat'] += meal.macronutrients.get('fat', 0)
        summary[day]['meal_count'] += 1
    
    # Convert to list and sort by date
    summary_list = list(summary.values())
    summary_list.sort(key=lambda x: x['date'])
    
    return jsonify({
        'summary': summary_list,
        'days': days
    })