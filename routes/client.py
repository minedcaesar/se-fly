# routes facing the clients (dashboard, airport info)

from flask import (Blueprint, flash, redirect, render_template, request, session, url_for, current_app)

from database.db import get_db
from routes import login_required, role_required

from datetime import datetime

bp = Blueprint('client', __name__)


@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('client/dashboard.html')


@bp.route('/info')
def info():
    db = get_db()
    rows = db.execute('SELECT key, content, content_type FROM airport_content').fetchall()
    content = {row['key']: row for row in rows}
    return render_template('client/info.html', content=content)


@bp.route('/flights')
def flights():
    db = get_db()
    iata = current_app.config['AIRPORT_IATA_CODE']
    departures = db.execute(
        'SELECT fi.*, fs.flight_number, fs.origin, fs.destination '
        'FROM flight_instances fi JOIN flight_schedules fs ON fi.schedule_id = fs.id '
        'WHERE fs.origin = ? ORDER BY fi.scheduled_departure_time', (iata,),
    ).fetchall()
    arrivals = db.execute(
        'SELECT fi.*, fs.flight_number, fs.origin, fs.destination '
        'FROM flight_instances fi JOIN flight_schedules fs ON fi.schedule_id = fs.id '
        'WHERE fs.destination = ? ORDER BY fi.scheduled_arrival_time', (iata,),
    ).fetchall()
    return render_template('client/flights.html', departures=departures, arrivals=arrivals)


@bp.route('/amenities', methods=['GET', 'POST'])
@login_required
@role_required('client')
def amenities():
    db = get_db()
    if request.method == 'POST':
        amenity_id = request.form.get('amenity_id')
        amenity = db.execute('SELECT * FROM amenities WHERE id = ? AND is_active = 1',
                             (amenity_id,)).fetchone()
        if amenity is None:
            flash('Amenity not found.', 'danger')
            return redirect(url_for('client.amenities'))
        db.execute(
            'INSERT INTO amenity_purchases (user_id, amenity_id, status, purchased_at) '
            'VALUES (?, ?, ?, ?)',
            (session['user_id'], amenity_id, 'pending', datetime.now().isoformat()),
        )
        db.commit()
        # hands off to payment provider, then redirects to url
        return redirect(url_for('client.mock_payment', amenity_id=amenity_id))
    items = db.execute('SELECT * FROM amenities WHERE is_active = 1').fetchall()
    return render_template('client/amenities.html', amenities=items)


@bp.route('/mock-payment')
@login_required
def mock_payment():
    amenity_id = request.args.get('amenity_id')
    db = get_db()
    if amenity_id:
        db.execute(
            "UPDATE amenity_purchases SET status = 'confirmed' "
            "WHERE user_id = ? AND amenity_id = ? AND status = 'pending'",
            (session['user_id'], amenity_id),
        )
        db.commit()
    flash('Payment confirmed! Enjoy your amenity.', 'success')
    return redirect(url_for('client.amenities'))


@bp.route('/assistance', methods=['GET', 'POST'])
@login_required
@role_required('client')
def assistance():
    if request.method == 'POST':
        a_type = request.form.get('type', '').strip()
        flight_num = request.form.get('flight_num', '').strip()
        if not a_type or not flight_num:
            flash('All fields are required.', 'danger')
            return redirect(url_for('client.assistance'))
        db = get_db()
        db.execute(
            'INSERT INTO assistance_requests (user_id, type, flight_num, is_fulfilled, created_at) '
            'VALUES (?, ?, ?, 0, ?)',
            (session['user_id'], a_type, flight_num, datetime.now().isoformat()),
        )
        db.commit()
        flash('Assistance request submitted.', 'success')
        return redirect(url_for('client.dashboard'))
    types = ['WheelchairService', 'PriorityBoarding', 'UnaccompaniedMinor']
    return render_template('client/assistance.html', assistance_types=types)