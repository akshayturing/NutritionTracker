# """API routes for Nutrition Tracking App."""
# from flask import jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
# from app.api import api_bp
# from app.models.user import User
# from app.models.meal import Meal  # Import if exists, otherwise create a placeholder

# # Add middleware for admin-only routes
# from functools import wraps

# def admin_required():
#     """Decorator to require administrative role for a route."""
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             jwt_data = get_jwt()
#             if jwt_data.get("role") != "admin":
#                 return jsonify(message="Admin privilege required"), 403
#             return fn(*args, **kwargs)
#         return decorator
#     return wrapper

# @api_bp.route('/meals', methods=['GET'])
# @jwt_required()
# def get_meals():
#     """Get meals for the current user."""
#     user_id = get_jwt_identity()
    
#     # Mock response for testing - in real app, query the database
#     return jsonify({
#         'meals': [
#             {'id': 1, 'name': 'Breakfast', 'calories': 500, 'date': '2023-06-15 08:30:00'},
#             {'id': 2, 'name': 'Lunch', 'calories': 700, 'date': '2023-06-15 12:30:00'},
#         ]
#     }), 200

# @api_bp.route('/admin/users', methods=['GET'])
# @jwt_required()
# @admin_required()
# def admin_get_users():
#     """Admin-only route to get all users."""
#     # In a real app, you'd query the database
#     return jsonify({
#         'users': [
#             {'id': 1, 'email': 'admin@example.com'},
#             {'id': 2, 'email': 'test@example.com'}
#         ]
#     }), 200

"""API routes for Nutrition Tracking App."""
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.api import api_bp
from app.models.meal import Meal
from app.models.user import User
from functools import wraps

# Admin role check decorator
def admin_required():
    """Decorator to require admin role for a route."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Get JWT claims
            claims = get_jwt()
            # Check if the role claim is admin
            if claims.get("role") != "admin":
                return jsonify(message="Admin privilege required"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@api_bp.route('/meals', methods=['GET'])
@jwt_required()
def get_meals():
    """Get meals for the current user."""
    user_id = get_jwt_identity()
    
    # You can uncomment and use the following to query the database
    # if you have the Meal model set up properly:
    # 
    # user = User.query.get(user_id)
    # 
    # if not user:
    #     return jsonify({'message': 'User not found'}), 404
    #
    # meals = Meal.query.filter_by(user_id=user_id).all()
    # 
    # result = []
    # for meal in meals:
    #     meal_data = {
    #         'id': meal.id,
    #         'name': meal.name,
    #         'calories': meal.calories,
    #         'date': meal.date.strftime('%Y-%m-%d %H:%M:%S')
    #     }
    #     result.append(meal_data)
    
    # For testing, return mock data
    result = [
        {'id': 1, 'name': 'Breakfast', 'calories': 500, 'date': '2023-06-15 08:30:00'},
        {'id': 2, 'name': 'Lunch', 'calories': 700, 'date': '2023-06-15 12:30:00'}
    ]
    
    return jsonify({
        'meals': result
    }), 200

@api_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@admin_required()
def admin_get_users():
    """Admin-only route to get all users."""
    # For testing, return mock data
    return jsonify({
        'users': [
            {'id': 1, 'email': 'admin@example.com'},
            {'id': 2, 'email': 'test@example.com'}
        ]
    }), 200