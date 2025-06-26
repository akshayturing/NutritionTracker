import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from app.auth.jwt_callbacks import generate_token, decode_token, token_is_blacklisted

class JwtAuthServiceTests(unittest.TestCase):
    """Test suite for JWT authentication service layer"""
    
    def setUp(self):
        """Set up test data"""
        self.user_id = 1
        self.email = "test@example.com"
        self.test_token_payload = {
            "sub": self.user_id,
            "email": self.email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

    @patch('app.auth.jwt_callbacks.jwt.encode')
    def test_generate_token(self, mock_jwt_encode):
        """Test token generation service"""
        # Setup mock returns
        mock_token = "mocked.jwt.token"
        mock_jwt_encode.return_value = mock_token
        
        # Execute
        token = generate_token(self.user_id, self.email)
        
        # Assert
        self.assertEqual(token, mock_token)
        mock_jwt_encode.assert_called_once()
    
    @patch('app.auth.jwt_callbacks.jwt.decode')
    def test_decode_token_valid(self, mock_jwt_decode):
        """Test token decoding service with valid token"""
        # Setup mock returns
        mock_jwt_decode.return_value = self.test_token_payload
        
        # Execute
        token = "valid.jwt.token"
        payload = decode_token(token)
        
        # Assert
        self.assertEqual(payload, self.test_token_payload)
        self.assertEqual(payload['sub'], self.user_id)
        mock_jwt_decode.assert_called_once()

    @patch('app.models.TokenBlacklist.is_blacklisted')
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
        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertEqual(mock_is_blacklisted.call_count, 2)


if __name__ == '__main__':
    unittest.main()