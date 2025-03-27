"""File Mock."""

import unittest
from unittest.mock import mock_open
from unittest import mock
from pathlib import Path
from pytoolkit.files import read_yaml, get_var_dir, get_config_location

config_locations = [
                str(Path.joinpath(Path.home() / ".config/appname.yaml")),
                str(Path.joinpath(Path.home() / ".config/appname.yml")),
                str(Path("/etc/infrasec-tools/appname.yaml")),
                str(Path("/etc/infrasec-tools/appname.yml"))
]

class TestReadYaml(unittest.TestCase):
    @mock.patch("builtins.open", mock_open(read_data="data"))
    @mock.patch("pathlib.Path.is_file")
    def test_read_yaml(self, patched_isfile) -> None:
        print("Testing Yaml Read.")
        # valid file case
        patched_isfile.return_value = True
        result = read_yaml("some_file.yaml")
        self.assertEqual("data", result)

    def test_get_var_dir(self):
        self.assertIs(type(get_var_dir()), str)

    def test_config_loc(self) -> None:
        self.assertIs(get_config_location(config_location=config_locations),'')