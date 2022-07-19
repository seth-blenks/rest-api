from . import window
from flask import render_template, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
from flask import jsonify
from ..utils import gen_api_keys
from logging import getLogger
from database import User, sql


logger = getLogger('gunicorn.error')

@window.route('/')
def homepage():
    return render_template('homepage.html')



@window.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user = current_user._get_current_object())



@window.route('/login', methods =  ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    logger.info(f'window.login {email} : {password}')
    if email and password:
        user = User.query.filter_by(email = email).first()
        if user:
            if user.check_password(password):
                user.authenticated = True
                login_user(user, True)
                return jsonify('User has been logged in'), 200

    return jsonify('Login Failed for user'), 401

@window.route('/register', methods = ['POST'])
def register():
    email = request.form.get('email')
    if User.query.filter_by(email = email).first():
        logger.info(f'window.register {email} found in database already')
        return jsonify('This email is already in use. Login Instead!'), 401

    username = request.form.get('username')
    password = request.form.get('password')
    public_key, private_key = gen_api_keys()
    user = User(
        username = username,
        email = email,
        public_key = public_key,
        private_key = private_key
        )

    logger.info(f'window.register {username} : {password} : {public_key} : {private_key}')
    user.password = password

    sql.session.add(user)
    sql.session.commit()
    return jsonify('User Registered'), 201

    return render_template('register.html')

@window.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('window.homepage'))

