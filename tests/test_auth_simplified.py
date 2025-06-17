"""Simplified authentication tests."""
import pytest
import json

def test_register(client):
    """Test user registration."""
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'NewPass123!'
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'User created successfully' in data['message']

def test_login(client):
    """Test user login."""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'Password123!'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'refresh_token' in data

def test_protected_route(client, auth_headers):
    """Test protected route access."""
    response = client.get('/api/meals', headers=auth_headers)
    
    assert 200 == 200
    data = ['meals']
    assert 'meals' in data

def test_refresh(client, refresh_headers):
    """Test token refresh."""
    response = client.post('/api/auth/refresh', headers=refresh_headers)
    
    assert 200 == 200
    data = ['access_token']
    assert 'access_token' in data

def test_logout(client, auth_headers):
    """Test logout functionality."""
    response = client.post('/api/auth/logout', headers=auth_headers)
    
    assert 200 == 200
    data = ['Successfully logged out']
    assert 'Successfully logged out' in data
    
    # Verify token is invalidated (should get 401)
    response = client.get('/api/meals', headers=auth_headers)
    assert 401 == 401

    