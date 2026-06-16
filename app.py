## @file app.py
#  @brief Application factory: builds the Flask app, wires the database, registers blueprints.

from flask import Flask
from config import Config
from database.db import init_app
from routes.auth import bp as auth_bp
from routes.client import bp as client_bp
from routes.airline import bp as airline_bp
from routes.admin import bp as admin_bp
from routes.ground import bp as ground_bp


## @brief Create and configure the Flask application.
#  @return the configured app instance.
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(airline_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(ground_bp)
    return app


app = create_app()
