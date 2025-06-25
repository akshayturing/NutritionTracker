import json
import pytest

def test_invalid_json_format(client):
    """Test sending invalid JSON."""
    response = client.post(
        '/api/foods/',
        data='invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 400

def test_invalid_nutrient_code(client):
    """Test creating a food with invalid nutrient code."""
    new_food = {
        'name': 'Food with Invalid Nutrient',
        'description': 'A food with a non-existent nutrient code',
        'nutrients': {
            'NONEXISTENT': {'value': 100}  # This nutrient code doesn't exist
        }
    }
    
    response = client.post(
        '/api/foods/',
        data=json.dumps(new_food),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201  # Should still work, just ignore invalid nutrients
    assert 'NONEXISTENT' not in data['nutrients']  # Invalid nutrient should be ignored

def test_invalid_category(client):
    """Test creating a food with non-existent category."""
    new_food = {
        'name': 'Food with Invalid Category',
        'description': 'A food with a non-existent category',
        'categories': ['NonexistentCategory']
    }
    
    response = client.post(
        '/api/foods/',
        data=json.dumps(new_food),
        content_type='application/json'
    )
    
    # Should create the category if it doesn't exist
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'NonexistentCategory' in data['categories']

def test_calculation_with_invalid_quantity(client):
    """Test calculating nutrition with invalid quantity."""
    # Get a food ID
    response = client.get('/api/foods/search?q=Apple')
    data = json.loads(response.data)
    food_id = data['foods'][0]['id']
    
    # Calculate with invalid quantity
    request_data = {
        'items': [
            {'food_id': food_id, 'quantity': 'not a number', 'unit': 'g'}
        ]
    }
    response = client.post(
        '/api/foods/calculate',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    # Should handle gracefully and return an error
    assert response.status_code == 400
