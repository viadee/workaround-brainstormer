# Logging Configuration Guide

This guide explains how to use the environment-based logging system in your application.

## Overview

The application now supports environment-specific logging levels and content filtering:

- **Development Mode (`dev`)**: Detailed logging including request content, query responses, and full API details
- **Production Mode (`prod`)**: Limited logging with sensitive information redacted and API keys masked

## Setting the Environment

Set the `ENVIRONMENT` environment variable to control logging behavior:

```bash
# Development mode - verbose logging
export ENVIRONMENT=dev

# Production mode - limited logging (default for safety)
export ENVIRONMENT=prod
```

If not set, the application defaults to `prod` mode for security.

## Features

### 1. Dynamic Log Levels

- **Dev Mode**: `DEBUG` level logging with full content visibility
- **Prod Mode**: `INFO` level logging with reduced noise

### 2. Sensitive Information Filtering

Automatically controlled by `should_log_sensitive_info()`:

- **Dev Mode**: Logs full request content, additional context, and API responses
- **Prod Mode**: Logs only `[REDACTED]` for sensitive user content

### 3. API Key Sanitization

Use `sanitize_api_key()` when logging API credentials:

```python
from app.logger_config import sanitize_api_key

api_key = os.getenv('AZURE_OPENAI_API_KEY')
# Dev: "sk-1234567890..."
# Prod: "sk-...9876 (42 chars)"
sanitized = sanitize_api_key(api_key, show_length=True)
```

### 4. Content Truncation

Use `truncate_content()` for user-provided data:

```python
from app.logger_config import truncate_content

# Dev: full content up to 100 chars
# Prod: [REDACTED] (prod_max_length=0 by default)
truncate_content(user_description, max_length=100, prod_max_length=50)
```

## Usage Examples

### Logging Sensitive Information Conditionally

```python
from flask import current_app
from app.logger_config import should_log_sensitive_info, truncate_content

# In routes.py
if should_log_sensitive_info():
    current_app.logger.debug(f"Process: {process_description}")
else:
    current_app.logger.debug("Process analysis started")
```

### Logging LLM API Calls

The `llm_calls.log` file automatically sanitizes input/output in production:

- **Dev Mode**: Full input/output logged for debugging
- **Prod Mode**: Input/output truncated to 50 characters

### Application Startup

The application logs the current environment on startup:

```
[2026-05-09 10:30:15] INFO in __init__: Application startup v0.3.1 (Environment: DEV)
[2026-05-09 10:30:15] INFO in __init__: Application startup v0.3.1 (Environment: PROD)
```

## Log Files

### `logs/app.log`

Main application log file with:
- Login/logout events
- Workaround generation status
- Error tracking

Log level controlled by `ENVIRONMENT`:
- **Dev**: DEBUG and above
- **Prod**: INFO and above

### `logs/llm_calls.log`

JSON-formatted LLM API call logs with:
- Function name
- Input/Output (sanitized in prod)
- Token usage and cost estimation
- Session ID
- Timestamp

Content sanitization in prod mode applies to `input` and `output` fields.

## Best Practices

### 1. Use Helper Functions for Sensitive Data

```python
from app.logger_config import should_log_sensitive_info, truncate_content

# DO: Conditional logging
if should_log_sensitive_info():
    current_app.logger.debug(f"Details: {data}")

# DON'T: Always logging
current_app.logger.debug(f"Details: {data}")
```

### 2. Sanitize API Keys

```python
from app.logger_config import sanitize_api_key

# DO: Use sanitize_api_key
key_display = sanitize_api_key(api_key)
current_app.logger.warning(f"API Key: {key_display}")

# DON'T: Log raw keys
current_app.logger.warning(f"API Key: {api_key}")
```

### 3. Truncate User Content

```python
from app.logger_config import truncate_content

# DO: Use truncate_content for user input
content_preview = truncate_content(user_input, max_length=100, prod_max_length=0)
current_app.logger.debug(f"Input: {content_preview}")

# DON'T: Log full user content
current_app.logger.debug(f"Input: {user_input}")
```

## Utility Functions Reference

### `get_environment() -> str`
Returns `'dev'` or `'prod'` based on `ENVIRONMENT` variable.

### `is_dev_mode() -> bool`
Returns `True` if running in development mode.

### `is_prod_mode() -> bool`
Returns `True` if running in production mode.

### `get_log_level() -> int`
Returns `logging.DEBUG` for dev, `logging.INFO` for prod.

### `should_log_sensitive_info() -> bool`
Returns `True` in dev mode, `False` in production.

### `sanitize_api_key(api_key, show_length=False) -> str`
Sanitizes API keys for logging.
- **show_length**: If `True`, appends the key length to the output.

### `truncate_content(content, max_length=100, prod_max_length=0) -> str`
Truncates content based on environment.
- **max_length**: Max chars in dev mode
- **prod_max_length**: Max chars in prod mode (0 = don't log)

### `configure_app_logging(app, logs_dir, app_version)`
Configures main application logging with environment awareness.

### `configure_llm_logging(logs_dir) -> Logger`
Configures LLM-specific JSON logging with sanitization.

## Debugging Issues

### Logs Not Showing Expected Detail in Dev Mode

1. Check environment variable: `echo $ENVIRONMENT`
2. Should be set to `dev` (case-insensitive)
3. Restart the application after setting the variable

### Production Logs Missing Information

This is **expected behavior**. In production mode:
- User content is redacted
- API responses are truncated
- Debug logs are not included

To see full details, switch to dev mode temporarily.

## Migration Notes

### Updating Existing Code

When adding logging to new features, follow this pattern:

```python
from app.logger_config import should_log_sensitive_info, truncate_content

# For informational logs (always safe)
current_app.logger.info("Operation completed")

# For potentially sensitive content
if should_log_sensitive_info():
    current_app.logger.debug(f"Processed: {user_data}")

# For content that might contain user info
truncated = truncate_content(user_input, prod_max_length=0)
current_app.logger.debug(f"Input: {truncated}")
```

## Questions & Troubleshooting

### Q: Why is my debug log not showing in production?

**A:** Debug logs are only enabled in dev mode. Set `ENVIRONMENT=dev` to see DEBUG level logs.

### Q: How do I know the current environment?

**A:** Check the startup message:
```
Application startup v0.3.1 (Environment: DEV)
Application startup v0.3.1 (Environment: PROD)
```

### Q: Can I change the log level without restarting?

**A:** The log level is set during application startup. You'll need to restart the app to apply changes.

### Q: What if I need to log something sensitive temporarily?

**A:** Use the `should_log_sensitive_info()` guard and switch to dev mode:
```python
if should_log_sensitive_info():
    current_app.logger.debug(f"Sensitive: {data}")
```
Then set `ENVIRONMENT=dev` before running the application.
