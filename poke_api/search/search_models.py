

import copy
from functools import reduce
from operator import lt, gt, eq, ne

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import or_, and_
from poke_api.models.pokemon import Pokemon


OPERATOR_SUBS = {
    "less": lt,
    "more": gt,
    "eq": eq,
    "ne": ne
}


class BaseQueryModel:
    """
    Query models help us create query logic and put it into a python objects.
    for example: {
        name: {
            like: "bulba"
        },
        attack: {
            and: {
                more: 100,
                less: 200
            },
            or: {
                eq: 80
            }
        }
    }
    given the above model we can create an adapter for any given storage
    and search according to the output conditions.
    """
    def __init__(self, query_obj: dict, *args, **kwargs):
        self.query_filters = []
        self.page = query_obj.get("page", 0)

    def normalize_int_conditions(self, attribute):
        """
        The Core logic here is to make sense of the int query conditions provided.
        for example:
            if lt == 200 and gt == 100:
                we query for  (> 100) AND (< 200)
            if lt == 100 and gt == 200:
                we query for (< 100) OR (< 200)
        Also unite (lt, lte), (gt, gte) to one comparison value
        """
        attr_query = {
            k: int(v) for k, v in self.query_obj[attribute].items()
            if str(v).isdigit()
        }

        methods = {
            "or": [],
            "and": []
        }

        if all([attr_query.get('lt'), attr_query.get('lte')]):
            del attr_query[min(['lt', 'lte'], key = lambda x: attr_query[x] + int(x == 'lt'))]

        if all([attr_query.get('gt'), attr_query.get('gte')]):
            del attr_query[min(['gt', 'gte'], key = lambda x: attr_query[x] + int(x == 'gt'))]

        lower_bound = min(attr_query.get('lt', float("inf")), attr_query.get('lte', float("inf")) - 1)
        upper_bound = max(attr_query.get('gt', -float("inf")), attr_query.get('gte', -float("inf")) + 1)

        if lower_bound != float("inf") and upper_bound != -float("inf"):
            if lower_bound < upper_bound:
                methods["or"] += [{"less": lower_bound}, {"more": upper_bound}]
            if lower_bound > upper_bound:
                methods["and"] += [{"less": lower_bound}, {"more": upper_bound}]
        else:
            if lower_bound != float("inf"):
                methods["and"] += [{"less": lower_bound}]
            if upper_bound != -float("inf"):
                methods["and"] += [{"more": upper_bound}]

        if attr_query.get('eq') is not None:
            methods["or"] += [{"eq": attr_query.get('eq')}]

        if attr_query.get('ne') is not None:
            methods["and"] += [{"ne": attr_query.get('ne')}]

        methods = {m: f for m,f in methods.items() if len(f)}
        self.query_filters += [{attribute: methods}]

    def normalize_string_conditions(self, attribute):
        required_string = self.query_obj[attribute]
        self.query_filters += [{attribute: {"like": required_string}}]


class PokemonQueryModel(BaseQueryModel):

    def __init__(self, query_obj: dict, *args, **kwargs):
        self.filter = []
        self._query = query_obj
        self.query_obj = copy.deepcopy(query_obj)
        self.parsers = [p for p in
                        self.__dir__() if p.startswith("parse_pokemon")]
        super(PokemonQueryModel, self).__init__(query_obj, *args, **kwargs)

    def fetch(self, amount):
        for parser in self.parsers:
            getattr(self, parser)()

    def parse_pokemon_name(self):
        if not self.query_obj.get('name'):
            return None
        self.normalize_string_conditions("name")

    def parse_pokemon_attack(self):
        if not self.query_obj.get('attack'):
            return None
        self.normalize_int_conditions("attack")

    def parse_pokemon_defense(self):
        if not self.query_obj.get('defense'):
            return None
        self.normalize_int_conditions("defense")

    def parse_pokemon_hp(self):
        if not self.query_obj.get('hp'):
            return None
        self.normalize_int_conditions("hp")
