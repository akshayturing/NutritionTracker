# routes/documentation.py
from flask import Blueprint, jsonify

docs_bp = Blueprint('docs', __name__, url_prefix='/api/docs')

@docs_bp.route('/', methods=['GET'])
def get_documentation():
    """Return API documentation"""
    return jsonify({
        'api_name': 'Custom Food Nutrition API',
        'version': '1.0',
        'endpoints': [
            {
                'path': '/api/foods/search',
                'method': 'GET',
                'description': 'Search for food items by name, description, or brand',
                'parameters': [
                    {'name': 'q', 'type': 'string', 'description': 'Search query'},
                    {'name': 'category', 'type': 'string', 'description': 'Filter by category'},
                    {'name': 'verified', 'type': 'boolean', 'description': 'Filter for verified foods only'},
                    {'name': 'page', 'type': 'integer', 'default': 1, 'description': 'Page number'},
                    {'name': 'per_page', 'type': 'integer', 'default': 20, 'description': 'Items per page'}
                ],
                'example': '/api/foods/search?q=apple&category=Fruits&page=1&per_page=10'
            },
            {
                'path': '/api/foods/categories',
                'method': 'GET',
                'description': 'Get all food categories',
                'example': '/api/foods/categories'
            },
            {
                'path': '/api/foods/{food_id}',
                'method': 'GET',
                'description': 'Get detailed information for a specific food',
                'parameters': [
                    {'name': 'food_id', 'type': 'integer', 'description': 'ID of the food item'},
                ],
                'example': '/api/foods/1'
            },
            {
                'path': '/api/foods/nutrient-list',
                'method': 'GET',
                'description': 'Get list of all available nutrients',
                'example': '/api/foods/nutrient-list'
            },
            {
                'path': '/api/foods/',
                'method': 'POST',
                'description': 'Create a new food item',
                'body': {
                    'name': {'type': 'string', 'required': True},
                    'brand': {'type': 'string'},
                    'description': {'type': 'string'},
                    'serving_size': {'type': 'number'},
                    'serving_unit': {'type': 'string'},
                    'serving_description': {'type': 'string'},
                    'categories': {'type': 'array'},
                    'nutrients': {'type': 'object'}
                },
                'example_body': {
                    'name': 'Banana',
                    'description': 'Medium yellow banana',
                    'serving_size': 118,
                    'serving_unit': 'g',
                    'serving_description': '1 medium',
                    'categories': ['Fruits'],
                    'nutrients': {
                        'ENERC_KCAL': 105,
                        'PROCNT': 1.3,
                        'FAT': 0.4,
                        'CHOCDF': 27,
                        'FIBTG': 3.1
                    }
                }
            },
            {
                'path': '/api/foods/{food_id}',
                'method': 'PUT',
                'description': 'Update an existing food item',
                'parameters': [
                    {'name': 'food_id', 'type': 'integer', 'description': 'ID of the food item'},
                ],
                'body': 'Same format as POST /api/foods/'
            },
            {
                'path': '/api/foods/{food_id}',
                'method': 'DELETE',
                'description': 'Delete a food item',
                'parameters': [
                    {'name': 'food_id', 'type': 'integer', 'description': 'ID of the food item'},
                ]
            },
            {
                'path': '/api/foods/calculate',
                'method': 'POST',
                'description': 'Calculate nutrition for a list of foods with quantities',
                'body': {
                    'items': {
                        'type': 'array',
                        'items': {
                            'food_id': {'type': 'integer'},
                            'quantity': {'type': 'number'},
                            'unit': {'type': 'string'}
                        }
                    }
                },
                'example_body': {
                    'items': [
                        {'food_id': 1, 'quantity': 100, 'unit': 'g'},
                        {'food_id': 2, 'quantity': 50, 'unit': 'g'}
                    ]
                }
            },
            {
                'path': '/api/foods/user-foods',
                'method': 'GET',
                'description': 'Get foods created or modified by a user',
                'parameters': [
                    {'name': 'user_id', 'type': 'integer', 'required': True, 'description': 'ID of the user'},
                ],
                'example': '/api/foods/user-foods?user_id=1'
            }
        ]
    })

# Register in app.py
# app.register_blueprint(docs_bp)