

import copy
from functools import reduce
from operator import lt, gt, eq, ne

from sqlalchemy import or_, and_
from poke_api.models.pokemon import Pokemon

OPERATOR_SUBS = {
    "lt": lt,
    "gt": gt,
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
        self.query_filters = {}
        self.page = query_obj.get("page", 0)
        self.clean_query()


    def clean_query(self):
        raise NotImplementedError

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

        self.query_filters[attribute] = {"and": {}, "or": {}}

        if all([attr_query.get('lt'), attr_query.get('lte')]):
            del attr_query[min(['lt', 'lte'], key = lambda x: attr_query[x] + int(x == 'lt'))]

        if all([attr_query.get('gt'), attr_query.get('gte')]):
            del attr_query[min(['gt', 'gte'], key = lambda x: attr_query[x] + int(x == 'gt'))]

        upper_bound = min(attr_query.get('lt', float("inf")), attr_query.get('lte', float("inf")) + 1)
        lower_bound = max(attr_query.get('gt', -float("inf")), attr_query.get('gte', -float("inf")) - 1)


        if all([upper_bound != float("inf"), lower_bound != -float("inf"), upper_bound > lower_bound]):
            self.query_filters[attribute]["and"]["lt"] = upper_bound
            self.query_filters[attribute]["and"]["gt"] = lower_bound
        else:
            if upper_bound != float("inf"):
                self.query_filters[attribute]["or"]['lt'] = upper_bound
            if lower_bound != -float("inf"):
                self.query_filters[attribute]["or"]['gt'] = lower_bound

        if attr_query.get('eq') is not None:
            self.query_filters[attribute]["or"]['eq'] = attr_query.get('eq')

        if attr_query.get('ne') is not None:
            self.query_filters[attribute]["and"]["ne"] = attr_query.get('ne')

    def normalize_string_conditions(self, attribute):
        required_string = self.query_obj[attribute]
        self.query_filters[attribute] = {"like": required_string}


class PokemonQueryModel(BaseQueryModel, Pokemon):

    def __init__(self, query_obj: dict, *args, **kwargs):
        self._query = query_obj
        self.query_obj = copy.deepcopy(query_obj)
        super(PokemonQueryModel, self).__init__(query_obj, *args, **kwargs)

    def create_alchemy_filter(self, attr, conditions):
        """
        Based on the given attribute and conditions,
        Creates a filter method for sql alchemy.
        """
        if bool(conditions.get('or')) and bool(conditions.get('and')):
            and_f = [OPERATOR_SUBS[k](getattr(Pokemon, attr), v) for k, v in conditions["and"].items()]
            or_f = [OPERATOR_SUBS[k](getattr(Pokemon, attr), v) for k, v in conditions["or"].items()]
            return or_(and_(*and_f), *or_f)
        if bool(conditions.get('and')):
            return and_(OPERATOR_SUBS[k](getattr(Pokemon, attr), v) for k, v in conditions["and"].items())
        if bool(conditions.get('or')):
            return and_(OPERATOR_SUBS[k](getattr(Pokemon, attr), v) for k, v in conditions["or"].items())
        if bool(conditions.get('like')):
            return getattr(getattr(Pokemon, attr), "like")("%" + conditions["like"] + "%")

    def clean_query(self):
        """
        Base method to pick up and clean search fields for this query model and organize them.
        """
        for parser in [p for p in self.__dir__() if p.startswith("parse_pokemon")]:
            getattr(self, parser)()


    def fetch(self, page=1, page_size=25):
        page = int(page) if page.isdigit() else 1
        filters = []
        for k, v in self.query_filters.items():
            filters.append(self.create_alchemy_filter(k, v))
        filtered_query = reduce(lambda qe, filt: getattr(qe, "filter")(filt),
                                filters,
                                self.query)
        return filtered_query.limit(page_size).offset((page - 1) * page_size)

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
