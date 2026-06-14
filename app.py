from flask import Flask
from config import Config
from database.db import init_app
from routes.auth import bp as auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)
    app.register_blueprint(auth_bp)
    return app


app = create_app()
