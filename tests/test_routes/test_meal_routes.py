import pytest
from datetime import datetime, date, timedelta
import json
from unittest.mock import patch, MagicMock

from app.routes.meal_routes import create_meal, get_meal, update_meal


class TestMealService:
    """Test suite for meal-related services in meal_routes.py"""
    
    @pytest.fixture
    def user_id(self, test_user):
        return test_user.id
    
    @pytest.fixture
    def meal_id(self):
        return 1
    
    @pytest.fixture
    def test_date(self):
        return date.today()
    
    @pytest.fixture
    def meal_data(self, test_date):
        """Test meal data fixture"""
        return {
            'meal_name': 'Dinner',
            'portion_size': 1.5,
            'timestamp': datetime.combine(test_date, datetime.min.time()) + timedelta(hours=19),
            'calories': 800,
            'macronutrients': {
                'protein': 40,
                'carbs': 80,
                'fat': 30
            }
        }
    
    @patch('app.models.meal.Meal')
    @patch('app.models.db.session')
    def test_create_meal(self, mock_db_session, mock_meal, user_id, meal_id, meal_data):
        """Test the meal creation service"""
        # Setup mock
        mock_meal_instance = MagicMock()
        mock_meal_instance.id = meal_id
        mock_meal_instance.user_id = user_id
        mock_meal_instance.to_dict.return_value = {
            'id': meal_id,
            'user_id': user_id,
            'meal_name': meal_data['meal_name'],
            'portion_size': meal_data['portion_size'],
            'timestamp': meal_data['timestamp'],
            'calories': meal_data['calories'],
            'macronutrients': json.dumps(meal_data['macronutrients'])
        }
        
        mock_meal.return_value = mock_meal_instance
        
        # Execute
        result = create_meal(user_id, meal_data)
        
        # Assert
        assert result['id'] == meal_id
        assert result['user_id'] == user_id
        assert result['meal_name'] == 'Dinner'
        assert json.loads(result['macronutrients'])['protein'] == 40
        
        # Verify mock calls
        mock_meal.assert_called_once()
        mock_db_session.add.assert_called_once_with(mock_meal_instance)
        mock_db_session.commit.assert_called_once()

    @patch('app.models.meal.Meal.query')
    def test_get_meal(self, mock_meal_query, meal_id, user_id):
        """Test getting a meal by ID"""
        # Setup mock
        mock_meal = MagicMock()
        mock_meal.id = meal_id
        mock_meal.user_id = user_id
        mock_meal.to_dict.return_value = {
            'id': meal_id,
            'user_id': user_id,
            'meal_name': 'Test Meal',
            'calories': 500
        }
        
        mock_meal_query.get.return_value = mock_meal
        
        # Execute
        result = get_meal(meal_id)
        
        # Assert
        assert result['id'] == meal_id
        assert result['user_id'] == user_id
        
        # Verify mock calls
        mock_meal_query.get.assert_called_once_with(meal_id)

    @patch('app.models.meal.Meal.query')
    @patch('app.models.db.session')
    def test_update_meal(self, mock_db_session, mock_meal_query, user_id, meal_id, test_date):
        """Test the meal update functionality"""
        # Setup existing meal mock
        mock_meal = MagicMock()
        mock_meal.id = meal_id
        mock_meal.user_id = user_id
        mock_meal.meal_name = 'Lunch'
        mock_meal.calories = 600
        mock_meal.portion_size = 1.0
        mock_meal.timestamp = datetime.combine(test_date, datetime.min.time()) + timedelta(hours=13)
        mock_meal.macronutrients = json.dumps({
            'protein': 30,
            'carbs': 70,
            'fat': 20
        })
        
        # Setup mock return from query
        mock_meal_query.get.return_value = mock_meal
        
        # Setup update data
        update_data = {
            'meal_name': 'Late Lunch',
            'calories': 650,
            'macronutrients': {
                'protein': 35,
                'carbs': 65,
                'fat': 25
            }
        }
        
        # Mock to_dict function
        def mock_to_dict():
            return {
                'id': meal_id,
                'user_id': user_id,
                'meal_name': mock_meal.meal_name,
                'calories': mock_meal.calories,
                'portion_size': mock_meal.portion_size,
                'timestamp': mock_meal.timestamp,
                'macronutrients': mock_meal.macronutrients
            }
            
        mock_meal.to_dict.side_effect = mock_to_dict
        
        # Execute
        result = update_meal(meal_id, update_data)
        
        # Assert - The update should have modified these attributes
        assert mock_meal.meal_name == 'Late Lunch'
        assert mock_meal.calories == 650
        assert json.loads(mock_meal.macronutrients)['protein'] == 35
        
        # The result should reflect these changes
        assert result['meal_name'] == 'Late Lunch'
        assert result['calories'] == 650
        
        # Verify mocks were called correctly
        mock_meal_query.get.assert_called_once_with(meal_id)
        mock_db_session.commit.assert_called_once()