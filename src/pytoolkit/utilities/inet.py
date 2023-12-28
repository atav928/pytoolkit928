"""Internet Utilities."""
import re

def convert_mac(mac: str, mac_format: str = ':', remove: bool = False) -> str:
    """
    Convert a Mac address into regular string or use seperators such as `:` or `-` for every 2 values.

    :param mac: Mac Address
    :type mac: str
    :param mac_format: _description_, defaults to ':'
    :type mac_format: _type_, optional
    :param remove: _description_, defaults to False
    :type remove: bool, optional
    :return: Formated Mac Address
    :rtype: str
    """
    if remove:
        return re.sub(rf'{mac_format}','',mac)
    return f'{mac_format}'.join(mac[i:i+2] for i in range(0,12,2))
