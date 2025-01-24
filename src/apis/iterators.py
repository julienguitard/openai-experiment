from src.chats.iterators import ChatInputIterator
from typing import Callable

class MessageIterator:
  def __init__(self,chat_history:list[str],api_caller:Callable[[str],str]):
    self.chat_history = chat_history
    self.api_caller = api_caller

  def __iter__(self):
    self.chat_iterator = iter(ChatInputIterator())
    return self
    
  def __next__(self):
    try:
      message = self.chat_iterator.__next__() 
      self.chat_history.append({"role":"user","content":message}) 
      answer = self.api_caller(self.chat_history)
      self.chat_history.append({"role":"assistant","content":answer})  
      return self.chat_history
    except Exception as e:
      print(e)
      raise StopIteration       
