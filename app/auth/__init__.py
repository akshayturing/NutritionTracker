# # """Authentication package for Nutrition Tracking App."""
# # from flask import Blueprint

# # # Create the authentication blueprint
# # auth_bp = Blueprint('auth', __name__)

# # # Import routes after blueprint creation to avoid circular imports
# # from app.auth import routes

# # app/auth/__init__.py
# from flask import Blueprint

# # Create the auth blueprint
# auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# # Import routes after blueprint is created to avoid circular imports
# from app.auth import auth_bp

# # Import jwt functions to make them available from app.auth
# from app.auth.jwt_callbacks import jwt_required, generate_token, decode_token, blacklist_token

# __all__ = ['auth_bp', 'jwt_required', 'generate_token', 'decode_token', 'blacklist_token']