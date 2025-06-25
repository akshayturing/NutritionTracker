import unittest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User
from app.models.food import Food, UserCustomFood
from app.models.meal import Meal, MealFood
from app.models.token_blacklist import TokenBlacklist
from werkzeug.security import generate_password_hash

class BaseTestCase(unittest.TestCase):
    """Base test case for all tests"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'JWT_SECRET_KEY': 'test-key',
            'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=1),
            'JWT_REFRESH_TOKEN_EXPIRES': timedelta(days=1)
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create database tables
        db.create_all()
        
        # Setup test data
        self.setup_test_data()
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def setup_test_data(self):
        """Create initial test data"""
        # Create test user
        test_user = User(
            email='test@example.com',
            password_hash=generate_password_hash('password123'),
            name='Test User',
            age=30,
            weight=70.5,
            height=175,
            gender='male',
            activity_level='moderate',
            calorie_goal=2000,
            protein_goal=150,
            carbs_goal=200,
            fat_goal=65,
            created_at=datetime.utcnow()
        )
        db.session.add(test_user)
        db.session.commit()
        self.test_user_id = test_user.id
        
        # Create another user for permission testing
        other_user = User(
            email='other@example.com',
            password_hash=generate_password_hash('password123'),
            name='Other User',
            created_at=datetime.utcnow()
        )
        db.session.add(other_user)
        db.session.commit()
        self.other_user_id = other_user.id
        
        # Create standard food items
        self.create_standard_foods()
    
    def create_standard_foods(self):
        """Create standard food items for testing"""
        foods = [
            {
                'name': 'Apple',
                'category': 'fruits',
                'reference_portion_size': 1.0,
                'reference_portion_unit': 'medium',
                'calories': 95,
                'protein': 0.5,
                'carbohydrates': 25,
                'fat': 0.3,
                'fiber': 4.0
            },
            {
                'name': 'Chicken Breast',
                'category': 'protein',
                'reference_portion_size': 100.0,
                'reference_portion_unit': 'g',
                'calories': 165,
                'protein': 31,
                'carbohydrates': 0,
                'fat': 3.6,
                'fiber': 0
            },
            {
                'name': 'Brown Rice',
                'category': 'grains',
                'reference_portion_size': 1.0,
                'reference_portion_unit': 'cup',
                'calories': 216,
                'protein': 5,
                'carbohydrates': 45,
                'fat': 1.8,
                'fiber': 3.5
            }
        ]
        
        for food_data in foods:
            food = Food(
                name=food_data['name'],
                category=food_data['category'],
                reference_portion_size=food_data['reference_portion_size'],
                reference_portion_unit=food_data['reference_portion_unit'],
                calories=food_data['calories'],
                protein=food_data['protein'],
                carbohydrates=food_data['carbohydrates'],
                fat=food_data['fat'],
                fiber=food_data['fiber'],
                is_custom=False
            )
            db.session.add(food)
        
        db.session.commit()
        
        # Store food IDs for later use
        self.apple_id = Food.query.filter_by(name='Apple').first().id
        self.chicken_id = Food.query.filter_by(name='Chicken Breast').first().id
        self.rice_id = Food.query.filter_by(name='Brown Rice').first().id
    
    def register_user(self, email, password, name, **kwargs):
        """Helper to register a user"""
        data = {
            'email': email,
            'password': password,
            'name': name
        }
        data.update(kwargs)  # Add any additional fields
        
        return self.client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
    
    def login_user(self, email, password):
        """Helper to login and get auth tokens"""
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({'email': email, 'password': password}),
            content_type='application/json'
        )
        return response
    
    def get_auth_headers(self, email='test@example.com', password='password123'):
        """Get authentication headers for a user"""
        response = self.login_user(email, password)
        data = json.loads(response.data)
        
        return {
            'Authorization': f"Bearer {data['access_token']}",
            'Content-Type': 'application/json'
        }
    
    def create_test_meal(self, user_id, meal_name='Test Meal', meal_type='lunch'):
        """Create a test meal with food items"""
        meal = Meal(
            user_id=user_id,
            meal_name=meal_name,
            meal_type=meal_type,
            timestamp=datetime.utcnow(),
            notes='Test meal notes',
            total_calories=0,
            total_protein=0,
            total_carbohydrates=0,
            total_fat=0
        )
        db.session.add(meal)
        db.session.flush()  # Get ID but don't commit yet
        
        # Add some foods to the meal
        meal_foods = [
            MealFood(
                meal_id=meal.id,
                food_id=self.apple_id,
                portion_size=1.0,
                portion_unit='medium'
            ),
            MealFood(
                meal_id=meal.id,
                food_id=self.chicken_id,
                portion_size=150.0,
                portion_unit='g'
            )
        ]
        
        for meal_food in meal_foods:
            db.session.add(meal_food)
        
        # Calculate nutritional totals
        meal.calculate_nutrition_totals()
        db.session.commit()
        
        return meal