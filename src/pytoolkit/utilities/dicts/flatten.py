"""Flatten a nested dictionary"""

from typing import Any, Generator, Union


def _flatten_dict_gen(
    d: Union[dict, list],
    parent_key: str = "",
    sep: str = ".",
    list_keys_filter: Union[list[str], None] = None,
    index_padding: int = 2,
    index_delim: str = "_",
    flatten_only_dicts: bool = False,
    max_depth: int = -1,
    depth: int = 0,  # internal counter
) -> Generator[tuple[str, Any], None, None]:
    if max_depth != -1 and depth > max_depth:
        yield parent_key, d
        return
    if isinstance(d, dict):
        for k, v in d.items():
            key_path = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                yield from _flatten_dict_gen(
                    v, key_path, sep, list_keys_filter, index_padding, index_delim, flatten_only_dicts, max_depth, depth + 1
                )
            else:
                yield key_path, v
    elif isinstance(d, list):
        # Check if we should flatten this list
        flatten = True
        if flatten_only_dicts:
            flatten = all(isinstance(i, dict) for i in d)
        for i, item in enumerate(d) if flatten else [(0, d)]:
            suffix = f"{index_delim}{str(i + 1).zfill(index_padding)}"
            key_path = f"{parent_key}{suffix}" if parent_key else suffix
            # if isinstance(item, (dict, list)):
            yield from _flatten_dict_gen(
                item, key_path, sep, list_keys_filter, index_padding, index_delim, flatten_only_dicts, max_depth, depth + 1
            )
    else:
        yield parent_key, d


def flatten_dict(
    d: Union[dict, list],
    parent_key: str = "",
    sep: str = ".",
    list_keys_filter: Union[list[str], None] = None,
    index_padding: int = 2,
    index_delim: str = "_",
    flatten_only_dicts: bool = False,
    max_depth: int = -1,  # Optional max depth
) -> dict[str, Any]:
    """
    Flatten out a nested dictionary that contains nested `dict` and or `list`.

    :param d: original dictionary
    :type d: Union[dict, list]
    :param parent_key: Change the top level key name, defaults to ""
    :type parent_key: str, optional
    :param sep: adjust separator between nested dictionary keys, defaults to "."
    :type sep: str, optional
    :param list_keys_filter: _description_, defaults to None
    :type list_keys_filter: Union[list[str], None], optional
    :param index_padding: _description_, defaults to 2
    :type index_padding: int, optional
    :param index_delim: _description_, defaults to "_"
    :type index_delim: str, optional
    :param flatten_only_dicts: _description_, defaults to False
    :type flatten_only_dicts: bool, optional
    :param max_depth: _description_, defaults to -1
    :type max_depth: int, optional
    :return: _description_
    :rtype: dict[str, Any]
    """
    return dict(
        _flatten_dict_gen(d, parent_key, sep, list_keys_filter, index_padding, index_delim, flatten_only_dicts, max_depth)
    )
