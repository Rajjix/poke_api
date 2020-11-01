from flask import Flask, Blueprint, jsonify
from .utils.response import success_response
from .models import db
from .models.migrate import run_migrations
from .config import settings


pokemon_bp = Blueprint('pokemon', __name__)


@pokemon_bp.route('/')
def ping():
    result = {
        "msg": "I'm alive"
    }
    return success_response(result)


@pokemon_bp.route('/pokemon')
def get_pokemon():
    result = {
        "msg": "Hello, Pokemon!"
    }
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
