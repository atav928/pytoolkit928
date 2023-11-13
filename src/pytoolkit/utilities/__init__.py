"""Package Supplied Utilities."""

from typing import Any, Generator, Hashable, Union
from collections.abc import MutableMapping

import pandas as pd


def _flatten_dict_gen(_d: MutableMapping[str, Any], parent_key: str,
                      sep: str, extended_label: bool,
                      skip_item: list[str]) -> Generator[tuple[str, Any], Any, None]:
    for k, v in _d.items():
        new_key: str = k
        if extended_label:
            new_key: str = parent_key + sep + \
                k if (parent_key and k not in skip_item) else k  # type: ignore
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v,  # type: ignore
                                    new_key, extended_label=extended_label,
                                    skip_item=skip_item,
                                    sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(_dict: MutableMapping[str, Any], parent_key: str = "",
                 sep: str = ".", extended_label: bool = True,
                 skip_item: Union[list[str], None] = None) -> dict[str, Any]:
    """
    Flatten out a dictionary with nested values.

    :param _dict: Dictionary
    :type _dict: MutableMapping[str,Any]
    :param parent_key: Top Level Key, defaults to ""
    :type parent_key: str, optional
    :param sep: Seperator, defaults to "."
    :type sep: str, optional
    :param extended_label: Uses the same key by default or appends the hierarchy
     into the name of the key used to express the nesting structure, defaults to True
    :type extended_label: bool, optional
    :param skip_item: List of Keys to ignore and flatten without the parent, defaults to []
    :type skip_item: list, optional
    :return: Flattened Dictionary
    :rtype: dict[str,Any]
    """
    skip_item = skip_item if skip_item else [""]
    return dict(_flatten_dict_gen(_dict, parent_key, sep, extended_label, skip_item))


def flatten_dictionary(_dict: MutableMapping[Any, Any], sep: str = '.') -> dict[Hashable, Any]:
    """
    Flatten a dictionary via pandas normalizer.

    :param d: _description_
    :type d: MutableMapping
    :param sep: _description_, defaults to '.'
    :type sep: str, optional
    :return: _description_
    :rtype: MutableMapping
    """
    [flat_dict] = pd.json_normalize(_dict, sep=sep).to_dict(orient='records')
    return flat_dict

# TODO: fix the nested structure add abiltiy to read in a csv or XCEL to help maniplate proper csv human readable datastructures


def _nest_dict_rec(key: str, value: Any, sep: str, out: dict[str, Any]) -> None:
    key, *rest = key.split(sep, 1)
    if rest:
        _nest_dict_rec(rest[0], value, sep, out.setdefault(key, {}))
    else:
        out[key] = value


def nested_dict(flat: MutableMapping[str, Any], sep: str = '.') -> dict[str, Any]:
    """
    Transform a Flattened Dictionary into a Nested Dictionary.

    :param flat: _description_
    :type flat: MutableMapping[str, Any]
    :param sep: _description_, defaults to '.'
    :type sep: str, optional
    :return: _description_
    :rtype: dict[str, Any]
    """
    result: dict[str, Any] = {}
    for k, v in flat.items():
        _nest_dict_rec(k, v, sep, result)
    return result
