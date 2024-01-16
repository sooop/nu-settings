from sys import base_prefix
from typing import Any, TypeVar

T = TypeVar('T')


def traverse(item: dict[str, Any], key: str) -> list[str]:
    if key not in item:
        return []
    value = item[key]
    if isinstance(value, list):
        return [*value, *(sum([traverse(x, key) for x in value], []))]
    return [value]
