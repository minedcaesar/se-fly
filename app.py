from flask import Flask
from config import Config

from database.db import init_app
from routes.auth import bp as auth_bp
from routes.client import bp as client_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    return app


app = create_app()