__author__ = 'tonnie.lwt@gmail.com'

from flask import Flask
from flask.ext.pymongo import PyMongo
from app.config import config

mongo = PyMongo()

def create_app(config_name='dev'):
    app = Flask(__name__)
    # 导入配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 初始化MongoDB
    mongo.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app