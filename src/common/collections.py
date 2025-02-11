from typing import List
from typing import Set
from typing import Callable
from typing import Dict
from typing import Tuple
from typing import Any
from typing import TypeVar
from typing import Dict
from typing import Iterable

T, T0, T1, T2, T3 = (
    TypeVar("T"),
    TypeVar("T0"),
    TypeVar("T1"),
    TypeVar("T2"),
    TypeVar("T3"),
)


def tuplify(x: Any) -> Tuple:
    """
    Return a tuple representation of the input `x`.

    Parameters:
        x (Any): The input value.

    Returns:
        tuple: A tuple representation of `x`.
    """
    return ((x,), x)[isinstance(x, tuple)]


def flatten_tuple_(ts: Tuple[Tuple[T]]) -> Tuple[T]:
    """
    Generates a flattened tuple from  a tuple of tuples.

    Parameters:
        Tuple[Tuple[T]]: The input tuple of tuples.

    Returns:
        Tuple[T]: The flattened tuple.
    """
    return (e for li in ts for e in li)


def flatten_tuple(ts: Tuple) -> Tuple:
    """
    Generate the function comment for the given function body in a markdown code block with the correct language syntax.

    Args:
        ts (Tuple): The input tuple to be flattened.

    Returns:
        Tuple: The flattened tuple.
    """
    return tuple(flatten_tuple_(map(tuplify, ts)))


def tmap(f: Callable, tu: Tuple) -> Callable[[Tuple], Tuple]:
    """
    Map a function over a tuple and return the result as a new tuple.

    Args:
        f (Callable): The function to apply to each element of the tuple.
        li(Tuple): The tuple to apply the function to.

    Returns:
        Callable: A function that takes a tuple and applies the given function to it.

    Example:
        >>> lmap(lambda x: x * 2, [1, 2, 3])
        [2, 4, 6]
    """
    return tuple(map(f, tu))


def listify(x: Any) -> List:
    """
    Return a list representation of the input `x`.

    Parameters:
        x (Any): The input value.

    Returns:
        list: A list representation of `x`.
    """
    return ([x], x)[isinstance(x, list)]


def flatten_(ls: List[List[T]]) -> List[T]:
    """
    Generates a flattened list from  a list of lists.

    Parameters:
        ls (List[List[T]]): The input list of lists.

    Returns:
        List[T]: The flattened list.
    """
    return [e for li in ls for e in li]


def flatten(ls: List) -> List:
    """
    Flattens a list of lists into a single list.

    Parameters:
        ls (List): The list of lists to be flattened.

    Returns:
        List: The flattened list.
    """
    return flatten_(map(listify, ls))


def concatenate(l0: List[T], l1: List[T]) -> List[T]:
    """
    Concatenates two lists into one list.

    Args:
        l0 (List[T]): The first list to be concatenated.
        l1 (List[T]): The second list to be concatenated.

    Returns:
        List[T]: A new list that is the result of concatenating l0 and l1.
    """
    return flatten([l0, l1])


def lmap(
    f: Callable[[T0], T1], li: List[T0]
) -> Callable[[List[T0]], List[T1]]:
    """
    Map a function over a list and return the result as a new list.

    Args:
        f (Callable[[T0], T1]): The function to apply to each element of the list.
        li(List[T0]): The list to apply the function to.

    Returns:
        Callable[[List[T0]], List[T1]]: A function that takes a list and applies the given function to it.

    Example:
        >>> lmap(lambda x: x * 2, [1, 2, 3])
        [2, 4, 6]
    """
    return list(map(f, li))


def lfilter(
    f: Callable[[T], bool], li: List[T]
) -> Callable[[List[T]], List[T]]:
    """
    Returns a function that filters a list based on a given predicate function.

    Parameters:
        f (Callable[[T], bool]): A predicate function that takes an element of type T and returns a boolean value.
        li(List[T]): A list of elements of type T.

    Returns:
        Callable[[List[T]], List[T]]: A function that accepts a list and returns a filtered list based on the given predicate function.
    """
    return list(filter(f, li))


def lzip(li0: List[T0], li1: List[T1]) -> List[Tuple[T0, T1]]:
    return list(zip(li0, li1))


def lmapzip(f: Callable, *args) -> List:
    if len(args) == 1:
        res = lmap(lambda t: f(*t), args[0])
    else:
        res = lmap(lambda t: f(*t), zip(*args))
    return res


def ujoin(
    where: Callable[[T0, T1], bool], l0: List[T0], l1: List[T1]
) -> List[Tuple[T0, List[T1]]]:
    return lmap(lambda t0: (t0, lfilter(lambda t1: where(t0, t1), l1)), l0)


