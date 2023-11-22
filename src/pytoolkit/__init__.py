"""Init."""

import functools

from pytoolkit._version import __version__
from pytoolkit.py_mailer.mailer import send_mail

try:
    from decorator import decorator
except ImportError:

    def decorator(caller):
        """Turns caller into a decorator.
        Unlike decorator module, function signature is not preserved.

        :param caller: caller(f, *args, **kwargs)
        """

        def decor(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return caller(f, *args, **kwargs)

            return wrapper

        return decor
