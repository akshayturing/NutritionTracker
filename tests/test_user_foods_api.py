# tests/test_user_foods_api.py
import json
import pytest

def test_get_user_foods(client):
    """Test getting foods associated with a user."""
    # First, get user ID
    with client.application.app_context():
        from models import User
        user = User.query.filter_by(username='testuser').first()
        user_id = user.id
    
    # Create a custom food for the user
    new_food = {
        'name': 'User Custom Food',
        'description': 'A custom food for a specific user',
        'serving_size': 100,
        'serving_unit': 'g'
    }
    
    response = client.post(
        '/api/foods/',
        data=json.dumps(new_food),
        content_type='application/json'
    )
    food_data = json.loads(response.data)
    food_id = food_data['id']
    
    # Associate this food with the user
    with client.application.app_context():
        from models import db, UserCustomFood
        user_food = UserCustomFood(
            user_id=user_id,
            food_id=food_id,
            is_created=True
        )
        db.session.add(user_food)
        db.session.commit()
    
    # Now get user foods
    response = client.get(f'/api/foods/user-foods?user_id={user_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'foods' in data
    assert len(data['foods']) >= 1  # At least the one we just created
    assert any(food['name'] == 'User Custom Food' for food in data['foods'])

def test_get_user_foods_no_user_id(client):
    """Test getting user foods without providing a user ID."""
    response = client.get('/api/foods/user-foods')
    
    assert response.status_code == 400  # Bad request

def test_get_user_foods_invalid_user(client):
    """Test getting foods for a non-existent user."""
    response = client.get('/api/foods/user-foods?user_id=99999')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'foods' in data
    assert len(data['foods']) == 0  # No foods for non-existent user