import pytest
from app.models.user import User
from werkzeug.security import check_password_hash

def test_password_hashing():
    user = User(name="Akshay", email="akshay@example.com", password="secure123")
    assert user.password_hash != "secure123"
    assert check_password_hash(user.password_hash, "secure123")

def test_password_verification():
    user = User(name="Akshay", email="akshay@example.com", password="secure123")
    assert user.check_password("secure123") is True
    assert user.check_password("wrongpass") is False

def test_user_to_dict_output():
    user = User(name="Akshay", email="akshay@example.com", password="secure123", age=25, weight=70)
    user_dict = user.to_dict()
    assert user_dict['name'] == "Akshay"
    assert 'password_hash' not in user_dict
    assert user_dict['email'] == "akshay@example.com"
    assert user_dict['age'] == 25
    assert user_dict['weight'] == 70
