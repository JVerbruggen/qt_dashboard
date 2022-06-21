from utils.com_supervisor.readable.readable import Readable
import time
from typing import Callable, Dict
import random
from utils.bytes import *


class Mock(Readable):
    """
    Mocker readable.
    Waits for given interval and sends back a message of a random identifier and some data provided by a function.
    Identifiers to pick from are given in the policy. The function that is called should return 8 bytes of data in string format.
    """

    def __init__(self, interval: float = 1.0, encoding: str = "utf-8", policy: Dict[str, Callable[[], str]] = dict()):
        self.interval = interval
        self.encoding = encoding
        self.policy = policy

    def read(self):
        time.sleep(self.interval)
        identifier, function = random.choice(list(self.policy.items()))
        value = function()

        print("\n--- INCOMING ---")
        print(value)

        data = "{\"identifier\":\"" + identifier + "\",\"value\":\"" + value + "\"}"
        return data.encode(self.encoding)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def random_first_byte():
        return "{:04}".format(hex(random.randint(0, 255)))[2:4].upper() + " 00 00 00 00 00 00 00"

    def all_random_bytes():
        return " ".join("{:04}".format(hex(random.randint(0, 255)))[2:4].upper() for _ in range(8))

    def take_from(items: list[str]):
        return random.choice(items)

    increment_state = {i: 0 for i in range(8)}

    def increment(index: int, base: list = ["00" for _ in range(8)]):
        incremented = int_to_byte_str(Mock.increment_state[index])
        Mock.increment_state[index] = (Mock.increment_state[index] + 1) % 256

        return " ".join(incremented if i == index else base[i] for i in range(8))

    def increment_multiple(indices: list[int], base: list = ["00" for _ in range(8)]):
        incremented = {}
        for index in indices:
            incremented[index] = int_to_byte_str(Mock.increment_state[index])
            Mock.increment_state[index] = (Mock.increment_state[index] + 1) % 256

        return " ".join(incremented[i] if i in indices else base[i] for i in range(8))
