import pytest
from sqlalchemy import inspect, text
from datetime import datetime, date

from app import create_app
from app.models import db
from app.models.user import User
from app.models.meal import Meal
from app.models.food import FoodItem
from app.models.token_blacklist import TokenBlacklist


class TestDatabaseSchema:
    """Test suite for validating database schema integrity"""

    @pytest.fixture(scope='class')
    def inspector(self, app, db):
        """Return a SQLAlchemy inspector for examining database schema"""
        with app.app_context():
            yield inspect(db.engine)
    
    def test_all_tables_exist(self, inspector):
        """Verify all expected tables exist in the database"""
        table_names = inspector.get_table_names()
        
        # Expected tables
        expected_tables = [
            'users',
            'meals',
            'food_items',
            'token_blacklist'
        ]
        
        # Check if all expected tables are present
        for table in expected_tables:
            assert table in table_names, f"Table '{table}' is missing from the database"
    
    def test_users_table_columns(self, inspector):
        """Verify structure of users table columns"""
        columns = {col['name']: col for col in inspector.get_columns('users')}
        
        # Required columns
        assert 'id' in columns, "Users table missing 'id' column"
        assert 'email' in columns, "Users table missing 'email' column"
        assert 'name' in columns, "Users table missing 'name' column"
        assert 'password_hash' in columns, "Users table missing 'password_hash' column"
        assert 'age' in columns, "Users table missing 'age' column"
        assert 'weight' in columns, "Users table missing 'weight' column"
        assert 'activity_level' in columns, "Users table missing 'activity_level' column"
        assert 'created_at' in columns, "Users table missing 'created_at' column"
        
        # Nutritional target columns
        assert 'calorie_goal' in columns, "Users table missing 'calorie_goal' column"
        assert 'protein_goal' in columns, "Users table missing 'protein_goal' column"
        assert 'carbs_goal' in columns, "Users table missing 'carbs_goal' column"
        assert 'fat_goal' in columns, "Users table missing 'fat_goal' column"
        
        # Verify column types
        assert columns['id']['type'].compile().upper() in ('INTEGER', 'INT'), "Users 'id' column should be INTEGER type"
        assert 'VARCHAR' in columns['email']['type'].compile().upper(), "Users 'email' column should be VARCHAR type"
        assert 'VARCHAR' in columns['password_hash']['type'].compile().upper(), "Users 'password_hash' column should be VARCHAR type"
        assert any(dtype in columns['created_at']['type'].compile().upper() for dtype in ('DATETIME', 'TIMESTAMP')), \
            "Users 'created_at' column should be DATETIME type"
    
    def test_meals_table_columns(self, inspector):
        """Verify structure of meals table columns"""
        columns = {col['name']: col for col in inspector.get_columns('meals')}
        
        # Required columns
        assert 'id' in columns, "Meals table missing 'id' column"
        assert 'user_id' in columns, "Meals table missing 'user_id' column"
        assert 'meal_name' in columns, "Meals table missing 'meal_name' column"
        assert 'portion_size' in columns, "Meals table missing 'portion_size' column"
        assert 'timestamp' in columns, "Meals table missing 'timestamp' column"
        assert 'calories' in columns, "Meals table missing 'calories' column"
        assert 'macronutrients' in columns, "Meals table missing 'macronutrients' column"
        
        # Verify column types
        assert columns['id']['type'].compile().upper() in ('INTEGER', 'INT'), "Meals 'id' column should be INTEGER type"
        assert columns['user_id']['type'].compile().upper() in ('INTEGER', 'INT'), "Meals 'user_id' column should be INTEGER type"
        assert 'VARCHAR' in columns['meal_name']['type'].compile().upper(), "Meals 'meal_name' column should be VARCHAR type"
        assert any(dtype in columns['portion_size']['type'].compile().upper() for dtype in ('FLOAT', 'REAL', 'DECIMAL')), \
            "Meals 'portion_size' column should be a floating-point type"
        assert any(dtype in columns['timestamp']['type'].compile().upper() for dtype in ('DATETIME', 'TIMESTAMP')), \
            "Meals 'timestamp' column should be DATETIME type"
    
    def test_food_items_table_columns(self, inspector):
        """Verify structure of food_items table columns"""
        columns = {col['name']: col for col in inspector.get_columns('food_items')}
        
        # Required columns
        assert 'id' in columns, "FoodItems table missing 'id' column"
        assert 'name' in columns, "FoodItems table missing 'name' column"
        assert 'calories' in columns, "FoodItems table missing 'calories' column"
        assert 'serving_size' in columns, "FoodItems table missing 'serving_size' column"
        assert 'serving_unit' in columns, "FoodItems table missing 'serving_unit' column"
        assert 'protein' in columns, "FoodItems table missing 'protein' column"
        assert 'carbs' in columns, "FoodItems table missing 'carbs' column"
        assert 'fat' in columns, "FoodItems table missing 'fat' column"
        
        # Verify column types
        assert columns['id']['type'].compile().upper() in ('INTEGER', 'INT'), "FoodItems 'id' column should be INTEGER type"
        assert 'VARCHAR' in columns['name']['type'].compile().upper(), "FoodItems 'name' column should be VARCHAR type"
        assert any(dtype in columns['calories']['type'].compile().upper() for dtype in ('INTEGER', 'INT')), \
            "FoodItems 'calories' column should be INTEGER type"
        assert any(dtype in columns['protein']['type'].compile().upper() for dtype in ('FLOAT', 'REAL', 'DECIMAL')), \
            "FoodItems 'protein' column should be a floating-point type"
    
    def test_token_blacklist_table_columns(self, inspector):
        """Verify structure of token_blacklist table columns"""
        columns = {col['name']: col for col in inspector.get_columns('token_blacklist')}
        
        # Required columns
        assert 'id' in columns, "TokenBlacklist table missing 'id' column"
        assert 'token' in columns, "TokenBlacklist table missing 'token' column"
        assert 'blacklisted_on' in columns, "TokenBlacklist table missing 'blacklisted_on' column"
        
        # Verify column types
        assert columns['id']['type'].compile().upper() in ('INTEGER', 'INT'), "TokenBlacklist 'id' column should be INTEGER type"
        assert 'VARCHAR' in columns['token']['type'].compile().upper(), "TokenBlacklist 'token' column should be VARCHAR type"
        assert any(dtype in columns['blacklisted_on']['type'].compile().upper() for dtype in ('DATETIME', 'TIMESTAMP')), \
            "TokenBlacklist 'blacklisted_on' column should be DATETIME type"
    
    def test_foreign_key_constraints(self, inspector):
        """Verify all foreign key relationships are properly defined"""
        # Check meals -> users foreign key
        meal_fks = inspector.get_foreign_keys('meals')
        assert any(fk['referred_table'] == 'users' and 'user_id' in fk['constrained_columns'] for fk in meal_fks), \
            "Foreign key from meals.user_id to users.id is missing"
    
    def test_unique_constraints(self, inspector):
        """Verify unique constraints are properly defined"""
        # Check unique constraint on users.email
        unique_constraints = inspector.get_unique_constraints('users')
        assert any('email' in constraint['column_names'] for constraint in unique_constraints), \
            "Unique constraint on users.email is missing"
        
        # Check unique constraint on token_blacklist.token
        token_constraints = inspector.get_unique_constraints('token_blacklist')
        assert any('token' in constraint['column_names'] for constraint in token_constraints), \
            "Unique constraint on token_blacklist.token is missing"
    
    def test_primary_key_constraints(self, inspector):
        """Verify primary key constraints are properly defined"""
        # Check primary keys for all tables
        assert inspector.get_pk_constraint('users')['constrained_columns'] == ['id'], \
            "Primary key constraint on users.id is missing or incorrect"
        assert inspector.get_pk_constraint('meals')['constrained_columns'] == ['id'], \
            "Primary key constraint on meals.id is missing or incorrect"
        assert inspector.get_pk_constraint('food_items')['constrained_columns'] == ['id'], \
            "Primary key constraint on food_items.id is missing or incorrect" 
        assert inspector.get_pk_constraint('token_blacklist')['constrained_columns'] == ['id'], \
            "Primary key constraint on token_blacklist.id is missing or incorrect"
    
    def test_indices(self, inspector):
        """Verify necessary indices are created"""
        # Check indices on users.email
        user_indices = inspector.get_indexes('users')
        assert any('email' in index['column_names'] for index in user_indices), \
            "Index on users.email is missing"
        
        # Check indices on meals.user_id
        meal_indices = inspector.get_indexes('meals')
        assert any('user_id' in index['column_names'] for index in meal_indices), \
            "Index on meals.user_id is missing"


