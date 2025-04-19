# app/__init__.py
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional

# App version
APP_VERSION = '0.3.1'

# Define project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_app(testing: bool = False) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='../templates',  
                static_folder='../static')       

    # Load configuration
    app.secret_key = os.getenv('APPSECRETKEY')
    app.config.update(
        UPLOAD_FOLDER=os.path.join(PROJECT_ROOT, 'temp_uploads'),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # 5MB limit
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'pdf'},
        APP_VERSION=APP_VERSION,
        TESTING=testing,
        # OpenAI settings
        AZURE_API_KEY=os.getenv('AZUREAPIKEY'),
        AZURE_API_VERSION=os.getenv('AZUREAPIVERSION', '2023-12-01-preview'),
        AZURE_API_URL=os.getenv('AZUREAPIURL'),
        DAILY_COST_THRESHOLD=float(os.getenv('DAILYCOSTTHRESHOLD', '10.0')),
        # Add logs directory to config
        LOGS_DIR=os.path.join(PROJECT_ROOT, 'logs')
    )

    # Ensure upload and log directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['LOGS_DIR'], exist_ok=True)

    # Configure logging
    if not testing:
        configure_logging(app)

    # Register blueprints
    from .routes import auth_bp, main_bp, info_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(info_bp)

    return app

def configure_logging(app: Flask) -> None:
    """Configure application logging."""
    logs_dir = app.config['LOGS_DIR']
    
    # Clear any existing handlers
    app.logger.handlers.clear()
    
    # Configure standard formatter for app logs
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Main app log handler
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'app.log'),
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Also add a stream handler for console output during development
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    
    # Add handlers and set level
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    
    # Start-up log message
    app.logger.info(f'Application startup (v{APP_VERSION})')