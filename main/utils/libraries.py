### FLASK LOGIN SETUP ###
from flask_login import LoginManager
from database import User
from logging import getLogger

logger = getLogger('gunicorn.error')

login_manager = LoginManager()
@login_manager.request_loader
def load_user(request):
	api_key = request.args.get('key')
	logger.info(f'The api key: {api_key}')
	if api_key:
		user = User.query.filter_by(api_key = api_key).first()
		logger.info(f'The user {user}')
		if user:
			return user

	return None
