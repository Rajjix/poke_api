from flask import jsonify
from typing import Union

def success_response(response: Union[dict, list], status_code: int = 200):
    return jsonify(response), status_code
