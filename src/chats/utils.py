import time

def get_epoch_str(factor=1000):
    epoch = time.time() 
    return str(int(factor * epoch))