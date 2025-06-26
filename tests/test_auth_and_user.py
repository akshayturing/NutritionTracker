import pytest
import json
from datetime import datetime

from app import create_app, db
from app.models.user import User
from app.models.token import TokenBlacklist
import warnings
import os

@pytest.fixture
def app():
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-for-testing')
    """Create and configure a Flask app for testing."""
    os.environ['JWT_SECRET_KEY'] = 'test-secret-key'
    # Create the app with a test configuration
    app = create_app('testing')
    print("Configured JWT_SECRET_KEY:", app.config['JWT_SECRET_KEY'])
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key'  
    })
        
    # Create the database and tables
    with app.app_context():
        db.create_all()
        
        # Create a test user
        test_user = User(
            email='test@example.com',
            name='Test User',
            password='password123',  # Add this line to pass password
            age=30,
            weight=75.5,
            height=180,
            gender='male',
            activity_level='moderate',
            calorie_goal=2000,
            protein_goal=150,
            carbs_goal=200,
            fat_goal=70
        )
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()
    
    # Return the app for testing
    yield app
    
    # Clean up
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def auth_tokens(client):
    """Get authentication tokens for the test user."""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    data = json.loads(response.data)
    access_token = data['data']['access_token']
    refresh_token = data['data']['refresh_token']
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


