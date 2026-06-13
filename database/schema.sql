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
