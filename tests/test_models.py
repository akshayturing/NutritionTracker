# tests/test_models.py
import pytest
from datetime import datetime, date, time
from app.models import User, meal

def ghjk():
    pass
# def test_create_user(app, _db):
#     """Test creating a user and retrieving it from the database."""
#     with app.app_context():
#         # Create test user
#         user = User(name='Test User', email='test@example.com', age=30, 
#                    weight=70.5, activity_level='moderate')
#         _db.session.add(user)
#         _db.session.commit()
        
#         # Retrieve the user from the database
#         retrieved_user = User.query.filter_by(email='test@example.com').first()
        
#         # Verify user data
#         assert retrieved_user is not None
#         assert retrieved_user.name == 'Test User'
#         assert retrieved_user.age == 30
#         assert retrieved_user.weight == 70.5
#         assert retrieved_user.activity_level == 'moderate'
#         assert isinstance(retrieved_user.created_at, datetime)


# def test_create_user():
#     """Test creating a user model."""
#     import uuid
#     from app import create_app, db
#     from app.models.user import User
    
#     app = create_app()
#     with app.app_context():
#         # Create a user with a unique email
#         unique_suffix = uuid.uuid4().hex[:8]
#         user = User(
#             name='Test User',
#             email=f'test_{unique_suffix}@example.com',
#             age=30,
#             weight=70.5,
#             activity_level='moderate'
#         )
        
#         # Clear any existing session and start fresh
#         db.session.close()
        
#         db.session.add(user)
#         db.session.commit()
        
#         # Verify the user was created
#         assert user.id is not None
        
#         # Clean up
#         db.session.delete(user)
#         db.session.commit()

# def test_create_food_item(app, _db):
#     """Test creating a food item and retrieving it from the database."""
#     with app.app_context():
#         # Create test food item
#         food_item = FoodItem(
#             name='Apple',
#             brand='Organic',
#             serving_size=100,
#             serving_unit='g',
#             calories=52,
#             protein=0.3,
#             carbs=14,
#             fats=0.2,
#             fiber=2.4,
#             sugar=10.3,
#             micronutrients={"vitamin_c": 4.6, "potassium": 107}
#         )
#         _db.session.add(food_item)
#         _db.session.commit()
        
#         # Retrieve the food item from the database
#         retrieved_food = FoodItem.query.filter_by(name='Apple').first()
        
#         # Verify food item data
#         assert retrieved_food is not None
#         assert retrieved_food.calories == 52
#         assert retrieved_food.protein == 0.3
#         assert retrieved_food.micronutrients['vitamin_c'] == 4.6

# def test_create_meal_with_food_items(app, _db):
#     """Test creating a meal with food items and retrieving it from the database."""
#     with app.app_context():
#         # Create test user
#         user = User(name='Meal Test User', email='meal_test@example.com')
#         _db.session.add(user)
        
#         # Create test food items
#         apple = FoodItem(
#             name='Apple',
#             serving_size=100,
#             serving_unit='g',
#             calories=52,
#             protein=0.3,
#             carbs=14,
#             fats=0.2
#         )
#         chicken = FoodItem(
#             name='Chicken Breast',
#             serving_size=100,
#             serving_unit='g',
#             calories=165,
#             protein=31,
#             carbs=0,
#             fats=3.6
#         )
#         _db.session.add_all([apple, chicken])
#         _db.session.flush()  # Get IDs without committing
        
#         # Create a meal
#         today = date.today()
#         now = time(12, 30)
#         meal = Meal(
#             user_id=user.id,
#             meal_name='Lunch',
#             meal_date=today,
#             meal_time=now,
#             notes='Healthy lunch'
#         )
#         _db.session.add(meal)
#         _db.session.flush()
        
#         # Associate food items with the meal
#         _db.session.execute(
#             db.text(
#                 'INSERT INTO meal_food_items (meal_id, food_item_id, servings, notes) '
#                 'VALUES (:meal_id, :food_id, :servings, :notes)'
#             ),
#             {'meal_id': meal.id, 'food_id': apple.id, 'servings': 1, 'notes': 'Fresh apple'}
#         )
#         _db.session.execute(
#             db.text(
#                 'INSERT INTO meal_food_items (meal_id, food_item_id, servings, notes) '
#                 'VALUES (:meal_id, :food_id, :servings, :notes)'
#             ),
#             {'meal_id': meal.id, 'food_id': chicken.id, 'servings': 1.5, 'notes': 'Grilled'}
#         )
        
