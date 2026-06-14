
import uuid
from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template,
    request, session, url_for,
)
from werkzeug.security import check_password_hash

from database.db import get_db

bp = Blueprint('auth', __name__)


@bp.route('/login')
def login():
    if 'user_id' in session:
        return redirect(_dashboard_for_role(session.get('role', '')))
    return render_template('auth/login.html')

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
        if not name:
            session['pending_oauth_email'] = email
            return redirect(url_for('auth.register'))
        db.execute(
            "INSERT INTO users (role, full_name, email, oauth_token, is_active) "
            "VALUES ('client', ?, ?, 'mock-oauth-token', 1)",
            (name, email),
        )
        db.commit()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    _create_session(db, user)
    return redirect(url_for('client.dashboard'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', session.pop('pending_oauth_email', '')).strip().lower()
        full_name = request.form.get('full_name', '').strip()
        dob = request.form.get('dob', '').strip()
        if not full_name or not email:
            flash('Name and email are required.', 'danger')
            return render_template('auth/register.html', email=email)

        db = get_db()
        if db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            flash('An account with that email already exists. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        db.execute(
            "INSERT INTO users (role, full_name, email, dob, oauth_token, is_active) "
            "VALUES ('client', ?, ?, ?, 'mock-oauth-token', 1)",
            (full_name, email, dob),
        )
        db.commit()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        _create_session(db, user)
        flash('Account created. Welcome!', 'success')
        return redirect(url_for('client.dashboard'))

    return render_template('auth/register.html', email=session.get('pending_oauth_email', ''))


@bp.route('/staff/login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ? AND role != 'client' AND is_active = 1",
            (email,),
        ).fetchone()
        if user is None or not check_password_hash(user['password'] or '', password):
            flash('Incorrect email or password.', 'danger')
            return render_template('auth/staff_login.html')

        _create_session(db, user)
        return redirect(_dashboard_for_role(user['role']))

    return render_template('auth/staff_login.html')


@bp.route('/logout', methods=['POST'])
def logout():
    db = get_db()
    if 'session_id' in session:
        db.execute('UPDATE sessions SET is_active = 0 WHERE id = ?', (session['session_id'],))
        db.commit()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/account/delete', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        user_id = session['user_id']
        db = get_db()
        db.execute(
            "UPDATE users SET full_name = 'DELETED', email = ?, "
            "oauth_token = NULL, dob = NULL, is_active = 0 WHERE id = ?",
            (f'deleted-{user_id}@fly.local', user_id),
        )
        db.execute('UPDATE sessions SET is_active = 0 WHERE user_id = ?', (user_id,))
        db.commit()
        session.clear()
        flash('Your account has been deleted.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/delete_account.html')


@bp.route('/reauth', methods=['GET', 'POST'])
def reauth():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        if user and check_password_hash(user['password'] or '', password):
            session['reauthed'] = True
            next_url = session.pop('next_url', None)
            flash('Identity confirmed.', 'success')
            return redirect(next_url or url_for('auth.staff_login'))
        flash('Incorrect password.', 'danger')
    return render_template('auth/reauth.html')


def _create_session(db, user):
    db.execute('UPDATE sessions SET is_active = 0 WHERE user_id = ?', (user['id'],))
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
