# pylint: disable=broad-exception-caught
"""Utilities."""

import base64
import json
import os
import platform
import pwd
import re
import socket
from enum import Enum
from pathlib import Path
from typing import Any, List, Union

import airportsdata

from pytoolkit.decorate import error_handler
from pytoolkit.static import ENCODING, NO_AIRPORTDATA, RE_DOMAIN, RE_IP4, SANATIZE_KEYS
from pytoolkit.utilities import flatten_dictionary, nested_dict

PATTERN = re.compile(r"(?<!^)(?=[A-Z])")
AIRPORTDATA = json.loads(json.dumps(airportsdata.load(code_type="IATA"), ensure_ascii=False))


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
        return isinstance(arg, basestring)  # type: ignore
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
        return re.split(delimeters, value, flags=re.IGNORECASE) if delimeters else [value]
    return (
        list(value)
        if "__iter__" in dir(value)
        else [
            value,
        ]
    )


def reform_except(error: Exception):
    """Shorter function call that calls `reformat_exception` Exception."""
    return reformat_exception(error=error)


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
        return ".".join(host.split(".")[:-2]) if ".".join(host.split(".")[:-2]) != "" else ".".join(host.split(".")[:-1])
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


def sanatize_data(data: dict[str, Any], keys: list[str] = SANATIZE_KEYS) -> dict[str, Any]:  # pylint: disable=W0102
    """
    Sanitize Data from a dictionary of values if a string is found to mask values that should not be exposed.

    :param data: _description_
    :type data: dict[str,Any]
    :param keys: _description_, defaults to SANATIZE_KEYS
    :type keys: list[str], optional
    :return: _description_
    :rtype: dict[str, Any]
    """
    flat = flatten_dictionary(data)
    new_dict = {key: "[MASKED]" if isinstance(key, str) and key.lower() in keys else value for key, value in flat.items()}
    return nested_dict(new_dict)


def split(event_list: list[Any], chunk_size: int):
    """
    Generator that yels n-sized chuncks.
       Ex: list(split(range(0,300),10))
             [[x,x,x,x,x],
              [x,x,x,x,x]]

    :param event_list: _description_
    :type event_list: _type_
    :param chunk_size: _description_
    :type chunk_size: _type_
    :yield: _description_
    :rtype: _type_
    """
    for i in range(0, len(event_list), chunk_size):
        yield event_list[i : i + chunk_size]


# Lambda func for chunk for quick object
# type: ignore # pylint: disable=C3001,line-too-long
chunk: list[Any] = lambda lst, n: [lst[i : i + n] for i in range(0, len(lst), n)]


