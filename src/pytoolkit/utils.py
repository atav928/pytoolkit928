"""Utilities."""

from typing import Any,List
import base64

def verify_list(value: Any) -> List[str]:
    """
    Verify value being passed is a list or split out a comma seperted string into a list.

    :param value: Original value. Should be a str|list
    :type value: Any
    :raises ValueError: If value is not a string or list
    :return: _description_
    :rtype: List[str]
    """
    if not isinstance(value, list) and isinstance(value, str):
        return value.split(',')
    if isinstance(value,list):
        return value  # type: ignore
    raise ValueError(f"Invalid value {value}")

def convert_to_base64(filename: str):
    """
    Converts a file to a byte string off base64.

    :param filename: Filename
    :type filename: str
    :return: Encoded File String.
    :rtype: base64
    """
    with open(filename, 'rb') as file:
        my_string = base64.b64decode(file.read())
    return my_string
