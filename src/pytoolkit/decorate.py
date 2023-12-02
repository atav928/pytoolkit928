# pylint: disable=too-many-arguments
"""Decorators."""

from typing import Union, Any, Callable
from functools import partial
import functools
from inspect import isfunction
import time
import random

from pytoolkit import decorator
from pytoolkit.utils import reformat_exception


def __retry_interval(
    func: Callable[[Any],Any],
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

    :param func: the funciton to execute.
    :type func: Function
    :param exceptions: an exception or tupple of exceptions to catch, defaults to Exception
    :type exceptions: Exception|tuple[Excpetion,Exception], optional
    :param tries: the maximum number of attempts, defaults to -1 (infinite).
    :type tries: int, optional
    :param delay: intial delay between attempts, defaults to 0.
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
            return func()
        except exceptions as err:
            _tries -= 1
            error = reformat_exception(err)
            if not _tries:
                raise
            if logger is not None:
                logger.warning(
                    'msg="attempt failed",error=%s,retrying_in=%ss', error, _delay
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

    :param exceptions: an exception or tupple of exceptions to catch, defaults to Exception
    :type exceptions: Exception|tuple[Excpetion,Exception], optional
    :param tries: the maximum number of attempts, defaults to -1 (infinite).
    :type tries: int, optional
    :param delay: intial delay between attempts, defaults to 0.
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
        error = reformat_exception(err)
        if logger:
            # need to call func.func to get the original callable function name since created by partial()
            logger.fatal(
                f'function={func.func.__name__},error="{message}:error_raw={error}",level=error'
            )
    if isinstance(default_return, functools.partial):
        return default_return(error=error, level="fatal")
    if default_return:
        return default_return


def error_handler(
    exceptions=Exception, default_return=None, logger=None, func_params={}
):  # pylint: disable=dangerous-default-value
    """
    Error Handler excption; allows passing a default return value if needed.

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
            func_params.update(
                {("args" + str(idx + 1)): arg for idx, arg in enumerate(args)}
            )
            return __exception_handler(
                partial(func, *args, **kwargs),
                exceptions,
                partial(default_return, **func_params),
                logger,
            )
        return __exception_handler(
            partial(func, *args, **kwargs), exceptions, default_return, logger
        )

    return error_handle_decorator
