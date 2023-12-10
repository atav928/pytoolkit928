# pylint: disable=invalid-name
"""Files."""

import re
import json
from typing import Any, Union
from pathlib import Path
import platform
import tempfile

import yaml

from pytoolkit.static import ENCODING, FILE_UMASK_PERMISSIONS, CONFIG_PATH


class BytesDump(json.JSONEncoder):
    """Resovlve error with byte present in Dict."""

    def default(self, o: Any) -> Union[str, Any]:
        """Resolve error with byte in Dict."""
        if isinstance(o, bytes):
            return o.decode()
        return json.JSONEncoder.default(self, o)


def get_config_section(filename: str, ftype: str, section: str = ""):
    """
    Returns a configuration dictionary or a section of a configuration if found.

    :param filename: _description_
    :type filename: str
    :param ftype: _description_
    :type ftype: str
    :param section: _description_, defaults to ""
    :type section: str, optional
    :return: _description_
    :rtype: _type_
    """
    settings = read_yaml(Path(filename))
    if section:
        settings = settings.get(section, {})
    return settings


def read_yaml(filename: Path) -> dict[str, Any]:
    """
    Read in a YAML configuration file.

    :param filename: Yaml File Full Path
    :type filename: Path
    :return: Yaml Configurations
    :rtype: dict[str,Any]
    """
    check_file(filename=str(filename))
    with open(filename, "r", encoding=ENCODING) as r_yaml:
        settings: Any = yaml.safe_load(r_yaml)
    return settings


def get_tempdir() -> str:
    """Returns tempdir"""
    return tempfile.gettempdir()


def get_var_dir(extend_path: Union[str, None] = None, mode: str = "default") -> str:
    """
    Get default var directory depending on OS. Extend to application path if path supplied.
     Allows for user to create a directory strcture where reports or logs can be stored. Using
     a variable directory or extend a path in a users home directory.

    :param extend_path: Extends the system default location;
     creates a new app directory, defaults to None
    :type extend_path: str, optional
    :return: Log Directory for Logs
    :rtype: str
    """
    directory: dict[str, Path] = {
        "darwin": Path.joinpath(Path.home() / "Library/Logs"),
        "linux": Path("/var/log"),
    }
    plat: str = platform.system()
    try:
        path = (
            Path(f"{str(directory[plat.lower()])}/{extend_path}")
            if extend_path
            else Path(str(directory[plat.lower()]))
        )
        mkdir(path=path, mode=mode)
        return str(path)
    except KeyError:
        path = (
            Path(f"{str(tempfile.gettempdir())}/{extend_path}")
            if extend_path
            else Path(tempfile.gettempdir())
        )
        mkdir(path=path, mode=mode)
        return str(path)


def set_location(
    location: str, extend_path: Union[str, None] = None, mode: str = "default"
) -> str:
    """Set default logDir or configuration directory based on mode defined."""
    loc = "var"
    if bool(re.match(r"(home|homedir)", location)):
        loc = "home"
    mode = mode if mode in FILE_UMASK_PERMISSIONS else "default"
    base_dir = {"home": set_homedir, "var": get_var_dir}
    return base_dir[loc](extend_path=extend_path, mode=mode)


def set_homedir(extend_path: Union[str, None] = None, mode: str = "default") -> str:
    """
    Return the users home dir and can extend if using a subdirctory.
     Use `mode` to restrict permissions.

    :param extend_path: _description_, defaults to None
    :type extend_path: Union[str,None], optional
    :param mode: _description_, defaults to "default"
    :type mode: str, optional
    :return: _description_
    :rtype: str
    """
    path = Path(Path.home() / extend_path) if extend_path else Path.home()
    mkdir(path=path, mode=mode)
    return str(path)


def mkdir(path: Path, mode: str = "default") -> None:
    """Makes Dir based on permissions passed."""
    # for parent in reversed(path.parents):
    path.mkdir(mode=FILE_UMASK_PERMISSIONS[mode], parents=True, exist_ok=True)


def get_home() -> str:
    """Return current users `home` direcotry."""
    return str(Path.home())


def with_suffix(logName: str) -> str:
    """Add suffix to logname."""
    return str(Path(logName).with_suffix(".log"))


def check_file(filename: str) -> None:
    """
    Checks if a file exists.

    :param filename: _description_
    :type filename: str
    :raises ValueError: _description_
    """
    if not Path(filename).is_file():
        raise ValueError(f"Not a file {filename}")


def get_config_location(
    config_location: list[str],
    app_name: Union[str, None] = None,
    file_format: str = "yml",
) -> str:
    """
    Retrieve configuraiton lcoation if one exists in the paths to search.

        Ex:
            config_location = [
                str(Path.joinpath(Path.home() / ".config/application.yaml")),
                str(Path.joinpath(Path.home() / ".config/application.yml")),
                str(Path("/etc/appname/appconfig.yaml")),
                str(Path("/Users/guest/Library/logs/appname/appconfig.yml"))
            ]
        OR:
            config_location = [
                str(Path.joinpath(Path.home() / ".config/application.yaml")),
                str(Path.joinpath(Path.home() / ".config/application.yml")),
                str(Path("/etc/appname/appconfig.yaml")),
                str(Path("/Users/guest/Library/logs/appname/appconfig.yml"))
            ]
    :param config_location: _description_
    :type config_location: list[str]
    :return: _description_
    :rtype: str
    """
    for location in config_location:
        # TODO: Allow for diff types as currentlu just allowing yaml.
        # if Path.is_file(Path(
        #    CONFIG_PATH.format(location,app_name, file_format) if app_name else location)
        # ):
        if Path.is_file(Path(location)):
            return location
        return ""
