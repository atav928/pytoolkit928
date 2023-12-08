"""OS Operations."""

from typing import Any, Union
import subprocess

from pytoolkit.utils import string_or_list

def return_subprocess_error(**kwargs: Any) -> subprocess.CompletedProcess[Any]:
    """
    Reformates exception for subprocess error.

    :return: _description_
    :rtype: subprocess.CompletedProcess[Any]
    """
    error = kwargs["error"]
    return subprocess.CompletedProcess(args=[], stdout="", returncode=255, stderr=error)

def exec_cmd(host: str, command: str, user: Union[str,None] = None,
             key: Union[str,None] = None, check: bool=False, text: bool =True,
             capture_output: bool=True, timeout: float = 5.0) -> subprocess.CompletedProcess[Any]:
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
    cmd: list[str] = string_or_list(command, delimeters=' |,')  # type: ignore
    exect = []
    if host not in ["self", "localhost"]:
        exect = [host]
    if key:
        exect.extend(['-i', key])
    if user:
        exect.append(user)
    result = subprocess.run(exect + cmd,
                            shell=False,
                            capture_output=capture_output,
                            text=text,
                            check=check,
                            timeout=timeout)
    return result
