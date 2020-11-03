import re
from typing import Any, List, Union
from itertools import groupby


OPERATOR_STRINGS = ["lt", "lte", "gt", "gte", "eq", "ne"]

SUPPORTED_QUERY_ATTRIBUTES = {"attack": int, "defense": int, "hp": int}


def parse_lhs_key(lhs_key: str, value: Any) -> Union[dict, None]:
    """
    Using regex, we validate given query parameter, validation should include the following points:
    1 - we support the provided query attribute (for example attack, defense, etc...)
    2 - given operator is valid. (lt, gt, eq, etc...)
    """
    supported_patterns = (f"^({('|').join(SUPPORTED_QUERY_ATTRIBUTES.keys())})" +
                          f"(\[({('|').join(OPERATOR_STRINGS)})\])$")

    match = re.search(supported_patterns, lhs_key)

    if match is None:
        return

    result = {
        "attribute": match.group(1),
        "operator": match.group(3),
        "value": value
    }
    return result


def lhs_queries_parser(query: dict) -> None:
    """
    Parse and validate all query parametes that we support for filtering.
    full list can be found at the top of this file. ^^SUPPORTED_QUERY_ATTRIBUTES
    Returns an dict that contains each filter attribute with it's filter confitions as list

    Example: {
        attack: [
            {
                'operator': 'eq',
                'value': 100
            },
            {
                'operator': 'lt',
                'value': 40
            }
        ],
        defense: [
            {
                'operator': 'gt',
                'value': 123
            }
        ]
    }
    """

    # Extract required filters (None if not valid)
    clean_queries = [parse_lhs_key(k, v) for k, v in query.items()]

    # Cast values (None if not valid)
    for i, q in enumerate(clean_queries):
        try:
            q["value"] = SUPPORTED_QUERY_ATTRIBUTES[q["attribute"]](q["value"])
        except:
            clean_queries[i] = None

    # Remove None Values
    clean_queries = list(filter(lambda x: x, clean_queries))

    return {k: list(v) for k, v in groupby(clean_queries, key=lambda i: i['attribute'])}
