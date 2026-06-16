## @file airline.py
#  @brief Airline staff routes: view / add / remove flight schedules + audit log (UC09–UC12)

from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,
)

from database.db import get_db
from routes import role_required

bp = Blueprint('airline', __name__, url_prefix='/airline')


## @brief Airline staff home page
@bp.route('/')
@role_required('airline_staff', 'airline_manager')
def dashboard():
    return render_template('airline/dashboard.html')


## @brief List the staff member's airline schedules with their instance counts (UC09)
@bp.route('/schedules')
@role_required('airline_staff', 'airline_manager')
def schedules():
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    airline = db.execute('SELECT * FROM airlines WHERE name = ?', (user['airline'],)).fetchone()
    rows = []
    instances = {}
    if airline:
        rows = db.execute(
            'SELECT fs.*, '
            '(SELECT COUNT(*) FROM flight_instances fi WHERE fi.schedule_id = fs.id) AS instance_count '
            'FROM flight_schedules fs WHERE fs.airline_id = ? ORDER BY fs.flight_number',
            (airline['id'],),
        ).fetchall()
        all_instances = db.execute(
            'SELECT fi.* FROM flight_instances fi '
            'JOIN flight_schedules fs ON fi.schedule_id = fs.id '
            'WHERE fs.airline_id = ? ORDER BY fi.scheduled_departure_time',
            (airline['id'],),
        ).fetchall()
        for inst in all_instances:
            instances.setdefault(inst['schedule_id'], []).append(inst)
    return render_template('airline/schedules.html', schedules=rows, instances=instances, airline=airline)


## @brief Add a flight schedule (UC10): validate, insert, and write an audit log entry
@bp.route('/schedules/add', methods=['GET', 'POST'])
@role_required('airline_staff', 'airline_manager')
def add_schedule():
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if request.method == 'POST':
        flight_number = request.form.get('flight_number', '').strip().upper()
        origin = request.form.get('origin', '').strip().upper()
        destination = request.form.get('destination', '').strip().upper()
        recurrence_rule = request.form.get('recurrence_rule', 'DAILY')
        departure_datetime = request.form.get('departure_datetime', '').strip()
        arrival_datetime = request.form.get('arrival_datetime', '').strip()

        error = None
        if not flight_number:
            error = 'Flight number is required.'
        elif not origin or not destination:
            error = 'Origin and destination are required.'
        elif origin == destination:
            error = 'Origin and destination must differ.'
        elif not departure_datetime or not arrival_datetime:
            error = 'Departure and arrival date/time are required.'
        elif arrival_datetime <= departure_datetime:
            error = 'Arrival must be after departure.'
        if error is None and db.execute('SELECT id FROM flight_schedules WHERE flight_number = ?',
                                        (flight_number,)).fetchone():
            error = f'Flight number {flight_number} already exists.'

        airline = db.execute('SELECT id FROM airlines WHERE name = ?', (user['airline'],)).fetchone()
        if error is None and airline is None:
            error = 'Your account is not linked to a valid airline.'

        if error is None:
            cur = db.execute(
                'INSERT INTO flight_schedules '
                '(airline_id, created_by, flight_number, origin, destination, recurrence_rule) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (airline['id'], session['user_id'], flight_number, origin, destination, recurrence_rule),
            )
            db.execute(
                'INSERT INTO flight_instances (schedule_id, scheduled_departure_time, scheduled_arrival_time) '
                'VALUES (?, ?, ?)',
                (cur.lastrowid, departure_datetime, arrival_datetime),
            )
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


## @brief Remove a flight schedule (UC11): owner-checked delete + audit log entry
#  @param schedule_id  Schedule to delete
@bp.route('/schedules/<int:schedule_id>/delete', methods=['POST'])
@role_required('airline_staff', 'airline_manager')
def delete_schedule(schedule_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    airline = db.execute('SELECT id FROM airlines WHERE name = ?', (user['airline'],)).fetchone()
    schedule = db.execute('SELECT * FROM flight_schedules WHERE id = ?', (schedule_id,)).fetchone()
    if schedule is None or (airline and schedule['airline_id'] != airline['id']):
        flash('Schedule not found or access denied.', 'danger')
        return redirect(url_for('airline.schedules'))

    db.execute('DELETE FROM flight_schedules WHERE id = ?', (schedule_id,))
    db.execute(
        'INSERT INTO audit_log_entries (timestamp, user_id, flight_id, action_performed) '
        'VALUES (?, ?, ?, ?)',
        (datetime.now().isoformat(), session['user_id'], schedule['flight_number'], 'DELETED'),
    )
    db.commit()
    flash(f'Schedule {schedule["flight_number"]} deleted.', 'success')
    return redirect(url_for('airline.schedules'))


## @brief Manager-only audit log for this airline's schedule changes (UC12)
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
