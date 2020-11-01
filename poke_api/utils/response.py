from flask import jsonify


def success_response(message: dict, status_code: int = 200):
    response = {
        "data": {**message}
    }
    return jsonify(response), status_code
