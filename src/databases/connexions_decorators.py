import time
from jax import numpy as jnp
from typing import List
from typing import Callable
from typing import Dict
from typing import Tuple
from typing import Any
from typing import TypeVar
from databases.constants import TOKEN_TEMPLATE
from databases.connexions import DBClient
from databases.connexions import Buffer
from databases.connexions import generate_config
from databases.connexions import generate_token


def buffer_decorator(func: Callable[[Buffer], None]) -> Callable[[], None]:
    def gunc():
        config = generate_config(TOKEN_TEMPLATE)
        token = generate_token(config, TOKEN_TEMPLATE)
        with DBClient(token) as db:
            with Buffer(db) as b:
                _ = func(b)

    return gunc
