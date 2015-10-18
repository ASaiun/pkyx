from flask import json
from bson import json_util, ObjectId

def bson_to_json(data):
    return json.dumps(data, default=json_util.default)

def bson_obj_id(id):
    return ObjectId(id)
