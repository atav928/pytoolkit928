"""Unflattened Extract Dictionary"""

import re
from typing import Any, Union


def _split_key_parts(key: str, sep: str, index_delim: str) -> list[Union[str, int]]:
    """Split a key like 'b_02_01.deep.val' into parts, handling list indices."""
    parts = []
    for part in key.split(sep):
        tokens = part.split(index_delim)
        for token in tokens:
            if re.fullmatch(r"\d+", token):
                parts.append(int(token) - 1)  # Convert to 0-based index
            else:
                parts.append(token)
    return parts


def _assign_nested(
    root: Union[dict, list],
    parts: list[Union[str, int]],
    value: Any,
    keep_only_dicts: bool = False,
    max_depth: int = -1,
):
    current = root
    for i, part in enumerate(parts):
        if max_depth != -1 and i >= max_depth:
            break
        is_last = i == len(parts) - 1
        next_part = None if is_last else parts[i + 1]

        if isinstance(part, int):
            if not isinstance(current, list):
                current_path = current
                current = []
                if isinstance(current_path, dict):
                    current_path.clear()
            while len(current) <= part:
                current.append(None)
            if is_last:
                current[part] = value
            else:
                if current[part] is None:
                    current[part] = {} if isinstance(next_part, str) else []
                current = current[part]
        else:
            if not isinstance(current, dict):
                raise TypeError("Inconsistent structure: expected dict.")
            if is_last:
                current[part] = value
            else:
                if part not in current:
                    current[part] = {} if isinstance(next_part, str) else []
                current = current[part]

    # Post-check: remove list if not dict-based and flag enabled
    if keep_only_dicts and isinstance(current, list):
        if not all(isinstance(i, dict) for i in current if i is not None):
            raise TypeError("List contains non-dict items; discarded due to `keep_only_dicts=True`.")


def unflat_dict(
    flat_dict: dict[str, Any], sep: str = ".", index_delim: str = "_", keep_only_dicts: bool = False, max_depth: int = -1
) -> dict[str, Any]:
    """
    Unflattened dictionary that was was flattened extracting the `lists` and `dicts`.

    :param flat_dict: _description_
    :type flat_dict: dict[str, Any]
    :param sep: _description_, defaults to "."
    :type sep: str, optional
    :param index_delim: _description_, defaults to "_"
    :type index_delim: str, optional
    :param keep_only_dicts: _description_, defaults to False
    :type keep_only_dicts: bool, optional
    :param max_depth: _description_, defaults to -1
    :type max_depth: int, optional
    :return: _description_
    :rtype: dict[str, Any]
    """
    result: dict[str, Any] = {}
    for flat_key, value in flat_dict.items():
        path_parts = _split_key_parts(flat_key, sep, index_delim)
        _assign_nested(result, path_parts, value, keep_only_dicts, max_depth)
    return result
