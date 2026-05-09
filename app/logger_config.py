"""
Logging configuration module with environment-based log levels.
Controls log verbosity between development and production environments.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


def get_environment() -> str:
    """
    Get the current environment setting.
    Returns 'dev' or 'prod' based on ENVIRONMENT env var or defaults to 'prod' for safety.
    """
    env = os.getenv('ENVIRONMENT', 'prod').lower()
    return 'dev' if env == 'dev' else 'prod'


def is_dev_mode() -> bool:
    """Check if running in development mode."""
    return get_environment() == 'dev'


def is_prod_mode() -> bool:
    """Check if running in production mode."""
    return get_environment() == 'prod'


def sanitize_api_key(api_key: Optional[str], show_length: bool = False) -> str:
    """
    Sanitize API key for logging in production.
    
    Args:
        api_key: The API key to sanitize
        show_length: If True, show the length of the key
        
    Returns:
        Original key in dev mode, redacted version in production
    """
    if is_dev_mode() or not api_key:
        return api_key or ''
    
    # In prod mode, show only masked version
    if len(api_key) <= 4:
        return '****'
    
    first_chars = api_key[:3]
    last_chars = api_key[-4:]
    key_len = len(api_key)
    
    if show_length:
        return f"{first_chars}...{last_chars} ({key_len} chars)"
    return f"{first_chars}...{last_chars}"


def truncate_content(content: str, max_length: int = 100, 
                     prod_max_length: Optional[int] = 0) -> str:
    """
    Truncate content for logging with different limits for dev/prod.
    
    Args:
        content: The content to truncate
        max_length: Max length in development mode
        prod_max_length: Max length in production mode (0 = don't log at all)
        
    Returns:
        Truncated content or empty string if should not log in this mode
    """
    if not content:
        return 'N/A'
    
    if is_dev_mode():
        if len(content) > max_length:
            return f"{content[:max_length]}..."
        return content
    else:  # production mode
        if prod_max_length == 0:
            return '[REDACTED]'
        if len(content) > prod_max_length:
            return f"{content[:prod_max_length]}..."
        return content


def should_log_sensitive_info() -> bool:
    """
    Determine if sensitive information should be logged.
    Returns True in dev mode, False in production.
    """
    return is_dev_mode()


def get_log_level() -> int:
    """
    Get the logging level based on environment.
    Returns DEBUG in dev mode, INFO in production.
    """
    if is_dev_mode():
        return logging.DEBUG
    return logging.INFO


def configure_app_logging(app, logs_dir: str, app_version: str) -> None:
    """
    Configure application logging with environment-aware settings.
    
    Args:
        app: Flask application instance
        logs_dir: Directory to store log files
        app_version: Application version string
    """
    # Clear any existing handlers
    app.logger.handlers.clear()
    
    # Determine log level based on environment
    log_level = get_log_level()
    
    # Configure formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Main app log handler (file)
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'app.log'),
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    
    # Add handlers and set level
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(log_level)
    
    # Environment-aware startup message
    env_str = f"(Environment: {get_environment().upper()})"
    app.logger.info(f'Application startup v{app_version} {env_str}')


def configure_llm_logging(logs_dir: str) -> logging.Logger:
    """
    Configure LLM-specific logging with environment-aware settings.
    
    Args:
        logs_dir: Directory to store log files
        
    Returns:
        Configured logger instance
    """
    import json
    
    logger = logging.getLogger('llm_calls')
    if logger.handlers:
        logger.handlers.clear()
    
    # Ensure log directory exists
    os.makedirs(logs_dir, exist_ok=True)
    
    # In production, limit logged data
    log_level = get_log_level()
    
    handler = RotatingFileHandler(
        os.path.join(logs_dir, 'llm_calls.log'),
        maxBytes=5*1024*1024,
        backupCount=5
    )
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            # For API call logs (containing all required fields)
            if all(hasattr(record, field) for field in 
                  ['function', 'input', 'output', 'estimated_cost']):
                
                # Sanitize input/output in production
                input_val = getattr(record, 'input')
                output_val = getattr(record, 'output')
                
                if is_prod_mode():
                    input_val = truncate_content(str(input_val), prod_max_length=50)
                    output_val = truncate_content(str(output_val), prod_max_length=50)
                
                log_record = {
                    'timestamp': self.formatTime(record, self.datefmt),
                    'level': record.levelname,
                    'type': 'api_call',
                    'session_id': getattr(record, 'session_id', 'unknown'),
                    'function': getattr(record, 'function'),
                    'input': input_val,
                    'output': output_val,
                    'estimated_cost': getattr(record, 'estimated_cost'),
                    'input_tokens': getattr(record, 'input_tokens'),
                    'output_tokens': getattr(record, 'output_tokens'),
                    'total_tokens': getattr(record, 'total_tokens')
                }
            # For regular logs
            else:
                log_record = {
                    'timestamp': self.formatTime(record, self.datefmt),
                    'level': record.levelname,
                    'type': 'info',
                    'session_id': getattr(record, 'session_id', 'unknown'),
                    'message': record.getMessage()
                }
            return json.dumps(log_record)

    handler.setFormatter(JsonFormatter(datefmt='%Y-%m-%d %H:%M:%S'))
    handler.setLevel(log_level)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    logger.propagate = False
    
    return logger
