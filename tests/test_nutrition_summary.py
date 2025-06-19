# tests/test_nutrition_summary.py

import unittest
from datetime import datetime, timedelta
import json
from app import create_app, db
from app.models.user import User
from app.models.meal import Meal
from app.auth.jwt_callbacks import generate_token

class NutritionSummaryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        
        # Create test user with nutritional targets
        self.test_user = User(
            name="Test User",
            email="test@example.com",
            password="password123",
            calorie_goal=2000,
            protein_goal=150,
            carbs_goal=200,
            fat_goal=70
        )
        db.session.add(self.test_user)
        db.session.commit()
        
        # Generate a token for the test user
        self.auth_token = generate_token(self.test_user.id)
        
        # Create test meals
        self.create_test_meals()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def create_test_meals(self):
        """Create test meals for the current day"""
        today = datetime.utcnow()
        
        # Breakfast
        breakfast = Meal(
            user_id=self.test_user.id,
            meal_name="Breakfast",
            timestamp=today.replace(hour=8, minute=0),
            calories=350,
            protein=25,
            carbs=40,
            fat=10
        )
        
        # Lunch
        lunch = Meal(
            user_id=self.test_user.id,
            meal_name="Lunch",
            timestamp=today.replace(hour=12, minute=30),
            calories=650,
            protein=35,
            carbs=75,
            fat=18
        )
        
        db.session.add_all([breakfast, lunch])
        db.session.commit()
        
    def test_nutrition_summary_unauthorized(self):
        """Test that unauthorized requests are rejected"""
        response = self.client.get('/api/nutrition/summary')
        self.assertEqual(response.status_code, 401)
        
    def test_nutrition_summary_day(self):
        """Test getting nutrition summary for current day"""
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        response = self.client.get('/api/nutrition/summary?period=day', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Verify structure and content
        self.assertEqual(data['period_name'], 'day')
        self.assertEqual(data['consumed']['calories'], 1000)  # 350 + 650
        self.assertEqual(data['consumed']['protein'], 60)     # 25 + 35
        self.assertEqual(data['consumed']['carbs'], 115)      # 40 + 75
        self.assertEqual(data['consumed']['fat'], 28)         # 10 + 18
        self.assertEqual(data['meal_count'], 2)
        
        # Verify target percentages
        self.assertEqual(data['percentage_of_targets']['calories'], 50.0)   # 1000/2000 * 100
        self.assertEqual(data['percentage_of_targets']['protein'], 40.0)    # 60/150 * 100
        self.assertEqual(data['percentage_of_targets']['carbs'], 57.5)      # 115/200 * 100
        self.assertEqual(data['percentage_of_targets']['fat'], 40.0)        # 28/70 * 100
        
    def test_nutrition_summary_with_suggestions(self):
        """Test getting nutrition summary with meal suggestions"""
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        response = self.client.get('/api/nutrition/summary?include_suggestions=true',
                                  headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Verify meal suggestions are included
        self.assertIn('meal_suggestions', data)
        self.assertIsInstance(data['meal_suggestions'], list)
        
    def test_nutrition_summary_custom_period(self):
        """Test getting nutrition summary for custom date range"""
        # Create a meal for yesterday
        yesterday = datetime.utcnow() - timedelta(days=1)
        yesterday_meal = Meal(
            user_id=self.test_user.id,
            meal_name="Yesterday's Dinner",
            timestamp=yesterday.replace(hour=19, minute=0),
            calories=800,
            protein=40,
            carbs=60,
            fat=35
        )
        db.session.add(yesterday_meal)
        db.session.commit()
        
        # Format dates for request
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        today_str = datetime.utcnow().strftime('%Y-%m-%d')
        
        # Make request with custom date range
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        url = f'/api/nutrition/summary?period=custom&start_date={yesterday_str}&end_date={today_str}'
        response = self.client.get(url, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should include all meals (2 from today, 1 from yesterday)
        self.assertEqual(data['meal_count'], 3)
        self.assertEqual(data['consumed']['calories'], 1800)  # 350 + 650 + 800
        
    def test_nutrition_summary_invalid_period(self):
        """Test that invalid period parameter is rejected"""
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        response = self.client.get('/api/nutrition/summary?period=invalid', headers=headers)
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()