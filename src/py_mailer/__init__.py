from py_mailer import logger
from py_mailer._version import __version__
# Enumerator type
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict(((v, k) for (k, v) in enums.items()))
    enums["reverse_mapping"] = reverse
    return type("Enum", (), enums)


def isstring(arg):
    try:
        return isinstance(arg, basestring)
    except NameError:
        return isinstance(arg, str) or isinstance(arg, bytes)

# Convenience methods used internally by module
# Do not use these methods outside the module

def string_or_list(value):
    """Return a list containing value

    This method allows flexibility in class __init__ arguments,
    allowing you to pass a string, object, list, or tuple.
    In all cases, a list will be returned.

    Args:
        value: a string, object, list, or tuple

    Returns:
        list

    Examples:
        "string" -> [string]
        ("t1", "t2") -> ["t1", "t2"]
        ["l1", "l2"] -> ["l1", "l2"]
        None -> None

    """
    if value is None:
        return None
    if isstring(value):
        return [
            value,
        ]
    return (
        list(value) if "__iter__" in dir(value) else [value,]
    )