from components.variable.watchable_variable import WatchableVariable
from dataclasses import dataclass

@dataclass(slots=True)
class ProxyVariable(WatchableVariable):
    """
    A variable that proxies assigned value to 8 underlying variables.
    Uses a byte configuration to determine which variable should be used.
    """
    configuration: dict[int, WatchableVariable]

    def get_value(self):
        raise NotImplementedError("Not supported")

    def set_value(self, value: bytes):
        """ Value is 8 bytes """
        byte_array = value.split()

        for (i, byte) in enumerate(byte_array):
            if i not in self.configuration: continue
            variable = self.configuration[i]
            if variable is None: continue
            variable.set_value(byte)

@dataclass(slots=True)
class ProxyVariableWithState(WatchableVariable):
    state_byte_index: int
    states: dict[int, WatchableVariable]

    def get_value(self):
        raise NotImplementedError("Not supported")

    def set_value(self, value: bytes):
        """ Value is 8 bytes """
        byte_array = value.split()
        state = byte_array[self.state_byte_index]

        if state not in self.states: return
        
        selected_proxy = self.states[state]
        selected_proxy.set_value(value)