from flask import Flask
from .utils.libraries import  login_manager
from .utils.tools import mailer
from .config import configurations
from database import sql
from .views import client

client_app = Flask(__name__)


def create_app(config):
    client_app.config.from_object(configurations[config])
    sql.init_app(client_app)
    login_manager.init_app(client_app)
    mailer.init_app(client_app)
    client_app.register_blueprint(client)
    
    return client_app