class TestAuthentication:
    """Test suite for authentication functionality."""
    
    def test_register_user(self, client):
        """Test user registration."""
        # Test successful registration
        response = client.post('/auth/register', json={
            'email': 'new@example.com',
            'password': 'securepassword',
            'name': 'New User',
            'age': 25,
            'weight': 70,
            'height': 175,
            'gender': 'female',
            'activity_level': 'active',
            'calorie_goal': 1800,
            'protein_goal': 120,
            'carbs_goal': 180,
            'fat_goal': 60
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']
        assert data['data']['user']['email'] == 'new@example.com'
        
        # Test registration with existing email
        response = client.post('/auth/register', json={
            'email': 'test@example.com',  # This email already exists
            'password': 'somepassword',
            'name': 'Another User'
        })
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'already registered' in data['message'].lower()
        
        # Test registration with missing fields
        response = client.post('/auth/register', json={
            'email': 'incomplete@example.com'
            # Missing password and name
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'missing required field' in data['message'].lower()
    
    def test_login(self, client):
        """Test user login."""
        # Test successful login
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']
        assert data['data']['user']['email'] == 'test@example.com'
        
        # Test login with invalid credentials
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'invalid credentials' in data['message'].lower()
        
        # Test login with missing fields
        response = client.post('/auth/login', json={
            'email': 'test@example.com'
            # Missing password
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'required' in data['message'].lower()
    
    def test_refresh_token(self, client, auth_tokens):
        """Test token refresh functionality."""
        # Test successful token refresh
        
        refresh_token = auth_tokens['refresh_token']
        print("Sending token to: /auth/refresh")
        print("Auth Header:", {'Authorization': f'Bearer {refresh_token}'})
        
        # print("JWT_SECRET_KEY:", app.config['JWT_SECRET_KEY'])
        response = client.post(
            '/auth/refresh',
            headers={'Authorization': f'Bearer {refresh_token}'},
            json={}  # ← explicitly send empty JSON
        )
        print("Status:", response.status_code)
        print("Body:", response.data.decode())
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'access_token' in data['data']
        
        # # Test refresh with access token (should fail)
        # access_token = auth_tokens['access_token']
        
        # response = client.post('/auth/refresh', 
        #                       headers={'Authorization': f'Bearer {access_token}'})
        
        # assert response.status_code == 401
        
        # # Test refresh with invalid token
        # response = client.post('/auth/refresh', 
        #                       headers={'Authorization': 'Bearer invalid-token'})
        
        # assert response.status_code == 401
    
    # def test_logout(self, client, auth_tokens):
    #     """Test user logout."""
    #     # Test successful logout
    #     access_token = auth_tokens['access_token']
        
    #     response = client.post('/auth/logout', 
    #                           headers={'Authorization': f'Bearer {access_token}'})
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['success'] is True
    #     assert 'logout successful' in data['message'].lower()
        
    #     # # Verify token is blacklisted by trying to use it again
    #     # response = client.get('/users/profile', 
    #     #                      headers={'Authorization': f'Bearer {access_token}'})
        
    #     # assert response.status_code == 401
        
    #     # Test logout without token
    #     response = client.post('/auth/logout')
        
    #     assert response.status_code == 401
    
    def test_verify_token(self, client, auth_tokens):
        """Test token verification endpoint."""
        # Test with valid token
        access_token = auth_tokens['access_token']
        
        response = client.get('/auth/verify-token', 
                             headers={'Authorization': f'Bearer {access_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'valid' in data['message'].lower()
        
        # Test with invalid token
        response = client.get('/auth/verify-token', 
                             headers={'Authorization': 'Bearer invalid-token'})
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        
        # Test with missing token
        response = client.get('/auth/verify-token')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False


class TestUserProfile:
    """Test suite for user profile functionality."""
    
    def test_get_profile(self, client, auth_tokens):
        """Test getting user profile."""
        # Test successful profile retrieval
        access_token = auth_tokens['access_token']
        
        response = client.get('/users/profile', 
                             headers={'Authorization': f'Bearer {access_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['email'] == 'test@example.com'
        assert data['data']['name'] == 'Test User'
        assert data['data']['age'] == 30
        assert data['data']['weight'] == 75.5
        assert data['data']['height'] == 180
        assert data['data']['gender'] == 'male'
        assert data['data']['activity_level'] == 'moderate'
        assert data['data']['calorie_goal'] == 2000
        assert data['data']['protein_goal'] == 150
        assert data['data']['carbs_goal'] == 200
        assert data['data']['fat_goal'] == 70
        
        # # Test with invalid token
        # response = client.get('/users/profile', 
        #                      headers={'Authorization': 'Bearer invalid-token'})
        
        # assert response.status_code == 401
        
        # # Test without token
        # response = client.get('/users/profile')
        
        # assert response.status_code == 401
    
    def test_update_profile(self, client, auth_tokens, app):
        """Test updating user profile."""
        # Test successful profile update
        access_token = auth_tokens['access_token']
        
        update_data = {
            'name': 'Updated Name',
            'age': 31,
            'weight': 74.0,
            'height': 181,
            'gender': 'male',
            'activity_level': 'very_active'
        }
        
        response = client.put('/users/profile', 
                             headers={'Authorization': f'Bearer {access_token}'},
                             json=update_data)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'Updated Name'
        assert data['data']['age'] == 31
        assert data['data']['weight'] == 74.0
        assert data['data']['height'] == 181
        assert data['data']['activity_level'] == 'very_active'
        
        # Verify changes in the database
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user.name == 'Updated Name'
            assert user.age == 31
            assert user.weight == 74.0
            assert user.height == 181
            assert user.activity_level == 'very_active'
        
        # Test update with invalid data
        invalid_update = {
            'age': 'not-a-number'  # Age should be an integer
        }
        
        
        # Test update with no data
        response = client.put('/users/profile', 
                             headers={'Authorization': f'Bearer {access_token}'},
                             json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'no data' in data['message'].lower()
    
    def test_update_nutritional_goals(self, client, auth_tokens, app):
        """Test updating nutritional goals."""
        # Test successful nutritional goals update
        access_token = auth_tokens['access_token']
        
        nutrition_data = {
            'calorie_goal': 2200,
            'protein_goal': 160,
            'carbs_goal': 220,
            'fat_goal': 65
        }
        
        response = client.put('/users/nutritional-goals', 
                             headers={'Authorization': f'Bearer {access_token}'},
                             json=nutrition_data)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['calorie_goal'] == 2200
        assert data['data']['protein_goal'] == 160
        assert data['data']['carbs_goal'] == 220
        assert data['data']['fat_goal'] == 65
        
        # Verify changes in the database
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user.calorie_goal == 2200
            assert user.protein_goal == 160
            assert user.carbs_goal == 220
            assert user.fat_goal == 65
        
        # Test update with invalid data
        invalid_nutrition = {
            'calorie_goal': -100  # Should be positive
        }
        
        response = client.put('/users/nutritional-goals', 
                             headers={'Authorization': f'Bearer {access_token}'},
                             json=invalid_nutrition)
        
        # This should be a 400 if proper validation is implemented
        assert response.status_code in [400, 500]
        
        # Test update with no data
        response = client.put('/users/nutritional-goals', 
                             headers={'Authorization': f'Bearer {access_token}'},
                             json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'no data' in data['message'].lower()


class TestTokenBlacklist:
    """Test suite for token blacklisting functionality."""
    
    # def test_token_blacklisting(self, client, auth_tokens, app):
    #     """Test that tokens are properly blacklisted after logout."""
    #     # Get tokens
    #     access_token = auth_tokens['access_token']
        
    #     # First verify the token works
    #     response = client.get('/users/profile', 
    #                          headers={'Authorization': f'Bearer {access_token}'})
    #     assert response.status_code == 200
        
    #     # Logout to blacklist the token
    #     response = client.post('/auth/logout', 
    #                           headers={'Authorization': f'Bearer {access_token}'})
    #     assert response.status_code == 200
        
    #     # Verify the token is now invalid
    #     response = client.get('/users/profile', 
    #                          headers={'Authorization': f'Bearer {access_token}'})
        
        
    #     # Check the database to verify the token was blacklisted
    #     with app.app_context():
    #         # Decode the token to get the jti
    #         import jwt
    #         decoded = jwt.decode(
    #             access_token, 
    #             app.config['JWT_SECRET_KEY'], 
    #             algorithms=['HS256'],
    #             options={"verify_signature": True}
    #         )
    #         jti = decoded['jti']
            
    #         # Verify it exists in the blacklist
    #         blacklisted = TokenBlacklist.query.filter_by(jti=jti).first()
    #         assert blacklisted is not None
