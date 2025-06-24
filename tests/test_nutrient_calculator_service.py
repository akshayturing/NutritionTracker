import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, date, timedelta
import json

# Import the service modules
from app.services.nutrient_calculator import calculate_daily_nutrients, calculate_nutrient_trends

class NutrientCalculatorServiceTests(unittest.TestCase):
    """Test suite for the nutrient calculator service layer"""
    
    def setUp(self):
        """Set up test data"""
        self.user_id = 1
        self.test_date = date.today()
        
        # Mock meals data
        self.mock_meals = [
            {
                'id': 1,
                'meal_name': 'Breakfast',
                'portion_size': 1.0,
                'timestamp': datetime.combine(self.test_date, datetime.min.time()) + timedelta(hours=8),
                'calories': 450,
                'macronutrients': json.dumps({
                    'protein': 20,
                    'carbs': 55,
                    'fat': 15
                })
            },
            {
                'id': 2,
                'meal_name': 'Lunch',
                'portion_size': 1.0,
                'timestamp': datetime.combine(self.test_date, datetime.min.time()) + timedelta(hours=13),
                'calories': 650,
                'macronutrients': json.dumps({
                    'protein': 35,
                    'carbs': 65,
                    'fat': 25
                })
            }
        ]

    @patch('app.models.Meal.get_meals_by_user_and_date')
    def test_calculate_daily_nutrients(self, mock_get_meals):
        """Test that daily nutrient calculations are accurate"""
        # Setup mock data
        mock_get_meals.return_value = self.mock_meals
        
        # Execute
        result = calculate_daily_nutrients(self.user_id, self.test_date)
        
        # Assert
        self.assertEqual(result['total_calories'], 1100)
        self.assertEqual(result['macronutrients']['protein'], 55)
        self.assertEqual(result['macronutrients']['carbs'], 120)
        self.assertEqual(result['macronutrients']['fat'], 40)
        mock_get_meals.assert_called_once_with(self.user_id, self.test_date)

    @patch('app.services.nutrient_calculator.calculate_daily_nutrients')
    def test_calculate_nutrient_trends(self, mock_daily_nutrients):
        """Test that the nutrient trends calculation works correctly"""
        # Setup mock returns for multiple days
        mock_returns = {
            self.test_date: {'total_calories': 1100, 'macronutrients': {'protein': 55, 'carbs': 120, 'fat': 40}},
            self.test_date - timedelta(days=1): {'total_calories': 1200, 'macronutrients': {'protein': 60, 'carbs': 130, 'fat': 42}},
            self.test_date - timedelta(days=2): {'total_calories': 1050, 'macronutrients': {'protein': 52, 'carbs': 115, 'fat': 38}}
        }
        mock_daily_nutrients.side_effect = lambda user_id, day: mock_returns[day]
        
        # Execute
        start_date = self.test_date - timedelta(days=2)
        end_date = self.test_date
        result = calculate_nutrient_trends(self.user_id, start_date, end_date)
        
        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['date'], start_date)
        self.assertEqual(result[2]['date'], end_date)
        self.assertEqual(result[2]['total_calories'], 1100)
        self.assertEqual(result[1]['macronutrients']['protein'], 60)
        
        # Verify mock was called for each day
        self.assertEqual(mock_daily_nutrients.call_count, 3)


if __name__ == '__main__':
    unittest.main()