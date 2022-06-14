from components.variable.watchable_variable import WatchableVariable
from dataclasses import dataclass, field
from utils.bytes import *

@dataclass
class Proxy8BitVariable(WatchableVariable):
    """
    Like a proxy variable but instead breaks down byte into 8 bits
    """
    configuration: dict[int, WatchableVariable]

    def get_value(self):
        raise NotImplementedError("Not supported")

    def set_value(self, value: int):
        """ Value is a byte """
        bits = byte_to_bit_string(value)
        # print("Setting variables to", bits)
        for i, v in enumerate(bits[::-1]):
            if i not in self.configuration: continue

            var = self.configuration[i]
            value = int(v)
            var.set_value(value)

        
        

