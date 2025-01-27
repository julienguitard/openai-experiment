import argparse
from chats.iterators import ChatInputIterator
from apis.connectors import APIClient, APIBuffer
from apis.constants import DEEPSEEK_API_KEY
from apis.iterators import MessageIterator

token = {"api_key":DEEPSEEK_API_KEY, "base_url":"https://api.deepseek.com"}

role_config = {
    "role": 'data engineer',
    "speciality":'domain modelling with Postregsql'
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a query on the database")
    _ = parser.add_argument("query", type=str)
    with APIClient(token) as client:
        with APIBuffer(client) as buffer:
            chat_history = [{"role": "system", "content": "You are a {role} specializing {speciality}".format(**role_config)}]
            for ch in iter(MessageIterator(chat_history,buffer.query)):
                print(ch[-1]["content"])
    