"""Internet Utilities."""

import re


def convert_mac(
    mac: str,
    mac_format: str = ":",
    remove: bool = False,
    to_lower: bool = True,
    split_by: int = 2,
) -> str:
    """
    Convert a Mac address into regular string or use separators such as `:` or `-` for every 2 values.

    :param mac: Mac Address
    :type mac: str
    :param mac_format: _description_, defaults to `':'`
    :type mac_format: _type_, optional
    :param remove: Remove formate, must be split by 2., defaults to `False`
    :type remove: bool, optional
    :param to_lower: _description_, defaults to True
    :type to_lower: bool, optional
    :param to_lower: Return all values in lower case; if set to `False` will return in uppercase, defaults to `True`
    :return: Formatted Mac Address
    :rtype: str
    :param split_by: Split MAC Address by 2 or 4, defaults to `2`
    :type split_by: bool, optional
    :raises ValueError: Invalid MAC format.
    :return: _description_
    :rtype: str
    """
    mac_addr = ""
    if split_by not in [2, 4]:
        raise ValueError(f"Split by {str(split_by)} invalid must be 2 or 4")
    if remove:
        pattern = re.compile(
            "^[a-f0-9]{2}"
            + f"{mac_format}"
            + "[a-f0-9]{2}"
            + f"{mac_format}"
            + "[a-f0-9]{2}"
            + f"{mac_format}"
            + "[a-f0-9]{2}"
            + f"{mac_format}"
            + "[a-z0-9]{2}"
            + f"{mac_format}"
            + "[a-f0-9]{2}$",
            re.IGNORECASE,
        )
        if not pattern.match(mac):
            raise ValueError(f"Unable to remove {mac_format} due to invalid MAC {mac}")
        mac_addr = re.sub(rf"{mac_format}", "", mac)
    else:
        pattern = re.compile("^[a-f0-9]{12}$", re.IGNORECASE)
        if not pattern.match(mac):
            raise ValueError(f"Unable to reformat MAC using {mac_format} due to invalid MAC {mac}")
        mac_addr = f"{mac_format}".join(mac[i : i + split_by] for i in range(0, 12, split_by))
    return mac_addr.lower() if to_lower else mac_addr.upper()
