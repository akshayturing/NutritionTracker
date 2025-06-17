# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import os

# # Initialize SQLAlchemy
# db = SQLAlchemy()

# def create_app():
#     # Create Flask app
#     app = Flask(__name__)
    
#     # Configure the SQLite database
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrition_tracker.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     # Initialize the database with the app
#     db.init_app(app)
    
#     # Import and register blueprints/routes
#     from app.routes.user_routes import user_bp
#     from app.routes.meal_routes import meal_bp
    
#     app.register_blueprint(user_bp, url_prefix='/api/users')
#     app.register_blueprint(meal_bp, url_prefix='/api/meals')
    
#     # Create database tables (if they don't exist)
#     with app.app_context():
#         db.create_all()
    
#     return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

db = SQLAlchemy()
jwt = JWTManager()

# migrate = Migrate()
def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_nutrition.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Configure JWT settings
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    # migrate.init_app(app, db)
    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.meal_routes import meal_bp
    from app.routes.food_item_routes import food_item_bp
    from app.routes.documentation import docs_bp
    from app.routes.food_api import food_api

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(meal_bp, url_prefix='/api/meals')
    app.register_blueprint(food_item_bp, url_prefix='/api/food-items')
    app.register_blueprint(docs_bp)
    app.register_blueprint(food_api)

    # Register blueprints
    from app.auth import auth_bp
    from app.api import api_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Other blueprints
    from app.auth.jwt_callbacks import register_jwt_callbacks
    register_jwt_callbacks(jwt)
    
    
    return app