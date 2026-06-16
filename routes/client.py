## @file client.py
#  @brief Client-facing routes: dashboard, airport info, flight board, amenities,
#         assistance and profile (UC04–UC07).

from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template,
    request, session, url_for, current_app,
)

from database.db import get_db
from routes import login_required, role_required

bp = Blueprint('client', __name__)


## @brief Client home page.
@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('client/dashboard.html')


## @brief Public airport information page (UC04): map, parking, regulations.
@bp.route('/info')
def info():
    db = get_db()
    rows = db.execute('SELECT key, content, content_type FROM airport_content').fetchall()
    content = {row['key']: row for row in rows}
    return render_template('client/info.html', content=content)


## @brief Public flight board (UC04): departures and arrivals for this airport.
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


## @brief List amenities and start a purchase (UC05).
#  GET lists active amenities; POST records a pending purchase and goes to mock payment.
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
        # production: hand off to PaymentProvider.processTransaction(...) and redirect to its url.
        return redirect(url_for('client.mock_payment', amenity_id=amenity_id))
    items = db.execute('SELECT * FROM amenities WHERE is_active = 1').fetchall()
    return render_template('client/amenities.html', amenities=items)


## @brief Mock payment confirmation: flip the pending purchase to confirmed (UC05).
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


## @brief Submit a special-assistance request (UC06).
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
        if not db.execute(
            'SELECT 1 FROM flight_schedules WHERE flight_number = ?', (flight_num,)
        ).fetchone():
            flash('Flight number not found.', 'danger')
            return redirect(url_for('client.assistance'))
        db.execute(
            'INSERT INTO assistance_requests (user_id, type, flight_num, is_fulfilled, created_at) '
            'VALUES (?, ?, ?, 0, ?)',
            (session['user_id'], a_type, flight_num, datetime.now().isoformat()),
        )
        db.commit()
        flash('Assistance request submitted.', 'success')
        return redirect(url_for('client.dashboard'))
    db = get_db()
    flights = db.execute(
        'SELECT DISTINCT fs.flight_number FROM flight_schedules fs '
        'JOIN flight_instances fi ON fi.schedule_id = fs.id '
        'ORDER BY fs.flight_number'
    ).fetchall()
    types = ['WheelchairService', 'PriorityBoarding', 'UnaccompaniedMinor']
    return render_template('client/assistance.html', assistance_types=types, flights=flights)


## @brief View and edit the client's profile (UC07).
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('client')
def profile():
    db = get_db()
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        dob = request.form.get('dob', '').strip()
        if not full_name:
            flash('Name cannot be empty.', 'danger')
            return redirect(url_for('client.profile'))
        db.execute('UPDATE users SET full_name = ?, dob = ? WHERE id = ?',
                   (full_name, dob, session['user_id']))
        db.commit()
        session['full_name'] = full_name
        flash('Profile updated.', 'success')
        return redirect(url_for('client.profile'))
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    purchases = db.execute(
        'SELECT ap.*, a.name, a.type, a.price '
        'FROM amenity_purchases ap JOIN amenities a ON ap.amenity_id = a.id '
        'WHERE ap.user_id = ? ORDER BY ap.purchased_at DESC',
        (session['user_id'],),
    ).fetchall()
    return render_template('client/profile.html', user=user, purchases=purchases)
