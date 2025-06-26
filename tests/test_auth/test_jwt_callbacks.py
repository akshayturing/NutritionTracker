import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app.auth.jwt_callbacks import generate_token, decode_token, token_is_blacklisted


class TestJwtCallbacks:
    """Test suite for JWT authentication callbacks"""
    
    @pytest.fixture
    def user_id(self, test_user):
        return test_user.id
    
    @pytest.fixture
    def email(self, test_user):
        return test_user.email
    
    @pytest.fixture
    def test_token_payload(self, user_id, email):
        return {
            "sub": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

    @patch('app.auth.jwt_callbacks.jwt.encode')
    def test_generate_token(self, mock_jwt_encode, user_id, email):
        """Test token generation service"""
        # Setup mock returns
        mock_token = "mocked.jwt.token"
        mock_jwt_encode.return_value = mock_token
        
        # Execute
        token = generate_token(user_id, email)
        
        # Assert
        assert token == mock_token
        mock_jwt_encode.assert_called_once()
    
    @patch('app.auth.jwt_callbacks.jwt.decode')
    def test_decode_token_valid(self, mock_jwt_decode, test_token_payload, user_id):
        """Test token decoding service with valid token"""
        # Setup mock returns
        mock_jwt_decode.return_value = test_token_payload
        
        # Execute
        token = "valid.jwt.token"
        payload = decode_token(token)
        
        # Assert
        assert payload == test_token_payload
        assert payload['sub'] == user_id
        mock_jwt_decode.assert_called_once()

    @patch('app.models.token_blacklist.TokenBlacklist.is_blacklisted')
    def test_token_is_blacklisted(self, mock_is_blacklisted):
        """Test token blacklist checking service"""
        # Setup test scenarios
        mock_is_blacklisted.side_effect = [True, False]
        
        # Execute - blacklisted token
        token1 = "blacklisted.jwt.token"
        result1 = token_is_blacklisted(token1)
        
        # Execute - valid token
        token2 = "valid.jwt.token"
        result2 = token_is_blacklisted(token2)
        
        # Assert
        assert result1 is True
        assert result2 is False
        assert mock_is_blacklisted.call_count == 2
