# # tests/conftest.py
# import pytest
# import os
# import tempfile
# from app import create_app, db
# from app.models import User, Meal, FoodItem

# @pytest.fixture
# def app():
#     """Create and configure a Flask app for testing."""
#     # Create a temporary file to isolate the database for each test
#     db_fd, db_path = tempfile.mkstemp()
    
#     app = create_app({
#         'TESTING': True,
#         'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
#         'SQLALCHEMY_TRACK_MODIFICATIONS': False,
#     })
    
#     # Create the database and load test data
#     with app.app_context():
#         db.create_all()
    
#     yield app
    
#     # Close and remove the temporary database
#     os.close(db_fd)
#     os.unlink(db_path)

# @pytest.fixture
# def client(app):
#     """A test client for the app."""
#     return app.test_client()

# @pytest.fixture
# def _db(app):
#     """Provide the database object for testing."""
#     with app.app_context():
#         yield db
#         # Clear any pending transactions at the end of each test
#         db.session.remove()
# # @pytest.fixture
# # def app():
# #     """Create and configure a Flask app for testing."""
# #     # Create a temporary file to isolate the database for each test
# #     db_fd, db_path = tempfile.mkstemp()
# #     app = create_app({'TESTING': True, 
# #                       'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
# #                       'SQLALCHEMY_TRACK_MODIFICATIONS': False})

# #     # Create the database and the database tables
# #     with app.app_context():
# #         db.create_all()
    
# #     yield app
    
# #     # Close and remove the temporary database
# #     os.close(db_fd)
# #     os.unlink(db_path)

# # @pytest.fixture
# # def client(app):
# #     """A test client for the app."""
# #     return app.test_client()

# # @pytest.fixture
# # def runner(app):
# #     """A test CLI runner for the app."""
# #     return app.test_cli_runner()

# # @pytest.fixture
# # def _db(app):
# #     """Provide the database instance for tests that need direct db access."""
# #     with app.app_context():
# #         yield db

# tests/conftest.py
import pytest
from app import create_app
from app.models import db, User, FoodItem, Nutrient, NutrientValue, FoodCategory
from app.models.food import food_category_association
import os
import tempfile

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    # Basic configuration for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        _populate_test_data()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

def _populate_test_data():
    """Create test data for the test database."""
    # Create test nutrients
    nutrients = [
        Nutrient(code='ENERC_KCAL', name='Energy', unit='kcal', category='Macronutrients', display_order=1),
        Nutrient(code='PROCNT', name='Protein', unit='g', category='Macronutrients', display_order=2),
        Nutrient(code='FAT', name='Total Fat', unit='g', category='Macronutrients', display_order=3),
        Nutrient(code='CHOCDF', name='Total Carbohydrate', unit='g', category='Macronutrients', display_order=4),
        Nutrient(code='FIBTG', name='Dietary Fiber', unit='g', category='Macronutrients', display_order=5),
    ]
    for nutrient in nutrients:
        db.session.add(nutrient)
    
    # Create test categories
    categories = [
        FoodCategory(name='Fruits', description='Fresh, frozen, canned, and dried fruits'),
        FoodCategory(name='Vegetables', description='Fresh, frozen, canned, and dried vegetables'),
        FoodCategory(name='Protein Foods', description='Meat, poultry, seafood, eggs, nuts, seeds'),
    ]
    for category in categories:
        db.session.add(category)
    
    # Create test foods
    foods = [
        {
            'name': 'Test Apple',
            'description': 'A test apple for unit tests',
            'serving_size': 100,
            'serving_unit': 'g',
            'verified': True,
            'categories': ['Fruits'],
            'nutrients': {
                'ENERC_KCAL': 52,
                'PROCNT': 0.3,
                'FAT': 0.2,
                'CHOCDF': 14,
                'FIBTG': 2.4
            }
        },
        {
            'name': 'Test Chicken',
            'description': 'A test chicken for unit tests',
            'serving_size': 100,
            'serving_unit': 'g',
            'verified': True,
            'categories': ['Protein Foods'],
            'nutrients': {
                'ENERC_KCAL': 165,
                'PROCNT': 31,
                'FAT': 3.6,
                'CHOCDF': 0,
                'FIBTG': 0
            }
        },
        {
            'name': 'Test Spinach',
            'description': 'A test spinach for unit tests',
            'serving_size': 100,
            'serving_unit': 'g',
            'verified': True,
            'categories': ['Vegetables'],
            'nutrients': {
                'ENERC_KCAL': 23,
                'PROCNT': 2.9,
                'FAT': 0.4,
                'CHOCDF': 3.6,
                'FIBTG': 2.2
            }
        },
        {
            'name': 'Unverified Food',
            'description': 'An unverified food for testing',
            'serving_size': 100,
            'serving_unit': 'g',
            'verified': False,
            'categories': ['Fruits'],
            'nutrients': {
                'ENERC_KCAL': 100,
                'PROCNT': 1.0,
                'FAT': 1.0,
                'CHOCDF': 10.0,
                'FIBTG': 1.0
            }
        }
    ]
    
    # Get categories and nutrients for reference
    category_dict = {c.name: c for c in FoodCategory.query.all()}
    nutrient_dict = {n.code: n for n in Nutrient.query.all()}
    
    # Add foods
    for food_data in foods:
        food = FoodItem(
            name=food_data['name'],
            description=food_data['description'],
            serving_size=food_data['serving_size'],
            serving_unit=food_data['serving_unit'],
            verified=food_data['verified']
        )
        
        # Add categories
        for category_name in food_data['categories']:
            if category_name in category_dict:
                food.categories.append(category_dict[category_name])
        
        # Add nutrients
        for nutrient_code, value in food_data['nutrients'].items():
            if nutrient_code in nutrient_dict:
                nutrient_value = NutrientValue(
                    nutrient=nutrient_dict[nutrient_code],
                    value=value
                )
                food.nutrients.append(nutrient_value)
        
        db.session.add(food)
    
    # Create test user
    user = User(username='testuser', email='test@example.com')
    db.session.add(user)
    
    db.session.commit()

import coverage
import pytest

@pytest.fixture(autouse=True, scope="session")
def setup_coverage():
    cov = coverage.Coverage(
        source=['models', 'routes', 'app.py'],
        omit=['tests/*', 'venv/*', '*/test_*.py']
    )
    cov.start()
    yield
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory='htmlcov')