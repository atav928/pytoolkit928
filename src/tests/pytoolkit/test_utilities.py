# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test Utilities to Import."""
import unittest

from typing import Any, Union, Hashable

from pytoolkit.utilities import nested_dict, flatten_dict, flatten_dictionary

test_nest_dict: dict[str, Union[str, dict[str, str]]] = {
    "key1": "value", "key2": "value2", "metadata": {"key1": "meta_value1", "key2": "meta_value2"}}
test_flat_dict: dict[str, str] = {'key1': 'value', 'key2': 'value2',
                                  'metadata.key1': 'meta_value1', 'metadata.key2': 'meta_value2'}


class TestDictionaries(unittest.TestCase):
    def test_nest(self) -> None:
        converted: dict[str, Any] = nested_dict(test_flat_dict)
        for k in converted:
            self.assertIsInstance(k, str)
        # Check for nested dictionary
        self.assertIsInstance(converted["metadata"], dict)

    def test_flat(self) -> None:
        converted: dict[str, Any] = flatten_dict(test_nest_dict)
        for v in converted.values():
            self.assertIsInstance(v, str)
            self.assertIsNot(v, dict)

    def test_flat_pd(self) -> None:
        converted: dict[Hashable, Any] = flatten_dictionary(test_nest_dict)
        for v in converted.values():
            self.assertIsInstance(v, str)
            self.assertIsNot(v, dict)
