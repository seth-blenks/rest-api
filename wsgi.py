from main import create_app as api
from window import create_app as window
from database import sql, User, Role
import os
from flask import current_app

api_server = api('development')
window_server = window('development')

@window_server.cli.command('setup')
def setup():
	Role.setup()
	admin_user = User(username= current_app.config['ADMINISTRATOR_USERNAME'], email = current_app.config['ADMIN_EMAIL'])
	sql.session.add(admin_user)
	sql.session.commit()


def run_app(environ, start_response):
	path = environ['PATH_INFO']
	if path.startswith('/api/'):
		return api_server(environ, start_response)
	else:
		return window_server(environ, start_response)
