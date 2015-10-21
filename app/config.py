import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BaseConfig:
    SECRET_KEY = '693bda65112eb4b1eab2bfe3fa8e672ad220fa7c'
    PKYX_MAIL_SENDER = 'PK一下 <tonnie@example.com>'
    PKYX_MAIL_SUBJECT_PREFIX = '[PKYX]'

    @staticmethod
    def init_app(app):
        pass

class DevConfig(BaseConfig):
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'pkyx'
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass

config = {
    'dev': DevConfig,
}