"""
The parsers module contains core functionality for
parsing and validating url query parameters.

"""

import re
from typing import Any, Dict, List, Union
from itertools import groupby

OPERATOR_STRINGS = ["lt", "lte", "gt", "gte", "eq", "ne"]


class BaseParser:
    def __init__(self, query: dict, *args, **kwargs):
        self.query = query

    def items(self) -> dict:
        return self.parse()

    def __rand__(self, other):
        return {**dict(other.items()), **self.items()}


class LHSParser(BaseParser):
    def __init__(self, query: dict, operators: list = OPERATOR_STRINGS, *args, **kwargs):
        self.operators = operators
        super(LHSParser, self).__init__(query, *args, **kwargs)

    def parse(self) -> dict:
        result = {}

        parsed_query = list(filter(
            lambda x: x,
            [self.parse_lhs_key(k, v) for k, v in self.query.items()]))

        for k, filters in groupby(parsed_query, key=lambda x: x['property']):
            result[k] = {fil["operator"]: fil["value"] for fil in filters}

        return result

    def parse_lhs_key(self, lhs_key: str, value: Any) -> Union[dict, None]:
        """
        Using regex, we validate given query parameter, validation should include the following points:
        1 - we support the provided query attribute (for example attack, defense, etc...)
        2 - given operator is valid. (lt, gt, eq, etc...)
        """
        supported_patterns = (f"^(.+)(\[({('|').join(self.operators)})\])$")

        match = re.search(supported_patterns, lhs_key)

        if match is None:
            return
        result = {
            "property": match.group(1),
            "operator": match.group(3),
            "value": value
        }
        return result


class NameParser(BaseParser):
    def parse(self) -> dict:
        return {'name': self.query.get('name')}