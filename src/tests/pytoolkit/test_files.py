"""File Mock."""

import unittest
from unittest.mock import mock_open
from unittest import mock

from pytoolkit.files import read_yaml, get_var_dir


class TestReadYaml(unittest.TestCase):
    @mock.patch("builtins.open", mock_open(read_data="data"))
    @mock.patch("os.path.isfile")
    def test_read_yaml(self, patched_isfile) -> None:
        print("Testing Yaml Read.")
        # valid file case
        patched_isfile.return_value = True
        result = read_yaml("some_file.yaml")
        self.assertEqual("data", result)


if __name__ == "__main__":
    unittest.main()
