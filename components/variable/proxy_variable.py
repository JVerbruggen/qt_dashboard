from components.variable.watchable_variable import WatchableVariable

class ProxyVariable(WatchableVariable):
    """
    A variable that proxies assigned value to 8 underlying variables.
    Uses a byte configuration to determine which variable should be used.
    """

    __slots__ = \
        "configuration"

    def __init__(self, configuration: dict[int, WatchableVariable] = []):
        self.configuration = configuration

    def get_value(self):
        raise NotImplementedError()

    def set_value(self, value: bytes):
        """ Value is 8 bytes """
        byte_array = value.split()

        for (i, byte) in enumerate(byte_array):
            if i not in self.configuration: continue
            variable = self.configuration[i]
            variable.set_value(byte)

        

