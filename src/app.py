from flask import Flask, request, jsonify, make_response
from utils import get_params


app = Flask(__name__)


@app.route("/predict/")
def predict():
    try:
        hardness, prod_rate, quality = get_params(request.args)
        return f'dureza: {hardness}, prod_rate: {prod_rate}, calidad: {quality}'

    except Exception as e:
        #print(isinstance(e, SyntaxError))
        return make_response(jsonify({"message": str(e)}), 400)


@app.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    username = params['username']
    password = params['password']
    
    # https://www.youtube.com/watch?v=J5bIPtEbS0Q&t=495s
    return jsonify({"token": "13565456"})


if __name__ == '__main__':
    app.run(debug=True, port=4000)