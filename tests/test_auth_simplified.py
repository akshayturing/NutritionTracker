"""Simplified authentication test module for Nutrition Tracking App."""
import pytest
import json

# Basic test for registration functionality
def test_register(client):
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'NewPassword123!'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'successfully' in data['message'].lower()

# Basic login test
def test_login(client):
    # First register a user
    client.post('/api/auth/register', json={
        'email': 'logintest@example.com',
        'password': 'Password123'
    })
    
    # Then try to log in
    response = client.post('/api/auth/login', json={
        'email': 'logintest@example.com',
        'password': 'Password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'refresh_token' in data