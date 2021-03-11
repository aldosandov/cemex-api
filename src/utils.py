import jwt
from flask import jsonify, request
import datetime
from functools import wraps
from security.admins import db


def get_secret_key():
    file = open("src/security/secret_key.txt")
    key = file.readline()
    return key 


def get_params(args, token=False):
    args = args.to_dict()
    params = ['dureza', 'tasaprod', 'calidad', 'token']

    if len(args) == 4 and list(args.keys()) == params:
        try:
            hardness = round(float(args[params[0]]), 3)
            prod_rate = round(float(args[params[1]]), 3)
            quality = round(float(args[params[2]]), 3)
            jwt = args[params[3]]
        
            if token:
                return jwt
            else:
                return hardness, prod_rate, quality

        except:
            raise SyntaxError("Values of parameters aren't valid. Only int or float type are allowed. Read API docs.")

    else:
        raise SyntaxError("Parameters are missing or not allowed. Read API docs.")


def check_identity(username, password):
    if username in db["users"] and password in db["passwords"]:
        return True
    else:
        return False


def create_token(username, key):
    token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, key, algorithm="HS256")

    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_params(request.args, token=True)

        if not token:
            return jsonify({'message' : 'Token is missing.'}), 403

        try:
            data = jwt.decode(token, get_secret_key(), algorithms="HS256")
            print(data)
        except:
            return jsonify({'message' : 'Token is invalid.'}), 403

        return f(*args, **kwargs)

    return decorated