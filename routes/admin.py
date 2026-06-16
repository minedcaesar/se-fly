## @file admin.py
#  @brief System administrator routes: manage staff accounts (UC21, UC22).

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,
)
from werkzeug.security import generate_password_hash

from database.db import get_db
from routes import role_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

## @brief Roles an administrator may assign to a staff account.
STAFF_ROLES = [
    'airline_staff', 'airline_manager',
    'ground_op_manager', 'shift_manager', 'operation_staff',
    'admin',
]


## @brief Admin dashboard: list active users.
@bp.route('/')
@role_required('admin')
def dashboard():
    db = get_db()
    staff = db.execute(
        "SELECT * FROM users WHERE is_active = 1 AND role != 'client' ORDER BY role, full_name"
    ).fetchall()
    clients = db.execute(
        "SELECT * FROM users WHERE is_active = 1 AND role = 'client' ORDER BY full_name"
    ).fetchall()
    return render_template('admin/dashboard.html', staff=staff, clients=clients)


## @brief Create a staff account with a hashed temporary password (UC21).
@bp.route('/staff/create', methods=['GET', 'POST'])
@role_required('admin')
def create_staff():
    db = get_db()
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        role = request.form.get('role', '')
        password = request.form.get('password', '').strip()
        airline = request.form.get('airline', '').strip()
        terminal = request.form.get('terminal', '').strip()

        error = None
        if not full_name or not email or not role or not password:
            error = 'Name, email, role, and password are required.'
        elif role not in STAFF_ROLES:
            error = 'Invalid role.'
        elif db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            error = 'An account with that email already exists.'

        AIRLINE_ROLES = {'airline_staff', 'airline_manager'}
        GROUND_ROLES = {'ground_op_manager', 'shift_manager', 'operation_staff'}
        if error is None:
            db.execute(
                'INSERT INTO users (role, full_name, email, password, airline, terminal, is_active) '
                'VALUES (?, ?, ?, ?, ?, ?, 1)',
                (role, full_name, email, generate_password_hash(password),
                 (airline or None) if role in AIRLINE_ROLES else None,
                 (terminal or None) if role in GROUND_ROLES else None),
            )
            db.commit()
            flash(f'Staff account created for {full_name}.', 'success')
            return redirect(url_for('admin.dashboard'))
        flash(error, 'danger')

    airlines = db.execute('SELECT name FROM airlines').fetchall()
    return render_template('admin/create_staff.html', roles=STAFF_ROLES, airlines=airlines)


## @brief Delete a staff account (UC22): anonymise + end their sessions
#  @param user_id  Account to delete, cant be your own
@bp.route('/staff/<int:user_id>/delete', methods=['POST'])
@role_required('admin')
def delete_staff(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ? AND is_active = 1', (user_id,)).fetchone()
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.dashboard'))
    if user_id == session['user_id']:
        flash('You cannot delete your own account from here.', 'danger')
        return redirect(url_for('admin.dashboard'))

    db.execute(
        "UPDATE users SET full_name = 'DELETED', email = ?, password = NULL, "
        "airline = NULL, terminal = NULL, is_active = 0 WHERE id = ?",
        (f'deleted-{user_id}@fly.local', user_id),
    )
    db.execute('UPDATE sessions SET is_active = 0 WHERE user_id = ?', (user_id,))
    db.commit()
    flash('Staff account deleted and data anonymised.', 'success')
    return redirect(url_for('admin.dashboard'))
