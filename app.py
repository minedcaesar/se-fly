from flask import Flask
from config import Config

# database
from database.db import init_app
 
# routes
from routes.auth import bp as auth_bp
from routes.client import bp as client_bp
from routes.airline import bp as airline_bp
from routes.admin import bp as admin_bp


# application
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # initializing
    init_app(app)
    # registering application routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(airline_bp)
    app.register_blueprint(admin_bp)
    return app


# instancing the app
app = create_app()