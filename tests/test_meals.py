import json
from datetime import datetime, timedelta
from tests.base_test import BaseTestCase
from app.models.meal import Meal, MealFood

class MealTestCase(BaseTestCase):
    """Test cases for meal endpoints"""
    
    def test_get_all_meals(self):
        """Test listing all meals for a user"""
        # Create some test meals
        meal1 = self.create_test_meal(self.test_user_id, 'Breakfast', 'breakfast')
        meal2 = self.create_test_meal(self.test_user_id, 'Lunch', 'lunch')
        
        headers = self.get_auth_headers()
        
        response = self.client.get(
            '/api/meals',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('meals', data)
        self.assertIn('pagination', data)
        self.assertEqual(len(data['meals']), 2)
    
    def test_get_meal_by_id(self):
        """Test getting a specific meal by ID"""
        meal = self.create_test_meal(self.test_user_id)
        
        headers = self.get_auth_headers()
        
        response = self.client.get(
            f'/api/meals/{meal.id}',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['meal_name'], 'Test Meal')
        self.assertEqual(data['meal_type'], 'lunch')
        self.assertIn('foods', data)
        self.assertEqual(len(data['foods']), 2)  # Should have two food items
    
    def test_get_other_users_meal(self):
        """Test attempting to access another user's meal"""
        # Create meal for other_user
        meal = self.create_test_meal(self.other_user_id)
        
        # Try to access as test_user
        headers = self.get_auth_headers()
        
        response = self.client.get(
            f'/api/meals/{meal.id}',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_create_meal(self):
        """Test creating a new meal"""
        headers = self.get_auth_headers()
        
        meal_data = {
            'meal_name': 'Dinner',
            'meal_type': 'dinner',
            'timestamp': (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            'notes': 'Test dinner notes',
            'foods': [
                {
                    'food_id': self.rice_id,
                    'portion_size': 1.5,
                    'portion_unit': 'cup'
                },
                {
                    'food_id': self.chicken_id,
                    'portion_size': 200,
                    'portion_unit': 'g'
                }
            ]
        }
        
        response = self.client.post(
            '/api/meals',
            data=json.dumps(meal_data),
            headers=headers
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('meal_id', data)
        self.assertEqual(data['meal_name'], 'Dinner')
        
        # Verify meal was created
        meal = Meal.query.get(data['meal_id'])
        self.assertIsNotNone(meal)
        self.assertEqual(meal.meal_name, 'Dinner')
        self.assertEqual(meal.user_id, self.test_user_id)
        
        # Verify meal-food relationships
        meal_foods = MealFood.query.filter_by(meal_id=meal.id).all()
        self.assertEqual(len(meal_foods), 2)
    
    def test_create_meal_validation(self):
        """Test meal creation with invalid data"""
        headers = self.get_auth_headers()
        
        # Missing required fields
        invalid_meal = {
            'meal_type': 'dinner',
            # Missing meal_name
            'foods': []
        }
        
        response = self.client.post(
            '/api/meals',
            data=json.dumps(invalid_meal),
            headers=headers
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error']['code'], 'VALIDATION_ERROR')
    
    def test_update_meal(self):
        """Test updating an existing meal"""
        meal = self.create_test_meal(self.test_user_id)
        
        headers = self.get_auth_headers()
        
        # Update meal data
        update_data = {
            'meal_name': 'Updated Meal Name',
            'notes': 'Updated notes',
            'foods': [
                {
                    'food_id': self.rice_id,
                    'portion_size': 2.0,
                    'portion_unit': 'cup'
                }
            ]
        }
        
        response = self.client.put(
            f'/api/meals/{meal.id}',
            data=json.dumps(update_data),
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Meal updated successfully')
        
        # Verify meal was updated
        updated_meal = Meal.query.get(meal.id)
        self.assertEqual(updated_meal.meal_name, 'Updated Meal Name')
        self.assertEqual(updated_meal.notes, 'Updated notes')
        
        # Verify meal foods were updated
        meal_foods = MealFood.query.filter_by(meal_id=meal.id).all()
        self.assertEqual(len(meal_foods), 1)  # Should now have only 1 food
        self.assertEqual(meal_foods[0].food_id, self.rice_id)
    
    def test_update_other_users_meal(self):
        """Test attempting to update another user's meal"""
        meal = self.create_test_meal(self.other_user_id)
        
        headers = self.get_auth_headers()
        
        update_data = {
            'meal_name': 'Hacked Meal'
        }
        
        response = self.client.put(
            f'/api/meals/{meal.id}',
            data=json.dumps(update_data),
            headers=headers
        )
        
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_delete_meal(self):
        """Test deleting a meal"""
        meal = self.create_test_meal(self.test_user_id)
        
        headers = self.get_auth_headers()
        
        response = self.client.delete(
            f'/api/meals/{meal.id}',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify meal was deleted
        meal = Meal.query.get(meal.id)
        self.assertIsNone(meal)
        
        # Verify associated food items were also deleted
        meal_foods = MealFood.query.filter_by(meal_id=meal.id).all()
        self.assertEqual(len(meal_foods), 0)
    
    def test_filter_meals_by_date(self):
        """Test filtering meals by date"""
        # Create meals with different dates
        today = datetime.utcnow()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        # Create a meal for yesterday
        yesterday_meal = Meal(
            user_id=self.test_user_id,
            meal_name='Yesterday Meal',
            meal_type='breakfast',
            timestamp=yesterday,
            notes='Yesterday test meal'
        )
        db.session.add(yesterday_meal)
        
        # Create a meal for today
        today_meal = Meal(
            user_id=self.test_user_id,
            meal_name='Today Meal',
            meal_type='lunch',
            timestamp=today,
            notes='Today test meal'
        )
        db.session.add(today_meal)
        
        # Create a meal for tomorrow
        tomorrow_meal = Meal(
            user_id=self.test_user_id,
            meal_name='Tomorrow Meal',
            meal_type='dinner',
            timestamp=tomorrow,
            notes='Tomorrow test meal'
        )
        db.session.add(tomorrow_meal)
        
        db.session.commit()
        
        headers = self.get_auth_headers()
        
        # Filter by yesterday's date
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        response = self.client.get(
            f'/api/meals?date={yesterday_str}',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['meals']), 1)
        self.assertEqual(data['meals'][0]['meal_name'], 'Yesterday Meal')
    
    def test_filter_meals_by_type(self):
        """Test filtering meals by meal type"""
        # Create meals with different types
        breakfast = Meal(
            user_id=self.test_user_id,
            meal_name='Breakfast',
            meal_type='breakfast',
            timestamp=datetime.utcnow(),
            notes='Breakfast test meal'
        )
        db.session.add(breakfast)
        
        lunch = Meal(
            user_id=self.test_user_id,
            meal_name='Lunch',
            meal_type='lunch',
            timestamp=datetime.utcnow(),
            notes='Lunch test meal'
        )
        db.session.add(lunch)
        
        db.session.commit()
        
        headers = self.get_auth_headers()
        
        # Filter by breakfast
        response = self.client.get(
            '/api/meals?meal_type=breakfast',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['meals']), 1)
        self.assertEqual(data['meals'][0]['meal_type'], 'breakfast')
    
    def test_pagination(self):
        """Test meal pagination"""
        # Create multiple meals
        for i in range(15):  # Create 15 meals
            meal = Meal(
                user_id=self.test_user_id,
                meal_name=f'Meal {i+1}',
                meal_type='snack',
                timestamp=datetime.utcnow() - timedelta(hours=i),
                notes=f'Pagination test meal {i+1}'
            )
            db.session.add(meal)
        
        db.session.commit()
        
        headers = self.get_auth_headers()
        
        # First page (default 10 items)
        response = self.client.get(
            '/api/meals',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['meals']), 10)
        self.assertEqual(data['pagination']['current_page'], 1)
        self.assertGreaterEqual(data['pagination']['total_pages'], 2)
        
        # Second page
        response = self.client.get(
            '/api/meals?page=2',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data['meals']), 5)  # At least 5 more items
        self.assertEqual(data['pagination']['current_page'], 2)