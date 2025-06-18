# # # # tests/conftest.py
# # # import pytest
# # # import os
# # # import tempfile
# # # from app import create_app, db
# # # from app.models import User, Meal, FoodItem

# # # @pytest.fixture
# # # def app():
# # #     """Create and configure a Flask app for testing."""
# # #     # Create a temporary file to isolate the database for each test
# # #     db_fd, db_path = tempfile.mkstemp()
    
# # #     app = create_app({
# # #         'TESTING': True,
# # #         'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
# # #         'SQLALCHEMY_TRACK_MODIFICATIONS': False,
# # #     })
    
# # #     # Create the database and load test data
# # #     with app.app_context():
# # #         db.create_all()
    
# # #     yield app
    
# # #     # Close and remove the temporary database
# # #     os.close(db_fd)
# # #     os.unlink(db_path)

# # # @pytest.fixture
# # # def client(app):
# # #     """A test client for the app."""
# # #     return app.test_client()

# # # @pytest.fixture
# # # def _db(app):
# # #     """Provide the database object for testing."""
# # #     with app.app_context():
# # #         yield db
# # #         # Clear any pending transactions at the end of each test
# # #         db.session.remove()
# # # # @pytest.fixture
# # # # def app():
# # # #     """Create and configure a Flask app for testing."""
# # # #     # Create a temporary file to isolate the database for each test
# # # #     db_fd, db_path = tempfile.mkstemp()
# # # #     app = create_app({'TESTING': True, 
# # # #                       'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
# # # #                       'SQLALCHEMY_TRACK_MODIFICATIONS': False})

# # # #     # Create the database and the database tables
# # # #     with app.app_context():
# # # #         db.create_all()
    
# # # #     yield app
    
# # # #     # Close and remove the temporary database
# # # #     os.close(db_fd)
# # # #     os.unlink(db_path)

# # # # @pytest.fixture
# # # # def client(app):
# # # #     """A test client for the app."""
# # # #     return app.test_client()

# # # # @pytest.fixture
# # # # def runner(app):
# # # #     """A test CLI runner for the app."""
# # # #     return app.test_cli_runner()

# # # # @pytest.fixture
# # # # def _db(app):
# # # #     """Provide the database instance for tests that need direct db access."""
# # # #     with app.app_context():
# # # #         yield db

# # # tests/conftest.py
# # import pytest
# # from app import create_app
# # from app.models import db, User, FoodItem, Nutrient, NutrientValue, FoodCategory
# # from app.models.food import food_category_association
# # import os
# # import tempfile

# # @pytest.fixture
# # def app():
# #     """Create and configure a Flask app for testing."""
# #     # Create a temporary file to isolate the database for each test
# #     db_fd, db_path = tempfile.mkstemp()
    
# #     app = create_app('testing')
# #     app.config.update({
# #         'TESTING': True,
# #         'SQLALCHEMY_DATABASE_URI': f'sqlite:///nutrition_tracker.db',
# #         'SQLALCHEMY_TRACK_MODIFICATIONS': False,
# #     })
# #     # # Basic configuration for testing
# #     # app.config['JWT_SECRET_KEY'] = 'test-secret-key'

# #     # Create the database and load test data
# #     with app.app_context():
# #         db.create_all()
# #         # _populate_test_data()
    
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

# # def _populate_test_data():
# #     """Create test data for the test database."""
# #     # Create test nutrients
# #     nutrients = [
# #         Nutrient(code='ENERC_KCAL', name='Energy', unit='kcal', category='Macronutrients', display_order=1),
# #         Nutrient(code='PROCNT', name='Protein', unit='g', category='Macronutrients', display_order=2),
# #         Nutrient(code='FAT', name='Total Fat', unit='g', category='Macronutrients', display_order=3),
# #         Nutrient(code='CHOCDF', name='Total Carbohydrate', unit='g', category='Macronutrients', display_order=4),
# #         Nutrient(code='FIBTG', name='Dietary Fiber', unit='g', category='Macronutrients', display_order=5),
# #     ]
# #     for nutrient in nutrients:
# #         db.session.add(nutrient)
    
