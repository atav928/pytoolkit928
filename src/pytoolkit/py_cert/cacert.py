"""Create a custo CA."""

import re
import tempfile
import uuid

from pathlib import Path
import certifi

from pytoolkit.static import ENCODING, PEM_REGEX, TMP_PEM_POSTFIX
from pytoolkit.utils import check_file, return_filelines, string_or_list


def create_custom_cert(certstore: list[str]) -> tuple[str, list[str]]:
    """
    Creates a temp custom certificate.

    :param certstore: list of pem certificates to use.
    :type certstore: list[str]
    :return: Returns CA_TMP_FILE, Raw CA_CONTEXT
    :rtype: tuple[str,list[str]]
    """
    # verify correct type
    certstore = string_or_list(value=certstore)
    # create context
    ca_context = castore_create_context(certstore=certstore)
    ca_tmp_file = castore_create_tmp(ca_context=ca_context)
    return ca_tmp_file, ca_context


def castore_create_tmp(ca_context: list[str]) -> str:
    """
    Create Temporary file for passing to a high level request.

    :param ca_context: _description_
    :type ca_context: list[str]
    :return: _description_
    :rtype: str
    """
    temp: str = tempfile.gettempdir()
    file_name: str = f"{uuid.uuid4()}{TMP_PEM_POSTFIX}"
    writeout: Path = Path.joinpath(Path(temp) / file_name)
    with open(writeout, "w", encoding=ENCODING) as fil:
        fil.writelines(ca_context)
    return str(writeout)


def castore_create_context(certstore: list[str]) -> list[str]:
    """
    Create a custom CA Store Context for verification.

    :param certstore: List of CA PEM files to add
    :type certstore: list[str]
    :return: Raw Pem file context
    :rtype: list[str]
    """
    castore: str = certifi.where()
    # Create CA context only return as raw list
    castore_context: list[str] = return_filelines(castore)
    if not certstore:
        return castore_context
    for cert in certstore:
        try:
            cert = check_file(filename=cert)
            castore_context.extend(return_filelines(filename=cert))
        except FileExistsError:
            pass
    return castore_context


def castore_custom_delete(custom_castore_loc: str) -> None:
    """
    Deletes Temporary custom CA Created.

    :param custom_castore_loc: Location of temp cert
    :type custom_castore_loc: str
    """
    if custom_castore_loc:
        try:
            castore = check_file(custom_castore_loc)
            # Delete using Pathlib returned value if it is a temp SNC CA
            if re.match(PEM_REGEX, str(castore), re.MULTILINE):
                Path(castore).unlink()
        except FileExistsError:
            # Nothing to delete moving on
            pass
