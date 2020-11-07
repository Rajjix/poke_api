from poke_api.search.parsers import NameParser, LHSParser

SIMPLE_QUERY = { "name": "bulba", "attack[lte]": 100, "defense[gt]": 100 }

QUERY_ONE = {
    "NaMe": "bulba",
    "attack[lt]": 100,
    "attack[lte]": 102,
    "attack[gt]": 50,
    "attack[gte]": 55,
    "attack[sdadgte]": 55,
    "attack[eq]": 20,
    "attadasdack[sdadgte]": 55,
    "attack[ne]": 76,
    "defense[ne]": 100
    }

def test_name_parser():
    query = NameParser(SIMPLE_QUERY).items()
    assert len(query.items()) == 1
    assert query.get('name') == 'bulba'


def test_lhs_parser():
    query = LHSParser(SIMPLE_QUERY).items()
    assert query.get('attack').get('lte') == 100
    assert query.get('defense').get('gt') == 100


def test_clean_lhs_parser():
    query = LHSParser(QUERY_ONE).items()
    assert len(query.items()) == 2
    assert len(query["attack"].items()) == 6
    assert len(query["defense"].items()) == 1