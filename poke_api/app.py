from flask import Flask, jsonify
from .utils.response import success_response


app = Flask(__name__)


@app.route('/')
def ping():
    result = {
        "msg": "I'm alive"
    }
    return success_response(result)


@app.route('/pokemon')
def get_pokemon():
    result = {
        "msg": "Hello, Pokemon!"
    }
    return success_response(result)
