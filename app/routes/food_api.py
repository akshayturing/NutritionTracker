# routes/food_api.py
from flask import Blueprint, jsonify, request, current_app
from models.food_database import db, FoodItem, Nutrient, NutrientValue, FoodCategory, UserCustomFood
from sqlalchemy import or_, desc, func
import math

food_api = Blueprint('food_api', __name__, url_prefix='/api/foods')

# ----------------------
# Search endpoints
# ----------------------

@food_api.route('/search', methods=['GET'])
def search_foods():
    """Search for food items by name, description, or brand"""
    query = request.args.get('q', '')
    category = request.args.get('category')
    verified_only = request.args.get('verified', 'false').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Build query
    food_query = FoodItem.query
    
    # Apply search filter if provided
    if query:
        search_filter = or_(
            FoodItem.name.ilike(f'%{query}%'),
            FoodItem.description.ilike(f'%{query}%'),
            FoodItem.brand.ilike(f'%{query}%')
        )
        food_query = food_query.filter(search_filter)
    
    # Apply category filter if provided
    if category:
        food_query = food_query.join(FoodItem.categories).filter(FoodCategory.name == category)
    
    # Apply verified filter if requested
    if verified_only:
        food_query = food_query.filter(FoodItem.verified == True)
    
    # Count total results for pagination
    total_count = food_query.count()
    total_pages = math.ceil(total_count / per_page)
    
    # Apply pagination
    foods = food_query.order_by(FoodItem.name).paginate(page=page, per_page=per_page, error_out=False)
    
    # Format response
    result = {
        'foods': [food.to_dict() for food in foods.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_count': total_count
        }
    }
    
    return jsonify(result)

@food_api.route('/categories', methods=['GET'])
def get_categories():
    """Get all food categories"""
    categories = FoodCategory.query.order_by(FoodCategory.name).all()
    return jsonify({
        'categories': [{'id': cat.id, 'name': cat.name, 'description': cat.description} 
                      for cat in categories]
    })

# ----------------------
# Detailed food endpoints
# ----------------------

@food_api.route('/<int:food_id>', methods=['GET'])
def get_food(food_id):
    """Get detailed information for a specific food"""
    food = FoodItem.query.get_or_404(food_id)
    return jsonify(food.to_dict())

@food_api.route('/nutrient-list', methods=['GET'])
def get_nutrients():
    """Get list of all available nutrients"""
    nutrients = Nutrient.query.order_by(Nutrient.category, Nutrient.display_order).all()
    result = {}
    
    # Group nutrients by category
    for nutrient in nutrients:
        category = nutrient.category or 'Other'
        if category not in result:
            result[category] = []
            
        result[category].append({
            'id': nutrient.id,
            'name': nutrient.name,
            'code': nutrient.code,
            'unit': nutrient.unit,
            'display_order': nutrient.display_order
        })
    
    return jsonify(result)

# ----------------------
# CRUD operations for foods
# ----------------------

@food_api.route('/', methods=['POST'])
def create_food():
    """Create a new food item"""
    data = request.json
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Food name is required'}), 400
    
    # Create new food item
    food = FoodItem(
        name=data['name'],
        brand=data.get('brand', ''),
        description=data.get('description', ''),
        serving_size=data.get('serving_size', 100.0),
        serving_unit=data.get('serving_unit', 'g'),
        serving_description=data.get('serving_description', ''),
        source=data.get('source', 'user-created'),
        verified=False  # User-created foods start as unverified
    )
    
    # Add categories if provided
    if 'categories' in data and isinstance(data['categories'], list):
        for category_name in data['categories']:
            # Get or create category
            category = FoodCategory.query.filter_by(name=category_name).first()
            if not category:
                category = FoodCategory(name=category_name)
                db.session.add(category)
            
            food.categories.append(category)
    
    # Add nutrients if provided
    if 'nutrients' in data and isinstance(data['nutrients'], dict):
        for nutrient_code, nutrient_data in data['nutrients'].items():
            # Get the nutrient by code
            nutrient = Nutrient.query.filter_by(code=nutrient_code).first()
            
            # Skip if nutrient doesn't exist
            if not nutrient:
                continue
                
            # Create nutrient value
            nutrient_value = NutrientValue(
                nutrient=nutrient,
                value=nutrient_data.get('value', 0)
            )
            
            food.nutrients.append(nutrient_value)
    
    # Save to database
    db.session.add(food)
    db.session.commit()
    
    # If user is authenticated, associate food with user
    if hasattr(request, 'user') and request.user:
        user_food = UserCustomFood(
            user_id=request.user.id,
            food_id=food.id,
            is_created=True
        )
        db.session.add(user_food)
        db.session.commit()
    
    return jsonify(food.to_dict()), 201