class TestModelRelationships:
    """Test suite for validating SQLAlchemy model relationships"""
    
    @pytest.fixture
    def db_session(self, app, db):
        """Create a clean database session for relationship testing"""
        with app.app_context():
            db.create_all()
            session = db.session
            yield session
            session.rollback()
            db.drop_all()
    
    def test_user_meal_relationship(self, db_session):
        """Test relationship between User and Meal models"""
        # Create a user
        user = User(
            email="test@example.com",
            name="Test User",
            age=30,
            weight=70,
            activity_level="moderate",
            calorie_goal=2000,
            protein_goal=120,
            carbs_goal=200,
            fat_goal=65
        )
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        # Create meals for the user
        meal1 = Meal(
            user_id=user.id,
            meal_name="Breakfast",
            portion_size=1.0,
            timestamp=datetime.now(),
            calories=450,
            macronutrients='{"protein": 20, "carbs": 55, "fat": 15}'
        )
        
        meal2 = Meal(
            user_id=user.id,
            meal_name="Lunch",
            portion_size=1.0,
            timestamp=datetime.now(),
            calories=650,
            macronutrients='{"protein": 35, "carbs": 65, "fat": 25}'
        )
        
        db_session.add_all([meal1, meal2])
        db_session.commit()
        
        # Refresh user from database to load relationships
        db_session.refresh(user)
        
        # Test relationship from User to Meal
        assert hasattr(user, 'meals'), "User model missing 'meals' relationship attribute"
        assert len(user.meals) == 2, "User.meals relationship not loading correctly"
        
        # Test relationship from Meal to User
        assert hasattr(meal1, 'user'), "Meal model missing 'user' relationship attribute"
        assert meal1.user.id == user.id, "Meal.user relationship not loading correctly"
    
    def test_cascade_delete(self, db_session):
        """Test that deleting a user cascades to related meals"""
        # Create a user with meals
        user = User(
            email="cascade@example.com",
            name="Cascade User",
            age=30,
            weight=70
        )
        db_session.add(user)
        db_session.commit()
        
        meal = Meal(
            user_id=user.id,
            meal_name="Dinner",
            portion_size=1.0,
            timestamp=datetime.now(),
            calories=800,
            macronutrients='{"protein": 40, "carbs": 80, "fat": 30}'
        )
        db_session.add(meal)
        db_session.commit()
        
        # Verify meal exists
        meal_id = meal.id
        assert db_session.query(Meal).filter_by(id=meal_id).count() == 1, "Meal not created properly"
        
        # Delete user
        db_session.delete(user)
        db_session.commit()
        
        # Verify meal was deleted
        assert db_session.query(Meal).filter_by(id=meal_id).count() == 0, "Meal not cascaded on user delete"
    
    def test_model_default_values(self, db_session):
        """Test that model default values are set correctly"""
        # Create a user with minimal fields
        user = User(
            email="defaults@example.com",
            name="Default User"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Check default values
        assert user.created_at is not None, "User.created_at default value not set"
        assert isinstance(user.created_at, datetime), "User.created_at should be a datetime object"
        
        # Create a meal with minimal fields
        meal = Meal(
            user_id=user.id,
            meal_name="Simple Meal",
            calories=400,
        )
        db_session.add(meal)
        db_session.commit()
        db_session.refresh(meal)
        
        # Check default values
        assert meal.portion_size == 1.0, "Meal.portion_size default value not set to 1.0"
        assert meal.timestamp is not None, "Meal.timestamp default value not set"
        assert isinstance(meal.timestamp, datetime), "Meal.timestamp should be a datetime object"
    
    def test_json_serialization(self, db_session):
        """Test JSON serialization and deserialization in models"""
        import json
        
        # Create meal with JSON macronutrients
        macronutrients = {
            "protein": 25,
            "carbs": 65,
            "fat": 20
        }
        
        meal = Meal(
            user_id=1,
            meal_name="JSON Test Meal",
            calories=500,
            macronutrients=json.dumps(macronutrients)
        )
        db_session.add(meal)
        db_session.commit()
        db_session.refresh(meal)
        
        # Test JSON deserialization
        loaded_macros = json.loads(meal.macronutrients)
        assert loaded_macros["protein"] == 25, "JSON deserialization failed for protein"
        assert loaded_macros["carbs"] == 65, "JSON deserialization failed for carbs"
        assert loaded_macros["fat"] == 20, "JSON deserialization failed for fat"
        
        # Test to_dict method if it exists
        if hasattr(meal, 'to_dict'):
            meal_dict = meal.to_dict()
            assert "macronutrients" in meal_dict, "to_dict() should include macronutrients"
            
            # Check if to_dict automatically deserializes JSON
            if isinstance(meal_dict["macronutrients"], dict):
                assert meal_dict["macronutrients"]["protein"] == 25, "to_dict() should deserialize macronutrients JSON"


class TestDatabaseOperations:
    """Test suite for validating database operations integrity"""
    
    @pytest.fixture
    def db_session(self, app, db):
        """Create a clean database session for operation testing"""
        with app.app_context():
            db.create_all()
            session = db.session
            yield session
            session.rollback()
            db.drop_all()
    
    def test_user_crud_operations(self, db_session):
        """Test CRUD operations for User model"""
        # Create
        user = User(
            email="crud@example.com",
            name="CRUD Test",
            age=35,
            weight=75,
            activity_level="active"
        )
        user.set_password("testpass")
        db_session.add(user)
        db_session.commit()
        
        # Read
        user_id = user.id
        db_session.expunge_all()  # Clear session to ensure fresh load
        
        loaded_user = db_session.query(User).get(user_id)
        assert loaded_user is not None, "User not found after creation"
        assert loaded_user.email == "crud@example.com", "User email incorrect after load"
        
        # Update
        loaded_user.name = "Updated Name"
        loaded_user.weight = 80
        db_session.commit()
        
        db_session.expunge_all()
        reloaded_user = db_session.query(User).get(user_id)
        assert reloaded_user.name == "Updated Name", "User name not updated"
        assert reloaded_user.weight == 80, "User weight not updated"
        
        # Delete
        db_session.delete(reloaded_user)
        db_session.commit()
        
        assert db_session.query(User).get(user_id) is None, "User not deleted properly"
    
    def test_integrity_constraints(self, db_session):
        """Test database integrity constraints"""
        # Test email uniqueness
        user1 = User(email="unique@example.com", name="First User")
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(email="unique@example.com", name="Second User")
        db_session.add(user2)
        
        # Should raise an integrity error for duplicate email
        with pytest.raises(Exception) as excinfo:
            db_session.commit()
        
        assert any(term in str(excinfo.value).lower() for term in ["unique", "duplicate", "integrity"]), \
            "Email uniqueness constraint not enforced"
        
        db_session.rollback()
        
        # Test foreign key constraints
        invalid_meal = Meal(
            user_id=999999,  # Non-existent user ID
            meal_name="Invalid Meal",
            calories=500
        )
        db_session.add(invalid_meal)
        
        # Should raise an integrity error for invalid foreign key
        with pytest.raises(Exception) as excinfo:
            db_session.commit()
        
        assert any(term in str(excinfo.value).lower() for term in ["foreign key", "constraint", "integrity"]), \
            "Foreign key constraint not enforced"
        
        db_session.rollback()
    
    def test_non_nullable_constraints(self, db_session):
        """Test non-nullable constraints"""
        # Try creating a user without required fields
        user = User()  # Missing required fields
        db_session.add(user)
        
        # Should raise an error for null values in non-nullable columns
        with pytest.raises(Exception) as excinfo:
            db_session.commit()
        
        assert any(term in str(excinfo.value).lower() for term in ["null", "not null", "constraint"]), \
            "Non-nullable constraint not enforced"
        
        db_session.rollback()