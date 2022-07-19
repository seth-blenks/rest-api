from flask_wtf import csrf
from flask_wtf.csrf import validate_csrf as val
from functools import wraps
from wtforms.validators import ValidationError
from flask_login import login_required, current_user
from threading import Thread
from uuid import uuid4
from flask import current_app, abort, redirect, url_for, g, request
from os import path, remove
from database import  sql, User
import logging
import math, random

logger = logging.getLogger('gunicorn.error')


def get_api_user(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		api_key = request.args.get('key')
		if api_key:
			user = User.query.filter_by(api_key = api_key).first()
			if user:
				g.app_user = user
				return f(*args, **kwargs)
		abort(401)
	return wrapper

 
# function to generate OTP
def generateOTP() :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

def validate_csrf(csrf):
	if current_app.config['PERSONALTESTING']:
		return True
		
	try:
		val(csrf)
		return True
	except ValidationError:
		return False

def gen_csrf():
	return csrf.generate_csrf()


def admin_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if not (current_user.is_admin() and current_user.is_authenticated):
			abort(404)
		else:
			return f(*args, **kwargs)

	return wrapper

def password_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated:
			if not current_user.has_password():
				return redirect(url_for('set_password'))	
		return f(*args, **kwargs)
	
	return wrapper


