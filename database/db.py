## @file db.py
#  @brief SQLite connection handling and the init-db CLI command.

import sqlite3
import click
from flask import current_app, g


## @brief Return the per-request database connection (cached on Flask's g).
#  @return an sqlite3 connection with row access by name and foreign keys enforced.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


## @brief Close the request's database connection, if one was opened.
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


## @brief Create the schema by executing schema.sql.
def init_db():
    db = get_db()
    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


## @brief `flask init-db` command: (re)create the database from the schema.
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database initialised.')


## @brief Register the teardown handler and CLI command on the app.
#  @param app  The Flask application.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)