"""
This module contains various reusable helper function.
"""
from typing import Union

PRIMITIVE_TYPES = Union[bool, float, int, str]


def cast_primitive_type(to_type: PRIMITIVE_TYPES, value: PRIMITIVE_TYPES) -> PRIMITIVE_TYPES:
    """
    Use only if it's acceptable to fallback to default values for primitive types.
    Ex:
        - str  => ''
        - bool => False
    """
    if to_type not in [bool, float, int, str]:
        raise Exception("Type casting not supported for ", to_type)
    try:
        if to_type == bool:
            return str(value).lower() in ['1', 'true']
        return to_type(value)
    except:
        # return base value for given type if type cannot be cast.
        return to_type()
