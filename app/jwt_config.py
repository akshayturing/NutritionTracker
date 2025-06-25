from flask_jwt_extended import get_jwt
from app import jwt
from app.models.token import TokenBlacklist

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return TokenBlacklist.is_token_revoked(jti)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return {
        'status': 401,
        'message': 'The token has expired.',
        'error': 'token_expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'status': 401,
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        'status': 401,
        'message': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }, 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_data):
    return {
        'status': 401,
        'message': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }, 401