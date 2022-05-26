from utils.com_supervisor.readable.readable import Readable
import time
from typing import Callable
import random

class TestOnInterval(Readable):
    """
    Serial mocker.
    Waits for given interval and sends back a message of a random identifier and some data provided by a function.
    Identifiers to pick from are given in the policy. The function that is called should return 8 bytes of data in string format.
    """

    def __init__(self, interval: float=1.0, encoding: str = "utf-8", policy: dict[str, Callable[[], str]] = dict()):
        self.interval = interval
        self.encoding = encoding
        self.policy = policy

    def read(self):
        time.sleep(self.interval)
        identifier, function = random.choice(list(self.policy.items()))

        data = "{\"identifier\":\"" + identifier + "\",\"value\":\"" + function() + "\"}"
        return data.encode(self.encoding)

    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        pass

    def random_first_byte():
        return str(hex(random.randint(0, 255)))[2:4].upper() + " 00 00 00 00 00 00 00"