from typing import List
from typing import Callable
from typing import Dict
from typing import Tuple
from typing import Any
from typing import TypeVar
from typing import Dict

T, T0, T1, T2, T3 = (
    TypeVar("T"),
    TypeVar("T0"),
    TypeVar("T1"),
    TypeVar("T2"),
    TypeVar("T3"),
)


def compose(
    f: Callable[[T0], T1], g: Callable[[T], T2], tuple_midput=False
) -> Callable[[T0], T2]:
    """
    Composes two functions `f` and `g` into a new function `h`.

    Parameters:
    - f: The first function to be composed.
    - g: The second function to be composed.
    - tuple_midput: A boolean flag indicating whether the input to `f` should be passed as a tuple to `g` (default: False).

    Returns:
    - h: The composed function.

    Note:
    - If `tuple_midput` is True, `h` calls `g` with the result of `f` as a tuple.
    - If `tuple_midput` is False, `h` calls `g` with the result of `f` as separate arguments.
    """
    if tuple_midput:

        def h(*args, **kwargs):
            return g(*f(*args, **kwargs))

    else:

        def h(*args, **kwargs):
            return g(f(*args, **kwargs))

    return h


def chained_compose(fs: List[Callable[[T], T]]) -> Callable[[T], T]:
    """
    A function that takes a list of functions `fs` and returns a new function `g`.
    The function `g` takes a parameter `x` and applies each function in `fs` to `x`
    in the order they appear in the list. The result of each function call is stored
    in a list `y`. The final result is the list `y` containing the result of applying
    each function in `fs` to `x`.

    Parameters:
    - fs (list): A list of functions to be applied to `x`.

    Returns:
    - g (function): A new function that applies each function in `fs` to its parameter `x`
      and returns the result as a list.
    """

    def g(x):
        y = [x for (i, f) in enumerate(fs)]
        for i, f in enumerate(fs[1:]):
            y[i] = fs[i](y[-1])
        return y

    return g


def apply(f: Callable[[T0], T1], x: T0) -> T1:
    return f(x)
