from main import create_app as api
from window import create_app as window
from database import sql, User, Role
import os
from flask import current_app

api_server = api('production')
window_server = window('production')

@window_server.cli.command('setup')
def setup():
	Role.setup()



def run_app(environ, start_response):
	path = environ['PATH_INFO']
	if path.startswith('/api/'):
		return api_server(environ, start_response)
	else:
		return window_server(environ, start_response)
