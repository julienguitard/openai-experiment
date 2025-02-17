import argparse, sys, time, json
from common.iterators import retry
from chats.iterators import ChatInputIterator
from apis.connectors import APIClient, APIBuffer
from apis.constants import DEEPSEEK_API_KEY
from apis.iterators import MessageIterator

sys.path.insert(0,'./')


token = {"api_key":DEEPSEEK_API_KEY, "base_url":"https://api.deepseek.com"}
role_config = {

    "role": 'data engineer',
    "speciality":'domain modelling with Postregsql'
}

content_config = {
    "output":'Postgresql database schema',
    "theme":"{theme}",
    "extra_context":"Do not hesitate to create enum type or small tables to avoid unguarded VARCHAR types and populate your tables",
    "negative_guideline":" Do not give examples of queries"
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a query on the database")
    _ = parser.add_argument("query", type=str)
    fname = str(int(1000*time.time()))
    with open('../.data/'+fname+'.txt','w') as f:
        with APIClient(token) as client:
            with APIBuffer(client) as buffer:
                chat_history = [{"role": "system", "content": "You are a {role} specializing {speciality}".format(**role_config)}]
                f.writelines(list(map(json.dumps,chat_history)))
                bf = retry(buffer.query)
                for ch in iter(MessageIterator(chat_history,bf)):
                    print(ch[-1]["content"])
                    f.writelines(list(map(json.dumps,chat_history)))