# #     # Create test categories
# #     categories = [
# #         FoodCategory(name='Fruits', description='Fresh, frozen, canned, and dried fruits'),
# #         FoodCategory(name='Vegetables', description='Fresh, frozen, canned, and dried vegetables'),
# #         FoodCategory(name='Protein Foods', description='Meat, poultry, seafood, eggs, nuts, seeds'),
# #     ]
# #     for category in categories:
# #         db.session.add(category)
    
# #     # Create test foods
# #     foods = [
# #         {
# #             'name': 'Test Apple',
# #             'description': 'A test apple for unit tests',
# #             'serving_size': 100,
# #             'serving_unit': 'g',
# #             'verified': True,
# #             'categories': ['Fruits'],
# #             'nutrients': {
# #                 'ENERC_KCAL': 52,
# #                 'PROCNT': 0.3,
# #                 'FAT': 0.2,
# #                 'CHOCDF': 14,
# #                 'FIBTG': 2.4
# #             }
# #         },
# #         {
# #             'name': 'Test Chicken',
# #             'description': 'A test chicken for unit tests',
# #             'serving_size': 100,
# #             'serving_unit': 'g',
# #             'verified': True,
# #             'categories': ['Protein Foods'],
# #             'nutrients': {
# #                 'ENERC_KCAL': 165,
# #                 'PROCNT': 31,
# #                 'FAT': 3.6,
# #                 'CHOCDF': 0,
# #                 'FIBTG': 0
# #             }
# #         },
# #         {
# #             'name': 'Test Spinach',
# #             'description': 'A test spinach for unit tests',
# #             'serving_size': 100,
# #             'serving_unit': 'g',
# #             'verified': True,
# #             'categories': ['Vegetables'],
# #             'nutrients': {
# #                 'ENERC_KCAL': 23,
# #                 'PROCNT': 2.9,
# #                 'FAT': 0.4,
# #                 'CHOCDF': 3.6,
# #                 'FIBTG': 2.2
# #             }
# #         },
# #         {
# #             'name': 'Unverified Food',
# #             'description': 'An unverified food for testing',
# #             'serving_size': 100,
# #             'serving_unit': 'g',
# #             'verified': False,
# #             'categories': ['Fruits'],
# #             'nutrients': {
# #                 'ENERC_KCAL': 100,
# #                 'PROCNT': 1.0,
# #                 'FAT': 1.0,
# #                 'CHOCDF': 10.0,
# #                 'FIBTG': 1.0
# #             }
# #         }
# #     ]
    
# #     # Get categories and nutrients for reference
# #     category_dict = {c.name: c for c in FoodCategory.query.all()}
# #     nutrient_dict = {n.code: n for n in Nutrient.query.all()}
    
# #     # Add foods
# #     for food_data in foods:
# #         food = FoodItem(
# #             name=food_data['name'],
# #             description=food_data['description'],
# #             serving_size=food_data['serving_size'],
# #             serving_unit=food_data['serving_unit'],
# #             verified=food_data['verified']
# #         )
        
# #         # Add categories
# #         for category_name in food_data['categories']:
# #             if category_name in category_dict:
# #                 food.categories.append(category_dict[category_name])
        
# #         # Add nutrients
# #         for nutrient_code, value in food_data['nutrients'].items():
# #             if nutrient_code in nutrient_dict:
# #                 nutrient_value = NutrientValue(
# #                     nutrient=nutrient_dict[nutrient_code],
# #                     value=value
# #                 )
# #                 food.nutrients.append(nutrient_value)
        
# #         db.session.add(food)
    
# #     # Create test user
# #     user = User(username='testuser', email='test@example.com')
# #     db.session.add(user)
    
# #     db.session.commit()

# # import coverage
# # import pytest

# # @pytest.fixture(autouse=True, scope="session")
# # def setup_coverage():
# #     cov = coverage.Coverage(
# #         source=['models', 'routes', 'app.py'],
# #         omit=['tests/*', 'venv/*', '*/test_*.py']
# #     )
# #     cov.start()
# #     yield
# #     cov.stop()
# #     cov.save()
# #     cov.report()
# #     cov.html_report(directory='htmlcov')

# """Test fixtures for Nutrition Tracking App."""
# import pytest
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager, create_access_token
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime, timedelta, timezone

# # Initialize extensions
# db = SQLAlchemy()
# jwt = JWTManager()

# # Define models
# class User(db.Model):
#     """User model for testing."""
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def __init__(self, email, password):
#         self.email = email
#         self.password_hash = generate_password_hash(password)
    
