# pylint: disable=broad-exception-caught
"""Utilities."""

from enum import Enum
import os
from pathlib import Path
import platform
import pwd
import socket
from typing import Any, List, Union
import base64
import re

from pytoolkit.static import ENCODING, RE_DOMAIN, RE_IP4, SANATIZE_KEYS
from pytoolkit.utilities import flatten_dictionary, nested_dict


def os_plat() -> str:
    """
    Return OS System.

    :return: darwin, linux, java, windows.
    :rtype: str
    """
    return platform.system().lower()


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
        return value.split(",")
    if isinstance(value, list):
        return value  # type: ignore
    raise ValueError(f"Invalid value {value}")


def convert_to_base64(filename: str) -> bytes:
    """
    Convert a file to a byte string off base64.

    :param filename: Filename
    :type filename: str
    :return: Encoded File String.
    :rtype: base64
    """
    with open(filename, "rb") as file:
        my_string: bytes = base64.b64decode(file.read())
    return my_string


# Enumerator type


def enum(*sequential: Any, **named: Any) -> type[Enum]:
    """
    Support for converting the values back to names can be added.

    Usage:
        >>> Numbers = enum(ONE=1, TWO=2, THREE='three')
        >>> Numbers.ONE
        1
        >>> Numbers.TWO
        2
        >>> Numbers.THREE
        'three'

    :return: Enumerated Object.
    :rtype: type[Enum]
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict(((v, k) for (k, v) in enums.items()))
    enums["reverse_mapping"] = reverse
    return type("Enum", (), enums)


def isstring(arg: Any) -> bool:
    """Verifies if an argument is a string."""
    try:
        return isinstance(arg, basestring)
    except NameError:
        return isinstance(arg, (str, bytes))


# Convenience methods used internally by module
# Do not use these methods outside the module


def string_or_list(value: Any, delimeters: Union[str, None] = None) -> list[str]:
    """
    Return a list containing value.

    This method allows flexibility in class __init__ arguments,
    allowing you to pass a string, object, list, or tuple.
    In all cases, a list will be returned.

    :param value: a string, object, list, or tuple
    :type value: str|obj|list|tuple
    :param delimeter: use a delimeter in the string using pipe(|) as an OR for multiple.
     (Optional) Default no delimeter used. Example: delimeters=',| |;|' or ',| |\|'
    :type delimeter: str|None
    :return: list
    :rtype: list[str]

    :examples:
        "string" -> [string]
        ("t1", "t2") -> ["t1", "t2"]
        ["l1", "l2"] -> ["l1", "l2"]
        None -> None
    """
    if value is None:
        return None  # type: ignore
    if isstring(value):
        return (
            re.split(delimeters, value, flags=re.IGNORECASE) if delimeters else [value]
        )
    return (
        list(value)
        if "__iter__" in dir(value)
        else [
            value,
        ]
    )


def reformat_exception(error: Exception) -> str:
    """
    Reformates Exception to print out as a string pass for logging.

    :param error: caught excpetion
    :type error: Exception
    :return: error as string
    :rtype: str
    """
    resp: str = f"{type(error).__name__}: {str(error)}" if error else ""
    # Replacing [ ] with list() due to issues with reading that format with some systems.
    resp = re.sub(r"\'", "", resp)
    resp = re.sub(r"\[", "list(", resp)
    resp = re.sub(r"\]", ")", resp)
    return resp


def return_filelines(filename: str) -> list[str]:
    """
    Return list of strings in a file.

    :param filename: _description_
    :type filename: str
    :return: _description_
    :rtype: list[str]
    """
    filelines: list[str] = []
    with open(filename, "r", encoding=ENCODING) as fil:
        filelines = fil.readlines()
    return filelines


def check_file(filename: str) -> str:
    """Check that filename exists and returns Pathlib object if does.

    :param filename: Name of file; full path
    :type filename: str
    :raises FileExistsError: _description_
    :return: File location
    :rtype: Path
    """
    file: Path = Path(filename)
    if not file.exists():
        raise FileExistsError(f"Filename does not exist: {str(filename)}")
    return filename


def return_username(log: Any = None) -> Union[str, None]:
    """
    Return Username Information.

    :param log: logger, defaults to None
    :type log: Logger, optional
    :return: username
    :rtype: Union[str,None]
    """
    try:
        return pwd.getpwuid(os.getuid())[0]
    except Exception as err:
        error: str = reformat_exception(err)
        if log:
            log.error(f'msg="Unable to get username"|{error=}')
    return None


def gethostipaddr(hostname: str) -> str:
    """
    Returns IP address of local host. Caution if multiple addresses are rturne due to load balancer.

    :param hostname: _description_
    :type hostname: str
    :raises ValueError: _description_
    :return: _description_
    :rtype: str
    """
    ipv4 = socket.gethostbyname(hostname)
    if not re.match(RE_IP4, ipv4):
        raise ValueError(f"Invalid Address {ipv4}")
    return f"{ipv4}/32" if ipv4.split("/")[-1] != "32" else ipv4


def gethostbyaddr(ip_addr: str) -> str:
    """
    Return FQDN from IP Address.

    :param ip_addr: _description_
    :type ip_addr: str
    :return: _description_
    :rtype: str
    """
    if not re.match(RE_IP4, ip_addr):
        raise ValueError(f"Invalid IPv4 {ip_addr}")
    return socket.gethostbyaddr(ip_addr)[0]


def return_hostinfo(fqdn: bool = True) -> str:
    """
    Return Hostname information on system.

    :param fqdn: Retun FQDN or Hostname, defaults to True
    :type fqdn: bool, optional
    :return: System Hostname/FQDN or root domain.
    :rtype: str
    """
    if fqdn:
        return socket.getfqdn()
    host: str = socket.gethostname()
    if re.match(RE_DOMAIN, host, re.IGNORECASE):
        return (
            ".".join(host.split(".")[:-2])
            if ".".join(host.split(".")[:-2]) != ""
            else ".".join(host.split(".")[:-1])
        )
    return host


def set_bool(value: str, default: bool = False) -> Union[str, bool]:
    """sets bool value when pulling string from os env

    Args:
        value (str|bool, Required): the value to evaluate
        default (bool): default return bool value. Default False

    Returns:
        (str|bool): String if certificate path is passed otherwise True|False
    """
    value_bool = default
    if isinstance(value, bool):
        value_bool = value
    elif str(value).lower() == "true":
        value_bool = True
    elif str(value).lower() == "false":
        value_bool = False
    elif Path.exists(Path(value)):
        value_bool = value
    return value_bool


def sanatize_data(
    data: dict[str, Any], keys: list[str] = SANATIZE_KEYS
) -> dict[str, Any]:
    """
    Sanatize Data from a dictionary of values if a string is found to mask values that should not be exposed.

    :param data: _description_
    :type data: dict[str,Any]
    :param keys: _description_, defaults to SANATIZE_KEYS
    :type keys: list[str], optional
    :return: _description_
    :rtype: dict[str, Any]
    """
    flat = flatten_dictionary(data)
    new_dict = {
        key: "[MASKED]" if isinstance(key, str) and key.lower() in keys else value
        for key, value in flat.items()
    }
    return nested_dict(new_dict)
