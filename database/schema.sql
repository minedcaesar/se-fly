-- FLY Airport Management System — SQLite schema

CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    role        TEXT NOT NULL,
    full_name   TEXT,
    email       TEXT UNIQUE NOT NULL,
    password    TEXT,
    oauth_token TEXT,
    dob         TEXT,
    airline     TEXT,
    terminal    TEXT,
    is_active   INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS sessions (
    id              TEXT PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    device_id       TEXT,
    login_timestamp TEXT NOT NULL,
    is_active       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS airlines (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS flight_schedules (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    airline_id      INTEGER NOT NULL REFERENCES airlines(id),
    created_by      INTEGER REFERENCES users(id),
    flight_number   TEXT NOT NULL UNIQUE,
    origin          TEXT NOT NULL,
    destination     TEXT NOT NULL,
    recurrence_rule TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS flight_instances (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id              INTEGER NOT NULL REFERENCES flight_schedules(id),
    scheduled_departure_time TEXT NOT NULL,
    scheduled_arrival_time   TEXT NOT NULL,
    actual_departure_time    TEXT,
    actual_arrival_time      TEXT,
    status                   TEXT NOT NULL DEFAULT 'Scheduled'
);

CREATE TABLE IF NOT EXISTS aircraft (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    airline_id       INTEGER REFERENCES airlines(id),
    registration     TEXT NOT NULL UNIQUE,
    model            TEXT NOT NULL,
    capacity         INTEGER NOT NULL,
    current_status   TEXT NOT NULL DEFAULT 'active',
    current_position TEXT
);

CREATE TABLE IF NOT EXISTS terminals (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS gates (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    terminal_id  INTEGER REFERENCES terminals(id),
    gate_code    TEXT NOT NULL UNIQUE,
    is_available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS operation_plans (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_instance_id INTEGER REFERENCES flight_instances(id),
    created_by         INTEGER REFERENCES users(id),
    status             TEXT NOT NULL DEFAULT 'Draft'
);

CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id     INTEGER NOT NULL REFERENCES operation_plans(id),
    task_type   TEXT NOT NULL,
    name        TEXT NOT NULL,
    start_time  TEXT NOT NULL,
    end_time    TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'Pending',
    assigned_to INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS subtasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id      INTEGER NOT NULL REFERENCES tasks(id),
    name         TEXT NOT NULL,
    is_completed INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS shifts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    published_by INTEGER REFERENCES users(id),
    terminal     TEXT,
    start_time   TEXT NOT NULL,
    end_time     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS amenities (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    type      TEXT NOT NULL,
    name      TEXT NOT NULL,
    price     REAL NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS amenity_purchases (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER REFERENCES users(id),
    amenity_id   INTEGER NOT NULL REFERENCES amenities(id),
    status       TEXT NOT NULL DEFAULT 'pending',
    purchased_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assistance_requests (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER REFERENCES users(id),
    type         TEXT NOT NULL,
    flight_num   TEXT NOT NULL,
    is_fulfilled INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log_entries (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp        TEXT NOT NULL,
    user_id          INTEGER REFERENCES users(id),
    flight_id        TEXT NOT NULL,
    action_performed TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accountability_log_entries (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp         TEXT NOT NULL,
    manager_id        INTEGER REFERENCES users(id),
    staff_id          INTEGER REFERENCES users(id),
    reason_for_change TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS airport_content (
    key          TEXT PRIMARY KEY,
    content      TEXT NOT NULL DEFAULT '',
    content_type TEXT NOT NULL DEFAULT 'text/plain',
    updated_at   TEXT NOT NULL
);
