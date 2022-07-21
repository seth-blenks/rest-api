from flask_sqlalchemy import SQLAlchemy, current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime
from enum import Enum
import bleach
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import logging 
from flask_login import LoginManager

logger = logging.getLogger('gunicorn.error')

sql = SQLAlchemy()

''' The necessary constraints for this database to work are added using the sql language of the specified database.
These constriants include:

cascade:
	images cannot be deleted if other records that depend on them still exists
	Blogs can be delete
	Users can be deleted along with their articles and images

In other to implement Full Text Search the necessary code is added using sql language in the specified database

'''

class PERMISSION:
	ADMIN = 4
	USER = 2
	VISITOR = 0



class Role(sql.Model):
	__tablename__ = 'role'
	__table_args__ = {"schema":"api"}
	id = sql.Column(sql.Integer, primary_key = True, autoincrement = True)
	name = sql.Column(sql.String(32), unique  = True)
	permission = sql.Column(sql.Integer)


	@classmethod
	def setup(self):
		permissions = [
			{
			'name': 'admin',
			'permission': PERMISSION.ADMIN,
			},
			{
			'name': 'user',
			'permission': PERMISSION.USER,
			},
			{
			'name': 'visitor',
			'permission': PERMISSION.VISITOR
			}
		]

		for perm in permissions:
			entry = Role(name = perm['name'], permission = perm['permission'])
			sql.session.add(entry)
			sql.session.commit()



class User(sql.Model, UserMixin):
	__tablename__ = 'webuser'
	__table_args__ = {"schema":"api"}
	id = sql.Column(sql.Integer, primary_key = True, autoincrement = True)
	username = sql.Column(sql.String(112))
	email = sql.Column(sql.String(112), unique = True)
	authenticated = sql.Column(sql.Boolean, default = False)
	restricted = sql.Column(sql.Boolean, default = False)
	public_key = sql.Column(sql.String(250), unique = True)
	private_key = sql.Column(sql.String(250), unique = True)
	_password = sql.Column(sql.String(225))
	role_id = sql.Column(sql.Integer, sql.ForeignKey('role.id'))
	role = sql.relationship('Role')

	def __init__(self, *args, **kwargs):
		sql.Model.__init__(self, *args, **kwargs)

		logger.info('creating user')

		if not self.role:
			logger.info(f'User has no role {self.role}')
			
			if self.email == current_app.config['ADMIN_EMAIL']:
				
				logger.info('user email is email of admin.')
				role = Role.query.filter_by(name='admin').first()

				logger.info(f'User role is now set to {self.role}')
				self.role = role

			else:
				role = Role.query.filter_by(name = 'user').first()
				self.role = role
				logger.info(f'adding user role to this user {self.role}')
		else:
			logger.info(f'User has role {self.role}')



	def can(self, perm):
		logger.info(f'Checking if user has permission value equal to or greater than {perm}')
		logger.info(self.username)
		logger.info(self.role)
		
		user_can = self.role.permission >= perm
		logger.info(user_can)
		return user_can


	def is_admin(self):
		logger.info(f'Checking if user is admin')
		user_is_admin = self.role.permission == PERMISSION.ADMIN
		logger.info(user_is_admin)
		return user_is_admin

	@property
	def password(self):
		raise AttributeError('Password is not readable')

	@password.setter
	def password(self, value):
		self._password = generate_password_hash(value)

	def check_password(self, password):
		return check_password_hash(self._password, password)

	def has_password(self):
		if self._password != None:
			return True
		return False

	@property
	def is_authenticated(self):
		return True

	def generate_confirmation_token(self, expiration = 3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirmation': self.id}).decode('utf8')

	def confirm_token(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf8'))
		except:
			return False

		if data.get('confirmation') != self.id:
			return False

		return True






class Visitor(AnonymousUserMixin):
	def can(self, perm):
		return False

	def is_admin(self):
		return False



class Employees(sql.Model):
	__tablename__ = 'employee'
	__table_args__ = {"schema":"api"}
	id = sql.Column(sql.Integer, primary_key = True, autoincrement = True)
	employee_id = sql.Column(sql.Integer, unique = True)
	first_name = sql.Column(sql.String(225))
	last_name = sql.Column(sql.String(200))
	email = sql.Column(sql.String(200))
	phone_number = sql.Column(sql.String(200))
	hire_date = sql.Column(sql.DateTime)
	job_id = sql.Column(sql.String(100))
	salary = sql.Column(sql.Integer)
	manager_id = sql.Column(sql.Integer)
	department_id = sql.Column(sql.Integer)





login_manager = LoginManager()
login_manager.login_view = 'window.login'
login_manager.login_message = 'login to continue'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

