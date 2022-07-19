import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Basic:
    ADMINISTRATOR_USERNAME = 'username'
    ADMIN_EMAIL = 'example@gmail.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
    GOOGLE_ANALYTICS_PROPERTY_ID = os.environ['GOOGLE_ANALYTICS_PROPERTY_ID']
    PERSONALTESTING = False
    SECRET_KEY = 'secret key'

    
class Development(Basic):
    SQLALCHEMY_DATABASE_URI = 'postgresql://privateuser:private@localhost:5432/api'
    


class Testing(Basic):
    SQLALCHEMY_DATABASE_URI = 'postgresql://privateuser:private@localhost:5432/testsecury'
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