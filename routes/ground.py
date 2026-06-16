## @file ground.py
#  @brief Ground staff routes. UC13 weather (mock api), UC14 shifts, UC16 move aircraft
#         UC20 accountability logs, UC15/17/18/19 are stubbed at the bottom

from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,
)

from database.db import get_db
from routes import role_required, reauth_required

bp = Blueprint('ground', __name__, url_prefix='/ground')

## @brief Roles that may access the ground module
GROUND_ROLES = ('ground_op_manager', 'shift_manager', 'operation_staff')


## @brief Ground operations home page
@bp.route('/')
@role_required(*GROUND_ROLES)
def dashboard():
    return render_template('ground/dashboard.html')


## @brief Landing endpoint for operation staff; redirects to the dashboard
@bp.route('/tasks')
@role_required(*GROUND_ROLES)
def tasks():
    return redirect(url_for('ground.dashboard'))


## @brief Weather forecast (UC13). Mocked here; production calls WeatherForecastAPI.
@bp.route('/weather')
@role_required(*GROUND_ROLES)
def weather():
    # production: WeatherForecastAPI.getWeeklyForecast() -> OpenWeatherMap.
    #   requests.get("https://api.openweathermap.org/data/2.5/forecast", params={...})
    forecast = [
        {'day': 'Mon', 'temp': 18, 'desc': 'Clear'},
        {'day': 'Tue', 'temp': 21, 'desc': 'Sunny'},
        {'day': 'Wed', 'temp': 16, 'desc': 'Rain'},
        {'day': 'Thu', 'temp': 17, 'desc': 'Cloudy'},
        {'day': 'Fri', 'temp': 20, 'desc': 'Clear'},
    ]
    return render_template('ground/weather.html', forecast=forecast)


## @brief Shift roster (UC14)
@bp.route('/shifts')
@role_required(*GROUND_ROLES)
def shifts():
    db = get_db()
    rows = db.execute(
        'SELECT s.*, u.full_name FROM shifts s '
        'LEFT JOIN users u ON s.user_id = u.id ORDER BY s.start_time'
    ).fetchall()
    return render_template('ground/shifts.html', shifts=rows)


## @brief Accountability log view for managers (UC20)
@bp.route('/logs')
@role_required('ground_op_manager', 'shift_manager')
def accountability_logs():
    db = get_db()
    logs = db.execute(
        'SELECT acl.*, m.full_name AS manager_name, s.full_name AS staff_name '
        'FROM accountability_log_entries acl '
        'LEFT JOIN users m ON acl.manager_id = m.id '
        'LEFT JOIN users s ON acl.staff_id = s.id '
        'ORDER BY acl.timestamp DESC'
    ).fetchall()
    return render_template('ground/logs.html', logs=logs)


## @brief Move an aircraft to a new gate (UC16). Privileged: needs re-auth (UC03) and
#         records an accountability log entry
@bp.route('/move-aircraft', methods=['GET', 'POST'])
@role_required('ground_op_manager')
@reauth_required
def move_aircraft():
    db = get_db()
    if request.method == 'POST':
        aircraft_id = request.form.get('aircraft_id')
        target_gate = request.form.get('target_gate', '').strip()
        reason = request.form.get('reason', '').strip()
        ac = db.execute('SELECT * FROM aircraft WHERE id = ?', (aircraft_id,)).fetchone()
        if ac is None:
            flash('Aircraft not found.', 'danger')
            return redirect(url_for('ground.move_aircraft'))
        db.execute('UPDATE aircraft SET current_position = ? WHERE id = ?',
                   (target_gate, aircraft_id))
        db.execute(
            'INSERT INTO accountability_log_entries '
            '(timestamp, manager_id, staff_id, reason_for_change) VALUES (?, ?, ?, ?)',
            (datetime.now().isoformat(), session['user_id'], session['user_id'],
             f'Moved {ac["registration"]} to {target_gate}: {reason}'),
        )
        db.commit()
        session.pop('reauthed', None)  # consume the re-auth
        flash('Aircraft moved.', 'success')
        return redirect(url_for('ground.move_aircraft'))
    aircraft = db.execute('SELECT * FROM aircraft ORDER BY registration').fetchall()
    return render_template('ground/move_aircraft.html', aircraft=aircraft)


# --- stubbed ground UCs (designed in D2, not implemented this deliverable) ---

## @brief Stub: monitor ground environment (UC15)
@bp.route('/monitor')
@role_required(*GROUND_ROLES)
def monitor():
    return render_template('ground/stub.html', feature='Monitor ground environment (UC15)')


## @brief Stub: move resources (UC17)
@bp.route('/resources')
@role_required('ground_op_manager')
def move_resources():
    return render_template('ground/stub.html', feature='Move resources (UC17)')


## @brief Stub: plan resources (UC18)
@bp.route('/plan')
@role_required('ground_op_manager')
def plan_resources():
    return render_template('ground/stub.html', feature='Plan resources (UC18)')


## @brief Stub: communicate shifts (UC19)
@bp.route('/communicate-shifts')
@role_required('shift_manager')
def communicate_shifts():
    return render_template('ground/stub.html', feature='Communicate shifts (UC19)')