def njoin(
    where: Callable[[T0, T1], bool], l0: List[T0], l1: List[T1]
) -> List[List[Tuple[T0, T1]]]:
    return lmap(
        lambda t0t1s: lmap(lambda t1: (t0t1s[0], t1), t0t1s[1]),
        ujoin(where, l0, l1),
    )


def ljoin(
    where: Callable[[T0, T1], bool], l0: List[T0], l1: List[T1]
) -> List[Tuple[T0, T1]]:
    return flatten(njoin(where, l0, l1))


def enumerate_flat(l0: List[T0]) -> List[Tuple]:
    return lmap(flatten_tuple, enumerate(l0))


def lreduce(f: Callable[[T0, T1], T0], val: T0, l: List[T1]) -> T0:
    """
    Reduce a list to a single value using a binary function.

    Parameters:
        - f: A binary function that takes two arguments of type T0 and T1,
            and returns a value of type T0.
        - val: The initial value of type T0 for the reduction.
        - l: A list of elements of type T1.

    Returns:
        The reduced value of type T0.

    """
    for v in l:
        val = f(val, v)
    return val


def lreduce_cumulatedly(
    f: Callable[[T0, T1], T0], val: T0, l: List[T1]
) -> List[T0]:
    """
    Reduce a list to a single value using a binary function.

    Parameters:
        - f: A binary function that takes two arguments of type T0 and T1,
            and returns a value of type T0.
        - val: The initial value of type T0 for the reduction.
        - l: A list of elements of type T1.

    Returns:
        The sequence reduced value of type T0.

    """
    res = []
    for v in l:
        val = f(val, v)
        _ = res.extend([val])
    return res


def convert_set_to_list(s: Set[T]) -> List[T]:
    """
    Convert a set to a list.

    Parameters:
        s (Set[T]): The set to be converted.

    Returns:
        List[T]: The converted list.
    """
    li = list(s)
    _ = li.sort()
    return li


def dmap(
    fkv: Callable[[T0, T1], Tuple[T0, T1]], d: Dict[T0, T1], verbose=False
) -> Dict[T0, T1]:
    """
    Generate a new dictionary by applying a function to each key-value pair in the input dictionary.

    Parameters:
        fkv (function): A function that takes a key-value pair from  the input dictionary and returns a new key-value pair.
        d (dict): The input dictionary.
        verbose (bool, optional): If True, print each new key-value pair. Defaults to False.

    Returns:
        dict: A new dictionary generated by applying the function to each key-value pair in the input dictionary.
    """
    ks, vs = [], []
    for k0, v0 in d.items():
        k1, v1 = fkv(k0, v0)
        if verbose:
            print(k1, v1)
        if (k1 is not None) and (v1 is not None):
            _, _ = ks.extend([k1]), vs.extend([v1])
    return dict(zip(ks, vs))


def dfilter(
    fkv: Callable[[T0, T1], bool], d: Dict[T0, T1], verbose=False
) -> Dict[T0, T1]:
    """
    Filters a dictionary `d` using a key-value filter function `fkv`.

    Parameters:
        - fkv (function): A function that takes a key `k` and a value `v` from  the dictionary `d` as input and returns a tuple `(k1, v1)`.
        - d (dict): The dictionary to be filtered.
        - verbose (bool, optional): If True, print the filtered key-value pairs. Defaults to False.

    Returns:
        dict: A new dictionary containing only the key-value pairs that pass the filter function `fkv`.
    """
    ks, vs = [], []
    for k0, v0 in d.items():
        k1, v1 = fkv(k0, v0)
        if verbose:
            print(k1, v1)
        if k1 and v1:
            _, _ = ks.extend([k0]), vs.extend([v0])
    return dict(zip(ks, vs))


def merge(dicts: Iterable[Dict]) -> Dict:
    return dict([item for d in dicts for item in d.items()])


def dicter(keys: List[str]) -> Callable[[Iterable], Dict]:
    def func(values: Iterable) -> dict:
        return dict(zip(keys, values))

    return func


def rename_(as_: Dict[str, str]) -> Callable[[str, T0], Tuple[str, T0]]:
    keys = as_.keys()

    def func(k: str, v: T0) -> Tuple[str, T0]:
        if k in keys:
            res = as_[k]
        else:
            res = k
        return (res, v)

    return func


def select_(sel: Set[str]) -> Callable[[str, T0], Tuple[bool, bool]]:
    def func(k: str, v: T0) -> Tuple[bool, bool]:
        return (k in sel, True)

    return func


def rename(
    mapping: Dict[str, str]
) -> Callable[[Dict[str, T0]], Dict[str, T0]]:
    def func(d: Dict[str, T0]) -> Dict[str, T0]:
        return dmap(rename_(mapping), d)

    return func


def select(sel: Set[str]) -> Callable[[Dict[str, T0]], Dict[str, T0]]:
    def func(d: Dict[str, T0]) -> Dict[str, T0]:
        return dfilter(select_(sel), d)

    return func
