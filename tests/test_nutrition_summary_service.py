# # # tests/test_nutrition_summary.py

# # import unittest
# # from datetime import datetime, timedelta
# # import json
# # from app import create_app, db
# # from app.models.user import User
# # from app.models.meal import Meal
# # from app.auth.jwt_callbacks import generate_token


# # import unittest
# # from datetime import datetime, timedelta
# # import json
# # from app import create_app, db
# # from app.models.user import User
# # from app.models.meal import Meal
# # from app.auth.jwt_callbacks import generate_token

# # class NutritionSummaryTestCase(unittest.TestCase):
# #     def setUp(self):
# #         self.app = create_app('testing')  # This should now work correctly
# #         self.app_context = self.app.app_context()
# #         self.app_context.push()
# #         self.client = self.app.test_client()
# #         db.create_all()
        
# #         # Create test user with nutritional targets
# #         self.test_user = User(
# #             name="Test User",
# #             email="test@example.com",
# #             password="password123",
# #             calorie_goal=2000,
# #             protein_goal=150,
# #             carbs_goal=200,
# #             fat_goal=70
# #         )
# #         db.session.add(self.test_user)
# #         db.session.commit()
        
# #         # Generate a token for the test user
# #         self.auth_token = generate_token(self.test_user.id)
        
# #         # Create test meals
# #         self.create_test_meals()
        
# #     def tearDown(self):
# #         db.session.remove()
# #         db.drop_all()
# #         self.app_context.pop()
        
# #     def create_test_meals(self):
# #         """Create test meals for the current day"""
# #         today = datetime.utcnow()
        
# #         # Breakfast
# #         breakfast = Meal(
# #             user_id=self.test_user.id,
# #             meal_name="Breakfast",
# #             timestamp=today.replace(hour=8, minute=0),
# #             calories=350,
# #             protein=25,
# #             carbs=40,
# #             fat=10
# #         )
        
# #         # Lunch
# #         lunch = Meal(
# #             user_id=self.test_user.id,
# #             meal_name="Lunch",
# #             timestamp=today.replace(hour=12, minute=30),
# #             calories=650,
# #             protein=35,
# #             carbs=75,
# #             fat=18
# #         )
        
# #         db.session.add_all([breakfast, lunch])
# #         db.session.commit()
        
# #     def test_nutrition_summary_unauthorized(self):
# #         """Test that unauthorized requests are rejected"""
# #         response = self.client.get('/api/nutrition/summary')
# #         self.assertEqual(response.status_code, 401)
        
# #     def test_nutrition_summary_day(self):
# #         """Test getting nutrition summary for current day"""
# #         headers = {'Authorization': f'Bearer {self.auth_token}'}
# #         response = self.client.get('/api/nutrition/summary?period=day', headers=headers)
        
# #         self.assertEqual(response.status_code, 200)
# #         data = json.loads(response.data)
        
# #         # Verify structure and content
# #         self.assertEqual(data['period_name'], 'day')
# #         self.assertEqual(data['consumed']['calories'], 1000)  # 350 + 650
# #         self.assertEqual(data['consumed']['protein'], 60)     # 25 + 35
# #         self.assertEqual(data['consumed']['carbs'], 115)      # 40 + 75
# #         self.assertEqual(data['consumed']['fat'], 28)         # 10 + 18
# #         self.assertEqual(data['meal_count'], 2)
        
# #         # Verify target percentages
# #         self.assertEqual(data['percentage_of_targets']['calories'], 50.0)   # 1000/2000 * 100
# #         self.assertEqual(data['percentage_of_targets']['protein'], 40.0)    # 60/150 * 100
# #         self.assertEqual(data['percentage_of_targets']['carbs'], 57.5)      # 115/200 * 100
# #         self.assertEqual(data['percentage_of_targets']['fat'], 40.0)        # 28/70 * 100
        
# #     def test_nutrition_summary_with_suggestions(self):
# #         """Test getting nutrition summary with meal suggestions"""
# #         headers = {'Authorization': f'Bearer {self.auth_token}'}
# #         response = self.client.get('/api/nutrition/summary?include_suggestions=true',
# #                                   headers=headers)
        
