from utils.com_supervisor.mapping.mapper import Mapper

class TwoBytesHexToDecMapper(Mapper):
    """
    Takes first byte of raw input and takes returns it as decimal value
    """

    def map(self, value):
        return int(value.split()[0], 16)