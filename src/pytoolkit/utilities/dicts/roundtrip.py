# flatten_utils/roundtrip.py
from typing import Any

from .flatten import flatten_dict
from .unflatten import unflat_dict


def validate_round_trip(
    original: dict[str, Any],
    flatten_kwargs: dict[str, Any] = {},
    unflatten_kwargs: dict[str, Any] = {},
    strict: bool = True,
) -> bool:
    """
    Validates a round-trip flatten → unflattened returns the original structure.

    :param original: The original nested dictionary
    :param flatten_kwargs: Args for flatten_dict_v3
    :param unflatten_kwargs: Args for nested_dict_v3
    :param strict: If True, performs exact equality
    :return: Whether round-trip returns original
    """
    flat = flatten_dict(original, **flatten_kwargs)
    rebuilt = unflat_dict(flat, **unflatten_kwargs)
    return original == rebuilt if strict else _loose_compare(original, rebuilt)


def _loose_compare(d1: Any, d2: Any) -> bool:
    """
    Recursive dict/list comparison for loose round-trip validation.
    Ignores key ordering and tolerates type normalization.
    """
    if isinstance(d1, dict) and isinstance(d2, dict):
        if set(d1.keys()) != set(d2.keys()):
            return False
        return all(_loose_compare(d1[k], d2[k]) for k in d1)
    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            return False
        return all(_loose_compare(i, j) for i, j in zip(d1, d2))
    return d1 == d2
