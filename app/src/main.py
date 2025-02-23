import argparse, sys, time, json
from common.decorators import retry
from common.constants import PERSISTENT_DATA_PATH
from chats.iterators import ChatInputIterator
from apis.connectors import APIClient, APIBuffer
from apis.constants import DEEPSEEK_API_KEY
from apis.iterators import MessageIterator
from database.connexions import generate_token, generate_config, DBClient, Buffer
from database.constants import TOKEN_TEMPLATE

sys.path.insert(0,'./')


token = {"api_key":DEEPSEEK_API_KEY, "base_url":"https://api.deepseek.com"}
role_config = {

    "role": 'data engineer',
    "speciality":'domain modeling with Postregsql'
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
    epoch = int(time.time())
    database_config = generate_config(TOKEN_TEMPLATE)
    database_token = generate_token(database_config, TOKEN_TEMPLATE)
    with DBClient(database_token) as database_client:
        with Buffer(database_client) as database_buffer:
            with APIClient(token) as client:
                with APIBuffer(client) as buffer:
                    system_role = "You are a {role} specializing {speciality}".format(**role_config)
                    insertable_chat_args = {"epoch":epoch,"system_role":system_role.encode("utf-8").hex()}
                    chat_history = [{"role": "system", 
                                     "content": system_role}]
                    bf = retry(buffer.query)
                    for ch in iter(MessageIterator(chat_history,bf)):
                        print(ch[-1]["content"])

            chat_insert_sql = '''INSERT INTO chats SELECT * FROM generate_insertable_chat({epoch},'\\x{system_role}')'''.format(**insertable_chat_args)
            database_buffer.query(chat_insert_sql)
            for i in range(0,(len(chat_history)-1)//2):
                insertable_chat_args = {"epoch":epoch,
                                        "rank_":i,
                                        "prompt":(chat_history[2 * i + 1]["content"]).encode("utf-8").hex(),
                                        "response":(chat_history[2 * i + 2]["content"]).encode("utf-8").hex(),
                                        "retries":0}
                qa_insert_sql = '''INSERT INTO qas SELECT * FROM generate_insertable_qa({epoch},{rank_},'\\x{prompt}','\\x{response}',{retries})'''.format(**insertable_chat_args)
                database_buffer.query(qa_insert_sql)

                