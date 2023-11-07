"""Test Utilities."""

import unittest

from pytoolkit import utils


class TestStringMethods(unittest.TestCase):
    def test_os(self) -> None:
        s: str = utils.os_plat()
        print(s)
        self.assertIn(s, ['darwin', 'linux', 'windows', 'java'])

    def test_isstring(self) -> None:
        valid = 'this is a string'
        invalid = 1
        self.assertTrue(utils.isstring(valid))
        self.assertFalse(utils.isstring(invalid))

    def test_refexcept(self) -> None:
        err = None
        error = None
        try:
            value: float = 1/0
            print(value)
        except Exception as err:
            error: str = utils.reformat_exception(err)
            self.assertIsInstance(err,Exception)
        self.assertIsInstance(error,str)

if __name__ == '__main__':
    unittest.main()
