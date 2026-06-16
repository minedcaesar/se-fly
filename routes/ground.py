# UC13 - See Weather
# mock api to show the weather forecast 
# UC14 - See Shift
# Shows to the authorised personnel the programmed shifts
# UC16 - Move Aircraft
# Allowing the personnel to move the resources
# UC20 - View Accountability Logs
# Keeps track of the user that made a modification to ensure accountability

from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,
)

from database.db import get_db
from routes import role_required, reauth_required

# Initialize a Flask Blueprint named 'ground' to compartmentalize ground operations routes under /ground
bp = Blueprint('ground', __name__, url_prefix='/ground')

# Tuple defining all authorization roles permitted to access ground-handling view endpoints
GROUND_ROLES = ('ground_op_manager', 'shift_manager', 'operation_staff')


@bp.route('/')
# Unpack the GROUND_ROLES tuple using '*' to pass all allowed roles to the authorization decorator
@role_required(*GROUND_ROLES)
def dashboard():
    return render_template('ground/dashboard.html')


# Temporary login for operation staff
@bp.route('/tasks')
@role_required(*GROUND_ROLES)
def tasks():
    return redirect(url_for('ground.dashboard'))


@bp.route('/weather')
@role_required(*GROUND_ROLES)
def weather():
    # production: WeatherForecastAPI.getWeeklyForecast() -> OpenWeatherMap.
    #   requests.get("https://api.openweathermap.org/data/2.5/forecast", params={...})
    # mocked 5-day forecast for the deliverable:
    forecast = [
        {'day': 'Mon', 'temp': 18, 'desc': 'Clear'},
        {'day': 'Tue', 'temp': 21, 'desc': 'Sunny'},
        {'day': 'Wed', 'temp': 16, 'desc': 'Rain'},
        {'day': 'Thu', 'temp': 17, 'desc': 'Cloudy'},
        {'day': 'Fri', 'temp': 20, 'desc': 'Clear'},
    ]

    # Render the weather template interface and inject the forecast dictionary list into its scope
    return render_template('ground/weather.html', forecast=forecast)

@bp.route('/shifts')
# Grant access to all baseline roles defined in the GROUND_ROLES tuple via unpacking
@role_required(*GROUND_ROLES)
def shifts():

    # Establish a connection to the active application database instance
    db = get_db()

    # Query all elements from the shifts table and combine it with matching records from the users table
    # Sorted sequentially by the upcoming start times
    rows = db.execute(
        'SELECT s.*, u.full_name FROM shifts s '
        'LEFT JOIN users u ON s.user_id = u.id ORDER BY s.start_time'
    ).fetchall()
    # Inject the resulting array of shift records directly into the UI rendering context
    return render_template('ground/shifts.html', shifts=rows)


@bp.route('/logs')
# Restrict endpoint visibility to managerial operations; standard 'operation_staff' are excluded here
@role_required('ground_op_manager', 'shift_manager')
def accountability_logs():

    # Establish a connection to the active application database instance
    db = get_db()

    # Query accountability records, running dual LEFT JOIN connections against the users table 
    # twice to distinctly bind the tracking manager's ID and the affected staff member's ID.
    logs = db.execute(
        'SELECT acl.*, m.full_name AS manager_name, s.full_name AS staff_name '
        'FROM accountability_log_entries acl '
        'LEFT JOIN users m ON acl.manager_id = m.id '
        'LEFT JOIN users s ON acl.staff_id = s.id '
        'ORDER BY acl.timestamp DESC'
    ).fetchall()

    # Render the system logs dashboard view containing the populated management dataset
    return render_template('ground/logs.html', logs=logs)

# Move an aircraft to a new gate. privileged -> needs re-auth (UC03), and writes an accountability log entry UC16
@bp.route('/move-aircraft', methods=['GET', 'POST'])
# Restrict endpoint visibility exclusively to ground operations managers
@role_required('ground_op_manager')
# Enforce a custom security middleware check requiring a fresh re-authentication challenge
@reauth_required
def move_aircraft():

    # Establish a connection to the active application database instance
    db = get_db()

    # Process form data only if a state mutation payload is submitted via POST
    if request.method == 'POST':
        # Retrieve and sanitize input fields from the incoming submission form payload
        aircraft_id = request.form.get('aircraft_id')
        target_gate = request.form.get('target_gate', '').strip()
        reason = request.form.get('reason', '').strip()

        # Verify that the specified aircraft exists in the system before mutating state
        ac = db.execute('SELECT * FROM aircraft WHERE id = ?', (aircraft_id,)).fetchone()
        if ac is None:
            flash('Aircraft not found.', 'danger')
            return redirect(url_for('ground.move_aircraft'))
        
        # Security/Operation Action 1: Mutate physical position state of the verified aircraft row
        db.execute('UPDATE aircraft SET current_position = ? WHERE id = ?',
                   (target_gate, aircraft_id))
        
        # Security/Operation Action 2: Write an entry to the tracking system for compliance auditing
        db.execute(
            'INSERT INTO accountability_log_entries '
            '(timestamp, manager_id, staff_id, reason_for_change) VALUES (?, ?, ?, ?)',
            (
                datetime.now().isoformat(), 
                session['user_id'],                                         # The validating manager logged in who signed off
            session['user_id'],                                             # The executing staff profile processing the action
                f'Moved {ac["registration"]} to {target_gate}: {reason}')   # Context audit string
        )

        # Persist both the update and structural log entries securely to the storage engine
        db.commit()

        # Security best practice: Revoke the temporary high-privilege token so subsequent
        # destructive requests are forced to prompt the operator for re-authentication again.
        session.pop('reauthed', None)  # consume the re-auth
        
        flash('Aircraft moved.', 'success')
        return redirect(url_for('ground.move_aircraft'))
    
    # GET Request Pipeline: Query all available airframes sequenced uniformly by registration marks
    aircraft = db.execute('SELECT * FROM aircraft ORDER BY registration').fetchall()

    # Render the allocation terminal template viewport populated with the aircraft dataset
    return render_template('ground/move_aircraft.html', aircraft=aircraft)