# #         self.assertEqual(response.status_code, 200)
# #         data = json.loads(response.data)
        
# #         # Verify meal suggestions are included
# #         self.assertIn('meal_suggestions', data)
# #         self.assertIsInstance(data['meal_suggestions'], list)
        
# #     def test_nutrition_summary_custom_period(self):
# #         """Test getting nutrition summary for custom date range"""
# #         # Create a meal for yesterday
# #         yesterday = datetime.utcnow() - timedelta(days=1)
# #         yesterday_meal = Meal(
# #             user_id=self.test_user.id,
# #             meal_name="Yesterday's Dinner",
# #             timestamp=yesterday.replace(hour=19, minute=0),
# #             calories=800,
# #             protein=40,
# #             carbs=60,
# #             fat=35
# #         )
# #         db.session.add(yesterday_meal)
# #         db.session.commit()
        
# #         # Format dates for request
# #         yesterday_str = yesterday.strftime('%Y-%m-%d')
# #         today_str = datetime.utcnow().strftime('%Y-%m-%d')
        
# #         # Make request with custom date range
# #         headers = {'Authorization': f'Bearer {self.auth_token}'}
# #         url = f'/api/nutrition/summary?period=custom&start_date={yesterday_str}&end_date={today_str}'
# #         response = self.client.get(url, headers=headers)
        
# #         self.assertEqual(response.status_code, 200)
# #         data = json.loads(response.data)
        
# #         # Should include all meals (2 from today, 1 from yesterday)
# #         self.assertEqual(data['meal_count'], 3)
# #         self.assertEqual(data['consumed']['calories'], 1800)  # 350 + 650 + 800
        
# #     def test_nutrition_summary_invalid_period(self):
# #         """Test that invalid period parameter is rejected"""
# #         headers = {'Authorization': f'Bearer {self.auth_token}'}
# #         response = self.client.get('/api/nutrition/summary?period=invalid', headers=headers)
        
# #         self.assertEqual(response.status_code, 400)
# #         data = json.loads(response.data)
# #         self.assertIn('error', data)

# # if __name__ == '__main__':
# #     unittest.main()

# import json
# from datetime import datetime, timedelta
# from tests.base_test import BaseTestCase
# from app.models.user import User
# from app.models.meal import Meal, MealFood

# class NutritionSummaryTestCase(BaseTestCase):
#     """Test cases for nutrition summary endpoints"""
    
#     def setUp(self):
#         """Set up test environment with nutritional data"""
#         super().setUp()
        
#         # Create a full day of meals for the user
#         self.create_day_of_meals()
    
#     def create_day_of_meals(self):
#         """Create a set of meals for a full day with known nutritional values"""
#         today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
#         # Breakfast - Apple and Chicken Breast
#         breakfast = Meal(
#             user_id=self.test_user_id,
#             meal_name='Breakfast',
#             meal_type='breakfast',
#             timestamp=today + timedelta(hours=8),
#             notes='Breakfast meal'
#         )
#         db.session.add(breakfast)
#         db.session.flush()
        
#         breakfast_foods = [
#             MealFood(
#                 meal_id=breakfast.id,
#                 food_id=self.apple_id,
#                 portion_size=1.0,
#                 portion_unit='medium'
#             ),
#             MealFood(
#                 meal_id=breakfast.id,
#                 food_id=self.chicken_id,
#                 portion_size=100.0,
#                 portion_unit='g'
#             )
#         ]
        
#         for food in breakfast_foods:
#             db.session.add(food)
        
#         breakfast.calculate_nutrition_totals()
        
#         # Lunch - Rice and more Chicken
#         lunch = Meal(
#             user_id=self.test_user_id,
#             meal_name='Lunch',
#             meal_type='lunch',
#             timestamp=today + timedelta(hours=13),
#             notes='Lunch meal'
#         )
#         db.session.add(lunch)
#         db.session.flush()
        
#         lunch_foods = [
#             MealFood(
#                 meal_id=lunch.id,
#                 food_id=self.rice_id,
#                 portion_size=1.0,
#                 portion_unit='cup'
#             ),
#             MealFood(
#                 meal_id=lunch.id,
#                 food_id=self.chicken_id,
#                 portion_size=150.0,
#                 portion_unit='g'
#             )
#         ]
        
