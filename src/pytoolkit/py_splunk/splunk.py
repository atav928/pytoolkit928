"""Splunk Integrations."""

from collections import OrderedDict
import datetime
from typing import Any, Optional, Union

from dataclasses import dataclass
import requests

from pytoolkit.utilities import BaseMonitor, NONETYPE

splunk_url = "{}//{}:{}"

@dataclass
class SplunkHecHeader(BaseMonitor):
    """Splunk Hec Header."""

    splunk_server: str
    token: str
    sourcetype: Optional[str] = NONETYPE
    source: Optional[str] = NONETYPE
    index: Optional[str] = NONETYPE
    splunk_port: int = 8088
    verify: Union[str, bool] = True
    upload: bool = True
    timeout: float = 15.0
    schema: str = "https"


def splunk_format(**kwargs: Any) -> str:
    """
    Reformat a list of key:value pairs into a simple logging message for Splunk.

    :return: _description_
    :rtype: str
    """
    ordered: OrderedDict[str, Any] = OrderedDict(sorted(kwargs.items()))
    string: list[str] = [f'{str(key)}="{value}"' for key, value in ordered.items()]
    return ",".join(string)


# TODO: fix the ability to send HEC formats in chuncks. ippoad
def splunk_hec_format(
    host: str,
    source: str,
    sourcetype: str,
    metrics_list: Union[list[str], None] = None,
    **kwargs: Any,
) -> dict[str, Any]:
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
        "time": kwargs.pop("time", datetime.datetime.now().timestamp()),
        "host": host,
        "source": source,
        "sourcetype": sourcetype,
        "event": {},
    }
    if metrics_list:
        # Build HEC style Metrics
        hec_json["fields"] = {
            f"metric_name:{metric}": kwargs.pop(metric, None) for metric in metrics_list
        }
        hec_json["fields"] = dict(sorted(hec_json["fields"].items()))
    hec_json["event"] = {**hec_json["event"], **kwargs}
    hec_json["event"] = dict(sorted(hec_json["event"].items()))
    return hec_json

def splunk_upload(
    server: str,
    token: str,
    hec_data: Any,
    verify: Any,
    timeout: float,
    port: int = 8088,
    chunk_size: int = 0,
):
    """
    Upload Splunk Data.

    :param server: _description_
    :type server: str
    :param token: _description_
    :type token: str
    :param hec_data: _description_
    :type hec_data: Any
    :param verify: _description_
    :type verify: str
    :param port: _description_, defaults to 8088
    :type port: int, optional
    :param chunk_size: Set size to split up data into if too large;
     hec_data must be a list of json entries, defaults to 0 or all data
    :type chunk_size: int, optional
    """
    EVENTPATH = "services/collector/event"
    # split_list = list(split(hec_json_list, 10))
    # for server in server_list:
    url = f"https://{server}:{port}/{EVENTPATH}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Splunk {token}",
        "X-Splunk-Request-Channel": token,
    }
    payload = hec_data
    response = requests.post(
        url, headers=headers, json=payload, verify=verify, timeout=timeout
    )
    msg = f'msg="uploaded splunk data response"|status_code={response.status_code}, response={response.json()}'
    response.raise_for_status()
