import time
from jax import numpy as jnp
from typing import List
from typing import Callable
from typing import Dict
from typing import Tuple
from typing import Any
from typing import TypeVar

from common.collections import tmap
from common.collections import lmap
from common.collections import lmapzip as lmz
from common.collections import dmap

T, T0, T1, T2, T3 = (
    TypeVar("T"),
    TypeVar("T0"),
    TypeVar("T1"),
    TypeVar("T2"),
    TypeVar("T3"),
)


def time_decorator(
    func: Callable[[T0], T1], now=time.time
) -> Callable[[T0], T1]:
    """
    Executes a function and measures its execution time.

       Args:
        *args: Variable length argument list.
         **kwargs: Arbitrary keyword arguments.

    Returns:
        The result of the executed function.
    Example:
            >>> gunc(func, arg1, arg2, kwarg1=val1, kwarg2=val2)
            execution took 123ms
            <function result>
    """

    def gunc(*args, **kwags):
        t0 = now()
        res = func(*args, **kwags)
        t1 = now()
        print(
            "execution of {} took {}ms".format(
                func.__name__, jnp.round(1000 * (t1 - t0))
            )
        )
        return res

    return gunc


def repeat_decorator(
    times=2, seconds=60
) -> Callable[[Callable[[T0], T1]], Callable[[T0], T1]]:
    """
    A decorator that repeats the execution of a function multiple times with a
    delay between each execution.

    Parameters:
        times (int): The number of times the function should be executed.
        Default is 2.
        seconds (int): The number of seconds to delay between each execution. Default is 60.

    Returns:
        function: The decorated function.

    """

    def inner(func):
        def gunc(*args, **kwargs):
            func(*args, **kwargs)
            for t in range(0, times - 1):
                time.sleep(seconds)
                func(*args, **kwargs)

        return gunc

    return inner


def logger_decorator(
    func: Callable[[T0], T1], now=time.time
) -> Callable[[T0], T1]:
    """
    Decorator that logs the function name, arguments, and keyword arguments before calling the decorated function.

    Parameters:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    def gunc(*args, **kwargs):
        print(
            "fname:{}, args:{}, kwargs:{}".format(func.__name__, args, kwargs)
        )
        return func(*args, **kwargs)

    return gunc


def curry_decorator(args_number=1) -> Callable[[Callable], Callable]:
    """
    A decorator that allows a function to be partially applied by currying.

    Parameters:
    - args_number (int): The number of arguments that the function takes.

    Returns:
    - function: The curried function.
    """

    def curry(func):
        if args_number == 1:

            def gunc(*args, **kwargs):
                def hunc(arg0):
                    return func(arg0, *args, *kwargs)

                return hunc

        else:
            gunc_ = curry(curry(func, args_number - 1))

            def gunc(*args, **kwargs):
                def hunc(*args_):
                    return gunc_(*args, **kwargs)(args_[-1])(*args_[:-1])

                return hunc

        return gunc

    return curry


def uncurry_decorator(args_number=1) -> Callable[[Callable], Callable]:
    """
    A decorator that takes a curried function and returns a function that uncurries it.

    Parameters:
    - gunc: The curried function to be uncurried.
    - args_number: The number of arguments to be passed to the uncurried function.

    Returns:
    - func: A function that takes the remaining arguments and applies them to the uncurried function.

    Example usage:
    ```
    @uncurry_decorator(args_number=2)
    def add(a, b):
        return a + b

    result = add(1, 2, 3)
    print(result) # Output: 3
    ```
    """

    def uncurry(gunc, args_number=1):
        def func(*args, **kwargs):
            return gunc(*args[args_number:], **kwargs)(*args[0:args_number])

        return func

    return uncurry


def listify_args_decorator(
    func: Callable[[T0], T1], now=time.time
) -> Callable[[List[T0]], T1]:
    """
    Returns a function that takes a list of arguments and applies them to the given function.

    Parameters:
        func (function): The function to be applied to the arguments.

    Returns:
        function: A new function that takes a list of arguments and applies them to the given function.
    """

    def gunc(args):
        return func(*args)

    return gunc


def flatten_args_decorator(
    func: Callable[[List[T0]], T1], now=time.time
) -> Callable[[T0], T1]:
    """
    Returns a function that takes a variable number of arguments and calls the input function `f` with the arguments as a single list.

    Args:
        f (function): The input function to be called with the flattened arguments.

    Returns:
        function: A new function `g` that takes a variable number of arguments and calls `f` with the arguments as a single list.
    """

    def gunc(*args):
        return func(list(args))

    return gunc


def of_decorator(func: Callable[[T0], T1]) -> Callable[[T0], Callable[[], T1]]:
    """
    A function that returns a closure that calls the given function with the provided arguments.

    Args:
         *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

    Returns:
            function: A closure that calls the given function with the provided arguments.
    """

    def gunc(*args, **kwargs):
        def hunc():
            return func(*args, **kwargs)

        return hunc

    return gunc


def assoc_decorator(
    args_fields: List[str], result_field: str
) -> Callable[[Callable], Callable[[Dict[str, Any]], Dict[str, Any]]]:
    def inner(func: Callable) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
        def gunc(dic: Dict[str, Any]) -> Dict[str, Any]:
            new_dic = {**dic}
            new_dic[result_field] = func(
                *map(lambda a: new_dic[a], args_fields)
            )
            return new_dic

        return gunc

    return inner


def try_decorator(func):
    def gunc(x):
        try:
            res = func(x)
        except Exception as e:
            res = x
        return x

    return gunc


def nested_decorator(func):
    def gunc(x):
        if isinstance(x, list):
            res = lmap(gunc, x)
        elif isinstance(x, tuple):
            res = tmap(gunc, x)
        elif isinstance(x, dict):
            res = dict(lmz(lambda k, v: (k, gunc(v)), x.items()))
        elif "tolist" in x.__dir__():
            res = gunc(x.tolist())
        else:
            res = func(x)
        return res

    return gunc


def nested_decorator_(func):
    def gunc(x):
        if isinstance(x, list):
            res = lmap(gunc, x)
        elif isinstance(x, tuple):
            res = tmap(gunc, x)
        elif isinstance(x, dict):
            res = dict(lmz(lambda k, v: (k, gunc(v)), x.items()))
        else:
            res = func(x)
        return res

    return gunc
