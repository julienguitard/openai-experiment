from typing import Any
from typing import Optional
from typing import Callable
from typing import List
from typing import Tuple
import psycopg2
from getpass import getpass

from common.types import Query
from common.types import Queries
from common.types import PipelinedQueries
from common.types import QueryResults
from common.types import PipelinedResults
from common.collections import lmap
from common.collections import dmap
from common.decorators import logger_decorator
from databases.sql.renderers import renderers


class DBClient:
    def __init__(self, token: dict) -> None:
        """
        Initialize the class with a token.

        Args:
            token (dict):The token to be assigned to the class.
        """
        self.token = token
        self.connexion_ = psycopg2.connect(**self.token)

    def connexion(self) -> None:
        """
        Opens a connection to the database if it is closed.

        :return:None
        """
        if self.connexion_.closed == 1:
            print("restart connexion")
            self.connexion_ = psycopg2.connect(**self.token)
        return self.connexion_

    def __enter__(self) -> Any:
        """
        Enter the context manager.
        :return:The context manager object.
        """
        print("opening connection")
        return self

    def __exit__(
        self, exc_type: Any, exc_value: Any, exc_traceback: Any
    ) -> None:
        """
        Exit the context manager.
        """
        self.connexion().close()
        print("closing connection")


class Buffer:
    def __init__(self, client: DBClient) -> None:
        """Initialize the class with a connexion"""
        self.client = client
        self.cursor_ = self.client.connexion().cursor()
        self.data = None

    def cursor(self) -> None:
        if self.client.connexion_.closed == 1:
            self.cursor_ = self.client.connexion().cursor()
        return self.cursor_

    def _rollback(self, func: Callable) -> Callable:
        def gunc(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                _ = self.client.connexion().rollback()
            _ = self.client.connexion().commit()

        return gunc

    def load(self, file_name: str, table_name: str, sep=";") -> None:
        with open(file_name, "r") as f:
            # Notice that we don't need the csv module.
            next(f)  # Skip the header row.
            self._rollback(self.cursor().copy_from)(f, table_name, sep=sep)

    def dump(self, file_name: str, table_name: str, sep=";") -> None:
        with open(file_name, "w") as f:
            # Notice that we don't need the csv module.
            next(f)  # Skip the header row.
            self._rollback(self.cursor().copy_to)(
                file_name, table_name, sep=sep
            )

    def query(self, q: Query, verbose: bool = False) -> QueryResults:
        """Return the output of the query when its select statement and None otherwise.
        If the query is empty nothing is done qnd None is returned"""
        if verbose:
            print(q)
        if len(q) == 0:
            self.data = None
        else:
            self._rollback(self.cursor().execute)(q)
            try:
                self.data = self.cursor().fetchall()
            except Exception as e:
                self.data = None
                _ = self.client.connexion().commit()
        return self.data

    def query_many(
        self,
        ddl_queries: Queries,
        select_queries: Queries,
        verbose: bool = False,
    ) -> PipelinedResults:
        _ = lmap(lambda q: self.query(q, verbose=verbose), ddl_queries)
        return lmap(lambda q: self.query(q, verbose=verbose), select_queries)

    def list_tables(self) -> List[str]:
        """
        This function returns a list of table names.

        :return:A list of strings representing the table names.
        :rtype:List[str]
        """
        s = renderers["list_tables"].render()
        li = self.query(s)
        return lmap(lambda x: x[0], li)

    def exists_in_tables(self, table_name: str) -> bool:
        """
        Checks if a given table name exists in the list of tables.

        Parameters:
            table_name (str):The name of the table to check.

        Returns:
            bool:True if the table exists, False otherwise.
        """
        li = self.list_tables()
        return table_name in l

    def __enter__(self) -> Any:
        """
        Enter the context manager.
        :return:The context manager object.
        """
        print("opening buffer")
        return self

    def __exit__(
        self, exc_type: Any, exc_value: Any, exc_traceback: Any
    ) -> None:
        """
        Exit the context manager.
        """
        self.client.connexion().commit()
        print("closing buffer and committing connexion")


def generate_config(token_template: dict) -> dict:
    """
    Generate a configuration dictionary based on a given token template.

    Args:
        token_template (dict):A dictionary containing token keys and format strings.

    Returns:
        dict:A configuration dictionary where each token key is replaced with its respective formatted value.

    Example:
        >>> token_template = {
        ...     'host':'http://{host}:{port}/api',
        ...     'key':'API_KEY={api_key}',
        ...     'username':'USERNAME={username}',
        ... }
        >>> generate_config(token_template)
        {
            'host':'http://localhost:5434/api',
            'key':'API_KEY={api_key}',
            'username':'USERNAME={username}',
        }

    Note:
        - The 'host', 'port', 'database', 'user', and 'password' tokens in the token_template dictionary will be replaced with their corresponding values.
        - The 'host' and 'port' values are fixed as 'localhost' and '5434', respectively.
        - The 'database', 'user', and 'password' values can be customized.
        - The 'password' value in the token_template dictionary should contain a placeholder '{password}' that will be replaced with the actual password value provided.

    """
    return dict(
        [
            (
                k,
                token_template[k].format(
                    host="localhost",
                    port=5434,
                    database="ai_chats",
                    user="postgres",
                    password="{password}",
                ),
            )
            for k in token_template.keys()
        ]
    )


def generate_token(config: dict, token_template: dict) -> dict:
    """
    Generate a token for the database.
    """
    config["password"] = getpass(
        "Enter password for {database}".format(**config)
    )
    return dmap(lambda k, v: (k, v.format(**config)), token_template)
