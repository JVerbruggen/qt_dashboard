from components.variable.watchable_variable import WatchableVariable
from dataclasses import dataclass
from utils.com_supervisor.mapping.mapper import Mapper


@dataclass
class ByteMapper(Mapper):
    """
    Maps individual bytes to corresponding variables.
    """

    def map_to(self, value: bytes, variable: WatchableVariable):
        variable.set_value(value)