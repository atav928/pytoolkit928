# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test Utilities."""

from typing import Any
import unittest

from pytoolkit.py_splunk import splunk

sample_data: dict[str, Any] = {
    "action": "test_cpu",
    "ca_type": "validation_authority",
    "city": "New York",
    "country": "US",
    "cpu_count": 4,
    "cpu_usage": 4.25,
    "datacenter": "jfk",
    "datacenter_num": "jfk100",
    "env": "prod",
    "environment": "production",
    "event_type": "stat_cpu via LOCAL",
    "function": "stat_cpu",
    "hostname": "server.jfk100.example.com",
    "level": "info",
    "message": "Gathering CPU Avg Load",
    "region": "United States",
    "username": "monitor",
}


class TestSplunk(unittest.TestCase):
    def test_hec(self) -> None:
        self.assertIsInstance(sample_data, dict)
        print("Reformating sample data to HEC Splunk format.")
        hec: dict[str, Any] = splunk.splunk_hec_format(
            host="sample.com",
            source="source",
            sourcetype="source_type",
            index="some_index",
            **sample_data,
        )
        self.assertIsInstance(hec["events"], dict)
        self.assertIs(hec["events"]["index"], "some_index")

    def test_splunk_form(self) -> None:
        string: str = splunk.splunk_format(**sample_data)
        print("Converting Splunk Data Dictionary to a string format.")
        self.assertIsInstance(string, str)
