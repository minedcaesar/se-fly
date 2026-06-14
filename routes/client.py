# routes facing the clients (dashboard, airport info)

from flask import Blueprint, render_template, current_app

from database.db import get_db
from routes import login_required

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