import codecs
from _ast import AST
from ast import parse
from pathlib import Path
from typing import Any, List, Optional, Tuple

BUILTIN_PURE = (int, float, bool)
BUILTIN_BYTES = (bytearray, bytes)


def get_value(attr_value):
    if attr_value is None:
        return attr_value
    if isinstance(attr_value, BUILTIN_PURE):
        return attr_value
    if isinstance(attr_value, BUILTIN_BYTES):
        return decode_bytes(attr_value)
    if isinstance(attr_value, str):
        return attr_value
    if isinstance(attr_value, complex):
        return str(attr_value)
    if isinstance(attr_value, list):
        # make everything a dict so that it can be keyed when nested
        return dict(enumerate([get_value(x) for x in attr_value]))
    if isinstance(attr_value, AST):
        return ast2dict(attr_value)
    if isinstance(attr_value, type(Ellipsis)):
        return "..."
    else:
        raise Exception(f"unknown case for '{attr_value}' of type '{type(attr_value)}'")


def decode_bytes(value):
    try:
        return value.decode("utf-8")
    except Exception:
        return codecs.getencoder("hex_codec")(value)[0].decode("utf-8")


def ast2dict(node, file: Optional[str] = None):
    assert isinstance(node, AST)
    to_return = dict()
    to_return["_type"] = node.__class__.__name__
    if file is not None:
        to_return["_file"] = file
    for attr in dir(node):
        if attr.startswith("_"):
            continue
        to_return[attr] = get_value(getattr(node, attr))
    return to_return


def ast2dict_from_str(code: str, file: Optional[str] = None):
    return ast2dict(parse(code), file=file)


def ast2dict_from_file(file_path: str | Path):
    return ast2dict(parse(Path(file_path).open().read()), file=str(file_path))


def get_info_by_key_value(dictionary, key, value) -> List[Tuple[str, List[Any]]]:
    """
    Returns a list of tuples containing values and their corresponding paths in the dictionary,
    where the given key matches the given value.

    Parameters:
    - dictionary (dict): The dictionary to search in.
    - key: The key to match in the dictionary.
    - value: The value to match with the key in the dictionary.

    Returns:
    - result (list): A list of tuples containing values and their corresponding paths in the dictionary.
    Each tuple consists of the matched value and the path to reach that value in the dictionary.

    Example:
    >>> dictionary = {'a': {'b': 1, 'c': {'d': 2}}, 'e': {'f': 3}}
    >>> get_info_by_key_value(dictionary, 'b', 1)
    [(1, ['a', 'b'])]
    >>> get_info_by_key_value(dictionary, 'f', 3)
    [(3, ['e', 'f'])]
    """
    result = []

    def get_info_by_key_value_helper(dictionary, key, value, path):
        if dictionary.get(key) == value:
            value = dictionary[key]
            result.append((value, path))
            if isinstance(value, dict):
                for k in value:
                    get_info_by_key_value_helper(value, key, value, path + [k])
        for k in dictionary:
            if isinstance(dictionary[k], dict):
                get_info_by_key_value_helper(dictionary[k], key, value, path + [k])

    get_info_by_key_value_helper(dictionary, key, value, [])
    return result
