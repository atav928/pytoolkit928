"""Global Static Vars."""

ENCODING: str = 'utf-8'

DEFAULT_TO: list[str] = ['john.doe@acme.com']
DEFAULT_FROM: str = 'python-script@acme.com'
DEFAULT_CC: list[str] = ['']
DEFAULT_BCC: list[str] = ['']
TMP_PEM_POSTFIX = "_pytookit.pem"
PEM_REGEX = r".*[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}_pytoolkit\.pem$"
