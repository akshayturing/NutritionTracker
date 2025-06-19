from flask import Blueprint, request, jsonify
from datetime import datetime
from app.auth.jwt_callbacks import jwt_required
from app.utils.nutrient_calculator import calculate_daily_nutrients, calculate_nutrient_trends

nutrition_bp = Blueprint('nutrition', __name__)

@nutrition_bp.route('/daily-summary', methods=['GET'])
@jwt_required
def get_daily_summary(current_user):
    """Get nutrient summary for a specific day"""
    # Get date from query parameter, default to today
    date_str = request.args.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD'}), 400
    else:
        date = None
    
    # Calculate nutrient totals for the specified date
    result = calculate_daily_nutrients(current_user.id, date)
    
    return jsonify(result), 200


@nutrition_bp.route('/nutrient-trends', methods=['GET'])
@jwt_required
def get_nutrient_trends(current_user):
    """Get nutrient trends over a period"""
    # Get number of days from query parameter, default to 7
    try:
        days = int(request.args.get('days', 7))
        if days < 1 or days > 90:  # Set a reasonable limit
            return jsonify({'error': 'Days parameter must be between 1 and 90'}), 400
    except ValueError:
        return jsonify({'error': 'Days parameter must be a valid integer'}), 400
    
    # Calculate trends for the specified period
    result = calculate_nutrient_trends(current_user.id, days)
    
    return jsonify(result), 200
