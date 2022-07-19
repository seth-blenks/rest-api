import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Basic:
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
    PERSONALTESTING = False

    

class Development(Basic):
    SQLALCHEMY_DATABASE_URI = 'postgresql://privateuser:private@localhost:5432/api'
    ADMIN_EMAIL = 'example@gmail.com'


class Testing(Basic):
    SQLALCHEMY_DATABASE_URI = 'postgresql://privateuser:private@localhost:5432/testsecury'
    PERSONALTESTING = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'admin.sethcodes.com'
    ADMIN_EMAIL = 'chembio451@gmail.com'


class Production(Basic):
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']




configurations = {
    'development': Development,
    'testing': Testing,
    'production': Production
}