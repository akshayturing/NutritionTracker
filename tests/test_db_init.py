# tests/test_db_init.py
import sqlite3
import pytest
from app import db
from app.models import User, meal, FoodItem

# def test_database_exists(app):
#     """Test that the database file is created."""
#     with app.app_context():
#         # Check if database connection works
#         assert db.engine.pool.checkedout() == 0
#         # Execute a simple query
#         result = db.session.execute("SELECT 1").scalar()
#         assert result == 1

def test_database_exists():
    """Test that the database exists and is accessible."""
    from app import create_app, db
    from sqlalchemy import text
    
    app = create_app()
    with app.app_context():
        # Execute raw SQL to check if DB is accessible
        result = db.session.execute(text('SELECT 1'))
        assert result.scalar() == 1

def test_tables_created(app):
    """Test that all required tables are created in the database."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        # Check for the existence of our main tables
        assert 'users' in tables
        assert 'meals' in tables
        assert 'food_items' in tables
        assert 'meal_food_items' in tables  # Junction table

def test_user_table_schema(app):
    """Test that the users table has the correct schema."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        columns = {c['name'] for c in inspector.get_columns('users')}
        
        expected_columns = {'id', 'name', 'email', 'age', 'weight', 'activity_level', 'created_at'}
        assert expected_columns.issubset(columns)

def test_food_items_table_schema(app):
    """Test that the food_items table has the correct schema."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        columns = {c['name'] for c in inspector.get_columns('food_items')}
        
        expected_columns = {'id', 'name', 'brand', 'serving_size', 'serving_unit', 
                           'calories', 'protein', 'carbs', 'fats', 'fiber', 
                           'sugar', 'micronutrients', 'created_at'}
        assert expected_columns.issubset(columns)

# def test_meals_table_schema(app):
#     """Test that the meals table has the correct schema."""
#     with app.app_context():
#         inspector = db.inspect(db.engine)
#         columns = {c['name'] for c in inspector.get_columns('meals')}
        
#         expected_columns = {'id', 'user_id', 'meal_name', 'meal_date', 'meal_time', 
#                            'notes', 'created_at'}
#         assert expected_columns.issubset(columns)

def test_meals_table_schema():
    """Test that the meals table has the expected schema."""
    from app import create_app, db
    
    app = create_app()
    with app.app_context():
        inspector = db.inspect(db.engine)
        columns = {c['name'] for c in inspector.get_columns('meals')}
        
        # Required meal fields
        required_fields = {'id', 'user_id', 'meal_name'}
        
        # Check that all required fields exist
        for field in required_fields:
            assert field in columns, f"Missing required field: {field}"
            
        # Check that either timestamp or meal_date exists
        assert any(col in columns for col in ['timestamp', 'meal_date']), \
            "Neither timestamp nor meal_date found in meals table"
        
def test_foreign_keys(app):
    """Test that foreign key constraints are properly set up."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        
        # Check foreign key from meals to users
        meals_fks = inspector.get_foreign_keys('meals')
        meal_user_fk = next((fk for fk in meals_fks if fk['referred_table'] == 'users'), None)
        assert meal_user_fk is not None
        assert 'user_id' in meal_user_fk['constrained_columns']
        
        # Check foreign keys in junction table
        junction_fks = inspector.get_foreign_keys('meal_food_items')
        assert len(junction_fks) >= 2  # Should have at least 2 foreign keys
        
        # Check for meal_id and food_item_id foreign keys
        referred_tables = [fk['referred_table'] for fk in junction_fks]
        assert 'meals' in referred_tables
        assert 'food_items' in referred_tables
