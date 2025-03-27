# pylint: disable=too-many-arguments
"""Decorators."""

import functools
import random
import re
import time
from dataclasses import fields
from functools import partial, wraps
from inspect import isfunction, signature
from typing import Any, Callable, Union

from pytoolkit import decorator


# Dataclass Wrappers
def _wrap_init(original_init):
    @wraps(original_init)
    def __init__(self, *args, **kwargs):
        aliases = {}
        for field in fields(self):
            alias = field.metadata.get("alias")
            if alias is not None:
                value = kwargs.pop(alias)
                aliases[field.name] = value

        original_init(self, *args, **kwargs)

        for name, value in aliases.items():
            setattr(self, name, value)

    return __init__


def aliased(cls):
    """
    Alias wrapper when using a dataclass to alias a value that may be sent in differently.

    Ex:
        @aliased
        @dataclass
        class MyClass:
            viewport: str = field(default="", metadata={"alias": "vp"})


        mc = MyClass(vp="foo")
    """
    original_init = cls.__init__
    cls.__init__ = _wrap_init(original_init)
    return cls


def add_from_kwargs(cls) -> Any:
    """
    Wrapper to add new attributes into a dataclass.

    Ex:
        ```
        @add_from_kwargs
        @dataclass
        class NewData:
            name: str

        params = {"name": "John", "age": 41}
        n = NewData.from_kwargs(**params)
        >>> print(n.age)
        41
        ```
    :return: _description_
    :rtype: Any
    """

    def from_kwargs(cls, **kwargs) -> Any:
        cls_fields: set[str] = {f for f in signature(cls).parameters}
        # split the kwargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls_fields:
                native_args[name] = val
                continue
            new_args[name] = val
        # add the new values by hand
        ret = cls(**native_args)
        for new_name, new_val in new_args.items():
            setattr(ret, new_name, new_val)
        return ret

    cls.from_kwargs = classmethod(from_kwargs)
    return cls


# Error Handling Wrappers
def __reform_except(error: Exception) -> str:
    """
    Reformats Exception to print out as a string pass for logging.

    :param error: caught exception
    :type error: Exception
    :return: error as string
    :rtype: str
    """
    resp: str = f"{type(error).__name__}: {str(error)}" if error else ""
    # Replacing [ ] with list() due to issues with reading that format with some systems.
    resp = re.sub(r"\'", "", resp)
    resp = re.sub(r"\[", "list(", resp)
    resp = re.sub(r"\]", ")", resp)
    return resp


def __retry_interval(
    func: Callable[[Any], Any],
    exceptions=Exception,
    tries: int = -1,
    delay: int = 0,
    max_delay: Union[int, None] = None,
    backoff: int = 1,
    jitter: int = 0,
    logger: Any = None,
) -> Union[Any, None]:
    """
    Executes a function and retries it if it failed.

    :param func: the function to execute.
    :type func: Function
    :param exceptions: an exception or tuple of exceptions to catch, defaults to Exception
    :type exceptions: Exception|tuple[Exception,Exception], optional
    :param tries: the maximum number of attempts, defaults to -1 (infinite).
    :type tries: int, optional
    :param delay: initial delay between attempts, defaults to 0.
    :type delay: int, optional
    :param max_delay: the maximum value of delay, defaults to None (no limit).
    :type max_delay: int, optional
    :param backoff: multiplier applied to delay between attempts, defaults to 1 (no backoff).
    :type backoff: int, optional
    :param jitter: extra seconds added to delay between attempts, defaults to 0
                   fixed if a number, random if a tuple (min,max)
    :type jitter: int|tuple[int,int], optional
    :param logger: logger.warning(fmt,error,delay) will be called on failed attempts, defaults to None
                    default is disabled.
    :type logger: Logger, optional
    :return: the result of the func Function.
    """
    _tries, _delay = tries, delay
    while _tries:
        try:
            return func()  # type: ignore
        except exceptions as err:
            _tries -= 1
            error = __reform_except(err)
            if not _tries:
                raise
            if logger is not None:
                logger.warning(
                    f'Retry decorator called attempt failed",function={func.__name__},retrying_in={_delay}s,retries={_tries},{backoff=},{jitter=},error="{error}"'
                )
            time.sleep(_delay)
            _delay *= backoff
            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter
            if max_delay is not None:
                _delay = min(_delay, max_delay)


def retry(
    exceptions=Exception,
    tries: int = -1,
    delay: int = 0,
    max_delay: Union[int, None] = None,
    backoff: int = 1,
    jitter: int = 0,
    logger: Any = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Returns a retry decorator.

    :param exceptions: an exception or tuple of exceptions to catch, defaults to Exception
    :type exceptions: Exception|tuple[Exception,Exception], optional
    :param tries: the maximum number of attempts, defaults to -1 (infinite).
    :type tries: int, optional
    :param delay: initial delay between attempts, defaults to 0.
    :type delay: int, optional
    :param max_delay: the maximum value of delay, defaults to None (no limit).
    :type max_delay: int, optional
    :param backoff: multiplier applied to delay between attempts, defaults to 1 (no backoff).
    :type backoff: int, optional
    :param jitter: extra seconds added to delay between attempts, defaults to 0
                   fixed if a number, random if a tuple (min,max)
    :type jitter: int|tuple[int,int], optional
    :param logger: logger.warning(fmt,error,delay) will be called on failed attempts, defaults to None
                    default is disabled.
    :type logger: Logger, optional
    :return: a retry decorator.
    :rtype: function
    """

    @decorator
    def retry_decorator(func, *fargs, **fkwargs):
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        return __retry_interval(
            partial(func, *args, **kwargs),
            exceptions,
            tries,
            delay,
            max_delay,
            backoff,
            jitter,
            logger,
        )

    return retry_decorator


def __exception_handler(
    func,
    exceptions=Exception,
    default_return=None,
    message="",
    logger=None,
    func_params={},
):  # pylint: disable=dangerous-default-value
    """Exception Handler Decorator."""
    try:
        return func()
    except exceptions as err:
        error = __reform_except(err)
        if logger:
            # need to call func.func to get the original callable function name since created by partial()
            logger.error(f'function={func.func.__name__},error="{message}:error_raw={error}"')
    if isinstance(default_return, functools.partial):
        return default_return(error=error, level="error")
    if default_return:
        return default_return


def error_handler(
    exceptions=Exception, default_return=None, logger: Any = None, func_params={}
):  # pylint: disable=dangerous-default-value
    """
    Error Handler exception; allows passing a default return value if needed.

    :param exceptions: _description_, defaults to Exception
    :type exceptions: _type_, optional
    :param default_return: _description_, defaults to None
    :type default_return: _type_, optional
    :param logger: _description_, defaults to None
    :type logger: _type_, optional
    :param func_params: _description_, defaults to {}
    :type func_params: dict, optional
    :return: _description_
    :rtype: _type_
    """

    @decorator
    def error_handle_decorator(func, *fargs, **fkwargs):
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        if isfunction(default_return):
            func_params.update({"func_name": func.__name__})
            func_params.update(kwargs)
            func_params.update({("args" + str(idx + 1)): arg for idx, arg in enumerate(args)})
            return __exception_handler(
                partial(func, *args, **kwargs),
                exceptions,
                partial(default_return, **func_params),
                logger,
            )
        return __exception_handler(partial(func, *args, **kwargs), exceptions, default_return, logger)

    return error_handle_decorator
