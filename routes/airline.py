# UC09 - See Flight Schedule
# Read-only schedule list for airlines' staff members
# UC10 - Add Schedule
# Allows the authorised manager to insert new schedules
# UC11 - Remove Schedule
# Allows the authorised manager to delete already present schedules
# UC12 - Access Schedule Logs
# Permits only authorised personnel to access data


from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,
)

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
# Expanded query utilizing scalar subqueries to calculate instance metrics - UC09
@role_required('airline_staff', 'airline_manager')
def schedules():
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    airline = db.execute('SELECT * FROM airlines WHERE name = ?', (user['airline'],)).fetchone()
    rows = []
    if airline:
        # Fetch schedules alongside a count of active physical flight instances
        rows = db.execute(
            'SELECT fs.*, '
            '(SELECT COUNT(*) FROM flight_instances fi WHERE fi.schedule_id = fs.id) AS instance_count '
            'FROM flight_schedules fs WHERE fs.airline_id = ? ORDER BY fs.flight_number',
            (airline['id'],),
        ).fetchall()
    return render_template('airline/schedules.html', schedules=rows, airline=airline)


@bp.route('/schedules/add', methods=['GET', 'POST'])
# Interface handling schema validation and record execution - UC10
@role_required('airline_staff', 'airline_manager')
def add_schedule():
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if request.method == 'POST':
        # Sanitize incoming text inputs to conform with structural constraints
        flight_number = request.form.get('flight_number', '').strip().upper()
        origin = request.form.get('origin', '').strip().upper()
        destination = request.form.get('destination', '').strip().upper()
        recurrence_rule = request.form.get('recurrence_rule', 'DAILY')

        # Implement parameter integrity assertions
        error = None
        if not flight_number:
            error = 'Flight number is required.'
        elif not origin or not destination:
            error = 'Origin and destination are required.'
        elif origin == destination:
            error = 'Origin and destination must differ.'
        if error is None and db.execute('SELECT id FROM flight_schedules WHERE flight_number = ?',
                                        (flight_number,)).fetchone():
            error = f'Flight number {flight_number} already exists.'

        airline = db.execute('SELECT id FROM airlines WHERE name = ?', (user['airline'],)).fetchone()
        if error is None and airline is None:
            error = 'Your account is not linked to a valid airline.'

        if error is None:
            # Commit the baseline flight sequence mapping entry to database state
            db.execute(
                'INSERT INTO flight_schedules '
                '(airline_id, created_by, flight_number, origin, destination, recurrence_rule) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (airline['id'], session['user_id'], flight_number, origin, destination, recurrence_rule),
            )
            # System automatically writes a persistent record to the security log table - UC11
            db.execute(
                'INSERT INTO audit_log_entries (timestamp, user_id, flight_id, action_performed) '
                'VALUES (?, ?, ?, ?)',
                (datetime.now().isoformat(), session['user_id'], flight_number, 'ADDED'),
            )
            db.commit()
            flash(f'Schedule {flight_number} added.', 'success')
            return redirect(url_for('airline.schedules'))
        flash(error, 'danger')

    return render_template('airline/add_schedule.html',
                           recurrence_options=['DAILY', 'WEEKLY', 'SPECIFIC_DAYS'])


@bp.route('/schedules/<int:schedule_id>/delete', methods=['POST'])
# Standard entry removal module with administrative verification - UC10
@role_required('airline_staff', 'airline_manager')
def delete_schedule(schedule_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    airline = db.execute('SELECT id FROM airlines WHERE name = ?', (user['airline'],)).fetchone()
    schedule = db.execute('SELECT * FROM flight_schedules WHERE id = ?', (schedule_id,)).fetchone()

    # Assert relational scope ownership parameters before execution
    if schedule is None or (airline and schedule['airline_id'] != airline['id']):
        flash('Schedule not found or access denied.', 'danger')
        return redirect(url_for('airline.schedules'))

    db.execute('DELETE FROM flight_schedules WHERE id = ?', (schedule_id,))

    # Structural deletion security assertion record append - UC11
    db.execute(
        'INSERT INTO audit_log_entries (timestamp, user_id, flight_id, action_performed) '
        'VALUES (?, ?, ?, ?)',
        (datetime.now().isoformat(), session['user_id'], schedule['flight_number'], 'DELETED'),
    )
    db.commit()
    flash(f'Schedule {schedule["flight_number"]} deleted.', 'success')
    return redirect(url_for('airline.schedules'))


# Administrative access-controlled view module tracking operational change history - UC12
@bp.route('/logs')
@role_required('airline_manager')
def audit_logs():
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    airline = db.execute('SELECT id FROM airlines WHERE name = ?', (user['airline'],)).fetchone()
    logs = []
    if airline:
        logs = db.execute(
            'SELECT ale.*, u.full_name AS actor_name '
            'FROM audit_log_entries ale '
            'LEFT JOIN users u ON ale.user_id = u.id '
            'WHERE ale.flight_id IN ('
            '    SELECT flight_number FROM flight_schedules WHERE airline_id = ?'
            ') ORDER BY ale.timestamp DESC',
            (airline['id'],),
        ).fetchall()
    return render_template('airline/audit_logs.html', logs=logs)