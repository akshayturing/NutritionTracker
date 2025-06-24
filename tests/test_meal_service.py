import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, date, timedelta
import json

class MealServiceTests(unittest.TestCase):
    """Test suite for meal-related services"""
    
    def setUp(self):
        """Set up test data"""
        self.user_id = 1
        self.meal_id = 1
        self.test_date = date.today()
        
        # Mock meal data
        self.meal_data = {
            'meal_name': 'Dinner',
            'portion_size': 1.5,
            'timestamp': datetime.combine(self.test_date, datetime.min.time()) + timedelta(hours=19),
            'calories': 800,
            'macronutrients': {
                'protein': 40,
                'carbs': 80,
                'fat': 30
            }
        }
    
    @patch('app.services.meal_service.create_meal')
    def test_create_meal_service(self, mock_create_meal):
        """Test the meal creation service"""
        # Setup mock
        expected_meal = {
            'id': self.meal_id,
            'user_id': self.user_id,
            **self.meal_data,
            'macronutrients': json.dumps(self.meal_data['macronutrients'])
        }
        mock_create_meal.return_value = expected_meal
        
        # Execute
        from app.services.meal_service import create_meal_entry
        result = create_meal_entry(self.user_id, self.meal_data)
        
        # Assert
        self.assertEqual(result['id'], self.meal_id)
        self.assertEqual(result['user_id'], self.user_id)
        self.assertEqual(result['meal_name'], 'Dinner')
        self.assertEqual(json.loads(result['macronutrients'])['protein'], 40)
        
        # Verify mock called correctly
        mock_create_meal.assert_called_once_with(self.user_id, self.meal_data)

    @patch('app.services.meal_service.get_meal')
    @patch('app.services.meal_service.update_meal')
    def test_update_meal_service(self, mock_update_meal, mock_get_meal):
        """Test the meal update service"""
        # Setup existing meal mock
        existing_meal = {
            'id': self.meal_id,
            'user_id': self.user_id,
            'meal_name': 'Lunch',
            'portion_size': 1.0,
            'timestamp': datetime.combine(self.test_date, datetime.min.time()) + timedelta(hours=13),
            'calories': 600,
            'macronutrients': json.dumps({
                'protein': 30,
                'carbs': 70,
                'fat': 20
            })
        }
        
        # Setup updated meal mock
        updated_meal = {
            **existing_meal,
            'meal_name': 'Late Lunch',
            'calories': 650,
            'macronutrients': json.dumps({
                'protein': 35,
                'carbs': 65,
                'fat': 25
            })
        }
        
        # Setup mocks
        mock_get_meal.return_value = existing_meal
        mock_update_meal.return_value = updated_meal
        
        # Execute
        update_data = {
            'meal_name': 'Late Lunch',
            'calories': 650,
            'macronutrients': {
                'protein': 35,
                'carbs': 65,
                'fat': 25
            }
        }
        
        from app.services.meal_service import update_meal_entry
        result = update_meal_entry(self.user_id, self.meal_id, update_data)
        
        # Assert
        self.assertEqual(result['meal_name'], 'Late Lunch')
        self.assertEqual(result['calories'], 650)
        self.assertEqual(json.loads(result['macronutrients'])['protein'], 35)
        
        # Verify mocks called correctly
        mock_get_meal.assert_called_once_with(self.meal_id)
        mock_update_meal.assert_called_once()


if __name__ == '__main__':
    unittest.main()