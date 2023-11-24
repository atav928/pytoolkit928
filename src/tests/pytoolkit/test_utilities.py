# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test Utilities to Import."""

import unittest
from typing import Any, Optional, Union, Hashable

from dataclasses import dataclass

from pytoolkit.utilities import (
    nested_dict,
    flatten_dict,
    flatten_dictionary,
    BaseMonitor,
)
from pytoolkit.static import NONETYPE

test_nest_dict: dict[str, Union[str, dict[str, str]]] = {
    "key1": "value",
    "key2": "value2",
    "metadata": {"key1": "meta_value1", "key2": "meta_value2"},
}
test_flat_dict: dict[str, str] = {
    "key1": "value",
    "key2": "value2",
    "metadata.key1": "meta_value1",
    "metadata.key2": "meta_value2",
}

test_dataclass: Union[dict[str, str], int]] = {"sample": "sample_text", "integer": 100}
test_dataclass_opt: Union[dict[str, str], int]] = {**test_dataclass, **{"novalue": "emptyvalue"}}


@dataclass
class TestDataClass(BaseMonitor):
    sample: str
    integer: int
    novalue: Optional[str] = NONETYPE


class TestDictionaries(unittest.TestCase):
    def test_nest(self) -> None:
        print("Running tests against Converting a Flat dictionary to a Nested Dict.")
        converted: dict[str, Any] = nested_dict(test_flat_dict)
        for k in converted:
            self.assertIsInstance(k, str)
        # Check for nested dictionary
        self.assertIsInstance(converted["metadata"], dict)

    def test_flat(self) -> None:
        print(
            "Running tests against Converting a Nested dictionary to a Flattened Dict."
        )
        converted: dict[str, Any] = flatten_dict(test_nest_dict)
        for v in converted.values():
            self.assertIsInstance(v, str)
            self.assertIsNot(v, dict)

    def test_flat_pd(self) -> None:
        print("Running testing pandas json normalization.")
        converted: dict[Hashable, Any] = flatten_dictionary(test_nest_dict)
        for v in converted.values():
            self.assertIsInstance(v, str, f"Value is {v}")
            self.assertIsNot(v, dict)

    def test_dataclass(self) -> None:
        print("Running tests against BaseMonitor Dataclass")
        base_dc = TestDataClass.create_from_dict(test_dataclass)
        base_dc_opt = TestDataClass.create_from_dict(test_dataclass_opt)
        self.assertIs(base_dc.sample, "sample_text", f"Base DC is {base_dc.to_dict()}")
        self.assertIs(base_dc_opt.integer, 100)
        self.assertNotIn("novalue", base_dc.to_dict().keys())


if __name__ == "__main__":
    unittest.main()
