from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.celery import Celery
from app.models import User
from app.util import bson_obj_id

mail = Mail()
mongo = PyMongo()
celery = Celery()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = None
    db_user = mongo.db.users.find_one({"_id": bson_obj_id(user_id)})
    if db_user is not None:
        user_id = db_user.pop('_id')
        user = User(user_id, extras=db_user)
    return user
