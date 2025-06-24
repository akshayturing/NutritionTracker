import pytest
from datetime import date
from unittest.mock import patch, MagicMock

from app.utils.nutrition_summary import calculate_nutrition_summary, format_nutrition_summary_response


class TestNutritionSummary:
    """Test suite for the nutrition summary utility functions"""
    
    @pytest.fixture
    def user_id(self, test_user):
        return test_user.id
    
    @pytest.fixture
    def test_date(self):
        return date.today()
    
    @pytest.fixture
    def mock_daily_nutrients(self):
        return {
            'total_calories': 1200,
            'macronutrients': {
                'protein': 65,
                'carbs': 130,
                'fat': 40
            }
        }
    
    @patch('app.models.user.User.query')
    @patch('app.utils.nutrient_calculator.calculate_daily_nutrients')
    def test_calculate_nutrition_summary_for_day(self, mock_calculate, mock_user_query, 
                                               user_id, test_date, test_user, mock_daily_nutrients):
        """Test that the nutrition summary calculation works correctly for a day"""
        # Setup mock returns
        mock_calculate.return_value = mock_daily_nutrients
        mock_user_query.get.return_value = test_user
        
        # Execute
        result = calculate_nutrition_summary(user_id, period='day', date=test_date)
        
        # Assert
        assert result['total_consumed']['calories'] == 1200
        assert result['total_consumed']['protein'] == 65
        assert result['remaining']['calories'] == 800
        assert result['remaining']['protein'] == 55
        assert result['period']['type'] == 'day'
        assert result['period']['date'] == test_date
        
        # Verify mocks were called correctly
        mock_calculate.assert_called_once_with(user_id, test_date)
        mock_user_query.get.assert_called_once_with(user_id)

    def test_format_nutrition_summary_response(self, test_date):
        """Test that the response formatter properly formats the nutrition summary"""
        # Test data
        summary = {
            'total_consumed': {
                'calories': 1200,
                'protein': 65,
                'carbs': 130,
                'fat': 40
            },
            'targets': {
                'calories': 2000,
                'protein': 120,
                'carbs': 200,
                'fat': 65
            },
            'remaining': {
                'calories': 800,
                'protein': 55,
                'carbs': 70,
                'fat': 25
            },
            'period': {
                'type': 'day',
                'date': test_date
            }
        }
        
        # Execute
        result = format_nutrition_summary_response(summary)
        
        # Assert
        assert result['status'] == 'success'
        assert result['data']['summary']['consumed']['calories'] == 1200
        assert result['data']['summary']['targets']['protein'] == 120
        assert result['data']['summary']['remaining']['carbs'] == 70
        assert result['data']['summary']['adherence_score'] == 60  # 60% of targets consumed
        assert result['data']['summary']['macronutrient_distribution']['protein_percent'] == round((65 * 4) / 1200 * 100)