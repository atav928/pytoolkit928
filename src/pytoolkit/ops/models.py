"""SSH Remote Comman Executions."""


from typing import Iterable, Mapping, Union, Any
from dataclasses import dataclass

from paramiko import PKey
from paramiko.auth_strategy import AuthStrategy

from pytoolkit.utilities import BaseMonitor
from pytoolkit.static import SSH_PORT


@dataclass
class SubProcessReturn(BaseMonitor):
    """Subprocess return."""

    stdin: Any
    stdout: Any
    stderr: Any
    returncode: int
    command: str
    timeout: int
    get_pty: bool


@dataclass
class Connector(BaseMonitor):
    """Paramiko Connector Variables"""

    hostname: str
    port: int = SSH_PORT
    username: Union[str, None] = None
    password: Union[str, None] = None
    pkey: Union[PKey, None] = None
    key_filename: Union[str, None] = None
    timeout: Union[float, None] = None
    allow_agent: bool = True
    look_for_keys: bool = True
    compress: bool = False
    sock: Any = None
    gss_auth: bool = False
    gss_kex: bool = False
    gss_deleg_creds: bool = True
    gss_host: Union[str, None] = None
    banner_timeout: Union[float, None] = None
    auth_timeout: Union[float, None] = None
    channel_timeout: Union[float, None] = None
    gss_trust_dns: bool = True
    passphrase: Union[str, None] = None
    disabled_algorithms: Union[Mapping[str, Iterable[str]], None] = None
    transport_factory: Any = None
    auth_strategy: Union[AuthStrategy, None] = None