@food_api.route('/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    """Update an existing food item"""
    food = FoodItem.query.get_or_404(food_id)
    data = request.json
    
    # Check if user can edit this food - system foods can only be edited by admins
    if food.source != 'user-created' and not (hasattr(request, 'user') and request.user.is_admin):
        return jsonify({'error': 'Cannot edit system food items'}), 403
    
    # Update basic properties
    if 'name' in data:
        food.name = data['name']
    if 'brand' in data:
        food.brand = data['brand']
    if 'description' in data:
        food.description = data['description']
    if 'serving_size' in data:
        food.serving_size = data['serving_size']
    if 'serving_unit' in data:
        food.serving_unit = data['serving_unit']
    if 'serving_description' in data:
        food.serving_description = data['serving_description']
    
    # Update categories if provided
    if 'categories' in data and isinstance(data['categories'], list):
        # Clear existing categories
        food.categories = []
        
        for category_name in data['categories']:
            # Get or create category
            category = FoodCategory.query.filter_by(name=category_name).first()
            if not category:
                category = FoodCategory(name=category_name)
                db.session.add(category)
            
            food.categories.append(category)
    
    # Update nutrients if provided
    if 'nutrients' in data and isinstance(data['nutrients'], dict):
        # Get current nutrients for efficient update
        current_nutrients = {nv.nutrient.code: nv for nv in food.nutrients}
        
        for nutrient_code, nutrient_data in data['nutrients'].items():
            # Get the nutrient by code
            nutrient = Nutrient.query.filter_by(code=nutrient_code).first()
            
            # Skip if nutrient doesn't exist
            if not nutrient:
                continue
                
            # Update existing value or create new one
            if nutrient_code in current_nutrients:
                current_nutrients[nutrient_code].value = nutrient_data.get('value', 0)
            else:
                nutrient_value = NutrientValue(
                    nutrient=nutrient,
                    value=nutrient_data.get('value', 0)
                )
                food.nutrients.append(nutrient_value)
    
    # Save changes
    db.session.commit()
    
    # If user is authenticated and this isn't already a user custom food, create that association
    if hasattr(request, 'user') and request.user:
        user_food = UserCustomFood.query.filter_by(
            user_id=request.user.id, 
            food_id=food.id
        ).first()
        
        if not user_food:
            user_food = UserCustomFood(
                user_id=request.user.id,
                food_id=food.id,
                is_created=False  # Modified an existing food
            )
            db.session.add(user_food)
            db.session.commit()
    
    return jsonify(food.to_dict())

@food_api.route('/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    """Delete a food item"""
    food = FoodItem.query.get_or_404(food_id)
    
    # Check if user can delete this food
    if food.source != 'user-created' and not (hasattr(request, 'user') and request.user.is_admin):
        return jsonify({'error': 'Cannot delete system food items'}), 403
    
    db.session.delete(food)
    db.session.commit()
    
    return jsonify({'message': 'Food deleted successfully'})

# ----------------------
# Nutrition calculation endpoints
# ----------------------

@food_api.route('/calculate', methods=['POST'])
def calculate_nutrition():
    """Calculate nutrition for a list of foods with quantities"""
    data = request.json
    
    if not data or 'items' not in data or not isinstance(data['items'], list):
        return jsonify({'error': 'Items list is required'}), 400
    
    # Format expected: [{'food_id': 1, 'quantity': 100, 'unit': 'g'}, ...]
    food_ids = [item['food_id'] for item in data['items']]
    foods = FoodItem.query.filter(FoodItem.id.in_(food_ids)).all()
    
    # Map foods by ID for easy lookup
    food_map = {food.id: food for food in foods}
    
    # Calculate total nutrients
    total_nutrients = {}
    missing_foods = []
    
    for item in data['items']:
        food_id = item['food_id']
        quantity = item.get('quantity', 0)
        unit = item.get('unit', 'g')
        
        # Skip if food not found
        if food_id not in food_map:
            missing_foods.append(food_id)
            continue
        
        food = food_map[food_id]
        
        # Skip if units don't match and we don't have conversion
        if unit != food.serving_unit:
            # In a production app, you would implement unit conversion here
            # For simplicity, we'll just use the ratio directly
            pass
        
        # Calculate scaling factor based on quantity
        scale_factor = quantity / food.serving_size
        
        # Add nutrients to total, scaled by quantity
        for nutrient_value in food.nutrients:
            nutrient_code = nutrient_value.nutrient.code
            
            if nutrient_code not in total_nutrients:
                total_nutrients[nutrient_code] = {
                    'value': 0,
                    'unit': nutrient_value.nutrient.unit,
                    'name': nutrient_value.nutrient.name
                }
            
            # Add scaled value to total
            total_nutrients[nutrient_code]['value'] += (nutrient_value.value * scale_factor)
    
    result = {
        'total_nutrients': total_nutrients
    }
    
    # Add warnings if any foods were missing
    if missing_foods:
        result['warnings'] = {
            'missing_foods': missing_foods
        }
    
    return jsonify(result)

# ----------------------
# User custom foods endpoints
# ----------------------

@food_api.route('/user-foods', methods=['GET'])
def get_user_foods():
    """Get foods created or modified by the current user"""
    # In a real app, you would get the user from the authentication system
    # For this example, we'll use a query parameter
    user_id = request.args.get('user_id', type=int)
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    # Get user's custom foods
    user_foods = UserCustomFood.query.filter_by(user_id=user_id).all()
    food_ids = [uf.food_id for uf in user_foods]
    
    foods = FoodItem.query.filter(FoodItem.id.in_(food_ids)).all()
    
    return jsonify({
        'foods': [food.to_dict() for food in foods]
    })