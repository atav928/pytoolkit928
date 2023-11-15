# pylint: disable=line-too-long
"""Package Supplied Utilities."""

from typing import Any, Generator, Hashable, Union
from collections.abc import MutableMapping

from dataclasses import dataclass, fields
import pandas as pd

from pytoolkit.static import NONETYPE


@dataclass
class BaseMonitor:
    """Base Dataclass Methods."""
    @classmethod
    def create_from_dict(cls, dict_: dict[str, Any]):
        """
        Class Method that returns dataclass using a
         dictionary and strips invalid params.

        :param dict_: _description_
        :type dict_: _type_
        :return: Dataclass
        :rtype: :dataclass: DataModel
        """
        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in class_fields})

    @classmethod
    def create_from_kwargs(cls, **kwargs: Any):
        """
        Class method that returns dataclass values by
          unpacking paramter values and strips out invalid params.

        :param kwargs: unpacked key:value pairs
        :type **kwargs: variable length argument list
        :return: Dataclass
        :rtype: :dataclass: DataModel
        """
        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in kwargs.items() if k in class_fields})

    def to_dict(self, extend: bool = True):
        """
        Returns dataclass as dictionary.

        :param extend: Extends the dataclass that have a value `NONETYPE`.
        :type bool: Optional True
        :return: dataclass dictionary
        :rtype: dict[str, Any]
        """
        return {key: value for key, value in self.__dict__.items() if value is not NONETYPE}


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
    :param sep: Adds seperator to Key, defaults to '.'
    :type sep: str, optional
    :return: Flattened Dictionary.
    :rtype: MutableMapping
    """
    [flat_dict] = pd.json_normalize(_dict, sep=sep).to_dict(orient='records')  # type: ignore
    return flat_dict

# TODO: fix the nested structure add abiltiy to read in a csv or XCEL to help maniplate proper csv human readable datastructures


def _nest_dict_rec(key: str, value: Any, sep: str, out: dict[str, Any]) -> None:
    """Maniplates dictionary into a nested dictionary based on seperator."""
    key, *rest = key.split(sep, 1)
    if rest:
        _nest_dict_rec(rest[0], value, sep, out.setdefault(key, {}))
    else:
        out[key] = value


def nested_dict(_dict: MutableMapping[str, Any], sep: str = '.') -> dict[str, Any]:
    """
    Transform a Flattened Dictionary into a Nested Dictionary.

    :param _dict: _description_
    :type _dict: MutableMapping[str, Any]
    :param sep: Seperator to split Keys with, defaults to '.'
    :type sep: str, optional
    :return: Nested Dictionary.
    :rtype: dict[str, Any]
    """
    result: dict[str, Any] = {}
    for k, v in _dict.items():
        _nest_dict_rec(k, v, sep, result)
    return result
