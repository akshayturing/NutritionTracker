import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User
from app.models.meal import Meal
from app.utils.nutrient_calculator import calculate_daily_nutrients

class NutrientCalculatorTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user with nutritional goals
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
        
        # Create test date variables
        self.today = datetime.utcnow().replace(hour=12, minute=0, second=0)
        self.yesterday = self.today - timedelta(days=1)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_empty_day_calculation(self):
        """Test calculation when no meals exist for the day"""
        result = calculate_daily_nutrients(self.test_user.id, self.today)
        
        self.assertEqual(result['total_meals'], 0)
        self.assertEqual(result['nutrients']['calories']['consumed'], 0)
        self.assertEqual(result['nutrients']['protein']['consumed'], 0)
        self.assertEqual(result['nutrients']['carbs']['consumed'], 0)
        self.assertEqual(result['nutrients']['fat']['consumed'], 0)
        
    def test_multiple_meals_calculation(self):
        """Test calculation with multiple meals in a day"""
        # Add breakfast
        breakfast = Meal(
            user_id=self.test_user.id,
            meal_name="Breakfast",
            timestamp=self.today.replace(hour=8),
            calories=500,
            protein=30,
            carbs=60,
            fat=15
        )
        
        # Add lunch
        lunch = Meal(
            user_id=self.test_user.id,
            meal_name="Lunch",
            timestamp=self.today.replace(hour=13),
            calories=700,
            protein=40,
            carbs=80,
            fat=20
        )
        
        # Add dinner
        dinner = Meal(
            user_id=self.test_user.id,
            meal_name="Dinner",
            timestamp=self.today.replace(hour=19),
            calories=800,
            protein=45,
            carbs=70,
            fat=25
        )
        
        db.session.add_all([breakfast, lunch, dinner])
        db.session.commit()
        
        result = calculate_daily_nutrients(self.test_user.id, self.today)
        
        # Check totals
        self.assertEqual(result['total_meals'], 3)
        self.assertEqual(result['nutrients']['calories']['consumed'], 2000)  # 500 + 700 + 800
        self.assertEqual(result['nutrients']['protein']['consumed'], 115)   # 30 + 40 + 45
        self.assertEqual(result['nutrients']['carbs']['consumed'], 210)     # 60 + 80 + 70
        self.assertEqual(result['nutrients']['fat']['consumed'], 60)        # 15 + 20 + 25
        
        # Check percentages
        self.assertEqual(result['nutrients']['calories']['percentage'], 100.0)  # 2000/2000 = 100%
        self.assertEqual(result['nutrients']['protein']['percentage'], 76.7)    # 115/150 = 76.7%
        self.assertEqual(result['nutrients']['carbs']['percentage'], 105.0)     # 210/200 = 105%
        self.assertEqual(result['nutrients']['fat']['percentage'], 85.7)        # 60/70 = 85.7%
        
    def test_date_filtering(self):
        """Test that only meals from the specified day are included"""
        # Add meal for today
        today_meal = Meal(
            user_id=self.test_user.id,
            meal_name="Today's Meal",
            timestamp=self.today,
            calories=500,
            protein=30,
            carbs=60,
            fat=15
        )
        
        # Add meal for yesterday
        yesterday_meal = Meal(
            user_id=self.test_user.id,
            meal_name="Yesterday's Meal",
            timestamp=self.yesterday,
            calories=600,
            protein=35,
            carbs=70,
            fat=20
        )
        
        db.session.add_all([today_meal, yesterday_meal])
        db.session.commit()
        
        # Test today's calculation
        today_result = calculate_daily_nutrients(self.test_user.id, self.today)
        self.assertEqual(today_result['total_meals'], 1)
        self.assertEqual(today_result['nutrients']['calories']['consumed'], 500)
        
        # Test yesterday's calculation
        yesterday_result = calculate_daily_nutrients(self.test_user.id, self.yesterday)
        self.assertEqual(yesterday_result['total_meals'], 1)
        self.assertEqual(yesterday_result['nutrients']['calories']['consumed'], 600)

if __name__ == '__main__':
    unittest.main()