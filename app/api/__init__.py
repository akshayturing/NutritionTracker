"""API package for Nutrition Tracking App."""
from flask import Blueprint

# Create the API blueprint
api_bp = Blueprint('api', __name__)

# Import routes after blueprint creation to avoid circular imports
from app.api import routes