#         for food in lunch_foods:
#             db.session.add(food)
        
#         lunch.calculate_nutrition_totals()
        
#         # Dinner - Rice, Chicken, and Apple
#         dinner = Meal(
#             user_id=self.test_user_id,
#             meal_name='Dinner',
#             meal_type='dinner',
#             timestamp=today + timedelta(hours=19),
#             notes='Dinner meal'
#         )
#         db.session.add(dinner)
#         db.session.flush()
        
#         dinner_foods = [
#             MealFood(
#                 meal_id=dinner.id,
#                 food_id=self.rice_id,
#                 portion_size=1.5,
#                 portion_unit='cup'
#             ),
#             MealFood(
#                 meal_id=dinner.id,
#                 food_id=self.chicken_id,
#                 portion_size=200.0,
#                 portion_unit='g'
#             ),
#             MealFood(
#                 meal_id=dinner.id,
#                 food_id=self.apple_id,
#                 portion_size=1.0,
#                 portion_unit='medium'
#             )
#         ]
        
#         for food in dinner_foods:
#             db.session.add(food)
        
#         dinner.calculate_nutrition_totals()
        
#         # Create some meals for yesterday and tomorrow too
#         yesterday = today - timedelta(days=1)
#         yesterday_meal = Meal(
#             user_id=self.test_user_id,
#             meal_name='Yesterday Meal',
#             meal_type='dinner',
#             timestamp=yesterday + timedelta(hours=19),
#             notes='Yesterday meal'
#         )
#         db.session.add(yesterday_meal)
        
#         tomorrow = today + timedelta(days=1)
#         tomorrow_meal = Meal(
#             user_id=self.test_user_id,
#             meal_name='Tomorrow Meal',
#             meal_type='breakfast',
#             timestamp=tomorrow + timedelta(hours=8),
#             notes='Tomorrow meal'
#         )
#         db.session.add(tomorrow_meal)
        
#         db.session.commit()
    
#     def test_daily_nutrition_summary(self):
#         """Test getting daily nutrition summary"""
#         headers = self.get_auth_headers()
        
#         # Get summary for today
#         today = datetime.utcnow().strftime('%Y-%m-%d')
#         response = self.client.get(
#             f'/api/nutrition/summary/daily?date={today}',
#             headers=headers
#         )
        
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
        
#         # Check if the structure is correct
#         self.assertIn('date', data)
#         self.assertIn('meals_count', data)
#         self.assertIn('total_intake', data)
#         self.assertIn('targets', data)
#         self.assertIn('remaining', data)
#         self.assertIn('percentage_achieved', data)
        
#         # We should have 3 meals today
#         self.assertEqual(data['meals_count'], 3)
        
#         # Check if nutritional totals are calculated
#         total_intake = data['total_intake']
#         self.assertIn('calories', total_intake)
#         self.assertIn('protein', total_intake)
#         self.assertIn('carbohydrates', total_intake)
#         self.assertIn('fat', total_intake)
        
#         # Calories should be the sum from all meals
#         self.assertGreater(total_intake['calories'], 0)
        
#         # Check if targets match user's goals
#         targets = data['targets']
#         user = User.query.get(self.test_user_id)
#         self.assertEqual(targets['calories'], user.calorie_goal)
#         self.assertEqual(targets['protein'], user.protein_goal)
    
#     def test_weekly_nutrition_summary(self):
#         """Test getting weekly nutrition summary"""
#         headers = self.get_auth_headers()
        
#         # Get weekly summary
#         response = self.client.get(
#             '/api/nutrition/summary/weekly',
#             headers=headers
#         )
        
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
        
#         # Check structure
#         self.assertIn('period', data)
#         self.assertEqual(data['period'], 'weekly')
#         self.assertIn('start_date', data)
#         self.assertIn('end_date', data)
#         self.assertIn('daily_summaries', data)
#         self.assertIn('average_intake', data)
        
#         # We should have some daily data
#         self.assertGreaterEqual(len(data['daily_summaries']), 1)
        
#         # Average intake should be calculated
#         avg_intake = data['average_intake']
#         self.assertIn('calories', avg_intake)
#         self.assertGreater(avg_intake['calories'], 0)
    
