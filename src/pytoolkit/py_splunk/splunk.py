"""Splunk Integrations."""

from collections import OrderedDict
import datetime
from typing import Any, Union

def splunk_format(**kwargs: Any) -> str:
    """
    Reformat a list of key:value pairs into a simple logging message for Splunk.

    :return: _description_
    :rtype: str
    """
    ordered: OrderedDict[str, Any] = OrderedDict(sorted(kwargs.items()))
    string: list[str] = [f"{str(key)}=\"{value}\"" for key, value in ordered.items()]
    return ','.join(string)


# TODO: fix the abilit to send HEC formats in chuncks.
def splunk_hec_format(host: str, source: str, sourcetype: str,
                      metrics_list: Union[list[str],None] = None,
                      **kwargs: Any) -> dict[str, Any]:
    """Create a JSON style hec format.

    :param host: hostname
    :type host: str
    :param source_name: source of dataa
    :type source_name: str
    :param metrics_list: list of metrics type fileds found in arguments
    :type metrics_list: list[str]
    :param kwargs: key:value pairs to extract and format data structure
    :return: Splunk Hec Datastructure
    :rtype: dict[str,Any]
    """
    hec_json: dict[str, Any] = {
        "time": datetime.datetime.now().timestamp(),
        "host": host,
        "source": source,
        "sourcetype": sourcetype,
        "events": {}
    }
    if metrics_list:
        # Build HEC style Metrics
        hec_json["fields"] = {f"metric_name:{metric}": kwargs.pop(
            metric, None) for metric in metrics_list}
        hec_json["fields"] = dict(sorted(hec_json["fields"].items()))
    hec_json["events"] = {**hec_json["events"], **kwargs}
    hec_json["events"] = dict(sorted(hec_json["events"].items()))
    return hec_json
