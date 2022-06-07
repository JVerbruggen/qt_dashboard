from utils.com_supervisor.mapping.mapper import Mapper

class TwoBytesHexToDecMapper(Mapper):
    """
    Takes first byte of raw input and takes returns it as decimal value
    """

    def map_to(self, value: bytes, variable):
        variable.set_value(int(value.split()[0], 16))