from poke_api.search import PokemonQueryModel

query_object = {
    'attack': {
        'lt': 100,
        'lte': 102,
        'gt': 50,
        'gte': 55,
        'eq': 20,
        'ne': 76
    },
    'defense': {
        'ne': 100
    }
}


def test_search_model_logic():
    search_obj = PokemonQueryModel(query_object).query_filters
    assert search_obj['attack']['or']['eq'] == 20
    assert len(search_obj['attack']['and'].items()) == 3
    assert search_obj['attack']['and']['lt'] == 103
    assert search_obj['attack']['and']['gt'] == 54
    assert search_obj['attack']['and']['ne'] == 76