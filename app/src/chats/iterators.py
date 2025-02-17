class ChatInputIterator:
  def __iter__(self):
    self.is_open = True
    self.end_of_chat = ':q'
    return self

  def __next__(self):
    message = input()
    self.is_open = (message!=self.end_of_chat)
    if self.is_open:
      return message
    else:
      raise StopIteration