#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)

# class TokenBlacklist(db.Model):
#     """Token blacklist model for testing."""
#     __tablename__ = 'token_blacklist'
    
#     id = db.Column(db.Integer, primary_key=True)
#     jti = db.Column(db.String(36), unique=True, nullable=False)
#     token_type = db.Column(db.String(10), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     revoked = db.Column(db.Boolean, default=True, nullable=False)
#     expires = db.Column(db.DateTime, nullable=False)
    
#     @classmethod
#     def is_token_revoked(cls, jti):
#         token = cls.query.filter_by(jti=jti).first()
#         return token is not None and token.revoked

# @pytest.fixture
# def app():
#     """Create Flask application for testing."""
#     # Create a Flask application instance
#     app = Flask(__name__)
    
#     # Configure the application
#     app.config['TESTING'] = True
#     app.config['DEBUG'] = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['JWT_SECRET_KEY'] = 'test-secret-key'
#     app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
#     app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)
    
#     # Initialize extensions with app
#     db.init_app(app)
#     jwt.init_app(app)
    
#     # Set up JWT token blocklist check
#     @jwt.token_in_blocklist_loader
#     def check_if_token_revoked(jwt_header, jwt_payload):
#         jti = jwt_payload["jti"]
#         return TokenBlacklist.is_token_revoked(jti)
    
#     # Create routes for testing
#     from flask import Blueprint, jsonify, request
#     from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
    
#     # Create auth blueprint
#     auth_bp = Blueprint('auth', __name__)
    
#     @auth_bp.route('/register', methods=['POST'])
#     def register():
#         data = request.get_json()
        
#         if not data or not data.get('email') or not data.get('password'):
#             return jsonify({'message': 'Missing required fields'}), 400
            
#         # Check if user exists
#         existing_user = User.query.filter_by(email=data['email']).first()
#         if existing_user:
#             return jsonify({'message': 'User already exists'}), 409
            
#         # Create new user
#         new_user = User(email=data['email'], password=data['password'])
#         db.session.add(new_user)
#         db.session.commit()
        
#         return jsonify({'message': 'User created successfully'}), 201
    
#     @auth_bp.route('/login', methods=['POST'])
#     def login():
#         data = request.get_json()
        
#         if not data or not data.get('email') or not data.get('password'):
#             return jsonify({'message': 'Missing required fields'}), 400
            
#         # Find user
#         user = User.query.filter_by(email=data['email']).first()
        
#         # Verify password
#         if not user or not user.verify_password(data['password']):
#             return jsonify({'message': 'Invalid credentials'}), 401
            
#         # Create tokens
#         access_token = create_access_token(identity=user.id)
#         refresh_token = create_access_token(
#             identity=user.id,
#             expires_delta=app.config['JWT_REFRESH_TOKEN_EXPIRES'],
#             additional_claims={'type': 'refresh'}
#         )
        
#         return jsonify({
#             'access_token': access_token,
#             'refresh_token': refresh_token,
#             'user_id': user.id,
#             'email': user.email
#         }), 200
    
#     @auth_bp.route('/refresh', methods=['POST'])
#     @jwt_required(refresh=True)
#     def refresh():
#         current_user = get_jwt_identity()
#         access_token = create_access_token(identity=current_user)
        
#         return jsonify({'access_token': access_token}), 200
    
#     @auth_bp.route('/logout', methods=['POST'])
#     @jwt_required()
#     def logout():
#         jti = get_jwt()["jti"]
#         user_id = get_jwt_identity()
        
#         token = TokenBlacklist(
#             jti=jti,
#             token_type="access",
#             user_id=user_id,
#             expires=datetime.fromtimestamp(get_jwt()["exp"], timezone.utc)
#         )
        
#         db.session.add(token)
#         db.session.commit()
        
#         return jsonify({'message': 'Successfully logged out'}), 200
    
#     # Create API blueprint
#     api_bp = Blueprint('api', __name__)
    
#     @api_bp.route('/meals', methods=['GET'])
#     @jwt_required()
#     def get_meals():
#         return jsonify({
#             'meals': [
#                 {'id': 1, 'name': 'Breakfast', 'calories': 500},
#                 {'id': 2, 'name': 'Lunch', 'calories': 700}
#             ]
#         }), 200
    