#     def test_custom_date_range_summary(self):
#         """Test getting custom date range nutrition summary"""
#         headers = self.get_auth_headers()
        
#         # Get custom date range summary
#         today = datetime.utcnow()
#         start_date = (today - timedelta(days=3)).strftime('%Y-%m-%d')
#         end_date = today.strftime('%Y-%m-%d')
        
#         response = self.client.get(
#             f'/api/nutrition/summary/custom?start_date={start_date}&end_date={end_date}',
#             headers=headers
#         )
        
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
        
#         # Check structure
#         self.assertIn('period', data)
#         self.assertEqual(data['period'], 'custom')
#         self.assertIn('start_date', data)
#         self.assertIn('end_date', data)
#         self.assertIn('daily_summaries', data)
        
#         # Start and end dates should match what we requested
#         self.assertEqual(data['start_date'], start_date)
#         self.assertEqual(data['end_date'], end_date)
        
#         # We should have summary data for 3-4 days
#         self.assertGreaterEqual(len(data['daily_summaries']), 1)
    
#     def test_invalid_date_format(self):
#         """Test submitting an invalid date format"""
#         headers = self.get_auth_headers()
        
#         response = self.client.get(
#             '/api/nutrition/summary/daily?date=invalid-date',
#             headers=headers
#         )
        
#         self.assertEqual(response.status_code, 400)
#         data = json.loads(response.data)
#         self.assertIn('error', data)
#         self.assertEqual(data['error']['code'], 'VALIDATION_ERROR')

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, date, timedelta
import json

from app.services.nutrition_summary import calculate_nutrition_summary, format_nutrition_summary_response

class NutritionSummaryServiceTests(unittest.TestCase):
    """Test suite for the nutrition summary service layer"""
    
    def setUp(self):
        """Set up test data"""
        self.user_id = 1
        self.test_date = date.today()
        
        # Mock user with nutritional targets
        self.mock_user = MagicMock()
        self.mock_user.id = self.user_id
        self.mock_user.calorie_goal = 2000
        self.mock_user.protein_goal = 120
        self.mock_user.carbs_goal = 200
        self.mock_user.fat_goal = 65
        
        # Mock daily nutrients data
        self.mock_daily_nutrients = {
            'total_calories': 1200,
            'macronutrients': {
                'protein': 65,
                'carbs': 130,
                'fat': 40
            }
        }

    @patch('app.models.User.query')
    @patch('app.services.nutrient_calculator.calculate_daily_nutrients')
    def test_calculate_nutrition_summary_for_day(self, mock_calculate, mock_user_query):
        """Test that the nutrition summary calculation works correctly for a day"""
        # Setup mock returns
        mock_calculate.return_value = self.mock_daily_nutrients
        mock_user_query.get.return_value = self.mock_user
        
        # Execute
        result = calculate_nutrition_summary(self.user_id, period='day', date=self.test_date)
        
        # Assert
        self.assertEqual(result['total_consumed']['calories'], 1200)
        self.assertEqual(result['total_consumed']['protein'], 65)
        self.assertEqual(result['remaining']['calories'], 800)
        self.assertEqual(result['remaining']['protein'], 55)
        self.assertEqual(result['period']['type'], 'day')
        self.assertEqual(result['period']['date'], self.test_date)
        
        # Verify mocks were called correctly
        mock_calculate.assert_called_once_with(self.user_id, self.test_date)
        mock_user_query.get.assert_called_once_with(self.user_id)

    def test_format_nutrition_summary_response(self):
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
                'date': self.test_date
            }
        }
        
        # Execute
        result = format_nutrition_summary_response(summary)
        
        # Assert
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['data']['summary']['consumed']['calories'], 1200)
        self.assertEqual(result['data']['summary']['targets']['protein'], 120)
        self.assertEqual(result['data']['summary']['remaining']['carbs'], 70)
        self.assertEqual(result['data']['summary']['adherence_score'], 60)  # 60% of targets consumed
        self.assertEqual(result['data']['summary']['macronutrient_distribution']['protein_percent'], round((65 * 4) / 1200 * 100))


if __name__ == '__main__':
    unittest.main()