# # # # # from flask import Flask
# # # # # from flask_sqlalchemy import SQLAlchemy
# # # # # import os

# # # # # # Initialize SQLAlchemy
# # # # # db = SQLAlchemy()

# # # # # def create_app():
# # # # #     # Create Flask app
# # # # #     app = Flask(__name__)
    
# # # # #     # Configure the SQLite database
# # # # #     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrition_tracker.db'
# # # # #     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
# # # # #     # Initialize the database with the app
# # # # #     db.init_app(app)
    
# # # # #     # Import and register blueprints/routes
# # # # #     from app.routes.user_routes import user_bp
# # # # #     from app.routes.meal_routes import meal_bp
    
# # # # #     app.register_blueprint(user_bp, url_prefix='/api/users')
# # # # #     app.register_blueprint(meal_bp, url_prefix='/api/meals')
    
# # # # #     # Create database tables (if they don't exist)
# # # # #     with app.app_context():
# # # # #         db.create_all()
    
# # # # #     return app

# # # # from flask import Flask
# # # # from flask_sqlalchemy import SQLAlchemy
# # # # from flask_jwt_extended import JWTManager
# # # # from datetime import timedelta
# # # # import os

# # # # db = SQLAlchemy()
# # # # jwt = JWTManager()

# # # # # migrate = Migrate()
# # # # def create_app(config_name='default'):
# # # #     app = Flask(__name__)
    
# # # #     # Load configuration
# # # #     app.config.from_object('app.config.config')
# # # #     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_nutrition.db'
# # # #     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # # #     # Configure JWT settings
# # # #     app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
# # # #     app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# # # #     app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
# # # #     app.config['JWT_BLACKLIST_ENABLED'] = True
# # # #     app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    
# # # #     # Initialize extensions
# # # #     db.init_app(app)
# # # #     jwt.init_app(app)
# # # #     # migrate.init_app(app, db)
# # # #     # Register blueprints
# # # #     from app.routes.user_routes import user_bp
# # # #     from app.routes.meal_routes import meal_bp
# # # #     from app.routes.food_item_routes import food_item_bp
# # # #     from app.routes.documentation import docs_bp
# # # #     from app.routes.food_api import food_api
# # # #     from app.api import api_bp
# # # #     app.register_blueprint(user_bp, url_prefix='/api/users')
# # # #     app.register_blueprint(meal_bp, url_prefix='/api/meals')
# # # #     app.register_blueprint(food_item_bp, url_prefix='/api/food-items')
# # # #     app.register_blueprint(docs_bp)
# # # #     app.register_blueprint(food_api)

# # # #     # Register blueprints
# # # #     from app.auth import auth_bp
# # # #     from app.api import api_bp
# # # #     app.register_blueprint(auth_bp, url_prefix='/api/auth')
# # # #     app.register_blueprint(api_bp, url_prefix='/api')
# # # #     from app.meals import register_meals_blueprint
# # # #     register_meals_blueprint(app)
# # # #     # # Other blueprints
# # # #     # from app.auth.jwt_callbacks import register_jwt_callbacks
# # # #     # register_jwt_callbacks(jwt)
    
    
# # # #     return app

# # # # app/__init__.py
# # # from flask_sqlalchemy import SQLAlchemy
# # # from flask import Flask
# # # db = SQLAlchemy()
# # # def create_app(config=None):
# # #     """Create and configure the Flask app"""
# # #     app = Flask(__name__)
    
# # #     # Set default configuration - important for tests
# # #     app.config.from_mapping(
# # #         SECRET_KEY='dev-key-for-testing',
# # #         SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
# # #         SQLALCHEMY_TRACK_MODIFICATIONS=False,
# # #     )
    
# # #     # Override with provided configuration if any
# # #     if config:
# # #         if isinstance(config, str):
# # #             app.config.from_object(config)
# # #         else:
# # #             # If config is an object, directly update config
# # #             app.config.update(config)
    
# # #     # Initialize extensions
# # #     from app.models import db
# # #     db.init_app(app)
    
# # #     # Register blueprints
# # #     from app.auth import auth_bp
# # #     app.register_blueprint(auth_bp)
    
# # #     from app.api import api_bp
# # #     app.register_blueprint(api_bp)
    
# # #     # Register meals blueprint using its registration function
# # #     from app.meals import register_meals_blueprint
# # #     register_meals_blueprint(app)
    
# # #     return app

# # # app/__init__.py
# # from flask import Flask
# # from flask_sqlalchemy import SQLAlchemy
# # from flask import Flask
# # db = SQLAlchemy()
# # def create_app(config=None):
# #     app = Flask(__name__)
    
# #     # Default configuration
# #     app.config.from_mapping(
# #         SQLALCHEMY_DATABASE_URI='sqlite:///nutrition_tracker.db',
# #         SQLALCHEMY_TRACK_MODIFICATIONS=False,
# #         SECRET_KEY='dev-secret-key',
# #         JWT_SECRET_KEY='dev-jwt-secret-key',
# #     )
    
# #     # Load configuration from object or class
# #     if config:
# #         if isinstance(config, str):
# #             app.config.from_object(config)
# #         else:
# #             app.config.from_object(config)
    
# #     # Initialize extensions
# #     from app.models import db
# #     db.init_app(app)
    
   
    
# #     from app.api import api_bp
# #     app.register_blueprint(api_bp)
    
# #     # Register meals blueprint using the function
# #     from app.meals import register_meals_blueprint
# #     register_meals_blueprint(app)
    
# #     from app.routes.nutrition import nutrition_bp
# #     app.register_blueprint(nutrition_bp, url_prefix='/api/nutrition')

# #     from app.auth.routes import auth_bp
# #     app.register_blueprint(auth_bp, url_prefix="/api/auth")

# #     return app

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from app.config import config

# # Initialize extensions
# db = SQLAlchemy()

# def create_app(config_name='default'):
#     """Create and configure the Flask application"""
#     app = Flask(__name__)
    
#     # Configure the app
#     app_config = config[config_name]
#     app.config.from_object(app_config)
#     app_config.init_app(app)
    
#     # Initialize extensions
#     db.init_app(app)
#     CORS(app)
    
#     # Register blueprints
#     from app.routes.auth import auth_bp
#     from app.routes.meals import nutrition_meals
#     from app.routes.foods import foods_bp
#     from app.routes.users import users_bp
#     from app.routes.nutrition import nutrition_bp
    
#     app.register_blueprint(auth_bp, url_prefix='/api/auth')
#     app.register_blueprint(nutrition_meals, url_prefix='/api/meals')
#     app.register_blueprint(foods_bp, url_prefix='/api/foods')
#     app.register_blueprint(users_bp, url_prefix='/api/users')
#     app.register_blueprint(nutrition_bp, url_prefix='/api/nutrition')
    
#     return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure the app
    app_config = config[config_name]
    app.config.from_object(app_config)
    app_config.init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize CORS - make it optional
    try:
        from flask_cors import CORS
        CORS(app)
        app.logger.info("CORS extension initialized")
    except ImportError:
        app.logger.warning("Flask-CORS extension not available. CORS support disabled.")
    
    # Register blueprints
    #from app.routes.auth import auth_bp
    from app.routes.meals import nutrition_meals
    from app.routes.foods import foods_bp
    from app.routes.users import users_bp
    from app.routes.nutrition import nutrition_bp
    
    #app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(nutrition_meals, url_prefix='/api/meals')
    app.register_blueprint(foods_bp, url_prefix='/api/foods')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(nutrition_bp, url_prefix='/api/nutrition')
    


    return app