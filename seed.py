## @file seed.py
#  @brief Sample data for local testing / demo.
#  Run after creating the schema:
#    flask --app app init-db
#    python seed.py

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from app import app
from database.db import get_db


## @brief Insert demo accounts and reference data into the database.
def seed():
    db = get_db()

    db.execute("INSERT INTO airlines (name, country) VALUES ('ITA Airways', 'Italy')")
    db.execute("INSERT INTO airlines (name, country) VALUES ('Lufthansa', 'Germany')")

    # staff (password = 'password' for every demo account)
    pw = generate_password_hash('password')
    db.execute("INSERT INTO users (role, full_name, email, password) VALUES "
               "('admin', 'Ada Admin', 'admin@fly.local', ?)", (pw,))
    db.execute("INSERT INTO users (role, full_name, email, password, airline) VALUES "
               "('airline_manager', 'Mara Manager', 'manager@ita.local', ?, 'ITA Airways')", (pw,))
    db.execute("INSERT INTO users (role, full_name, email, password, airline) VALUES "
               "('airline_staff', 'Sam Schedule', 'staff@ita.local', ?, 'ITA Airways')", (pw,))
    db.execute("INSERT INTO users (role, full_name, email, password, terminal) VALUES "
               "('ground_op_manager', 'Gio Ground', 'ground@fly.local', ?, 'T1')", (pw,))
    db.execute("INSERT INTO users (role, full_name, email, password, terminal) VALUES "
               "('operation_staff', 'Otto Ops', 'ops@fly.local', ?, 'T1')", (pw,))

    # a client (oauth, no password)
    db.execute("INSERT INTO users (role, full_name, email, oauth_token, dob) VALUES "
               "('client', 'Cleo Client', 'cleo@example.com', 'mock-oauth-token', '1995-04-12')")

    db.execute("INSERT INTO amenities (type, name, price) VALUES ('FastTrack', 'Fast Track Security', 12.0)")
    db.execute("INSERT INTO amenities (type, name, price) VALUES ('LoungeAccess', 'Lounge Access', 35.0)")
    db.execute("INSERT INTO amenities (type, name, price) VALUES ('LineSkip', 'Priority Line', 8.0)")

    now = datetime.now().isoformat()
    db.execute("INSERT INTO airport_content (key, content, updated_at) VALUES "
               "('parking', 'Short-stay P1 and long-stay P3 open 24/7.', ?)", (now,))
    db.execute("INSERT INTO airport_content (key, content, updated_at) VALUES "
               "('regulations', 'Liquids limited to 100ml. Arrive 2h before departure.', ?)", (now,))

    db.execute("INSERT INTO terminals (name) VALUES ('T1')")
    db.execute("INSERT INTO gates (terminal_id, gate_code) VALUES (1, 'A1')")
    db.execute("INSERT INTO gates (terminal_id, gate_code) VALUES (1, 'A2')")
    db.execute("INSERT INTO aircraft (airline_id, registration, model, capacity, current_position) "
               "VALUES (1, 'EI-ABC', 'Airbus A320', 180, 'A1')")

    # flight schedule + instance (origin TN -> shows on the departures board)
    db.execute("INSERT INTO flight_schedules (airline_id, created_by, flight_number, origin, destination, recurrence_rule) "
               "VALUES (1, 3, 'AZ123', 'TN', 'FCO', 'DAILY')")
    dep = (datetime.now() + timedelta(hours=3)).isoformat()
    arr = (datetime.now() + timedelta(hours=4)).isoformat()
    db.execute("INSERT INTO flight_instances (schedule_id, scheduled_departure_time, scheduled_arrival_time) "
               "VALUES (1, ?, ?)", (dep, arr))

    # a shift for the operation staff (user id 5), published by the ground manager (id 4)
    start = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    db.execute("INSERT INTO shifts (user_id, published_by, terminal, start_time, end_time) "
               "VALUES (5, 4, 'T1', ?, ?)", (start.isoformat(), (start + timedelta(hours=8)).isoformat()))

    db.commit()
    print('Seeded sample data.')


if __name__ == '__main__':
    with app.app_context():
        seed()
