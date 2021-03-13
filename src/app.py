from flask import Flask, request, jsonify, make_response
from utils import *


app = Flask(__name__)
app.config['SECRET_KEY'] = get_secret_key()


@app.route("/predict/")
@token_required
def predict():
    try:
        hardness, prod_rate, quality = get_params(request.args)
        res = build_json(hardness, prod_rate, quality)

        return res

    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 400)


@app.route('/login', methods=['POST'])
def login():
    try:
        params = request.get_json()
        username = params['username']
        password = params['password']

        if check_identity(username, password):
            return jsonify({'token' : create_token(username, app.config['SECRET_KEY'])})
        else: 
            raise Exception

    except:
        return make_response(jsonify({'message':'Login error, username or password are missing or not allowed.'}), 401)


if __name__ == '__main__':
    app.run()