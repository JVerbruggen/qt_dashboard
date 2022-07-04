from utils.com_supervisor.mapping.mapper import Mapper
from dataclasses import dataclass


class TwoBytesHexToDecMapper(Mapper):
    """
    Takes first byte of raw input and takes returns it as decimal value
    """

    def map_to(self, value: bytes, variable):
        variable.set_value(int(value.split()[0], 16))


@dataclass
class ToIntegerMapper(Mapper):
    """
    Takes byte x returns it as an integer
    """
    byte_index: int

    def map_to(self, value: bytes, variable):
        variable.set_value(int(value.split()[self.byte_index], 16))