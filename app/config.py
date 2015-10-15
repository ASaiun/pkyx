import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

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

config = {
    'dev': DevConfig,
}