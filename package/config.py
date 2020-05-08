class Config(object):
    SECRET_KEY = 'some sort of secret key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tomobase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # flask-security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'