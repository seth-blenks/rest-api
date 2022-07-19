from flask import Blueprint

window = Blueprint('window', __name__, static_folder = 'assets')

from . import views

window.app_errorhandler(401)
def handle_401(e):
    return jsonify('You are not authorized to access this page'), 401