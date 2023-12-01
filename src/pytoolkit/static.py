# pylint: disable=line-too-long
"""Global Static Vars."""

from typing import cast

ENCODING: str = "utf-8"

NONETYPE: None = cast(None, object())
DEFAULT_TO: list[str] = ["john.doe@acme.com"]
DEFAULT_FROM: str = "python-script@acme.com"
DEFAULT_CC: list[str] = [""]
DEFAULT_BCC: list[str] = [""]
TMP_PEM_POSTFIX = "_pytookit.pem"
PEM_REGEX = (
    r".*[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}_pytoolkit\.pem$"
)

RE_DOMAIN = r".*\..*\.[com|net|gov]$"
RE_IP4 = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
