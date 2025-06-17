# tests/test_auth.py
import pytest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User
from app.models.token import TokenBlacklist
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)
    
    with app.app_context():
        db.create_all()
        # Create a test user
        test_user = User(email='test@example.com', password='Password123!')
        db.session.add(test_user)
        
        # Create an admin user with role claim
        admin_user = User(email='admin@example.com', password='Admin123!')
        db.session.add(admin_user)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_headers(app, client):
    """Get auth headers with valid tokens."""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'Password123!'
    })
    data = json.loads(response.data)
    
    return {
        'Authorization': f"Bearer {data['access_token']}",
        'Content-Type': 'application/json'
    }

@pytest.fixture
def refresh_headers(app, client):
    """Get refresh token headers."""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'Password123!'
    })
    data = json.loads(response.data)
    
    return {
        'Authorization': f"Bearer {data['refresh_token']}",
        'Content-Type': 'application/json'
    }

# Test user registration
def test_register(client):
    # Test valid registration
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'NewPassword123!'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'User created successfully' in data['message']
    
    # Test duplicate registration
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'NewPassword123!'
    })
    assert response.status_code == 409
    
    # Test missing fields
    response = client.post('/api/auth/register', json={
        'email': 'incomplete@example.com'
    })
    assert response.status_code == 400

# Test user login
def test_login(client):
    # Test valid login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'Password123!'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'refresh_token' in data
    
    # Test invalid credentials
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'WrongPassword'
    })
    assert response.status_code == 401
    
    # Test nonexistent user
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'Password123!'
    })
    assert response.status_code == 401

# Test protected routes
def test_protected_route(client, auth_headers):
    # Test access with valid token
    response = client.get('/api/meals', headers=auth_headers)
    assert response.status_code == 200
    
    # Test access without token
    response = client.get('/api/meals')
    assert response.status_code == 401

# Test token refresh
def test_token_refresh(client, refresh_headers):
    # Test valid token refresh
    response = client.post('/api/auth/refresh', headers=refresh_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    
    # Test refresh with access token instead of refresh token
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'Password123!'
    })
    data = json.loads(response.data)
    
    wrong_headers = {
        'Authorization': f"Bearer {data['access_token']}",
        'Content-Type': 'application/json'
    }
    
    response = client.post('/api/auth/refresh', headers=wrong_headers)
    assert response.status_code == 401

# Test logout functionality
def test_logout(client, auth_headers, app):
    # Test valid logout
    response = client.post('/api/auth/logout', headers=auth_headers)
    assert response.status_code == 200
    
    # Verify token is blacklisted
    with app.app_context():
        # Get the token from auth_headers
        token = auth_headers['Authorization'].split(' ')[1]
        
        # Verify token is in blacklist
        blacklist_entry = TokenBlacklist.query.filter_by(token_type='access').first()
        assert blacklist_entry is not None
        
        # Test that blacklisted token cannot access protected routes
        response = client.get('/api/meals', headers=auth_headers)
        assert response.status_code == 401

# Test token expiration
def test_token_expiration(app, client):
    with app.app_context():
        # Create expired token
        user = User.query.filter_by(email='test@example.com').first()
        expires = datetime.utcnow() - timedelta(minutes=10)
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(minutes=-10)
        )
        
        # Try to use expired token
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
        
        response = client.get('/api/meals', headers=headers)
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'expired' in data['message'].lower()

# Test role-based access control
def test_admin_access(app, client):
    with app.app_context():
        # Create admin token with role claim
        admin = User.query.filter_by(email='admin@example.com').first()
        admin_token = create_access_token(
            identity=admin.id,
            additional_claims={"role": "admin"}
        )
        
        # Create regular user token
        user = User.query.filter_by(email='test@example.com').first()
        user_token = create_access_token(identity=user.id)
        
        # Test admin access to protected route
        admin_headers = {
            'Authorization': f"Bearer {admin_token}",
            'Content-Type': 'application/json'
        }
        
        user_headers = {
            'Authorization': f"Bearer {user_token}",
            'Content-Type': 'application/json'
        }
        
        # Assuming we have an admin-only endpoint
        response = client.get('/api/admin/users', headers=admin_headers)
        assert response.status_code == 200
        
        # Regular user should not access admin route
        response = client.get('/api/admin/users', headers=user_headers)
        assert response.status_code == 403
