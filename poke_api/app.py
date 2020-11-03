from flask import Flask, Blueprint, jsonify, request
from .utils.response import success_response
from .models import db
from .models.migrate import run_migrations
from .config import settings
from .search import search_me

pokemon_bp = Blueprint('pokemon', __name__)


@pokemon_bp.route('/')
def ping():
    result = {
        "msg": "I'm alive"
    }
    return success_response(result)


@pokemon_bp.route('/pokemon')
def get_pokemon():
    request_arguments = {k.lower(): v for k, v in request.args.items()}
    result = {
        "msg": "Hello, Pokemon!"
    }
    # result = search_me(request_arguments)
    return success_response(result)


def create_app(migrate: bool = False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.register_blueprint(pokemon_bp)
    db.init_app(app)

    if migrate:
        run_migrations(app)

    return app
