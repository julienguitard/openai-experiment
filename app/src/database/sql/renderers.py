from typing import List
from typing import Tuple
from typing import Dict
from typing import Callable
from common.collections import lmap
from common.collections import lmapzip as lmz
from common.collections import dmap
from common.collections import convert_set_to_list
from common.strings import extract_moustache_signature
from common.strings import generate_from_moustache_signature
from common.strings import format_partially
from database.sql.templates import sql_templates
from common.decorators import logger_decorator


class Renderer(object):
    def __init__(self, template: str) -> None:
        """
        Initializes an instance of the class.

        Parameters:
            template (str): The template used for initialization.

        Returns:
            None
        """
        self.template = template
        self.signature = extract_moustache_signature(self.template)
        self.args, self.kwargs = generate_from_moustache_signature(
            self.signature
        )

    @staticmethod
    def generate_render_method(
        template: str, signature: Tuple[List[str], Dict[str, str]]
    ) -> Callable[..., str]:
        """
        Generates a render method based on a given template and signature.

        Args:
            template (str): The template string to be used for rendering.
            signature (Tuple[List[str],Dict[str,str]]): The signature of the render method. It consists of a list of positional arguments and a dictionary of keyword arguments.

        Returns:
            Callable[[Any], str]: The generated render method that takes any number of arguments and returns a rendered string.
        """
        n_0, l_1 = signature
        l_2 = convert_set_to_list(l_1)

        def render(*args):
            mapping = dict(zip(range(0, n_0), args[:n_0]))
            for i, k in enumerate(l_2):
                mapping[k] = args[n_0 + i]
            return format_partially(template, mapping)

        return render

    def render(self, *args: List[str]) -> str:
        """
        Renders the template using the given arguments and returns the rendered string.

        Args:
            *args (Any): The arguments to be passed to the render method.

        Returns:
            str: The rendered string.

        """
        return Renderer.generate_render_method(self.template, self.signature)(
            *args
        )


def merge_predicates(
    variables: List[str], predicates: List[str], values: List[str]
) -> str:
    """
    Generate a SQL WHERE clause by merging a list of variables, predicates, and values.

    Args:
        variables (List[str]): A list of strings representing the variables.
        predicates (List[str]): A list of strings representing the predicates.
        values (List[Any]): A list of values corresponding to the variables and predicates.

    Returns:
        str: A string representing the SQL WHERE clause.
    """
    wheres = " AND ".join(
        lmz(
            lambda var, p, val: "{}{}{}".format(var, p, val),
            zip(variables, predicates, values),
        )
    )
    return wheres


renderers = dmap(lambda k, v: (k, Renderer(v)), sql_templates)
