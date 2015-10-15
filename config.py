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
    MONGO_HOST = '10.211.55.5'
    MONGO_PORT = 27107

config = {
    'dev': DevConfig,
}