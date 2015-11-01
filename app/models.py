from app.util import bson_obj_id, bson_to_json
from flask import current_app
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

import json

class User(UserMixin):
    def __init__(self, user_id, extras=None):
        self.id = user_id
        if (extras is not None) and isinstance(extras, dict):
            for name, attr in extras.items():
                setattr(self, name, attr)

    @staticmethod
    def gen_passwd_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_passwd(passwd_hash, passwd):
        return check_password_hash(passwd_hash, passwd)

    def gen_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps(bson_to_json({"id": self.id}))

    @staticmethod
    def verify_auth_token(token):
        from app.extensions import mongo
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        dict_ = json.loads(data)
        return mongo.db.users.find_one({"_id": bson_obj_id(dict_['id']["$oid"])})
