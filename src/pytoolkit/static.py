# pylint: disable=line-too-long
"""Global Static Vars."""

from typing import cast

ENCODING: str = "utf-8"

# See https://www.linuxtrainingacademy.com/all-umasks/
FILE_UMASK_PERMISSIONS = {
    "default": 0o40775,  # umask 002 rw-rw-r- rwxrwx-r
    "restrictive": 0o40770,  # umask 037 rw-r--- rwxr---
    "root": 0o40755,  # umask 022 rw-r-r- rwxr-xr-x
}

NONETYPE: None = cast(None, object())
DEFAULT_TO: list[str] = ["john.doe@acme.com"]
DEFAULT_FROM: str = "python-script@acme.com"
DEFAULT_CC: list[str] = [""]
DEFAULT_BCC: list[str] = [""]
TMP_PEM_POSTFIX = "_pytookit.pem"
PEM_REGEX = r".*[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}_pytoolkit\.pem$"

RE_DOMAIN = r".*\.(com|net|gov)$"
RE_IP4 = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
SANATIZE_KEYS = [
    "password",
    "cacontext",
    "log",
    "plaintext",
    "token",
    "jwt",
    "cert",
    "authorization",
    "auth",
    "-p",
    "-P",
]
CONFIG_PATH = "{}/{}.{}"
SSH_PORT = 22
DISABLED_ALGORITHMS = {
    "ciphers": [
        "aes128-cbc",
        "aes192-cbc",
        "aes256-cbc",
        "3des-cbc",
    ],
    "macs": ["hmac-sha1", "hmac-md5", "hmac-sha1-96", "hmac-md5-96"],
    "keys": ["ssh-dss", "ssh-rsa"],
    "pubkeys": ["ssh-rsa", "ssh-dss"],
    "kex": [
        "diffie-hellman-group1-sha1",
        "diffie-hellman-group14-sha1",
        "diffie-hellman-group-exchange-sha1",
    ],
}
NO_AIRPORTDATA = {
    "icao": None,
    "iata": None,
    "name": None,
    "city": None,
    "subd": None,
    "country": None,
    "elevation": None,
    "lat": None,
    "lon": None,
    "tz": None,
    "lid": None,
}
SPLUNK_HEC_EVENTPATH = "services/collector/event"
