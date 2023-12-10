"""SSH Remote Comman Executions."""
import subprocess
from typing import Union, Any

import paramiko
from paramiko import AutoAddPolicy
from paramiko.client import SSHClient

from pytoolkit.ops.models import SubProcessReturn, Connector
from pytoolkit.static import DISABLED_ALGORITHMS, SSH_PORT
from pytoolkit.utils import string_or_list

def _ssh_client():
    return paramiko.SSHClient()


class SSHConnector:
    _missing_host_key_policy = AutoAddPolicy()
    _private_key = ""
    _timeout: float = 120.0
    _disabled_algorithms = DISABLED_ALGORITHMS

    def __init__(
        self,
        hostname: str,
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        port: int = SSH_PORT,
        **kwargs: Any,
    ):
        self.client: SSHClient = _ssh_client()
        self.hostname = hostname
        self._timeout = kwargs.pop("timeout", self._timeout)
        banner_timeout = kwargs.pop("banner_timeout", self._timeout)
        auth_timeout = kwargs.pop("auth_timeout", self._timeout)
        disabled_algorithms = kwargs.pop(
            "disabled_algorithms", self._disabled_algorithms
        )
        if kwargs.get("auto_add", False) == True:
            self.client.set_missing_host_key_policy(self._missing_host_key_policy)
        self.connection_settings = Connector.create_from_kwargs(
            **{
                **{
                    "hostname": hostname,
                    "username": username,
                    "password": password,
                    "port": port,
                    "timeout": self._timeout,
                    "banner_timeout": banner_timeout,
                    "auth_timeout": auth_timeout,
                    "disabled_algorithms": disabled_algorithms,
                },
                **kwargs,
            }
        )
        self.sftp = None

    @property
    def disabled_algorithms(self):
        return self._disabled_algorithms

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value: float):
        self._timeout = value

    def connect(self):
        """
        SSHClient Context Manager.

        Connect to an SSH server and authenticate to it.  The server's host key
        is checked against the system host keys (see `load_system_host_keys`)
        and any local host keys (`load_host_keys`).  If the server's hostname
        is not found in either set of host keys, the missing host key policy
        is used (see `set_missing_host_key_policy`).  The default policy is
        to reject the key and raise an `.SSHException`.

        Authentication is attempted in the following order of priority:

            - The ``pkey`` or ``key_filename`` passed in (if any)

              - ``key_filename`` may contain OpenSSH public certificate paths
                as well as regular private-key paths; when files ending in
                ``-cert.pub`` are found, they are assumed to match a private
                key, and both components will be loaded. (The private key
                itself does *not* need to be listed in ``key_filename`` for
                this to occur - *just* the certificate.)

            - Any key we can find through an SSH agent
            - Any "id_rsa", "id_dsa" or "id_ecdsa" key discoverable in
              ``~/.ssh/``

              - When OpenSSH-style public certificates exist that match an
                existing such private key (so e.g. one has ``id_rsa`` and
                ``id_rsa-cert.pub``) the certificate will be loaded alongside
                the private key and used for authentication.

            - Plain username/password auth, if a password was given

        If a private key requires a password to unlock it, and a password is
        passed in, that password will be used to attempt to unlock the key.

        :param str hostname: the server to connect to
        :param int port: the server port to connect to
        :param str username:
            the username to authenticate as (defaults to the current local
            username)
        :param str password:
            Used for password authentication; is also used for private key
            decryption if ``passphrase`` is not given.
        :param str passphrase:
            Used for decrypting private keys.
        :param .PKey pkey: an optional private key to use for authentication
        :param str key_filename:
            the filename, or list of filenames, of optional private key(s)
            and/or certs to try for authentication
        :param float timeout:
            an optional timeout (in seconds) for the TCP connect
        :param bool allow_agent:
            set to False to disable connecting to the SSH agent
        :param bool look_for_keys:
            set to False to disable searching for discoverable private key
            files in ``~/.ssh/``
        :param bool compress: set to True to turn on compression
        :param socket sock:
            an open socket or socket-like object (such as a `.Channel`) to use
            for communication to the target host
        :param bool gss_auth:
            ``True`` if you want to use GSS-API authentication
        :param bool gss_kex:
            Perform GSS-API Key Exchange and user authentication
        :param bool gss_deleg_creds: Delegate GSS-API client credentials or not
        :param str gss_host:
            The targets name in the kerberos database. default: hostname
        :param bool gss_trust_dns:
            Indicates whether or not the DNS is trusted to securely
            canonicalize the name of the host being connected to (default
            ``True``).
        :param float banner_timeout: an optional timeout (in seconds) to wait
            for the SSH banner to be presented.
        :param float auth_timeout: an optional timeout (in seconds) to wait for
            an authentication response.
        :param float channel_timeout: an optional timeout (in seconds) to wait
             for a channel open response.
        :param dict disabled_algorithms:
            an optional dict passed directly to `.Transport` and its keyword
            argument of the same name.
        :param transport_factory:
            an optional callable which is handed a subset of the constructor
            arguments (primarily those related to the socket, GSS
            functionality, and algorithm selection) and generates a
            `.Transport` instance to be used by this client. Defaults to
            `.Transport.__init__`.
        :param auth_strategy:
            an optional instance of `.AuthStrategy`, triggering use of this
            newer authentication mechanism instead of SSHClient's legacy auth
            method.

            .. warning::
                This parameter is **incompatible** with all other
                authentication-related parameters (such as, but not limited to,
                ``password``, ``key_filename`` and ``allow_agent``) and will
                trigger an exception if given alongside them.

        :returns:
            `.AuthResult` if ``auth_strategy`` is non-``None``; otherwise,
            returns ``None``.

        :raises BadHostKeyException:
            if the server's host key could not be verified.
        :raises AuthenticationException:
            if authentication failed.
        :raises UnableToAuthenticate:
            if authentication failed (when ``auth_strategy`` is non-``None``;
            and note that this is a subclass of ``AuthenticationException``).
        :raises socket.error:
            if a socket error (other than connection-refused or
            host-unreachable) occurred while connecting.
        :raises NoValidConnectionsError:
            if all valid connection targets for the requested hostname (eg IPv4
            and IPv6) yielded connection-refused or host-unreachable socket
            errors.
        :raises SSHException:
            if there was any other error connecting or establishing an SSH
            session.
        """
        self.client.connect(**self.connection_settings.to_dict())

    def exec_command(self, **kwargs: Any) -> SubProcessReturn:
        """
        (method) def exec_command(
        command: str,
        bufsize: int = -1,
        timeout: Union[float, None] = None,
        get_pty: bool = False,
        environment: Mapping[str, str] | None = None
        )
        """
        timeout = kwargs.pop("timeout", self._timeout)
        get_pty = kwargs.pop("get_pty", False)
        # try:
        self.connect()
        stdin, stdout, stderr = self.client.exec_command(
            timeout=timeout, get_pty=get_pty, **kwargs
        )
        return SubProcessReturn(
            stderr=stderr,
            stdin=stdin,
            stdout=stdout,
            returncode=255 if not stderr.readline() else 0,
            timeout=timeout,
            get_pty=get_pty,
            command=kwargs["command"],
        )
        # except paramiko.SSHException as err:
        # return SubProcessReturn(stderr=stderr,stdin=stdin,stdout=stdout,returncode=255 if not stderr.readline() else 0,timeout=timeout,get_pty=get_pty,command=kwargs["command"])

    def open_sftp(self):
        self.sftp = self.client.open_sftp()


