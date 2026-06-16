## @file __init__.py
#  @brief Shared route helpers: access-control decorators

from functools import wraps
from flask import session, redirect, url_for, flash, request


## @brief Require an active login; otherwise redirect to the login page
#  @param f  View function to protect
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


## @brief Restrict a view to one or more roles
#  @param roles  Allowed role names
#  Usage: role_required('admin') or role_required('airline_staff', 'airline_manager')
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('role') not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated
    return decorator


## @brief Require a recent password re-confirmation (UC03) before sensitive actions
#  @param f  View function to protect
def reauth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('reauthed'):
            session['next_url'] = url_for(request.endpoint)
            flash('Please confirm your password to continue.', 'warning')
            return redirect(url_for('auth.reauth'))
        return f(*args, **kwargs)
    return decorated