#         _db.session.commit()
        
#         # Verify the meal was created with proper associations
#         retrieved_meal = Meal.query.filter_by(user_id=user.id).first()
#         assert retrieved_meal is not None
#         assert retrieved_meal.meal_name == 'Lunch'
        
#         # Count associated food items
#         food_count = _db.session.execute(
#             db.text('SELECT COUNT(*) FROM meal_food_items WHERE meal_id = :meal_id'),
#             {'meal_id': meal.id}
#         ).scalar()
#         assert food_count == 2

# def test_create_meal_with_food_items():

#     """Test creating a meal with associated food items."""
#     from app import create_app, db
#     from app.models.user import User
#     from app.models.meal import Meal
#     from app.models.food_item import FoodItem
#     import datetime
#     import uuid
    
#     app = create_app()
#     with app.app_context():
#         # Create a user with unique email
#         unique_suffix = uuid.uuid4().hex[:8]
#         user = User(name='Meal Test', email=f'meal_test_{unique_suffix}@example.com')
#         db.session.add(user)
        
#         # Create food items
#         apple = FoodItem(name='Apple', serving_size=100, serving_unit='g', 
#                         calories=52, protein=0.3, carbs=14, fats=0.2)
#         db.session.add(apple)
#         db.session.commit()
        
#         # Create a meal - check which fields exist in your model
#         meal = Meal(
#             user_id=user.id,
#             meal_name='Test Breakfast'
#         )
        
#         # Set timestamp if it exists in the model
#         if hasattr(Meal, 'timestamp'):
#             meal.timestamp = datetime.datetime.now()
            
#         # Add the meal
#         db.session.add(meal)
#         db.session.commit()
        
#         # Verify the meal was created
#         assert meal.id is not None
        
#         # Clean up
#         db.session.delete(meal)
#         db.session.delete(apple)
#         db.session.delete(user)
#         db.session.commit()


# def test_database_constraints(app, _db):
#     """Test that database constraints are enforced."""
#     with app.app_context():
#         # Test unique email constraint
#         user1 = User(name='User One', email='same@example.com', age=30)
#         _db.session.add(user1)
#         _db.session.commit()
        
#         # Try to add another user with the same email
#         user2 = User(name='User Two', email='same@example.com', age=40)
#         _db.session.add(user2)
        
#         # Assert that committing raises an IntegrityError
#         with pytest.raises(Exception) as excinfo:
#             _db.session.commit()
        
#         # Roll back the failed transaction
#         _db.session.rollback()
        
#         # Test NOT NULL constraint on required fields
#         invalid_food = FoodItem(name='Invalid Food')  # Missing required fields
#         _db.session.add(invalid_food)
        
#         # Assert that committing raises an IntegrityError
#         with pytest.raises(Exception) as excinfo:
#             _db.session.commit()

#         # Roll back the failed transaction
#         _db.session.rollback()

# def test_database_constraints():
    """Test that database constraints are enforced."""
    import pytest
    from app import create_app, db
    from app.models.user import User
    import uuid
    
    app = create_app()
    with app.app_context():
        # Generate a unique email for this test
        unique_email = f'constraint_{uuid.uuid4().hex[:8]}@example.com'
        
        # Create a user
        user1 = User(
            name='Constraint Test',
            email=unique_email,
            age=25
        )
        db.session.add(user1)
        db.session.commit()
        
        # Try to create another user with the same email
        user2 = User(
            name='Constraint Test 2',
            email=unique_email  # Same email as user1
        )
        db.session.add(user2)
        
        # This should raise an integrity error
        with pytest.raises(Exception) as excinfo:
            db.session.commit()
        
        # Verify it's the right type of error
        assert "UNIQUE constraint failed" in str(excinfo.value) or \
               "IntegrityError" in str(excinfo.value)
        
        # Roll back the failed transaction
        db.session.rollback()
        
        # Clean up
        db.session.delete(user1)
        db.session.commit()