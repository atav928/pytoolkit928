# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test Utilities."""

import unittest

from pytoolkit import utils


class TestStringMethods(unittest.TestCase):
    def test_os(self) -> None:
        print("Checking System Platform.")
        s: str = utils.os_plat()
        self.assertIn(s, ['darwin', 'linux', 'windows', 'java'])

    def test_isstring(self) -> None:
        print("Testing isstring() function.")
        valid = 'this is a string'
        invalid = 1
        self.assertTrue(utils.isstring(valid))
        self.assertFalse(utils.isstring(invalid))

    def test_refexcept(self) -> None:
        print("Testing reformating exceptions.")
        err = None
        error = None  # type: ignore
        try:
            value: float = 1/0
            print(value)
        except Exception as err:
            error: str = utils.reformat_exception(err)
            self.assertIsInstance(err, Exception, "exception passed")
        self.assertIsInstance(
            error, str, f"exception converted to string {error}")

    def test_string_or_list(self) -> None:
        print("Testing string to list conversion.")
        string = "some string to convert to list"
        multistring = "Multiple values|used to split out,into a list"
        self.assertIs(type(utils.string_or_list(string, delimeters=' ')),
                      list, "String was converted to a list")
        self.assertEqual(len(utils.string_or_list(
            multistring, ',| |\|')), 9, "Split out mutilple string to 10 values.")

    def test_username(self):
        print("Testing Username Values.")
        name = utils.return_username()
        self.assertIsInstance(name, str, f"Returned username {name}")

    def test_hostname(self) -> None:
        hostname = utils.return_hostinfo()
        print(f"Testing hostname value {hostname}.")
        self.assertIsInstance(hostname, str)

    def test_bool(self) -> None:
        values = ["true", "false", True, False]
        for v in values:
            print(f"Testing if {v} is True/False")
            self.assertIsInstance(utils.set_bool(
                v), bool, f"Value {v} is a bool")
        values = "/path/to/certificate"
        print(f"Testing if location will return from {values}")
        self.assertIsNot(utils.set_bool(values), True)

    def test_enum(self) -> None:
        print("Testing Enumaration Function.")
        Numbers = utils.enum(ONE=1, TWO=2, THREE='three')
        self.assertEqual(Numbers.ONE,1)
        self.assertEqual(Numbers.TWO,2)
        self.assertEqual(Numbers.THREE,'three')

if __name__ == '__main__':
    unittest.main()
