# app/meals/utils.py

def validate_meal_data(data):
    """
    Validate meal data from API requests
    
    Args:
        data (dict): Meal data from request
        
    Returns:
        str: Error message if validation fails, None if validation passes
    """
    # Check required fields
    required_fields = ['meal_name', 'portion_size', 'calories']
    for field in required_fields:
        if field not in data:
            return f'Missing required field: {field}'
    
    # Validate field types
    if not isinstance(data['meal_name'], str):
        return 'meal_name must be a string'
    
    try:
        float(data['portion_size'])
    except (ValueError, TypeError):
        return 'portion_size must be a number'
    
    try:
        float(data['calories'])
    except (ValueError, TypeError):
        return 'calories must be a number'
    
    # Validate macronutrients if provided
    if 'macronutrients' in data:
        if not isinstance(data['macronutrients'], dict):
            return 'macronutrients must be an object'
            
        for nutrient in ['protein', 'carbs', 'fat']:
            if nutrient in data['macronutrients']:
                try:
                    float(data['macronutrients'][nutrient])
                except (ValueError, TypeError):
                    return f'{nutrient} must be a number'
    
    return None