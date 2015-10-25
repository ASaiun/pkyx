#-*- coding:utf-8 -*-
from flask import Flask
from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager
from app.config import config
from app.models import User
from util import bson_obj_id

mongo = PyMongo()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = None
    db_user = mongo.db.users.find_one({"_id": bson_obj_id(user_id)})
    if db_user is not None:
        user_id = db_user.pop('_id')
        user = User(user_id, extras=db_user)
    return user

def create_app(config_name='dev'):
    app = Flask(__name__)
    # 导入配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 初始化MongoDB
    mongo.init_app(app)
    # 初始化Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = '请登录'

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
