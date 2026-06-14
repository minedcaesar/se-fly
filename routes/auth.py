import uuid
from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template,
    request, session, url_for,
)

from database.db import get_db

bp = Blueprint('auth', __name__)


@bp.route('/login')
def login():
    if 'user_id' in session:
        return redirect(_dashboard_for_role(session.get('role', '')))
    return render_template('auth/login.html')


#mock oauth callback

@bp.route('/oauth/mock', methods=['POST'])
def oauth_mock():
    email = request.form.get('email', '').strip().lower()
    name = request.form.get('full_name', '').strip()
    if not email:
        flash('Email is required.', 'danger')
        return redirect(url_for('auth.login'))

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ? AND role = 'client'",
                      (email,)).fetchone()
    if user is None:
        db.execute(
            "INSERT INTO users (role, full_name, email, oauth_token, is_active) "
            "VALUES ('client', ?, ?, 'mock-oauth-token', 1)",
            (name, email),
        )
        db.commit()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    session_id = str(uuid.uuid4())
    db.execute(
        'INSERT INTO sessions (id, user_id, device_id, login_timestamp, is_active) '
        'VALUES (?, ?, ?, ?, 1)',
        (session_id, user['id'], request.headers.get('User-Agent', ''),
         datetime.now().isoformat()),
    )
    db.commit()
    session.clear()
    session['user_id'] = user['id']
    session['role'] = user['role']
    session['full_name'] = user['full_name']
    session['session_id'] = session_id
    return redirect(url_for('client.dashboard'))


def _dashboard_for_role(role):
    mapping = {
        'client': 'client.dashboard',
        'airline_staff': 'airline.dashboard',
        'airline_manager': 'airline.dashboard',
        'ground_op_manager': 'ground.dashboard',
        'shift_manager': 'ground.dashboard',
        'operation_staff': 'ground.tasks',
        'admin': 'admin.dashboard',
    }
    return url_for(mapping.get(role, 'auth.login'))
