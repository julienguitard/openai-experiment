from typing import Any
from typing import Callable
from typing import List
from typing import Dict
from typing import Tuple
from typing import TypeVar
from typing import Union

from typing import Optional

T0 = TypeVar("T0")
T1 = TypeVar("T1")
ComplexValue = Union[T0, Dict[str, T1]]
Query = str
QueryResults = Optional[List[Tuple]]
Queries = List[Query]
PipelinedQueries = Tuple[Queries, Queries]
PipelinedResults = List[QueryResults]
