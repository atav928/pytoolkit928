# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test Utilities."""

from enum import Enum
import functools
import re
import unittest
from unittest import mock

from pytoolkit import utils
from pytoolkit import static

SANTIZE_DATA = {'password': 'welcome123', 'username': 'testuser'}

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
        error = None
        error2 = None
        try:
            value: float = 1 / 0
        except Exception as err:
            error = utils.reformat_exception(err)
            error2 = utils.reform_except(err)
            self.assertIsInstance(err, Exception, "exception passed")
        self.assertIsInstance(error, str, f"exception converted to string {error}")
        self.assertIsInstance(error2, str, f"Reformated Error {error2}")

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
        self.assertIsNone(utils.string_or_list(value=None))

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

    def test_camel(self):
        camel_case = "camelCase"
        self.assertEqual(utils.camel_to_snake(camel_case), "camel_case")

    def test_snake(self):
        snake_case = "snake_case"
        self.assertEqual(utils.snake_to_camel(snake_case), "snakeCase")

    def test_airport_codes(self):
        valid = 'jfk'
        invalid = 'att'
        valid_response = utils.get_airport_info(valid)
        invalid_response = utils.get_airport_info(invalid)
        self.assertEqual(valid_response['iata'],'JFK')
        self.assertEqual(valid_response['country'],'US')
        self.assertIsNone(invalid_response['country'])
        self.assertIsInstance(valid_response,dict)
        self.assertIsInstance(invalid_response,dict)

    def test_chunk(self):
        mock_hec_data = [{'empty': 'dict','for': 'testing', 'value': x} for x in range(200)]
        chunk_data = utils.chunk_func(mock_hec_data,100)
        self.assertEqual(len(chunk_data),2,'Data has been chunked into two arrays')
        self.assertEqual(len(chunk_data[1]),100,'Confirmed data was split into 100 events in series 2')
        chunk_data = utils.chunk(mock_hec_data,50)
        self.assertEqual(len(chunk_data),4,'Lamda function split data into 4 series')

    def test_split(self):
        values = list(utils.split(range(0,300),10))
        self.assertEqual(len(values),300/10,'Split function split events out by 30')

    def test_sanatize(self):
        new_dict = utils.sanatize_data(data=SANTIZE_DATA)
        self.assertEqual(new_dict['password'], '[MASKED]')
        self.assertNotEqual(new_dict['password'],SANTIZE_DATA['password'])

    def test_verify_list(self):
        test_str = 'one,two,three'
        test_lst = ['one',2,'three']
        new_str = utils.verify_list(test_str)
        new_lst = utils.verify_list(test_lst)
        self.assertEqual(test_lst,new_lst,'List unchanged')
        self.assertIsInstance(new_str,list,'Converted string to a list')
        self.assertRaises(ValueError,utils.verify_list,{'object':'not-a-list'})
