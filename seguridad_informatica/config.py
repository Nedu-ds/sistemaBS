class Config(object):
    SECRET_KEY = 'MFRSTWBPG@PYTHN'

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/accesos'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
