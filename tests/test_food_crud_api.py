import json
import pytest

def test_create_food(client):
    """Test creating a new food item."""
    new_food = {
        'name': 'Test New Food',
        'description': 'A new food created for testing',
        'serving_size': 100,
        'serving_unit': 'g',
        'categories': ['Fruits', 'Vegetables'],
        'nutrients': {
            'ENERC_KCAL': {'value': 100},
            'PROCNT': {'value': 5},
            'FAT': {'value': 2},
            'CHOCDF': {'value': 15}
        }
    }
    
    response = client.post(
        '/api/foods/',
        data=json.dumps(new_food),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['name'] == new_food['name']
    assert data['description'] == new_food['description']
    assert data['serving_size'] == new_food['serving_size']
    assert 'Fruits' in data['categories']
    assert 'Vegetables' in data['categories']
    assert 'id' in data  # Should have assigned an ID
    
    # Check that nutrients were added
    assert 'ENERC_KCAL' in data['nutrients']
    assert data['nutrients']['ENERC_KCAL']['value'] == 100

def test_create_food_missing_name(client):
    """Test creating a food without a name."""
    new_food = {
        'description': 'A food with no name',
        'serving_size': 100,
        'serving_unit': 'g'
    }
    
    response = client.post(
        '/api/foods/',
        data=json.dumps(new_food),
        content_type='application/json'
    )
    
    assert response.status_code == 400  # Bad request

def test_update_food(client):
    """Test updating an existing food."""
    # First, create a food
    new_food = {
        'name': 'Food to Update',
        'description': 'A food that will be updated',
        'serving_size': 100,
        'serving_unit': 'g',
        'nutrients': {
            'ENERC_KCAL': {'value': 100}
        }
    }
    
    create_response = client.post(
        '/api/foods/',
        data=json.dumps(new_food),
        content_type='application/json'
    )
    create_data = json.loads(create_response.data)
    food_id = create_data['id']
    
    # Now update it
    update_data = {
        'name': 'Updated Food Name',
        'description': 'Updated description',
        'nutrients': {
            'ENERC_KCAL': {'value': 150},
            'PROCNT': {'value': 10}
        }
    }
    
    response = client.put(
        f'/api/foods/{food_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['name'] == update_data['name']
    assert data['description'] == update_data['description']
    assert data['nutrients']['ENERC_KCAL']['value'] == 150
    assert data['nutrients']['PROCNT']['value'] == 10

def test_update_nonexistent_food(client):
    """Test updating a food that doesn't exist."""
    update_data = {
        'name': 'This Food Doesn\'t Exist',
        'description': 'Trying to update a nonexistent food'
    }
    
    response = client.put(
        '/api/foods/99999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 404  # Not found

def test_delete_food(client):
    """Test deleting a food."""
    # First, create a food to delete
    new_food = {
        'name': 'Food to Delete',
        'description': 'A food that will be deleted',
        'serving_size': 100,
        'serving_unit': 'g'
    }
    
    create_response = client.post(
        '/api/foods/',
        data=json.dumps(new_food),
        content_type='application/json'
    )
    create_data = json.loads(create_response.data)
    food_id = create_data['id']
    
    # Now delete it
    delete_response = client.delete(f'/api/foods/{food_id}')
    
    assert delete_response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f'/api/foods/{food_id}')
    assert get_response.status_code == 404
