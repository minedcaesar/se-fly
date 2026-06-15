# UC09 - See Flight Schedule
# Read-only schedule list for airlines' staff members


from flask import Blueprint, render_template, session

from database.db import get_db
from routes import role_required

# Initialize blueprint for airline management operations
bp = Blueprint('airline', __name__, url_prefix='/airline')


@bp.route('/')
# Ensure only authorized airline employees can access the main dashboard
@role_required('airline_staff', 'airline_manager')
def dashboard():
    return render_template('airline/dashboard.html')


@bp.route('/schedules')
# Allows staff to view current flight records
@role_required('airline_staff', 'airline_manager')
def schedules():
    db = get_db()

    # Identify the logged-in user from the active session
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    # Retrieve the specific airline company associated with this staff member
    airline = db.execute('SELECT * FROM airlines WHERE name = ?', (user['airline'],)).fetchone()
    
    # Fetch and sort schedules belonging exclusively to the user's airline
    rows = []
    if airline:
        rows = db.execute(
            'SELECT * FROM flight_schedules WHERE airline_id = ? ORDER BY flight_number',
            (airline['id'],),
        ).fetchall()
    return render_template('airline/schedules.html', schedules=rows, airline=airline)