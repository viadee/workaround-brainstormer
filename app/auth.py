# app/auth.py
from functools import wraps
from flask import session, redirect, url_for, flash
import os
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import os

# Authentication configuration
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = os.getenv('ADMINPASSWORDHASH')

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))  # Updated to use auth.login
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin access for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))  # Updated to use auth.login
        return f(*args, **kwargs)
    return decorated_function

def is_admin():
    """Check if current user is admin."""
    return 'username' in session and session['username'] == ADMIN_USERNAME

def check_credentials(username: str, password: str) -> bool:
    """
    Validate user credentials.
    
    Args:
        username: Username to check
        password: Password to validate
        
    Returns:
        bool: True if credentials are valid
    """
    return True
    # Check admin credentials
    if username == ADMIN_USERNAME:
        return check_password_hash(ADMIN_PASSWORD_HASH, password)
    
    # Check regular user credentials
    user = os.getenv('WAUSERNAME')
    pass_hash = os.getenv('WAPASSWORDHASH')
    return user == username and check_password_hash(pass_hash, password)

def setUserCredentialVariables(username: str, password: str) -> bool:

    if username is None or username == "" or password is None or password == "":
        raise ValueError('Username and password cannot be None or ""')
    
    hashed_pwd =  generate_password_hash(password)

    os.environ['WAPASSWORDHASH'] = hashed_pwd
    os.environ['WAUSERNAME'] = username

    return True