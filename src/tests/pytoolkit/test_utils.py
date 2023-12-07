# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test Utilities."""

from enum import Enum
import functools
import re
import unittest
from unittest import mock

from pytoolkit import utils
from pytoolkit import static


def patch_getfqdn(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return "server01.b100.example.com"

    return wrapper


def test_getfqdn():
    # Create a mock object for the socket module
    with mock.patch("socket.getfqdn") as mock_getfqdn:
        # Set the return value of mock_getfqdn
        mock_getfqdn.return_value = "server01.b100.example.com"
        result = utils.return_hostinfo(fqdn=True)
        assert result == "server01.b100.example.com"

def test_gethostname():
    # Create a mock object for the socket module
    with mock.patch("socket.gethostname") as mock_hostname:
        # Set the return value of mock_getfqdn
        mock_hostname.return_value = "server01.b100.example.com"
        result = utils.return_hostinfo(fqdn=False)
        print(result)
        assert result == "server01.b100"

class TestStringMethods(unittest.TestCase):
    def test_os(self) -> None:
        print("Checking System Platform.")
        s: str = utils.os_plat()
        self.assertIn(s, ["darwin", "linux", "windows", "java"])

    def test_isstring(self) -> None:
        print("Testing isstring() function.")
        valid = "this is a string"
        invalid = 1
        self.assertTrue(utils.isstring(valid))
        self.assertFalse(utils.isstring(invalid))

    def test_refexcept(self) -> None:
        print("Testing reformating exceptions.")
        err = None
        error = None  # type: ignore
        try:
            value: float = 1 / 0
            print(value)
        except Exception as err:
            error: str = utils.reformat_exception(err)
            self.assertIsInstance(err, Exception, "exception passed")
        self.assertIsInstance(error, str, f"exception converted to string {error}")

    def test_string_or_list(self) -> None:
        print("Testing string to list conversion.")
        string = "some string to convert to list"
        multistring = "Multiple values|used to split out,into a list"
        self.assertIs(
            type(utils.string_or_list(string, delimeters=" ")),
            list,
            "String was converted to a list",
        )
        self.assertEqual(
            len(utils.string_or_list(multistring, r"\,|\ |\|")),
            9,
            "Split out mutilple string to 10 values.",
        )

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
            self.assertIsInstance(utils.set_bool(v), bool, f"Value {v} is a bool")
        values = "/path/to/certificate"
        print(f"Testing if location will return from {values}")
        self.assertIsNot(utils.set_bool(values), True)

    def test_enum(self) -> None:
        print("Testing Enumaration Function.")
        Numbers: type[Enum] = utils.enum(ONE=1, TWO=2, THREE="three")
        self.assertEqual(Numbers.ONE, 1)
        self.assertEqual(Numbers.TWO, 2)
        self.assertEqual(Numbers.THREE, "three")

    @patch_getfqdn
    def test_hostinfo_host(self):
        result = utils.return_hostinfo(fqdn=False)
        print(result)
        self.assertIsNone(re.match(static.RE_DOMAIN, result))


if __name__ == "__main__":
    unittest.main()