def chunk_func(lst: list[Any], n: int) -> list[list[Any]]:
    """
    Splits up events into chunks.

    :param lst: _description_
    :type lst: list[Any]
    :param n: _description_
    :type n: int
    :return: _description_
    :rtype: list[list[Any]]
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def camel_to_snake(name: Union[str, list[str]], output: Union[str, None] = None) -> Union[List[str], str]:
    """
    Convert a complex Camel to Snake case does not handle complex patterns.
    Manages more complex patterns when the original CamelCase is not written correctly.
    ie. When a `.` is introduced or another `special char`.

    Example:
        >>> value = 'someValue.1'
        >>> camel_to_snake(value)
        `some_value1`

    :param name: Value to convert in camelCase.
    :type name: str
    :param output: Type of output. Default `str`
    :type output: str
    :return: Snake case value.
    :rtype: str | List[str]
    """
    # TODO: convert to precompiled patterns
    names: List[str] = string_or_list(name)
    snake_case: List[str] = []
    for n in names:
        # Handle any unusual characters select option on how to handle
        n: str = re.sub(r"\ |\.|\|\,|", "", n)
        n = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", n)
        n = re.sub("([a-z0-9])([A-Z])", r"\1_\2", n).lower()
        snake_case.append(n)
    if output in ["list"]:
        # Returns a List of Snake formated strings. Defaults to string
        return snake_case
    # Returns a string value
    return ",".join(snake_case)


def snake_to_camel(name: str) -> str:
    """
    Convert Snake Case into Camel Case.

    Example:
        >>> value="snake_format"
        >>> snake_to_camel(value)
        'snakeFormat'

    :param name: Value to convert to snake_case.
    :type name: str
    :return: snake_case value.
    :rtype: str
    """
    # TODO: add `output='list'` param to return a list of camelCase names
    init, *temp = name.split("_")
    return "".join([init.lower(), *map(str.title, temp)])


@error_handler(default_return=NO_AIRPORTDATA)
def get_airport_info(airport_code: str) -> dict[str, Any]:
    """
    Extracts Airport Code from Airport Database using the `IATA` value.

    :param airport_code: `IATA` airport code
    :type airport_code: str
    :return: Airport Information. Returns Emtpy Dictionary if not found or invalid
    :rtype: dict[str,Any]
    """
    return AIRPORTDATA[airport_code.upper()]


def convert_list_to_dict(lst: list[str]) -> dict[str, str]:
    """
    Converts a list to a dictionary.

    :param lst: List of strings.
    :type lst: list[str]
    :return: Converted list of strings as a Key: Value pair.
    :rtype: dict
    """
    res_dct = map(lambda i: (lst[i], lst[i + 1]), range(len(lst) - 1)[::2])
    return dict(res_dct)


def convert_dict_to_string(_dict: dict[str, Any]) -> str:
    """
    Convert a dictionary into a string output.
     Make sure the dictionary is not nested.
     Use flattening function if it is.

    :param _dict: Flattened Dictionary
    :type _dict: dict[str, Any]
    :return: string
    :rtype: str
    """
    return " ".join([f"{k} {v}" for k, v in _dict.items()])


# Algorithms


def swap(arr: list[Any], left_pos, right_pos):
    """
    A Python function that swaps two adjacent values in a list.

    :param arr: _description_
    :type arr: _type_
    :param left_pos: _description_
    :type left_pos: _type_
    :param right_pos: _description_
    :type right_pos: _type_
    """
    tmp = arr[left_pos]
    arr[left_pos] = arr[right_pos]
    arr[right_pos] = tmp


def bubble_sort(arr: list[Any]):
    """
    The Bubble Sort algorithm is a simple algorithm to sort a list of N numbers in ascending order. Bubble sort works by iterating through a list and checking whether the current element is larger or smaller than the next element.
    The Bubble Sort algorithm utilizes two loops: an outer loop to iterate over each element in the input list, and an inner loop to iterate, compare and exchange a pair of values in the list. The inner loop takes (N-1) iterations while the outer loop takes N iterations. Hence, the Big-O runtime for the algorithm is the product of O(N) and O(N-1), which is O(N^2).

    :param arr: _description_
    :type arr: list[Any]
    """
    for _ in arr:
        for idx in range(len(arr) - 1):
            if arr[idx] > arr[idx + 1]:
                swap(arr, idx, idx + 1)


def merge_sort(lst: list[Any]) -> list[Any]:
    """
    Merge Sort is a divide and conquer algorithm. It consists of two parts:
    1) splitting the original list into smaller sorted lists recursively until there is only 1 element in the list,
    2) merging back the presorted 1-element lists into 2-element lists, 4-element lists, and so on recursively.

    :param lst: _description_
    :type lst: list[Any]
    :return: _description_
    :rtype: _type_
    """
    if len(lst) <= 1:
        return lst
    middle: int = len(lst) // 2
    left: List[Any] = lst[:middle]
    right: List[Any] = lst[middle:]
    sleft: List[Any] = merge_sort(left)
    sright: List[Any] = merge_sort(right)
    return merge(sleft, sright)


def merge(left: list[Any], right: list[Any]):
    """
    The Merge Sort algorithm is divided into two parts. The first part repeatedly splits the input list into smaller lists to eventually produce single-element lists. The best, worst and average runtime for this part is Θ(log N). The second part repeatedly merges and sorts the single-element lists to twice its size until the original input size is achieved. The best, worst and average runtime for this part is Θ(N). Therefore, the combined runtime is Θ(N log N).

    :param left: _description_
    :type left: _type_
    :param right: _description_
    :type right: _type_
    :return: _description_
    :rtype: _type_
    """
    result: list[Any] = []
    while left and right:
        if left[0] < right[0]:
            result.append(left[0])
            left.pop(0)
        else:
            result.append(right[0])
            right.pop(0)
    if left:
        result += left
    if right:
        result += right
    return result
