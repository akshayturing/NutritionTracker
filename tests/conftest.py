# tests/conftest.py
import pytest
import os
import tempfile
from app import create_app, db
from app.models import User, Meal, FoodItem

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def _db(app):
    """Provide the database object for testing."""
    with app.app_context():
        yield db
        # Clear any pending transactions at the end of each test
        db.session.remove()
# @pytest.fixture
# def app():
#     """Create and configure a Flask app for testing."""
#     # Create a temporary file to isolate the database for each test
#     db_fd, db_path = tempfile.mkstemp()
#     app = create_app({'TESTING': True, 
#                       'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
#                       'SQLALCHEMY_TRACK_MODIFICATIONS': False})

#     # Create the database and the database tables
#     with app.app_context():
#         db.create_all()
    
#     yield app
    
#     # Close and remove the temporary database
#     os.close(db_fd)
#     os.unlink(db_path)

# @pytest.fixture
# def client(app):
#     """A test client for the app."""
#     return app.test_client()

# @pytest.fixture
# def runner(app):
#     """A test CLI runner for the app."""
#     return app.test_cli_runner()

# @pytest.fixture
# def _db(app):
#     """Provide the database instance for tests that need direct db access."""
#     with app.app_context():
#         yield db