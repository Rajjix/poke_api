

from operator import lt, gt, le, ge, eq, ne
# from functools import reduce
#
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import or_, and_

from .lhs_parser import lhs_queries_parser

OPERATOR_SUBS = {"lt": lt, "lte": le, "gt": gt, "gte": ge, "eq": eq, "ne": ne}


def search_me(query_params: dict):
    name = query_params.get('name', "")
    page = query_params.get('page', 0)
    lhs_queries = lhs_queries_parser(query_params)

    print("Name: ", name)

    print("Page: ", page)

    print("LHS_queries: ", lhs_queries)

    return None
