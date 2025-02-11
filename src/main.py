import argparse, json
from chats.iterators import ChatInputIterator
from chats.utils import get_epoch_str
from apis.connectors import APIClient, APIBuffer
from apis.constants import DEEPSEEK_API_KEY
from apis.iterators import MessageIterator


token = {"api_key":DEEPSEEK_API_KEY, "base_url":"https://api.deepseek.com"}

role_config = {
    "role": 'data engineer',
    "speciality":'domain modelling with Postregsql'
}

epoch =  get_epoch_str()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Have a chat with Deepseek")
    _ = parser.add_argument("prefix", type=str)
    args = parser.parse_args()
    file_path = '../.data/' + args.prefix +'_' + epoch + '.txt'
    with open(file_path,'w') as f:
        with APIClient(token) as client:
            with APIBuffer(client) as buffer:
                chat_history = [{"role": "system", "content": "You are a {role} specializing {speciality}".format(**role_config)}]
                for ch in iter(MessageIterator(chat_history,buffer.query)):
                    print(ch[-1]["content"])
                f.writelines(list(map(json.dumps,chat_history)))
    
    