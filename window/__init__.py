from flask import Flask
from .config import configurations
from database import sql, login_manager
from .views import window
from flask_wtf import CSRFProtect

window_app = Flask(__name__, static_folder='assets')


def create_app(config):
    window_app.config.from_object(configurations[config])
    sql.init_app(window_app)
    login_manager.init_app(window_app)
    window_app.register_blueprint(window)
    CSRFProtect(window_app) # X-CSRFToken = {{csrf_token()}}

    return window_app