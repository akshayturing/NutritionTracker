# from flask import Blueprint, request, jsonify
# from datetime import datetime
# from app.auth.jwt_callbacks import jwt_required
# from app.utils.nutrient_calculator import calculate_daily_nutrients, calculate_nutrient_trends

# nutrition_bp = Blueprint('nutrition', __name__)

# @nutrition_bp.route('/daily-summary', methods=['GET'])
# @jwt_required
# def get_daily_summary(current_user):
#     """Get nutrient summary for a specific day"""
#     # Get date from query parameter, default to today
#     date_str = request.args.get('date')
#     if date_str:
#         try:
#             date = datetime.strptime(date_str, '%Y-%m-%d')
#         except ValueError:
#             return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD'}), 400
#     else:
#         date = None
    
#     # Calculate nutrient totals for the specified date
#     result = calculate_daily_nutrients(current_user.id, date)
    
#     return jsonify(result), 200


# @nutrition_bp.route('/nutrient-trends', methods=['GET'])
# @jwt_required
# def get_nutrient_trends(current_user):
#     """Get nutrient trends over a period"""
#     # Get number of days from query parameter, default to 7
#     try:
#         days = int(request.args.get('days', 7))
#         if days < 1 or days > 90:  # Set a reasonable limit
#             return jsonify({'error': 'Days parameter must be between 1 and 90'}), 400
#     except ValueError:
#         return jsonify({'error': 'Days parameter must be a valid integer'}), 400
    
#     # Calculate trends for the specified period
#     result = calculate_nutrient_trends(current_user.id, days)
    
#     return jsonify(result), 200

# app/routes/nutrition.py

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app.auth.jwt_callbacks import jwt_required
from app.utils.nutrition_summary import calculate_nutrition_summary, suggest_remaining_meals

nutrition_bp = Blueprint('nutrition', __name__)

# ... existing routes ...

@nutrition_bp.route('/summary', methods=['GET'])
@jwt_required
def get_nutrition_summary(current_user):
    """
    Get comprehensive real-time nutrition summary for the current user.
    
    Query parameters:
    - period: 'day' (default), 'week', 'month', or 'custom'
    - start_date: Required for custom period (YYYY-MM-DD format)
    - end_date: Optional for custom period, defaults to now (YYYY-MM-DD format)
    - include_suggestions: Boolean to include meal suggestions (default: False)
    """
    period = request.args.get('period', 'day').lower()
    include_suggestions = request.args.get('include_suggestions', 'false').lower() == 'true'
    
    # Calculate date range based on period
    end_date = datetime.utcnow()
    
    if period == 'day':
        start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'week':
        # Start from the beginning of current week (Monday)
        days_since_monday = end_date.weekday()
        start_date = (end_date - timedelta(days=days_since_monday)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    elif period == 'month':
        # Start from the first day of current month
        start_date = end_date.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
    elif period == 'custom':
        # Parse custom date range
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        if not start_date_str:
            return jsonify({
                'error': 'Missing start_date parameter for custom period'
            }), 400
            
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            return jsonify({
                'error': 'Invalid date format. Use YYYY-MM-DD format.'
            }), 400
    else:
        return jsonify({
            'error': f"Invalid period '{period}'. Use 'day', 'week', 'month', or 'custom'."
        }), 400
    
    try:
        # Get nutrition summary
        summary = calculate_nutrition_summary(
            user_id=current_user.id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Add meal suggestions if requested
        if include_suggestions:
            summary['meal_suggestions'] = suggest_remaining_meals(
                user_id=current_user.id,
                summary=summary
            )
            
        # Add period name to response
        summary['period_name'] = period
        
        return jsonify(summary), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500