from openai import OpenAI
from typing import Any

class APIClient:
    def __init__(self, token: dict) -> None:
        """
        Initialize the class with a token.

        Args:
            token (dict):The token to be assigned to the class.
        """
        self.token = token
        try :
            self.connexion_ = OpenAI(**self.token)
            self.closed = 0
        except Exception as e:
            print(e)
            self.closed = 1

    def connexion(self) -> None:
        """
        Opens a connection to the database if it is closed.

        :return:None
        """
        if self.closed == 1:
            print("restart connexion")
            try :
                self.connexion_ = OpenAI(**self.token)
                self.closed = 0
            except Exception as e:
                print(e)
                self.closed = 1
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
        self.closed == 1
        print("closing connection")

class APIBuffer:
    def __init__(self, client: APIClient) -> None:
        """Initialize the class with a connexion"""
        self.client = client
        self.model = "deepseek-reasoner"
        self.stream = False

    def query(self, messages:list[dict]):
        response = self.client.connexion_.chat.completions.create(model=self.model,messages=messages,stream=self.stream)
        return response.choices[0].message.content

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
        print("closing buffer")
