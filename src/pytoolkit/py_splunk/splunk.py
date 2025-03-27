# pylint: disable=logging-fstring-interpolation
"""Splunk Integrations."""

import datetime
import logging
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Optional, Union

import requests
import urllib3

from pytoolkit.static import SPLUNK_HEC_EVENTPATH
from pytoolkit.utilities import NONETYPE, BaseMonitor
from pytoolkit.utils import chunk, reformat_exception

splunk_log = logging.getLogger(__name__)

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
        # Build HEC Style Metrics
        hec_json["fields"] = {f"metric_name:{metric}": kwargs.pop(metric, None) for metric in metrics_list}
        hec_json["fields"] = dict(sorted(hec_json["fields"].items()))
    hec_json["event"] = {**hec_json["event"], **kwargs}
    hec_json["event"] = dict(sorted(hec_json["event"].items()))
    return hec_json


def splunk_hec_upload(  # pylint: disable=too-many-arguments,too-many-locals
    server: str,
    token: str,
    hec_data: list[dict[str, Any]],
    timeout: float = 15.0,
    verify: Union[str, bool] = True,
    port: int = 8088,
    chunk_size: int = 100,
    log: Any = splunk_log,
):
    """
    Upload Splunk Data.

    :param server: _description_
    :type server: str
    :param token: _description_
    :type token: str
    :param hec_data: List of dictionary events.
    :type hec_data: list[str,Any]
    :param verify: Validation of Rest call
    :type verify: [str|bool]
    :param port: Port to use, defaults to 8088
    :type port: int, optional
    :param chunk_size: Set size to split up data into if too large;
     hec_data must be a list of json entries, defaults to 100 (0 will indicate all)
    :type chunk_size: int, optional
    """
    if not verify:
        log.error(f'msg="SSL Verficiation is off recommended this be fixed"|{verify=}')
        urllib3.disable_warnings  # pylint: disable=pointless-statement
    url: str = f"https://{server}:{port}/{SPLUNK_HEC_EVENTPATH}"
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": f"Splunk {token}",
        "X-Splunk-Request-Channel": token,
    }
    chunk_data: list[list[dict[str, Any]]] = chunk(hec_data, chunk_size) if len(hec_data) > chunk_size > 0 else [hec_data]
    resp_list: list[dict[str, Any]] = []
    for payload in chunk_data:
        response: requests.Response = requests.post(url, headers=headers, json=payload, verify=verify, timeout=timeout)
        splunk_log.info(f'msg="uploaded splunk data response"|status_code={response.status_code}, response={response.json()}')
        resp_list.append(
            {
                "status_code": response.status_code,
                "payload_len": len(payload),
                "message": response.json() if response.json() else "",
            }
        )
        try:
            response.raise_for_status()
        except Exception as err:
            error = reformat_exception(err)
            splunk_log.error(f'msg="Unable to upload data to splunk server"|splunk_server={server}, {error=}')
    return resp_list


def splunk_upload_async():
    """_summary_"""
