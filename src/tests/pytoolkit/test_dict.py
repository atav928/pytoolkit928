# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test Utilities to Import."""
import sys
import unittest
from typing import Any, Hashable


# from pytoolkit.utilities.pkg_utils import (
#     flatten_dictionary,
# )
from pytoolkit.utilities import flatten_dictionary
from pytoolkit.utilities.dicts.flatten import flatten_dict
from pytoolkit.utilities.dicts.unflatten import unflat_dict
from pytoolkit.utilities.dicts.roundtrip import validate_round_trip

test_dict = {
    "key": "value",
    "key_one": "value2",
    "metadata": {
        "key_one": "meta_value1",
        "key_twho": "meta_value_two",
    },
}

test_flat = {"a": 1, "b_01.x": 2, "b_02_01": 3, "b_02_02.y": 4, "b_03": "text", "c_01_01.deep.val": 5}

test_nested = {
    "a": 1,
    "b": [{"x": 2}, [3, {"y": 4}], "text"],
    "c": [[{"deep": {"val": 5}}]],
}


class TestDictionaries(unittest.TestCase):
    def test_nest(self) -> None:
        """Running tests against Converting a Flat dictionary to a Nested Dict."""
        converted: dict[str, Any] = unflat_dict(test_flat)
        for k in converted:
            self.assertIsInstance(k, str, f"Expected a string from {k}")
        # Check for nested dictionary
        self.assertIsInstance(converted["a"], int, f"Expected type `int` from {converted}")
        self.assertIsInstance(converted["b"][0], dict, f"Expected type `dict` from {converted['b'][0]}")
        self.assertIsInstance(converted["b"][2], str, f"Expected a string from {converted}")
        self.assertIsInstance(converted["c"][0][0]["deep"], dict, f"Expected a dictionary from {converted}")

    def test_flat(self) -> None:
        """Running tests against Converting a Nested dictionary to a Flattened Dict."""
        converted: dict[str, Any] = flatten_dict(test_dict)
        for v in converted.values():
            self.assertIsInstance(v, str, f"Value of {v} should be type `str`")
            self.assertIsNot(v, dict, f"Value of {v} should not be a type `dict`")
            self.assertIsNot(v, list, f"Value of {v} should not be a type `list`")

    def test_complex_flat(self):
        converted = flatten_dict(test_flat)
        self.assertTrue(
            all([isinstance(k, str)] for k in list(converted)), f"A key is not a string in the reformated {test_flat}"
        )
        for v in converted.values():
            self.assertIsNot(v, dict)
            self.assertIsNot(v, list)

    def test_validate_flat_unflat(self):
        sys.setrecursionlimit(1000)
        self.assertTrue(
            validate_round_trip(test_nested, strict=False),
            f"Unable to validate that {test_nested} is returning expected results",
        )

    def test_flat_pd(self) -> None:
        """Running testing pandas json normalization."""
        converted: dict[Hashable, Any] = flatten_dictionary(test_dict)
        for v in converted.values():
            self.assertIsInstance(v, str, f"Value of {v} is not of type `str`")
            self.assertIsNot(v, dict, f"Value of {v} should not be a type `dict`")