def return_subprocess_error(**kwargs: Any) -> subprocess.CompletedProcess[Any]:
    """
    Reformates exception for subprocess error.

    :return: _description_
    :rtype: subprocess.CompletedProcess[Any]
    """
    error = kwargs["error"]
    return subprocess.CompletedProcess(args=[], stdout="", returncode=255, stderr=error)


def exec_cmd(
    host: str,
    command: str,
    user: Union[str, None] = None,
    key: Union[str, None] = None,
    check: bool = False,
    text: bool = True,
    capture_output: bool = True,
    timeout: float = 5.0,
) -> subprocess.CompletedProcess[Any]:
    """
    Runs Command via subprocess. Configure local ssh first if using defaults if executing remote command.

    :param host: target host to send the command to
    :type host: str
    :param command: command to run on the host
    :type command: str
    :param user: user to use to login to host, defaults to None
    :type user: _type_, optional
    :param key: _description_, defaults to None
    :type key: _type_, optional
    :param stdin: override sys.stdin, defaults to None
    :type stdin: _type_, optional
    :param check: pass to *subprocess.run*; if set, checks return code
        and raises subprocess.CalledProcessError, if none-zero result, defaults to False
    :type check: bool, optional
    :return: _description_
    :rtype: _type_
    """
    cmd: list[str] = []
    cmd: list[str] = string_or_list(command, delimeters=" |,")  # type: ignore
    exect = []
    if host not in ["self", "localhost"]:
        exect = [host]
    if key:
        exect.extend(["-i", key])
    if user:
        exect.append(user)
    result = subprocess.run(
        exect + cmd,
        shell=False,
        capture_output=capture_output,
        text=text,
        check=check,
        timeout=timeout,
    )
    return result
