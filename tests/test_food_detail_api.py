import json
import pytest

def test_get_food_by_id(client):
    """Test getting a food by ID."""
    # First, search to get a food ID
    response = client.get('/api/foods/search?q=Apple')
    data = json.loads(response.data)
    
    assert len(data['foods']) > 0
    food_id = data['foods'][0]['id']
    
    # Now get the food by ID
    response = client.get(f'/api/foods/{food_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['id'] == food_id
    assert 'name' in data
    assert 'nutrients' in data
    assert 'categories' in data
    assert isinstance(data['nutrients'], dict)
    assert isinstance(data['categories'], list)

def test_get_food_not_found(client):
    """Test getting a non-existent food."""
    response = client.get('/api/foods/99999')
    
    assert response.status_code == 404

def test_food_response_format(client):
    """Test the format of food response data."""
    # First, search to get a food ID
    response = client.get('/api/foods/search?q=Apple')
    data = json.loads(response.data)
    
    food_id = data['foods'][0]['id']
    
    # Get the food by ID
    response = client.get(f'/api/foods/{food_id}')
    food = json.loads(response.data)
    
    # Check all required fields
    required_fields = [
        'id', 'name', 'description', 'serving_size', 'serving_unit',
        'nutrients', 'categories', 'verified'
    ]
    for field in required_fields:
        assert field in food
    
    # Check nutrient format (at least one nutrient for our test data)
    assert len(food['nutrients']) > 0
    first_nutrient = next(iter(food['nutrients'].values()))
    assert 'value' in first_nutrient
    assert 'unit' in first_nutrient
    assert 'name' in first_nutrient

def test_get_nutrients_list(client):
    """Test getting the list of all nutrients."""
    response = client.get('/api/foods/nutrient-list')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    # Should have at least the 'Macronutrients' category
    assert 'Macronutrients' in data
    # Should have at least the nutrients we added in setup
    assert len(data['Macronutrients']) >= 5
    
    # Check format of a nutrient
    nutrient = data['Macronutrients'][0]
    assert 'id' in nutrient
    assert 'name' in nutrient
    assert 'code' in nutrient
    assert 'unit' in nutrient

def test_get_categories(client):
    """Test getting the list of food categories."""
    response = client.get('/api/foods/categories')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'categories' in data
    assert len(data['categories']) >= 3  # At least the ones we added in setup
    
    # Check format of a category
    category = data['categories'][0]
    assert 'id' in category
    assert 'name' in category
    assert 'description' in category