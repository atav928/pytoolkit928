# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test Utilities Inet."""

import unittest

from pytoolkit.utilities import inet

VALUE3 = "12346345fdggqaggagfadfds"
VALUE2 = "5eb76c15ecc4"
VALUE1 = "5e:b7:6c:15:ec:c4"


class TestStringMethods(unittest.TestCase):
    def test_mac_conversion(self):
        self.assertEqual(inet.convert_mac(mac=VALUE2), VALUE1)
        self.assertEqual(inet.convert_mac(mac=VALUE1, remove=True), VALUE2)
        self.assertRaises(ValueError, inet.convert_mac, VALUE3)
        self.assertRaises(ValueError,inet.convert_mac,**{'mac': VALUE3,'remove': True})
        self.assertEqual(
            inet.convert_mac(mac=VALUE1, remove=True, to_lower=False), VALUE2.upper()
        )
        self.assertRaises(ValueError,inet.convert_mac,**{'mac': VALUE3,'remove': True, 'split_by': 6})
