import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Basic:
    ADMINISTRATOR_USERNAME = 'username'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERSONALTESTING = False
    SECRET_KEY = 'secret key'

    
class Development(Basic):
    SQLALCHEMY_DATABASE_URI = 'postgresql://privateuser:private@localhost:5432/api'
    


class Testing(Basic):
    SQLALCHEMY_DATABASE_URI = 'postgresql://privateuser:private@localhost:5432/api'
    PERSONALTESTING = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'www.testserver.com'
    


class Production(Basic):
    SECRET_KEY = os.environ['SECRET_KEY']
    ADMIN_EMAIL = os.environ['ADMIN_EMAIL'] 
    ADMINISTRATOR_USERNAME = os.environ['ADMINISTRATOR_USERNAME']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']




configurations = {
    'development': Development,
    'testing': Testing,
    'production': Production
}