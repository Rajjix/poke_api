from flask import Flask, Blueprint, jsonify, request
from .utils.response import success_response
from .models import db
from .models.migrate import run_migrations
from .config import settings
from .search import LHSParser, NameParser, PokemonQueryModel

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/')
def ping():
    result = {
        "msg": "I'm alive"
    }
    return success_response(result)


@pokemon_bp.route('/pokemon')
def get_pokemon():
    query = {k.lower(): v for k, v in request.args.items()}
    page_size = 25
    page = query.get('page', '')

    query_model = PokemonQueryModel(LHSParser(query) & NameParser(query))

    pokemons = [p.to_python for p in query_model.fetch(page=page, page_size=page_size)]

    return success_response(pokemons)


def create_app(migrate: bool = False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JSON_SORT_KEYS'] = False

    app.register_blueprint(pokemon_bp)
    db.init_app(app)

    if migrate:
        run_migrations(app)

    return app
