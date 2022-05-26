from utils.com_supervisor.readable.readable import Readable
import time
from random import randint

class TestOnInterval(Readable):
    def __init__(self, interval: float=1.0, encoding: str = "utf-8"):
        self.interval = interval
        self.encoding = encoding

    def read(self):
        time.sleep(self.interval)
        data = "{\"identifier\":\"0x18\",\"value\":\"" + str(hex(randint(0, 255)))[2:4].upper() + " 00 00 00 00 00 00 00\"}"
        return data.encode(self.encoding)

    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        pass