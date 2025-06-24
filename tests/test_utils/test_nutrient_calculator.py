import pytest
from datetime import date, datetime, timedelta
import json
from unittest.mock import patch, MagicMock

from app.utils.nutrient_calculator import calculate_daily_nutrients, calculate_nutrient_trends


class TestNutrientCalculator:
    """Test suite for the nutrient calculator utility functions"""
    
    @pytest.fixture
    def user_id(self, test_user):
        return test_user.id
    
    @pytest.fixture
    def test_date(self):
        return date.today()
    
    @patch('app.models.meal.Meal.get_meals_by_user_and_date')
    def test_calculate_daily_nutrients(self, mock_get_meals, user_id, test_date, test_meals):
        """Test that daily nutrient calculations are accurate"""
        # Setup mock data
        mock_get_meals.return_value = test_meals
        
        # Execute
        result = calculate_daily_nutrients(user_id, test_date)
        
        # Assert
        assert result['total_calories'] == 1100
        assert result['macronutrients']['protein'] == 55
        assert result['macronutrients']['carbs'] == 120
        assert result['macronutrients']['fat'] == 40
        mock_get_meals.assert_called_once_with(user_id, test_date)

    @patch('app.utils.nutrient_calculator.calculate_daily_nutrients')
    def test_calculate_nutrient_trends(self, mock_daily_nutrients, user_id, test_date):
        """Test that the nutrient trends calculation works correctly"""
        # Setup mock returns for multiple days
        mock_returns = {
            test_date: {'total_calories': 1100, 'macronutrients': {'protein': 55, 'carbs': 120, 'fat': 40}},
            test_date - timedelta(days=1): {'total_calories': 1200, 'macronutrients': {'protein': 60, 'carbs': 130, 'fat': 42}},
            test_date - timedelta(days=2): {'total_calories': 1050, 'macronutrients': {'protein': 52, 'carbs': 115, 'fat': 38}}
        }
        mock_daily_nutrients.side_effect = lambda user_id, day: mock_returns[day]
        
        # Execute
        start_date = test_date - timedelta(days=2)
        end_date = test_date
        result = calculate_nutrient_trends(user_id, start_date, end_date)
        
        # Assert
        assert len(result) == 3
        assert result[0]['date'] == start_date
        assert result[2]['date'] == end_date
        assert result[2]['total_calories'] == 1100
        assert result[1]['macronutrients']['protein'] == 60
        
        # Verify mock was called for each day
        assert mock_daily_nutrients.call_count == 3