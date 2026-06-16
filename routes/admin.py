# system admin routes: manage staff accounts (UC21, UC22)

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,
)
from werkzeug.security import generate_password_hash

from database.db import get_db
from routes import role_required

# admin route registration
bp = Blueprint('admin', __name__, url_prefix='/admin')

# roles that can be managed by administrators

STAFF_ROLES = [
    'airline_staff', 'airline_manager',
    'ground_op_manager', 'shift_manager', 'operation_staff',
    'admin',
]


@bp.route('/')
@role_required('admin')
def dashboard():
    db = get_db()

    # retrieve active staff accounts
    users = db.execute(
        "SELECT * FROM users WHERE is_active = 1 ORDER BY role, full_name"
    ).fetchall()
    return render_template('admin/dashboard.html', users=users)


@bp.route('/staff/create', methods=['GET', 'POST'])
@role_required('admin')
def create_staff():
    db = get_db()

    # process staff account creation
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        role = request.form.get('role', '')
        password = request.form.get('password', '').strip()
        airline = request.form.get('airline', '').strip()
        terminal = request.form.get('terminal', '').strip()

        # validate submitted data
        error = None
        if not full_name or not email or not role or not password:
            error = 'Name, email, role, and password are required.'
        elif role not in STAFF_ROLES:
            error = 'Invalid role.'
        elif db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            error = 'An account with that email already exists.'

        # create new staff account
        if error is None:
            db.execute(
                'INSERT INTO users (role, full_name, email, password, airline, terminal, is_active) '
                'VALUES (?, ?, ?, ?, ?, ?, 1)',
                (role, full_name, email, generate_password_hash(password),
                 airline or None, terminal or None),
            )
            db.commit()
            flash(f'Staff account created for {full_name}.', 'success')
            return redirect(url_for('admin.dashboard'))
        flash(error, 'danger')

    # load airline options for the form
    airlines = db.execute('SELECT name FROM airlines').fetchall()
    return render_template('admin/create_staff.html', roles=STAFF_ROLES, airlines=airlines)


@bp.route('/staff/<int:user_id>/delete', methods=['POST'])
@role_required('admin')
def delete_staff(user_id):
    db = get_db()

    # retrieve target account
    user = db.execute('SELECT * FROM users WHERE id = ? AND is_active = 1', (user_id,)).fetchone()

    # check that the account does in fact exists
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.dashboard'))

    # stop administrators from deleting their own account
    if user_id == session['user_id']:
        flash('You cannot delete your own account from here.', 'danger')
        return redirect(url_for('admin.dashboard'))

    # anonymise + deactivate the selected account
    db.execute(
        "UPDATE users SET full_name = 'DELETED', email = ?, password = NULL, "
        "airline = NULL, terminal = NULL, is_active = 0 WHERE id = ?",
        (f'deleted-{user_id}@fly.local', user_id),
    )

    # invalidate any active sessions of the deleted account
    db.execute('UPDATE sessions SET is_active = 0 WHERE user_id = ?', (user_id,))

    # commit account removal changes
    db.commit()
    flash('Staff account deleted and data anonymised.', 'success')
    return redirect(url_for('admin.dashboard'))