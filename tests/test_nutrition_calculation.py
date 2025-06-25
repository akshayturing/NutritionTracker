import json
import pytest

def test_calculate_nutrition_single_food(client):
    """Test calculating nutrition for a single food."""
    # Get a food ID
    response = client.get('/api/foods/search?q=Apple')
    data = json.loads(response.data)
    food_id = data['foods'][0]['id']
    
    # Calculate nutrition
    request_data = {
        'items': [
            {'food_id': food_id, 'quantity': 100, 'unit': 'g'}
        ]
    }
    response = client.post(
        '/api/foods/calculate',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'total_nutrients' in data
    
    # Check that the values match the original food (since quantity=100g)
    orig_response = client.get(f'/api/foods/{food_id}')
    orig_data = json.loads(orig_response.data)
    
    for code, nutrient in data['total_nutrients'].items():
        assert code in orig_data['nutrients']
        assert nutrient['value'] == orig_data['nutrients'][code]['value']
        assert nutrient['unit'] == orig_data['nutrients'][code]['unit']

def test_calculate_nutrition_multiple_foods(client):
    """Test calculating nutrition for multiple foods."""
    # Get food IDs
    apple_response = client.get('/api/foods/search?q=Apple')
    apple_data = json.loads(apple_response.data)
    apple_id = apple_data['foods'][0]['id']
    
    spinach_response = client.get('/api/foods/search?q=Spinach')
    spinach_data = json.loads(spinach_response.data)
    spinach_id = spinach_data['foods'][0]['id']
    
    # Calculate nutrition for both
    request_data = {
        'items': [
            {'food_id': apple_id, 'quantity': 150, 'unit': 'g'},
            {'food_id': spinach_id, 'quantity': 50, 'unit': 'g'}
        ]
    }
    response = client.post(
        '/api/foods/calculate',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    calc_data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'total_nutrients' in calc_data
    
    # Calculate expected values manually
    apple_orig = json.loads(client.get(f'/api/foods/{apple_id}').data)
    spinach_orig = json.loads(client.get(f'/api/foods/{spinach_id}').data)
    
    # Check a few nutrients
    energy_expected = (apple_orig['nutrients']['ENERC_KCAL']['value'] * 1.5 + 
                      spinach_orig['nutrients']['ENERC_KCAL']['value'] * 0.5)
    protein_expected = (apple_orig['nutrients']['PROCNT']['value'] * 1.5 + 
                       spinach_orig['nutrients']['PROCNT']['value'] * 0.5)
    
    assert calc_data['total_nutrients']['ENERC_KCAL']['value'] == pytest.approx(energy_expected)
    assert calc_data['total_nutrients']['PROCNT']['value'] == pytest.approx(protein_expected)

def test_calculate_nutrition_invalid_food(client):
    """Test calculating nutrition with non-existent food."""
    request_data = {
        'items': [
            {'food_id': 99999, 'quantity': 100, 'unit': 'g'}
        ]
    }
    response = client.post(
        '/api/foods/calculate',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200  # Still works but with warnings
    assert 'warnings' in data
    assert 'missing_foods' in data['warnings']
    assert 99999 in data['warnings']['missing_foods']
    assert 'total_nutrients' in data  # Should still return empty nutrition data

def test_calculate_nutrition_invalid_request(client):
    """Test calculating nutrition with invalid request format."""
    request_data = {
        'invalid_key': 'invalid_value'
    }
    response = client.post(
        '/api/foods/calculate',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400

def test_calculate_nutrition_different_units(client):
    """Test calculating nutrition with different units."""
    # Get a food ID
    response = client.get('/api/foods/search?q=Apple')
    data = json.loads(response.data)
    food_id = data['foods'][0]['id']
    
    # Calculate nutrition with different unit (ml instead of g)
    request_data = {
        'items': [
            {'food_id': food_id, 'quantity': 200, 'unit': 'ml'}
        ]
    }
    response = client.post(
        '/api/foods/calculate',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    # This should still work by treating ml as equivalent to g for simplicity
    assert response.status_code == 200
    assert 'total_nutrients' in data
    
    # Should be double the original values since quantity is 200
    orig_response = client.get(f'/api/foods/{food_id}')
    orig_data = json.loads(orig_response.data)
    
    for code, nutrient in data['total_nutrients'].items():
        if code in orig_data['nutrients']:
            assert nutrient['value'] == pytest.approx(orig_data['nutrients'][code]['value'] * 2)