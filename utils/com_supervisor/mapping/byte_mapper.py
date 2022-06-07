from components.variable.watchable_variable import WatchableVariable
from dataclasses import dataclass, field

@dataclass
class ByteMapper:
    """
    Maps individual bytes to corresponding variables.
    """

    def map_to(self, value: bytes, variable: WatchableVariable):
        variable.set_value(value)