"""Authentication package for Nutrition Tracking App."""
from flask import Blueprint

# Create the authentication blueprint
auth_bp = Blueprint('auth', __name__)

# Import routes after blueprint creation to avoid circular imports
from app.auth import routes