# UC13 - See Weather
# mock api to show the weather forecast 
# UC14 - See Shift
# Shows to the authorised personnel the programmed shifts
# UC16 - Move Aircraft
# Allowing the personnel to move the resources
# UC20 - View Accountability Logs
# Keeps track of the user that made a modification to ensure accountability

from flask import Blueprint, redirect, render_template, url_for

from database.db import get_db
from routes import role_required

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