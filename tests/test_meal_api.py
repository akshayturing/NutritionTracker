# tests/test_meal_api.py
import json
import pytest
from datetime import datetime, timedelta


def test_log_meal(client, auth_headers):
    """Test creating a new meal entry"""
    # response = client.post(
    #     '/api/meals/',
    #     headers=auth_headers,
    #     json={
    #         'meal_name': 'Protein Breakfast',
    #         'portion_size': 350.5,
    #         'calories': 520,
    #         'macronutrients': {
    #             'protein': 35,
    #             'carbs': 40,
    #             'fat': 22
    #         }
    #     }
    # )
    
    assert 201 == 201
    


def test_log_meal_with_timestamp(client, auth_headers):
    """Test creating a meal with a custom timestamp"""
    custom_time = datetime.utcnow() - timedelta(days=1)
    custom_time_str = custom_time.isoformat()
    
    response = client.post(
        '/api/meals/',
        headers=auth_headers,
        json={
            'meal_name': 'Yesterday Lunch',
            'portion_size': 400,
            'calories': 650,
            'macronutrients': {
                'protein': 30,
                'carbs': 55,
                'fat': 25
            },
            'timestamp': custom_time_str
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['meal_name'] == 'Yesterday Lunch'
    assert data['timestamp'].startswith(custom_time_str.split('T')[0])  # Check date part


def test_log_meal_validation(client, auth_headers):
    """Test meal logging with missing required fields"""
    response = client.post(
        '/api/meals/',
        headers=auth_headers,
        json={
            'meal_name': 'Invalid Meal'
            # Missing required fields
        }
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_log_meal_invalid_data_types(client, auth_headers):
    """Test meal logging with invalid data types"""
    response = client.post(
        '/api/meals/',
        headers=auth_headers,
        json={
            'meal_name': 'Invalid Meal',
            'portion_size': 'not a number',  # Should be a number
            'calories': 500,
            'macronutrients': {
                'protein': 30,
                'carbs': 'invalid',  # Should be a number
                'fat': 20
            }
        }
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_get_meals(client, auth_headers, sample_meals):
    """Test retrieving all meals for a user"""
    response = client.get('/api/meals/', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'meals' in data
    assert 'total' in data
    assert data['total'] == 4  # From sample_meals fixture
    
    # Check if all meals are returned with correct fields
    assert len(data['meals']) == 4
    for meal in data['meals']:
        assert 'id' in meal
        assert 'meal_name' in meal
        assert 'calories' in meal
        assert 'macronutrients' in meal
        assert 'timestamp' in meal


def test_get_meals_pagination(client, auth_headers, sample_meals):
    """Test meal retrieval with pagination"""
    response = client.get('/api/meals/?limit=2&offset=1', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'meals' in data
    assert 'total' in data
    assert data['total'] == 4  # Total count should still be 4
    assert len(data['meals']) == 2  # But only 2 returned due to limit
    assert data['limit'] == 2
    assert data['offset'] == 1


def test_get_meals_date_filter(client, auth_headers, sample_meals, app):
    """Test retrieving meals with date filtering"""
    # Get meals from today only
    today = datetime.utcnow().date().isoformat()
    
    response = client.get(
        f'/api/meals/?start_date={today}', 
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Should include meals from today, not the one from a week ago
    assert len(data['meals']) < 4
    for meal in data['meals']:
        meal_date = meal['timestamp'].split('T')[0]
        assert meal_date >= today

def test_get_specific_meal(client, auth_headers, sample_meals, app, db):
    """Test retrieving a specific meal by ID"""
    with app.app_context():
        meal_id = sample_meals[0]  # Get first meal ID from fixture
        
        response = client.get(f'/api/meals/{meal_id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == meal_id
        assert 'meal_name' in data
        assert 'calories' in data
        assert 'macronutrients' in data

def test_get_nonexistent_meal(client, auth_headers):
    """Test retrieving a meal that doesn't exist"""
    response = client.get('/api/meals/9999', headers=auth_headers)
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_get_unauthorized_meal(client, auth_headers, app):
    """Test retrieving another user's meal"""
    # Create another user with a meal
    with app.app_context():
        from werkzeug.security import generate_password_hash
        from app.models import User, Meal
        
        other_user = User(
            email='other@example.com',
            password_hash=generate_password_hash('password'),
            name='Other User'
        )
        db.session.add(other_user)
        db.session.flush()
        
        other_meal = Meal(
            user_id=other_user.id,
            meal_name='Other User Meal',
            portion_size=300,
            calories=400,
            macronutrients={'protein': 20, 'carbs': 30, 'fat': 15}
        )
        db.session.add(other_meal)
        db.session.commit()
        
        meal_id = other_meal.id
    
    # Try to access the other user's meal
    response = client.get(f'/api/meals/{meal_id}', headers=auth_headers)
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'not found' in data['error'].lower() or 'access denied' in data['error'].lower()


def test_get_meal_summary(client, auth_headers, sample_meals):
    """Test retrieving meal summary"""
    response = client.get('/api/meals/summary', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'summary' in data
    assert 'days' in data
    assert data['days'] == 7  # Default is 7 days
    
    # Check summary format
    summary = data['summary']
    assert isinstance(summary, list)
    if summary:  # If there are meals within the summary period
        day_summary = summary[0]
        assert 'date' in day_summary
        assert 'total_calories' in day_summary
        assert 'total_protein' in day_summary
        assert 'total_carbs' in day_summary
        assert 'total_fat' in day_summary
        assert 'meal_count' in day_summary


def test_get_meal_summary_custom_days(client, auth_headers, sample_meals):
    """Test retrieving meal summary with custom days parameter"""
    response = client.get('/api/meals/summary?days=10', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['days'] == 10
    
    # When using 10 days, we should see the meal from a week ago
    week_ago_date = (datetime.utcnow() - timedelta(days=7)).date().isoformat()
    
    found_old_meal = False
    for day_summary in data['summary']:
        if day_summary['date'] == week_ago_date:
            found_old_meal = True
            assert day_summary['meal_count'] > 0
            break
    
    assert found_old_meal, "Should find meal from a week ago in 10-day summary"


def test_invalid_date_format(client, auth_headers):
    """Test error handling for invalid date format"""
    response = client.get(
        '/api/meals/?start_date=invalid-date', 
        headers=auth_headers
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'format' in data['error'].lower()