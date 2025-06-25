# # app/config.py
# import os

# class Config:
#     """Base configuration"""
#     SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
#     JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# class DevelopmentConfig(Config):
#     """Development configuration"""
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///nutrition_tracker.db')

# class TestingConfig(Config):
#     """Testing configuration"""
#     TESTING = True
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# class ProductionConfig(Config):
#     """Production configuration"""
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }
import os
from datetime import timedelta

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-for-testing')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev-nutrition-tracker.db'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        # Set any specific testing configurations here
        app.config['SERVER_NAME'] = 'localhost'

class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///nutrition-tracker.db'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        # Set any production-specific settings

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}