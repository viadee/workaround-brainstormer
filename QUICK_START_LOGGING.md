# Quick Start: Environment-Based Logging

## TL;DR

To control logging verbosity:

```bash
# Development - Detailed logs with request content
export ENVIRONMENT=dev

# Production - Limited logs, sensitive data masked
export ENVIRONMENT=prod
```

## What Gets Logged

### Dev Mode (`ENVIRONMENT=dev`)
✅ Full process descriptions  
✅ Complete LLM API responses  
✅ Complete additional context  
✅ Full API keys (with prefix/suffix shown)  
✅ DEBUG level logs  

### Prod Mode (default)
✅ Operation status  
✅ Errors with context  
❌ User content (shows as `[REDACTED]`)  
❌ Full API keys (masked: `sk-...1234`)  
❌ DEBUG level logs  

## Setup (One-Time)

1. The logging system is already integrated. No code changes needed.

2. Set the environment variable:
   ```bash
   # In .env file:
   ENVIRONMENT=dev
   
   # Or set it before running:
   export ENVIRONMENT=dev
   python run.py
   ```

3. That's it! Restart your application to apply changes.

## Checking Current Environment

Look at the startup message:
```
Application startup v0.3.1 (Environment: DEV)
Application startup v0.3.1 (Environment: PROD)
```

## Adding Logging to New Code

### Safe to Always Log
```python
current_app.logger.info("Operation completed")
current_app.logger.error("Error occurred")
```

### Conditionally Log Sensitive Data
```python
from app.logger_config import should_log_sensitive_info

if should_log_sensitive_info():
    current_app.logger.debug(f"User input: {user_data}")
```

### Log User Content Safely
```python
from app.logger_config import truncate_content

content = truncate_content(user_description, prod_max_length=0)
current_app.logger.debug(f"Processing: {content}")
```

### Log API Keys Safely
```python
from app.logger_config import sanitize_api_key

key_display = sanitize_api_key(api_key, show_length=True)
current_app.logger.warning(f"Using API: {key_display}")
```

## Log File Locations

- **app.log** - Main application logs
- **llm_calls.log** - LLM API calls (JSON format)

Both in `logs/` directory.

## Common Issues

### Debug logs not appearing
→ Set `ENVIRONMENT=dev` and restart

### Production logs too detailed
→ Ensure `ENVIRONMENT=prod` or leave unset

### Need to debug production issue
→ Set `ENVIRONMENT=dev`, restart, check logs, then switch back to `prod`

## For Complete Details

See [LOGGING.md](LOGGING.md) for:
- All available functions
- Detailed examples
- Best practices
- Troubleshooting
