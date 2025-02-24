from common.decorators import logger_decorator
from typing import List
from typing import Set
from typing import Callable
from typing import Dict
from typing import Tuple
from typing import Any
from typing import TypeVar
from typing import Dict


def extract_moustache_signature(s: str) -> Tuple[int, Set[str]]:
    """
    Extracts the signature from  a moustache string.

    Args:
        s (str): The moustache string to extract the signature from .

    Returns:
        tuple: A tuple containing the number of empty signatures and a set of non-empty signatures.
    """
    li = [s_.split("}")[0] for s_ in s.split("{")[1:]]
    n_0, l_1 = len([s__ for s__ in li if len(s__) == 0]), set(
        [s__ for s__ in li if len(s__) > 0]
    )
    signature = n_0, l_1
    return signature


def generate_from_moustache_signature(
    signature: Tuple[int, Set[str]]
) -> Tuple[List[str], Dict[str, str]]:
    """
    Generate a list of arguments and a dictionary of keyword arguments based on a given signature.

    Parameters:
        signature (tuple): A tuple containing two elements - an integer and a set of strings. The integer represents the number of arguments, and the set of strings represents the names of keyword arguments.

    Returns:
        tuple: A tuple containing two elements - a list of arguments and a dictionary of keyword arguments. The list of arguments contains empty strings, and the dictionary of keyword arguments contains the keyword arguments as keys with empty strings as values.
    """
    n_0, l_1 = signature
    op, cl = "{", "}"
    args = ["{}" for i in range(0, n_0)]
    kwargs = {m: "{m}".format(m=(op + m + cl)) for m in l_1}
    return args, kwargs


def format_partially(s: str, mapping: Dict[str, str]) -> str:
    """
    Formats a string `s` with a dictionary `mapping` by replacing placeholders in `s` with corresponding values from  `mapping`.

    Parameters:
        s (str): The string to be formatted.
        mapping (dict): A dictionary containing the key-value pairs for replacing placeholders in `s`.

    Returns:
        str: The formatted string after replacing the placeholders with the corresponding values from  `mapping`.
    """
    signature = extract_moustache_signature(s)
    args, kwargs = generate_from_moustache_signature(signature)
    for i, a in enumerate(args):
        if i in mapping.keys():
            args[i] = mapping[i]
    for k in kwargs.keys():
        if k in mapping.keys():
            kwargs[k] = mapping[k]
    return s.format(*args, **kwargs)


def get_hex(s:str)->str:
    return s.encode("utf-8").hex()