#     @api_bp.route('/admin/users', methods=['GET'])
#     @jwt_required()
#     def admin_users():
#         claims = get_jwt()
#         if claims.get("role") != "admin":
#             return jsonify({'message': 'Admin privilege required'}), 403
            
#         return jsonify({
#             'users': [
#                 {'id': 1, 'email': 'admin@example.com'},
#                 {'id': 2, 'email': 'test@example.com'}
#             ]
#         }), 200
        
#     # Register blueprints
#     app.register_blueprint(auth_bp, url_prefix='/api/auth')
#     app.register_blueprint(api_bp, url_prefix='/api')
    
#     # Create application context
#     with app.app_context():
#         # Create database tables
#         db.create_all()
        
#         # Create test users
#         if not User.query.filter_by(email='test@example.com').first():
#             test_user = User(email='test@example.com', password='Password123!')
#             admin_user = User(email='admin@example.com', password='Admin123!')
            
#             db.session.add(test_user)
#             db.session.add(admin_user)
#             db.session.commit()
        
#         yield app
        
#         # Teardown - clean up after tests
#         db.session.remove()
#         db.drop_all()

# @pytest.fixture
# def client(app):
#     """Create a test client."""
#     return app.test_client()

# @pytest.fixture
# def auth_headers(app, client):
#     """Get auth headers with access token."""
#     with app.app_context():
#         # Log in to get tokens
#         response = client.post('/api/auth/login', json={
#             'email': 'test@example.com',
#             'password': 'Password123!'
#         })
        
#         data = response.get_json()
        
#         return {
#             'Authorization': f'Bearer {data["access_token"]}',
#             'Content-Type': 'application/json'
#         }

# @pytest.fixture
# def refresh_headers(app, client):
#     """Get auth headers with refresh token."""
#     with app.app_context():
#         # Log in to get tokens
#         response = client.post('/api/auth/login', json={
#             'email': 'test@example.com',
#             'password': 'Password123!'
#         })
        
#         data = response.get_json()
        
#         return {
#             'Authorization': f'Bearer {data["refresh_token"]}',
#             'Content-Type': 'application/json'
#         }

# @pytest.fixture
# def admin_headers(app, client):
#     """Get admin auth headers."""
#     with app.app_context():
#         # Create a token with admin role
#         admin_token = create_access_token(
#             identity=2,  # Admin user ID
#             additional_claims={"role": "admin"}
#         )
        
#         return {
#             'Authorization': f'Bearer {admin_token}',
#             'Content-Type': 'application/json'
#         }

# tests/conftest.py
import pytest
import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from app import create_app
from app.models import db, User, Meal
from app.auth.jwt_callbacks import generate_token


class TestConfig:
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    JWT_SECRET_KEY = 'test-jwt-secret'


@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    app = create_app(TestConfig)
    
    # Create all tables
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Clean up / reset resources
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create a test user and return the user object"""
    with app.app_context():
        user = User(
            email='test@example.com',
            password_hash=generate_password_hash('test_password'),
            name='Test User',
            age=30,
            weight=70,
            activity_level='moderate'
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def auth_headers(app, test_user):
    """Create authentication headers with valid JWT token"""
    with app.app_context():
        token = generate_token(test_user.id)
        
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def sample_meals(app, test_user):
    """Create sample meals for the test user"""
    with app.app_context():
        meals = []
        # Create meals for today and yesterday
        for i in range(3):
            meal = Meal(
                user_id=test_user.id,
                meal_name=f'Test Meal {i+1}',
                portion_size=300 + i*50,
                calories=400 + i*100,
                macronutrients={'protein': 20+i*5, 'carbs': 30+i*10, 'fat': 15+i*5},
                timestamp=datetime.utcnow() - timedelta(hours=i*6)
            )
            db.session.add(meal)
            meals.append(meal)
        
        # Add an older meal from a week ago
        old_meal = Meal(
            user_id=test_user.id,
            meal_name='Old Meal',
            portion_size=250,
            calories=350,
            macronutrients={'protein': 18, 'carbs': 25, 'fat': 12},
            timestamp=datetime.utcnow() - timedelta(days=7)
        )
        db.session.add(old_meal)
        meals.append(old_meal)
        
        db.session.commit()
        
        # Return IDs of all created meals
        return [meal.id for meal in meals]